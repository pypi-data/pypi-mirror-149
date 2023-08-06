import datetime
import warnings
from collections import defaultdict

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.api import OLS
import rqdatac
from rqdatac.decorators import ttl_cache
from rqdatac.utils import to_date_str

from rqfactor.analysis.winsorize import WINSORIZE_METHODS
from rqfactor.analysis.analysis_result import *

__all__ = [
    'Winzorization', 'Normalization', 'Neutralization',
    'ICAnalysis', 'QuantileReturnAnalysis', 'FactorReturnAnalysis',
    'FactorAnalysisEngine'
]
# constant
VALID_INDUSTRY_SOURCE = ('citics_2019', 'sws')
VALID_WINSORIZE_METHODS = ('mad', 'std', 'percentile')


def _get_return_fields(columns):
    return [col for col in columns if col.startswith('P_')]


def _format_factor_data(factor_data, returns, periods):
    """ 将因子数据格式化 """
    ret_table = {}
    cumprod = (returns + 1).cumprod().ffill()
    for p in periods:
        # 计算 T...T+p日的的累积收益
        key = f"P_{p}"
        prod = (cumprod.shift(-p) / cumprod) - 1
        ret_table[key] = np.concatenate(prod.values)
    index = pd.MultiIndex.from_product([returns.index, returns.columns], names=['datetime', 'order_book_id'])
    df = pd.DataFrame(ret_table, index=index)
    factor_data = factor_data.reindex(returns.index, columns=returns.columns)
    df['factor'] = np.concatenate(factor_data.values)
    df.index = df.index.set_names(['datetime', 'order_book_id'])
    return df


def _validate_data_frame(df, name):
    """ 确保index为pd.DatetimeIndex， columns为order_book_ids """
    if not isinstance(df, pd.DataFrame):
        raise ValueError(
            '{}: expect pd.DataFrame, got {}'.format(name, type(df))
        )
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(
            '{}: expect index type=pd.DatetimeIndex, got {}'.format(name, type(df.index))
        )


# 数据缓存一个小时
@ttl_cache(3600)
def _cache_industry_data(source='citics_2019'):
    # 缓存行业分类数据
    if source == 'citics_2019':
        data_field = 'first_industry_name'
        data = rqdatac.client.get_client().execute('__internal__zx2019_industry')
        df = pd.DataFrame(data, columns=[data_field, 'order_book_id', 'start_date'])
    elif source == 'sws':
        data_field = 'index_name'   # 申万行业数据的内部接口将 first_industry_name 聚合成了此字段
        data = rqdatac.client.get_client().execute('__internal__shenwan_industry')
        df = pd.DataFrame(data, columns=[data_field, 'order_book_id', 'start_date', 'version'])
        #
        # 申万数据源需要根据日期选择不同version的行业分类数据
        # 20140101之前选择 version=1
        # 20140101-20210731选择 version=2
        # 20210731之后选择 version=3
        #
        df['select'] = 1
        df.loc[df['start_date'] > pd.Timestamp('2014-01-01'), 'select'] = 2
        df.loc[df['start_date'] > pd.Timestamp('2021-07-31'), 'select'] = 3
        df = df[df['version'] == df['select']]
    else:
        raise ValueError('source: invalid source={}, expect one of [sws, citics_2019]'.format(source))

    df.set_index(['order_book_id', 'start_date'], inplace=True)
    return df[data_field].sort_index()


def _get_listed_date_mask_series(order_book_ids, trading_dates):
    """
    获取合约的有效期mask， trading_dates 中的合约，未退市时值为True
    """
    stocks = rqdatac.all_instruments("CS")
    stocks = stocks.set_index('order_book_id')
    stocks['de_listed_date'] = stocks['de_listed_date'].replace('0000-00-00', '2999-12-31')
    listed_date_map = stocks['listed_date'].to_dict()
    de_listed_date_map = stocks['de_listed_date'].to_dict()
    dates = np.array([to_date_str(dt) for dt in trading_dates])
    data = {
        oid: (listed_date_map[oid] <= dates) & (dates < de_listed_date_map[oid]) for oid in order_book_ids
    }
    return pd.DataFrame(data, index=pd.to_datetime(trading_dates)).stack()


def _load_industry_data(order_book_ids, dates, source='citics_2019'):
    """ 加载行业分类数据

    :return: MultiIndex(datetime, order_book_id) Series
    """
    df = _cache_industry_data(source=source)
    index = pd.MultiIndex.from_product([order_book_ids, dates], names=['order_book_id', 'datetime'])
    # 可以使用reindex的方法，写起来简单些，但是性能较差，因此这里使用查找位置构造Series的方法，快2-3倍
    # 查找数据对应位置
    pos = df.index.searchsorted(index, side='right') - 1
    index = index.swaplevel()   # level change (oid, datetime) --> (datetime, oid)
    result = pd.Series(df.values[pos], index=index)
    result = result.sort_index()
    # 去除未上市股票和已退市股票数据
    msk = _get_listed_date_mask_series(order_book_ids, dates)
    return result[msk.values]


def _get_ic_func(rank_ic=False):
    func = stats.spearmanr if rank_ic else stats.pearsonr

    def wrapper(fs, rs):
        # drop all nan data
        mask = ~(np.isnan(fs) | np.isnan(rs))
        if np.any(mask):
            return func(fs[mask], rs[mask])
        return 0, 0
    return wrapper


def _get_datetime_freq(index: pd.DatetimeIndex):
    # 获取datetime index对应的频率
    if not np.alltrue(index.second == 0):
        return 'tick'
    elif not np.alltrue(index.minute == 0):
        return '1m'
    elif np.alltrue(index.time == datetime.time(0, 0)):
        return '1d'

    raise ValueError("Unknown datetime index: {}".format(index))


def _is_date_frequency_index(index: pd.DatetimeIndex):
    """ 检查index是否为日频率 """
    return _get_datetime_freq(index) == '1d'

# --------------- processors ---------------


class FactorPreprocessor:
    """ 因子数据预处理基类 """
    def process(self, factor_data):
        raise NotImplementedError('Need implement FactorPreprocessor.process')


class Winzorization(FactorPreprocessor):
    def __init__(self, method='mad'):
        """ 离群值数据处理

        :param method: 处理方法，默认='mad'，可选 mad/std/percentile
        """
        if method not in VALID_WINSORIZE_METHODS:
            raise ValueError("method: expect one of {}, got {}".format(VALID_WINSORIZE_METHODS, method))
        self.method = method

    def process(self, factor_data):
        winsorize = WINSORIZE_METHODS[self.method]
        return factor_data.apply(winsorize, axis=1)


class Normalization(FactorPreprocessor):
    """ 标准化方法 """

    def process(self, factor_data):
        # 数据标准化一行写法
        # 相当于针对每日因子值x，result = (x - x.mean()) / x.std()
        return factor_data.sub(factor_data.mean(axis=1), axis=0).div(
            factor_data.std(axis=1), axis=0).where(
            lambda x: ~np.isinf(x), 0)      # 对std=0，相除之后为inf，将其替换为0


class Neutralization(FactorPreprocessor):

    def __init__(self, industry='citics_2019', style_factors='all'):
        """ 因子中性化处理

        :param industry: 行业中性化参数，指定行业数据源，默认='citics_2019', 可选citics_2019/sws/None, 如果是None则不做行业中性化
        :param style_factors: 风格因子中性化参数，默认='all', 如果指定None，则不做风格中性化处理

        Note:
        不可同时指定 industry 和 style_factors 为None
        """
        if industry and industry not in VALID_INDUSTRY_SOURCE:
            raise ValueError('industry: expect one of {}, got {}'.format(VALID_INDUSTRY_SOURCE, industry))
        if industry is None and style_factors is None:
            raise ValueError('Expect at least one of [industry, style_factors] not None, but get both None.')
        self.industry = industry
        self.style_neutralize = True if style_factors else False
        self.style_factors = None if style_factors == 'all' else style_factors

    def process(self, factor_data):
        if not (self.style_neutralize or self.industry):
            warnings.warn("Do not make any processing because no industry nor style factors specify.")
            return
        exog = None
        dates = factor_data.index.tolist()
        order_book_ids = factor_data.columns.tolist()
        if self.style_neutralize:
            # 加载风格因子数据
            exog = rqdatac.get_style_factor_exposure(
                order_book_ids=order_book_ids, start_date=dates[0], end_date=dates[-1], factors=self.style_factors
            )
            exog = exog.reorder_levels(['date', 'order_book_id'])
            if not _is_date_frequency_index(factor_data.index):
                # 针对非日度频率的数据，对风格因子进行数据展开
                exog = exog.unstack('order_book_id').reindex(factor_data.index.date)
                exog.index = factor_data.index
                exog = exog.stack('order_book_id')
        if self.industry:
            # 加载行业分类数据，处理成 MultiIndex(datetime, order_book_id)，columns=行业 的DataFrame
            industry_data = _load_industry_data(order_book_ids, dates, source=self.industry)
            industry_df = pd.get_dummies(industry_data)
            exog = industry_df if exog is None else pd.concat([exog, industry_df], axis=1)

        index = pd.MultiIndex.from_product([dates, order_book_ids], names=['datetime', 'order_book_id'])
        exog = exog.reindex(index)  # reindex 一下，确保order_book_id顺序与factor_data保持一致

        # start process
        def _neutralize(x):
            _exog = exog.loc[x.name]
            return OLS(x, exog=_exog, hasconst=False, missing='drop').fit().resid

        return factor_data.apply(_neutralize, axis=1)


# --------------- end processors ---------------


class FactorAnalyser:
    step_name = 'FactorAnalysisStep'

    def analysis(self, factor_data, returns, periods, ascending=True):
        raise NotImplementedError('Need implement FactorAnalyser.analysis')


class ICAnalysis(FactorAnalyser):
    def __init__(self, rank_ic=True, industry_classification=None, max_decay=None):
        """ 因子IC分析

        :param rank_ic: 默认=True，使用stats.spearmanr计算ic，否则使用 stats.pearsonr计算
        :param industry_classification: IC行业分布计算，指定行业数据源，可选citics_2019/sws/None，也支持pd.Series/dict 默认=None，不计算IC行业分布
        :param max_decay: IC衰减期数，默认=None，不计算衰减

        Notes
        ---------
        industry_classification 传入pd.Series时，格式如下
        ::
        order_book_id
        600837.XSHG      金融服务
        601857.XSHG        采掘
        600547.XSHG      有色金属
        600809.XSHG      食品饮料
        600438.XSHG      电气设备

        传入dict时，key为order_book_id, value为行业名称，如 {'000001.XSHE': '银行', '600837.XSHG': '金融服务'}
        缺失的 order_book_id 将使用 Unknown 填充
        """
        if industry_classification is not None:
            if not isinstance(industry_classification, (str, dict, pd.Series)):
                raise ValueError('Unsupported industry_classification type, expect one of None/str/pd.Series/dict, '
                                 'got type={}'.format(type(industry_classification)))

            if isinstance(industry_classification, str) and industry_classification not in VALID_INDUSTRY_SOURCE:
                raise ValueError('industry_classification: expect one of {}, '
                                 'got {}'.format(VALID_INDUSTRY_SOURCE, industry_classification))
        self.rank_ic = rank_ic
        self.ic_func = _get_ic_func(rank_ic)
        self.industry = industry_classification
        self.max_decay = max_decay

    def _get_industry_data(self, factor_data):
        # return multi-index industry series
        if isinstance(self.industry, str):
            # load industry data from rqdatac
            return _load_industry_data(
                order_book_ids=factor_data.index.get_level_values('order_book_id').unique(),
                dates=factor_data.index.get_level_values('datetime').unique(),
                source=self.industry
            )
        if isinstance(self.industry, dict):
            # convert dict to Series
            industry_series = pd.Series(self.industry)
        elif isinstance(self.industry, pd.Series):
            industry_series = self.industry.copy()
        else:
            raise RuntimeError('Invalid industry type, expect str/dict/pd.Series, go {} '.format(type(self.industry)))
        order_book_ids = factor_data.index.get_level_values('order_book_id')
        industry_series = industry_series.reindex(order_book_ids.unique()).fillna('Unknown')
        return pd.Series(index=factor_data.index, data=industry_series[order_book_ids].values)

    def _calc_ic(self, factor_data):
        ic_func = self.ic_func
        return_fields = _get_return_fields(factor_data.columns)

        def _ic_calculate(g):
            f = g['factor']
            return g[return_fields].apply(lambda x: ic_func(x, f))

        df = factor_data.groupby(level='datetime').apply(_ic_calculate)
        # ic_func 返回 ic, p_value 两个值，构造成DataFrame后，index值为0的是ic，否则是p_value
        ic_msk = df.index.get_level_values(1) == 0
        df.reset_index(1, drop=True, inplace=True)
        return df[ic_msk], df[~ic_msk]

    def _calc_ic_decay(self, factor_data, ic):
        if not self.max_decay:
            return None
        ic_func = self.ic_func
        return_fields = _get_return_fields(factor_data.columns)

        def _ic_calculate(g):
            f = g['factor']
            return g[return_fields].apply(lambda x: ic_func(x, f)[0])

        ic = ic.copy()
        ic['decay'] = 0
        ic = ic.set_index('decay', append=True)
        decay_list = [ic]
        for d in range(1, self.max_decay):
            _factor_data = factor_data[return_fields].unstack('order_book_id').shift(-d)
            _factor_data = _factor_data.stack('order_book_id')
            _factor_data['factor'] = factor_data['factor']
            _factor_data.dropna(inplace=True)
            ret = _factor_data.groupby(level='datetime').apply(_ic_calculate)
            ret['decay'] = d
            decay_list.append(ret.set_index('decay', append=True))
        # return MultiIndex(datetime, decay) DataFrame
        return pd.concat(decay_list).sort_index()

    def _calc_ic_industry_distribute(self, factor_data):
        if self.industry is None:
            return None
        industry_data = self._get_industry_data(factor_data)
        ic_func = self.ic_func
        return_fields = _get_return_fields(factor_data.columns)

        def _classify(group):
            fs = group['factor']
            return group[return_fields].apply(lambda x: ic_func(x, fs)[0])

        return factor_data.groupby(industry_data).apply(_classify)

    def analysis(self, factor_data, returns, periods, ascending=True):
        factor_data = _format_factor_data(factor_data, returns, periods)
        if self.rank_ic and ascending:
            factor_data['factor'] *= -1
        ic, ic_p_value = self._calc_ic(factor_data)
        ic_decay = self._calc_ic_decay(factor_data, ic)
        ic_industry_distribute = self._calc_ic_industry_distribute(factor_data)
        return ICAnalysisResult(
            ic=ic, ic_p_value=ic_p_value,
            ic_decay=ic_decay,
            ic_industry_distribute=ic_industry_distribute,
            name=self.step_name,
        )


class QuantileReturnAnalysis(FactorAnalyser):
    def __init__(self, quantile=5, benchmark=None):
        """ 因子分组收益率分析

        :param quantile: 分组数，默认=5
        :param benchmark: 指数基准合约代码，默认=None
        """
        self.quantile = quantile
        self.benchmark = None
        if benchmark is not None:
            # 检查benchmark是否为指数合约
            i = rqdatac.instruments(benchmark)
            if i is None or i.type != "INDX":
                warnings.warn("Invalid benchmark: {} is not INDX order_book_id.".format(benchmark))
            else:
                self.benchmark = benchmark

    def _load_benchmark_series(self, index: pd.DatetimeIndex):
        if self.benchmark is None:
            return

        freq = _get_datetime_freq(index)
        field = 'last' if freq == 'tick' else 'close'
        price = rqdatac.get_price(
            self.benchmark, start_date=index[0].date(), end_date=index[-1].date(),
            frequency=freq, fields=[field], expect_df=True)
        if price is None:
            warnings.warn("No price data for benchmark [{}] from %s to %s".format(
                self.benchmark, index[0].date(), index[-1].date()
            ))
            return
        price = price[field]
        price.index = price.index.droplevel('order_book_id')
        # reindex后ffill，避免不同频率的某些行情数据缺失
        returns = price.reindex(index).ffill().pct_change()
        returns.fillna(0, inplace=True)     # 第一个收益率为0
        returns.name = self.benchmark

        return returns.add(1).cumprod() - 1

    def analysis(self, factor_data, returns, periods, ascending=True):
        """
        - quantile_factor_returns: 因子分组累积收益率
        - quantile_turnover: 各期分组换手率
        - quantile_long_short_returns：因子分组多空收益率
        """
        # shift因子值，【T日因子收益率】使用【T-1日因子】和【T日的日收益率】计算得到
        factor = factor_data.shift(1)
        tags = np.array(["q{}".format(i) for i in range(1, self.quantile + 1)])

        def _calc_level_returns_of_period(lv_returns):
            # 处理当前调仓周期的某一层
            lv_name = lv_returns.name
            _returns = lv_returns.groupby(period_tags[lv_name]).apply(
                # 处理当前【层】的每一个分组
                lambda lv_series: lv_series.groupby(level='datetime').mean()
            )
            _returns = _returns.unstack(lv_name)
            # 对于得到的收益率序列 _returns, 在调仓周期 i ... i+period, r_i1_c 表示该周期第1日合约c的日收益率
            # 在第k天（ i < k <= i+period ) 合约c的收益率为 r_k_c = (r_i1_c + 1) * (r_i2_c + 1) * ... * (r_ik_c + 1)
            # 则 r_k 表示 从T_i（调仓日）到T_k（当前时间）的累积收益率（整个组合求平均），即 Σ(r_k_c)/n （组合里面n个合约）
            # 为了表示当前组合的每日收益率，对于非调仓日，组合的日收益率使用 pct_change 来表示：
            pct = _returns.pct_change()
            pct[::period] = _returns[::period] - 1
            return pct.unstack()

        def _calc_turnover(x):
            # 计算换手率
            x = x.reset_index().groupby('datetime').agg({'order_book_id': set})['order_book_id']
            diff = x.diff()
            diff[0] = set()
            return diff.apply(len) / x.apply(len)

        def _my_quantile(arr, q=1, labels=None):
            # pd.qcut 方法太慢了，改为使用numpy
            res = np.zeros(arr.size, dtype='O')
            msk = ~np.isnan(arr)
            x = arr[msk]
            res[~msk] = np.nan
            if x.size == 0:
                return res
            # 获取划分关键字
            # 这部分代码是pd.qcut内部实现的做法
            ls = np.linspace(0, 1, q + 1)
            idx = ls * (x.size - 1)
            fraction = idx % 1
            pos = idx.astype(int)
            _x = np.sort(x)
            a = _x[pos]
            b = np.roll(_x, shift=-1)[pos]
            bins = a + (b - a) * fraction
            # 由于使用的是np.digitize，bins的第一个数值如果是数组中的最小值的话，
            # 划分后会将其放到【第0组】，因此这里将第一个值减一，
            # 可以将待划分数组中的所有值都包含进去
            bins[0] -= 1
            res[msk] = labels[np.digitize(x, bins, True) - 1]
            return res

        # 计算总体累积收益率
        cum_returns = returns.add(1).cumprod()
        cum_returns = cum_returns.reindex(factor.index, columns=factor.columns)

        quantile_returns = pd.DataFrame(
            index=pd.MultiIndex.from_product([tags, cum_returns.index], names=['tag', 'datetime'])
        )
        quantile_turnover = quantile_returns.copy()

        multi_index = pd.MultiIndex.from_product([cum_returns.index, cum_returns.columns],
                                                 names=['datetime', 'order_book_id'])
        df_sample = pd.DataFrame(index=multi_index)
        shape = cum_returns.shape
        data_length = len(multi_index)

        ranked = factor.rank(method='first', ascending=ascending, axis=1)
        tags_value = np.apply_along_axis(_my_quantile, axis=1, arr=ranked.values, q=self.quantile, labels=tags)

        cum_value = cum_returns.values
        div_value = cum_returns.shift(1, fill_value=1).values

        for period in periods:
            # 根据【层】构造multi-index分层结果
            period_tags = df_sample.copy()
            period_returns = df_sample.copy()

            for lv in range(1, period + 1):
                # 开始根据【层】进行划分
                lv_col = 'lv{}'.format(lv)

                _tags = np.repeat(tags_value[lv::period], period, axis=0)
                _tags = np.roll(np.resize(_tags, shape), shift=lv, axis=0)
                _tags[:lv] = np.nan
                period_tags[lv_col] = np.resize(_tags, (data_length,))

                _div = np.repeat(div_value[lv::period], period, axis=0)
                _div = np.roll(np.resize(_div, shape), shift=lv, axis=0)
                _div[:lv] = np.nan
                _cum = cum_value / _div
                period_returns[lv_col] = np.resize(_cum, (data_length,))

            period_col = 'P_{}'.format(period)
            quantile_returns[period_col] = period_returns.apply(_calc_level_returns_of_period).mean(axis=1)
            quantile_turnover[period_col] = period_tags.apply(
                # 处理当前调仓周期的每一层
                lambda lv_components: lv_components.groupby(lv_components).apply(_calc_turnover)
            ).mean(axis=1)

        quantile_returns.fillna(0, inplace=True)
        # quantile long short returns
        quantile_long_short_returns = quantile_returns.loc[tags[0]] - quantile_returns.loc[tags[-1]]
        quantile_long_short_returns = quantile_long_short_returns.add(1).cumprod().sub(1)
        # cumulative returns
        quantile_returns = quantile_returns.groupby(level='tag').apply(lambda x: x.add(1).cumprod().sub(1))

        benchmark_returns = self._load_benchmark_series(factor.index)
        quantile_detail = pd.DataFrame(data=tags_value, index=factor.index, columns=factor.columns)

        return QuantileReturnAnalysisResult(
            quantile_turnover=quantile_turnover,
            quantile_returns=quantile_returns,
            quantile_detail=quantile_detail,
            benchmark_return=benchmark_returns,
            top_minus_bottom_returns=quantile_long_short_returns,
            name=self.step_name,
        )


class FactorReturnAnalysis(FactorAnalyser):
    """ 分析器：因子收益率检验 """

    def analysis(self, factor_data, returns, periods, ascending=True):
        """
        计算daily returns
        """
        # shift因子值，【T日因子收益率】使用【T-1日因子】和【T日的日收益率】计算得到
        factor = factor_data.shift(1)
        # 计算因子多空权重
        demean = factor.sub(factor.mean(axis=1), axis=0)
        weights = demean.div(demean.abs().sum(axis=1), axis=0)
        if ascending:
            weights = -weights
        # 计算总体累积收益率
        cum_returns = returns.add(1).cumprod()
        cum_returns = cum_returns.reindex(factor.index, columns=factor.columns)

        factor_returns = pd.DataFrame(index=factor.index, columns=["P_{}".format(p) for p in periods])
        factor_returns.index.name = 'datetime'
        for period in periods:
            res = []
            for lv in range(1, period + 1):
                weight = weights[lv::period].reindex(factor.index).ffill()
                # 根据【层】计算 i..i+period 阶段累积收益率
                div_factor = cum_returns.shift(1, fill_value=1)[lv::period]
                div_factor = div_factor.reindex(cum_returns.index).ffill()
                _returns = (cum_returns / div_factor) - 1       # 减一取得累积收益率净值
                # 计算多空收益率
                wr = (weight * _returns).sum(axis=1)
                # 计算得到每日的因子多空收益率
                change_rate = wr.add(1).pct_change()
                change_rate[lv::period] = wr[lv::period]
                res.append(change_rate)
            col = "P_{}".format(period)
            factor_returns[col] = pd.concat(res, axis=1).mean(axis=1)

        # 因子累积收益率
        factor_returns = factor_returns.fillna(0).add(1).cumprod().sub(1)
        return FactorReturnAnalysisResult(factor_returns=factor_returns, name=self.step_name)


class FactorAnalysisEngine:
    """ 因子检验引擎 """

    def __init__(self):
        self.preprocess_pipelines = []
        self.analysis_pipelines = defaultdict(FactorAnalyser)
        self.__exists_step_names = []

    def append(self, step: tuple):
        """ 构造因子检验步骤

        :param step: tuple(name, Processor) 因子检验处理步骤, 如 ('winzorize', Winzorization(method='mad'))

        预处理可选：
            - Winzorization - 离群值处理
            - Neutralization - 中性化处理
            - Normalization - 标准化处理
        因子分析可选：
            - ICAnalysis - ic分析
            - QuantileReturnAnalysis - 分组收益分析
            - FactorReturnAnalysis - 因子收益分析

        Example
        ----
        >>> from rqfactor.analysis import FactorAnalysisEngine, Winzorization, ICAnalysis
        >>> engine = FactorAnalysisEngine()
        >>> engine.append(('step_winsorize', Winzorization(method='mad')))
        >>> engine.append(('step_ic_analysis', ICAnalysis(rank_ic=True, industry_classification='citics_2019', max_decay=20)))
        """
        name, processor = step
        if name in self.__exists_step_names:
            raise RuntimeError('pipeline step name={} already exists, please use another name.'.format(name))
        self.__exists_step_names.append(name)
        if isinstance(processor, FactorPreprocessor):
            self.preprocess_pipelines.append(step)
        elif isinstance(processor, FactorAnalyser):
            processor.step_name = name
            self.analysis_pipelines[name] = processor
        else:
            raise ValueError(
                'Invalid step={}, unknown processor={}'.format(name, processor)
            )

    def analysis(self, factor_data, returns, ascending=True, periods=1, keep_preprocess_result=False):
        """因子检验

        :param factor_data: 因子值， pd.DataFrame, index=pd.DatetimeIndex, columns为order_book_id
        :param returns: 因子收益数据，可选 daily 或 pd.DataFrame，如果是pd.DataFrame，index和columns应与factor_data一致
        :param ascending: 因子排序方向，默认True（升序）
        :param periods: tuple/list/int 因子检验频率， 默认 1
        :param keep_preprocess_result: 是否保留预处理结果（默认False）
        :returns: dict

        Example
        ----
        >>> import rqdatac
        >>> from rqfactor.analysis import FactorAnalysisEngine, ICAnalysis
        >>> obs = rqdatac.index_components('000300.XSHG')
        >>> factor = rqdatac.get_factor(obs, 'pb_ratio', '20200101', '20200601', expect_df=True)
        >>> factor = factor['pb_ratio'].unstack(level='order_book_id')
        >>> engine = FactorAnalysisEngine()
        >>> engine.append(('ic_analysis', ICAnalysis()))
        >>> result = engine.analysis(factor_data=factor, returns='daily', ascending=True, periods=(1, 3))
        >>> result['ic_analysis'].show()
        """
        if len(self.preprocess_pipelines) == 0 and len(self.analysis_pipelines) == 0:
            warnings.warn('no pipelines to execute.')
            return
        _validate_data_frame(df=factor_data, name='factor_data')
        if isinstance(returns, str):
            if returns == 'daily':
                # load daily returns
                # 计算逻辑是T日的因子值对应的是T+1日的收益率，因此需要往后多取一日
                _end_date = rqdatac.get_next_trading_date(factor_data.index[-1])
                returns = rqdatac.get_price_change_rate(
                    order_book_ids=factor_data.columns,
                    start_date=factor_data.index[0],
                    end_date=_end_date,
                    expect_df=True,
                    market='cn'
                )
                returns = returns.shift(-1)[:-1]
            else:
                raise ValueError('returns: expect pd.DataFrame or "daily", got {}'.format(returns))
        else:
            _validate_data_frame(df=returns, name='returns')
        # ensure periods list
        if not isinstance(periods, (tuple, list)):
            periods = [periods]

        # ensure index name and columns name
        for df in [factor_data, returns]:
            df.index.name = 'datetime'
            df.columns.name = 'order_book_id'

        result = {}
        # preprocess factor data
        for name, preprocessor in self.preprocess_pipelines:
            factor_data = preprocessor.process(factor_data)
            if keep_preprocess_result:
                result[name] = factor_data.copy()
        # start factor analysis
        for name, analyser in self.analysis_pipelines.items():
            result[name] = analyser.analysis(factor_data, returns, periods, ascending=ascending)
        return result

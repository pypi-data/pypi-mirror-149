# !/usr/bin/env python
import random
import datetime
import logging
import pandas as pd
import numpy as np

from collections import defaultdict, namedtuple

from scipy import stats

import rqdatac
from rqfactor.analysis.winsorize import winsorize
from rqfactor.analysis.neutralize import neutralize
from rqfactor.exception import RQFactorUserException, InvalidArgument


USE_JUPYTER_NOTEBOOK = False

try:
    import IPython

    if type(IPython.get_ipython()).__module__.startswith('ipykernel.'):
        USE_JUPYTER_NOTEBOOK = True
except:
    pass


FactorAnalysisResult = namedtuple('FactorAnalysisResult', [
    'ic', 'ic_rolling', 'ic_summary', 'ic_decay', 'quantile_factor_returns',
    'quantile_turnover', 'ic_industry_distribute', 'benchmark_return',
    'total_return', 'max_drawdown', 'volatility'
])


def draw_analysis_result(result, mode='column', **kwargs):
    """
    绘制因子检验结果

    @params mode: 绘制方式，支持 column（默认）, grid, split
    @params kwargs: bokeh layout 参数，仅 mode=column/grid 生效

    Example
    ----
    >>> # 显示每个图像为独立文件
    >>> result.show(mode='split')
    >>> # 显示一个按列分布的html图像
    >>> result.show(mode='column', sizing_mode='stretch_both')
    >>> # 显示一个按2列的栅格分布的html图像
    >>> result.show(mode='grid', ncols=2, sizing_mode='stretch_both')
    """
    # Judge arguments
    if mode not in {'split', 'column', 'grid'}:
        raise InvalidArgument("Invalid mode {}, support [split/column/grid] only.".format(mode))

    from bokeh.io import output_notebook, reset_output
    from bokeh.plotting import show
    from bokeh.layouts import gridplot, column
    from rqfactor.analysis.plot import (
        ic_series, ic_decay, ic_industry_distribute,
        quantile_turnover, quantile_factor_returns
    )
    reset_output()

    if USE_JUPYTER_NOTEBOOK:
        output_notebook()

    # Initialize params
    _layout_config = {'sizing_mode': 'stretch_both'}
    if kwargs:
        _layout_config.update(kwargs)

    figures = [
        ic_series(result.ic),
        ic_decay(result.ic_decay),
        ic_industry_distribute(result.ic_industry_distribute, u'IC 行业分布'),
        quantile_factor_returns(result.quantile_factor_returns, result.benchmark_return),
        quantile_turnover(result.quantile_turnover),
    ]

    if mode == 'split':
        # 每个图显示在一个独立的浏览器窗口
        for fig in figures:
            show(fig)
    elif mode == 'column':
        # 所有图像排成一列显示在一个窗口
        show(column(figures, **_layout_config))
    elif mode == 'grid':
        # 图像按照栅格视图显示在一个窗口
        if 'ncols' not in _layout_config:
            _layout_config['ncols'] = 2
        show(gridplot(figures, **_layout_config))


def save_analysis_figs(result, mode='split',
                       to='factor_analysis', filetype='html', silent=True,
                       **kwargs):
    """
    保存因子检验结果

    @params mode: 绘制方式，支持 split（默认）, grid, column
    @params to: 图片文件名称，默认 factor_analysis，如果mode=split，filename将作为独立图片文件的前缀
    @params filetype: 保存的文件类型，默认html，目前仅支持html
    @params silent: 仅保存，不打开, 默认True
    @params kwargs: bokeh layout 参数，仅 mode=column/grid 生效

    Example
    ----
    >>> # 输出每个图像为独立文件
    >>> result.save_figs(mode='split', to='result.html', silent=True)
    >>> # 输出图像为一个html文件，按列分布，并使用浏览器打开
    >>> result.save_figs(mode='column', to='result.html', silent=False, sizing_mode='stretch_both')
    >>> # 输出图像为一个html文件，按2列的栅格分布
    >>> result.save_figs(mode='column', to='/tmp/result.html', ncols=2, sizing_mode='stretch_both')
    """
    # Judge arguments
    if mode not in {'split', 'column', 'grid'}:
        raise InvalidArgument("Invalid mode {}, support [split/column/grid] only.".format(mode))
    if filetype not in {'html'}:    # 暂时支持保存html格式文件
        # todo: support png/jpeg formats.
        raise InvalidArgument("Invalid filetype {}, support [html] only.".format(filetype))

    import re
    from bokeh.io import output_file, reset_output
    from bokeh.plotting import show
    from bokeh.layouts import gridplot, column
    from rqfactor.analysis.plot import (
        ic_series, ic_decay, ic_industry_distribute,
        quantile_turnover, quantile_factor_returns
    )
    reset_output()  # prevent displaying at jupyter notebook.

    # Initialize params
    _layout_config = {'sizing_mode': 'stretch_both'}
    if kwargs:
        _layout_config.update(kwargs)
    browser = 'none' if silent else None
    suffix = "." + filetype
    to = re.sub(r'\.{}$'.format(filetype), '', to)       # 为了方便mode=split格式化，去掉后缀

    def _save(figure, _filename=to):
        output_file(_filename + suffix)
        show(figure, browser=browser)

    figures = {
        '_ic': ic_series(result.ic),
        '_ic_decay': ic_decay(result.ic_decay),
        '_ic_industry_distribute': ic_industry_distribute(result.ic_industry_distribute, u'IC 行业分布'),
        '_quantile_factor_returns': quantile_factor_returns(result.quantile_factor_returns, result.benchmark_return),
        '_quantile_turnover': quantile_turnover(result.quantile_turnover),
    }

    if mode == 'split':
        # 每个图显示在一个独立的浏览器窗口
        for name, fig in figures.items():
            _save(fig, to + name)
    elif mode == 'column':
        # 所有图像排成一列显示在一个窗口
        _save(column(list(figures.values()), **_layout_config))
    elif mode == 'grid':
        # 图像按照栅格视图显示在一个窗口
        if 'ncols' not in _layout_config:
            _layout_config['ncols'] = 2
        _save(gridplot(list(figures.values()), **_layout_config))


FactorAnalysisResult.draw = FactorAnalysisResult.show = draw_analysis_result
FactorAnalysisResult.save_figs = FactorAnalysisResult.save_figs = save_analysis_figs


def normalize(data):
    std = data.std()
    if std != 0:
        return (data - data.mean()) / std
    else:
        r = data.copy()
        r.values[:] = 0
        return r


def ic_summary(ic, ic_p_value):
    from scipy import stats
    t_stat, p_value = stats.ttest_1samp(ic, 0)
    return {
        'mean': float(ic.mean()),
        'std': float(ic.std()),
        'positive': int(np.sum(ic >= 0)),
        'negative': int(np.sum(ic < 0)),
        'significance': float(np.sum(ic_p_value < 0.01) / len(ic_p_value)),
        'sig_positive': float(np.sum((ic > 0) & (ic_p_value < 0.01)) / len(ic)),
        'sig_negative': float(np.sum((ic < 0) & (ic_p_value < 0.01)) / len(ic)),
        't_stat': float(t_stat),
        'p_value': float(p_value),
        'skew': float(stats.skew(ic)),
        'kurtosis': float(stats.kurtosis(ic)),
        'ir': float(ic.mean() / ic.std()),
    }


def date2str(d):
    if isinstance(d, (datetime.date, datetime.datetime)):
        return d.strftime('%Y-%m-%d')
    return d


def date2int(d):
    if isinstance(d, (datetime.date, datetime.datetime)):
        return d.year * 10000 + d.month * 100 + d.day
    return d


def load_returns(data_source, order_book_ids, start_date, end_date, interval):
    returns = data_source.get_price_change_rate(order_book_ids, start_date, end_date)
    if returns.index[-1] < pd.to_datetime(end_date):
        raise RQFactorUserException(
            'daily return @ {} is missing!'.format(end_date))
    returns = returns.fillna(0)
    df = (returns + 1).cumprod()

    # index为调仓日期，value为从以该调仓日期开始的调仓周期的累积return
    result = df.iloc[::interval].pct_change().shift(-1)
    return result


def load_returns_v2(order_book_ids, start_date, end_date, index, shift=-1, data_source=None):
    if isinstance(order_book_ids, str):
        order_book_ids = [order_book_ids]
    close = data_source.get_close_price(order_book_ids, start_date, end_date)
    returns = close.reindex(index).pct_change()
    if close.index[-1] < pd.to_datetime(end_date):
        raise RQFactorUserException('daily return @ {} is missing!'.format(end_date))
    return returns.shift(shift, fill_value=0)


def _filter_inf_inplace(df):
    masked = np.ma.masked_invalid(df.values)
    min_value = masked.min()
    max_value = masked.max()
    df.replace(np.inf, max_value, inplace=True)
    df.replace(-np.inf, min_value, inplace=True)


def get_ic_func(rank_ic=False, ascending=False):
    func = stats.spearmanr if rank_ic else stats.pearsonr
    op = -1 if (rank_ic and ascending) else 1

    def wrapper(fs, rs):
        mask = ~np.isnan(fs)
        fs = fs[mask]
        rs = rs[mask]
        if len(fs):
            return func(fs * op, rs)
        return 0, 0
    return wrapper


class ProgressBar(object):

    def __init__(self):
        self.current = 0
        self.end = 1

    def more(self, value):
        self.current += value

    def update_state(self, value):
        self.current = value

    @property
    def progress(self):
        return self.current


def _parse_neutralization(how):
    if isinstance(how, tuple):
        method, args = how
    else:
        method, args = how, None

    if method not in ('style', 'industry_style') and args is not None:
        raise ValueError('invalid neutralization method')

    return method, args


def adjust_index_by_frequency(index: pd.DatetimeIndex, interval=1, frequency='D'):
    # 根据调仓频率和调仓周期对因子index进行调整
    # 检查频率和周期的合法性
    if frequency == 'D':
        if interval < 1:
            raise InvalidArgument("expect interval >= 1 for D frequency, got {}.".format(interval))
        return index[::interval]

    mx_itv = {'W': 5, 'M': 22}
    if not 1 <= abs(interval) <= mx_itv.get(frequency):
        raise InvalidArgument("expect 1 <= abs(interval) <= {mx} for {freq} frequency."
                              .format(mx=mx_itv.get(frequency), freq=frequency))

    _index_end = index[-1]
    if interval < 0:
        # extend index to frequency end
        period = _index_end.to_period(frequency)
        _tds = rqdatac.get_trading_dates(period.start_time, period.end_time)
        index = index.append(pd.to_datetime(_tds)).unique()

    # 周度/月度调仓
    abs_interval = abs(interval)
    pos = interval - 1 if interval > 0 else interval
    group_key = index.to_period(frequency)
    valid_dates = pd.Series(index, index=index).groupby(group_key)\
        .apply(lambda x: None if len(x) < abs_interval else x[pos])
    valid_dates = valid_dates.dropna()
    if valid_dates.empty:
        return
    if valid_dates[-1] > _index_end:
        # re-adjust
        valid_dates = valid_dates[:-1]

    return pd.to_datetime(valid_dates.values)


def factor_analysis(full_factor_value,
                    data_source,
                    interval,
                    frequency='D',
                    universe=None,
                    shift=1,
                    start_date=None,
                    end_date=None,
                    rank_ic=True,
                    quantile=5,
                    ascending=True,
                    winzorization='mad',
                    normalization=True,
                    neutralization='none',
                    include_st=False,
                    include_new=False,
                    update_class=None,
                    benchmark=None):
    logging.info('Begin factor analysis: '
                 '\nfactor: {full_factor_value}'
                 '\ninterval: {interval}\nfrequency={frequency}\npool: {universe}\nstart_date: {start_date}, '
                 '\nend_data: {end_date}\nrank_ic: {rank_ic}\nquantile: {quantile}, '
                 '\nascending: {ascending}\nwinzorization: {winzorization}, '
                 '\nnormalization: {normalization}\nneutralization: {neutralization}, '
                 '\ninclude_st: {include_st}\ninclude_new: {include_new}'.format(**locals()))
    # 先判断调仓频率是否合法
    if frequency not in {'D', 'W', 'M'}:
        raise InvalidArgument('frequency only support D/W/M')

    update_class = update_class or ProgressBar()

    order_book_ids = full_factor_value.columns.tolist()
    _filter_inf_inplace(full_factor_value)
    shifted = full_factor_value.shift(shift).iloc[shift:]
    # 根据调仓频率和调仓周期对日期index进行调整
    date_start = shifted.index[0]
    date_end = rqdatac.get_previous_trading_date(datetime.date.today())
    if frequency == 'W':
        date_start = date_start.to_period('W').start_time
    elif frequency == 'M':
        date_start = date_start.to_period('M').start_time
    # 新index
    ori_index = data_source.get_trading_dates(date_start, date_end)
    value_index = adjust_index_by_frequency(ori_index, interval, frequency)
    if value_index is None:
        raise RQFactorUserException('No valid dates for factor analysis from {} to {} with interval {} @ {} frequency'
                                    .format(start_date, end_date, interval, frequency))
    if value_index[0] < shifted.index[0]:
        value_index = value_index[1:]

    more_index_end_pos = value_index.searchsorted(shifted.index[-1], side='right')

    if more_index_end_pos >= len(value_index):
        more_index_end_pos -= 1
    index_end_pos = more_index_end_pos - 1

    more_index = value_index[:more_index_end_pos+1]
    value_index = value_index[:index_end_pos+1]
    target_value = shifted.reindex(value_index)

    if more_index[-1] <= pd.Timestamp(str(end_date)):
        logging.info("using more-index as returns index")
        returns_index = more_index
    else:
        logging.info('using value-index as returns index')
        returns_index = value_index

    end_date = more_index[-1]

    if len(target_value) < 1:
        raise RQFactorUserException(
            'Not enough trading days from {} to {} for period {} @ {} frequency. '
            .format(date2str(start_date), date2str(end_date), interval, frequency))

    logging.info('load_returns from {} to {} with interval={}, frequency={}'.format(
        start_date, end_date, interval, frequency))
    returns = load_returns_v2(order_book_ids, start_date, end_date, more_index, data_source=data_source)
    returns = returns.iloc[:-1]  # trim last row nans

    ic_decay = defaultdict(list)
    ic = {}
    ic_p_value = {}

    industry_factor_value = defaultdict(list)
    industry_return = defaultdict(list)

    quantile_factor_returns = {}
    total_returns = {}

    ic_func = get_ic_func(rank_ic, ascending)

    last_quantile_tag = None
    quantile_turnover = {}

    update_class.more(0.01 + 0.03 * random.random())
    update_interval = (update_class.end - update_class.current - 0.02) / len(target_value.index)

    neutralization, neutralization_style_factors = _parse_neutralization(neutralization)

    if universe == 'all':
        universe = None

    instruments = rqdatac.all_instruments('CS')
    instruments = instruments[instruments['listed_date'] != '2999-12-31']
    instruments['listed_date'] = instruments['listed_date'].astype('datetime64')
    instruments['de_listed_date_int'] = instruments['de_listed_date'].apply(lambda x: int(x.replace('-', '')))
    instruments['is_living'] = instruments['de_listed_date'] == '0000-00-00'
    instruments = instruments.set_index('order_book_id', drop=False)

    _180days = pd.Timedelta(days=180)       # 新股的判断阈值
    tags = ['q{}'.format(i) for i in range(quantile)]

    for index, date in enumerate(target_value.index):
        series = target_value.iloc[index]
        if series.isna().all():
            logging.warning("{}因子值缺失".format(date.strftime('%Y-%m-%d')))
            continue

        if universe is None:
            stocks = instruments
        else:
            pool_stocks = data_source.index_components(universe, date)
            if pool_stocks is None:
                logging.warning("has None pool stocks at {} for universe={}".format(date, universe))
                continue
            stocks = instruments.reindex(pool_stocks)

        stocks = stocks[stocks['is_living'] | (stocks['de_listed_date_int'] > date2int(date))]
        if not include_new:
            stocks = stocks['order_book_id'][(date - stocks['listed_date']) >= _180days].tolist()
        else:
            stocks = stocks['order_book_id'].tolist()

        if not include_st:
            stocks = np.array(stocks)[~data_source.is_st_stock(stocks, date)].tolist()

        stocks = np.array(stocks)[~data_source.is_suspended(stocks, date)].tolist()
        stocks.sort()
        series = series.reindex(stocks)

        industry_tag = data_source.get_industry_tag(stocks, date)
        # check industry_tag
        if industry_tag.isna().all():
            logging.warning(f"{date.strftime('%Y-%m-%d')}行业分类数据缺失")
            continue

        # 对因子值进行处理，去极值，标准化，中性化
        winsorized = winsorize(series, winzorization)
        normalized = normalize(winsorized) if normalization else winsorized

        if neutralization in {'style', 'industry_style'}:
            data = data_source.get_style_factor(stocks, date, neutralization_style_factors)
        elif neutralization in {'market', 'industry_market'}:
            data = data_source.get_market_cap(stocks, date)
            # check market_cap data
            if data.isna().all():
                logging.warning("{} market_cap 数据缺失".format(date.strftime('%Y-%m-%d')))
                continue
        else:
            data = None
        f_s = neutralize(normalized, neutralization, industry_tag, data)

        r_s = returns.iloc[index].reindex(f_s.index)

        # 计算股票的多空收益率
        demeaned = f_s - f_s.mean()
        weight = demeaned / demeaned.abs().sum()
        if ascending:
            weight = -weight
        weight.dropna(inplace=True)

        ret = returns.loc[date].reindex(weight.index)

        total_returns[date] = np.sum(weight.values * ret.values)

        ic[date], ic_p_value[date] = ic_func(f_s, r_s)

        def _classify_industry(x):
            """根据行业分类将因子值和收益划分出来"""
            x_name = x.name
            industry_factor_value[x_name].extend(x.values)
            industry_return[x_name].extend(r_s.reindex(x.index).values)
        f_s.groupby(industry_tag.reindex(stocks)).apply(_classify_industry)

        try:
            quantile_tag = pd.qcut(f_s.rank(method='first', ascending=ascending), quantile, tags)
        except ValueError:
            raise RQFactorUserException('can not cut factor value to {} quantiles'.format(quantile))

        quantile_tag = quantile_tag.dropna()
        quantile_ret = {}

        def _agg_quantile(x):
            """获取当前分组的所有order_book_id，并计算当前分组的平均收益"""
            tag = x.values[0]
            quantile_ret[tag] = r_s.reindex(x.index).mean()
            return set(x.index)

        quantile_tag = quantile_tag.groupby(quantile_tag.values).agg(_agg_quantile)
        tag_components = quantile_tag.to_dict()
        quantile_factor_returns[date] = quantile_ret

        if last_quantile_tag is not None:
            turnover = {
                k: float(len(v - last_quantile_tag[k])) / len(v) for k, v in tag_components.items() if v
            }
            quantile_turnover[date] = turnover
        last_quantile_tag = tag_components

        decay_return = (returns.iloc[index:index+20] + 1).cumprod() - 1
        decay_return = decay_return.reindex(f_s.index, axis=1)
        # decay 分析最多20期
        dr_vs = decay_return.values
        fs_vs = f_s.values
        for k in range(1, min(20, len(dr_vs))):
            ic_decay[k].append(ic_func(fs_vs, dr_vs[k])[0])

        update_class.more(update_interval)

    ic_decay_result = {k: np.mean(v) for k, v in ic_decay.items()}
    ic_decay_result[0] = np.mean(list(ic.values()))

    ic_industry_distribute = pd.Series({
        name: ic_func(np.array(f), np.array(industry_return[name]))[0] for name, f in industry_factor_value.items()
    })

    # 调整收益曲线的index
    quantile_factor_returns_df = pd.DataFrame(quantile_factor_returns).T.reindex(target_value.index)
    quantile_factor_returns_df = quantile_factor_returns_df.shift(1, fill_value=0)
    quantile_factor_returns_df = quantile_factor_returns_df.T

    # 用原始index获取基准收益率
    benchmark_return = load_returns_v2(benchmark, start_date, end_date, ori_index, shift=0, data_source=data_source)
    benchmark_return = benchmark_return[benchmark]
    benchmark_return = (benchmark_return + 1).cumprod() - 1
    benchmark_return = benchmark_return.reindex(target_value.index)     # 调整基准index
    benchmark_return.iloc[0] = 0
    benchmark_return.name = benchmark

    # 分组累计收益率
    quantile_factor_returns_df = (quantile_factor_returns_df + 1).cumprod(axis=1) - 1
    # 多空收益率
    total_returns_df = pd.Series(total_returns).reindex(returns_index)
    total_returns_df = total_returns_df.shift(1, fill_value=0)
    # 计算最大回撤
    returns_cum = np.exp(np.log1p(total_returns_df).cumsum())
    max_returns = np.maximum.accumulate(returns_cum)
    max_drawdown = ((max_returns - returns_cum) / max_returns).max()
    if np.isnan(max_drawdown):
        max_drawdown = 0
    # 计算年化波动率
    # get period
    if frequency == 'D':
        period = interval
    elif frequency == 'W':
        period = 5
    else:
        period = 22
    volatility = 0
    if len(total_returns_df) > 1:
        volatility = total_returns_df.std(ddof=1) * ((252 / period) ** 0.5)

    series_ic = pd.Series(ic)
    rolling_ic = series_ic.rolling(window=12).mean()

    result = {
        'ic': series_ic,
        'ic_rolling': rolling_ic,
        'ic_summary': ic_summary(pd.Series(ic), pd.Series(ic_p_value)),
        'ic_decay': pd.Series(ic_decay_result),
        'quantile_factor_returns': quantile_factor_returns_df,
        'quantile_turnover': pd.DataFrame(quantile_turnover).fillna(0.0),
        'ic_industry_distribute': ic_industry_distribute,
        'benchmark_return': benchmark_return,
        'total_return': total_returns_df,
        'max_drawdown': max_drawdown,
        'volatility': volatility,
    }

    update_class.update_state(update_class.end)

    return FactorAnalysisResult(**result)

# -*- coding:utf-8 -*-
# Copyright @2018 Ricequant, Inc
import pandas as pd
from rqfactor.interface import AbstractFactor

_analysis_data_source = None


def factor_analysis(f, period, start_date=None, end_date=None, frequency='D', universe=None, shift=1,
                    rank_ic=True, quantile=5, ascending=True, winzorization='mad',
                    normalization=True, neutralization='none',
                    include_st=True, include_new=True, benchmark='000300.XSHG'):
    """
    因子检验

    Parameters
    ----------
    f : pandas.DataFrame, rqfactor.interface.AbstractFactor
    period : int
        调仓周期
    frequency : string
        调仓频率，支持 日度：D， 周度：W， 月度：M
    start_date : date_like, str, int, float, datetime, 默认 None
        开始时间
    end_date : date_like, str, int, float, datetime, 默认 None
        结束时间
    universe : str, 默认 None
        股票池
    shift : int, 默认 1
        因子平移量
    rank_ic : boolean, 默认 True,
        * True: 斯皮尔曼
        * False: 皮尔逊
    quantile : int, 默认 5
        分组数
    ascending : boolean, 默认 True
        是否升序
    winzorization : {'mad', 'percentile', 'std', 'none'}, 默认 'mad'
        去极值处理方式
        * mad: 保留[中位数-3*绝对中位差, 中位数+3*绝对中位差]范围
        * percentile: 保留[2.5%, 97.5%]范围
        * std: 保留[均值-3*标准差, 均值+3*标准差]范围
        * none: 不做去极值处理
    normalization : boolean, 默认 True
        是否归一化
    neutralization : {'none', 'industry', 'style', 'industry_style'}, 默认 'none'
        中心化方式
        * none: 不做中心化处理
        * industry: 行业中心化
        * style: 风格因子中心化, 此时参数可为tuple,('style', styles), 不指定styles将表示使用全部风格因子暴露度
            styles: 为下面的一种或多种风格因子暴露度:
             beta, book_to_price, earnings_yield, growth, leverage,
            liquidity, momentum, non_linear_size, residual_volatility, size
        * industry_style: 行业风格因子中心化, 此时参数可为tuple,见'style'
    include_st : boolean, 默认 True
        是否包含ST股
    include_new: boolean, 默认 True
        是否包含新股, 新股即: 上市日期距离分析日天数<180个自然日
    benchmark: str, 默认 '000300.XSHG'
        基准

    Returns
    -------
    rqfactor.analysis.FactorAnalysisResult
        通过show或draw绘制基于bokeh的图形，默认在jupyter notebook中绘制
        通过show(notebook=False)可以直接在网页中绘制

    Examples
    --------
    进行因子检验并且输出图像

    >>> from rqfactor import Factor
    >>> from rqfactor.notebook import factor_analysis
    >>> factor = Factor('close')
    >>> result = factor_analysis(factor, period=5, start_date='20170101', end_date='20170601')
    >>> result.show(False)
    # 将会打开浏览器显示
    """
    global _analysis_data_source
    if _analysis_data_source is None:
        from rqfactor.analysis.analysis_data_source import AnalysisDataSource
        _analysis_data_source = AnalysisDataSource()
    # from rqfactor.analysis import factor_analysis as _factor_analysis
    from rqfactor.analysis import factor_analysis as _factor_analysis
    if benchmark is None:
        raise ValueError('Benchmark required!')
    if f is None or (isinstance(f, pd.DataFrame) and f.empty) or (
            not isinstance(f, pd.DataFrame) and not isinstance(f, AbstractFactor)):
        raise ValueError('non-empty dataframe or AbstractFactor object is required!')

    if isinstance(f, AbstractFactor):
        if start_date is None or end_date is None:
            raise ValueError('both start_date and end_date must not be None!')
        trading_dates = _analysis_data_source.get_trading_dates(start_date, end_date)

        prev_start_date = _analysis_data_source.get_previous_trading_date(trading_dates[0])
        end_date = trading_dates[-1]

        s_start = trading_dates[0].strftime('%Y-%m-%d')
        s_end = trading_dates[-1].strftime('%Y-%m-%d')

        if universe is None:
            all_stocks = _analysis_data_source.all_instruments('CS')
            order_book_ids = all_stocks.order_book_id[
                (all_stocks['listed_date'] < s_start) &
                ((all_stocks['de_listed_date'] == '0000-00-00')
                 | (all_stocks['de_listed_date'] > s_end))].tolist()  # de_listed_date当天没有数据
        else:
            dates = trading_dates[::period]
            order_book_ids = _analysis_data_source.get_combined_index_components(universe, dates[0], dates[-1])

            order_book_ids = [
                i.order_book_id for i in _analysis_data_source.instruments(list(order_book_ids))
                if i.listed_date < s_start and (
                        i.de_listed_date == '0000-00-00' or i.de_listed_date > s_end)
            ]
        f = execute_factor(
            f, order_book_ids,
            start_date=prev_start_date,
            end_date=end_date,
            universe=universe
        )

    if isinstance(f, pd.DataFrame):
        try:
            f.index = index = pd.to_datetime(f.index)
        except ValueError:
            raise ValueError('index must be datetime likely object')

        trading_dates = _analysis_data_source.get_trading_dates(index[0], index[-1])
        if len(trading_dates) > len(index):
            raise ValueError('not enough trading dates!')
        out_dates = [i for i in trading_dates if i not in index]
        if out_dates:
            raise ValueError('Ambiguous index! dates {} is outside the index!'.format(out_dates))
        f = f.reindex(trading_dates)

        start_date = f.index[1]
        end_date = f.index[-1]

    return _factor_analysis(f, _analysis_data_source, period, frequency=frequency, universe=universe, shift=shift,
                            start_date=start_date, end_date=end_date, rank_ic=rank_ic,
                            quantile=quantile, ascending=ascending, winzorization=winzorization,
                            normalization=normalization, neutralization=neutralization,
                            include_st=include_st, include_new=include_new, benchmark=benchmark,
                            update_class=None)


def execute_factor(factor, order_book_ids, start_date, end_date, universe=None):
    """
    因子计算

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
        因子对象
    order_book_ids : list
        股票列表
    start_date : date_like, str, int, float, datetime
        开始日期
    end_date : date_like, str, int, float, datetime
        结束日期
    universe: str, 默认 None
        股票池

    Returns
    -------
    pandas.DataFrame
    """
    from rqfactor.engine_v2 import execute_factor as _execute_factor
    return _execute_factor(factor, order_book_ids, start_date, end_date, universe=universe)

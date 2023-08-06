# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from collections import defaultdict
from functools import partial

from .interface import AbstractFactor

__all__ = [
    'RANK', 'SCALE', 'DEMEAN',
    'CS_ZSCORE', 'QUANTILE',
    'TOP', 'BOTTOM',
    'INDUSTRY_NEUTRALIZE',
    'CS_REGRESSION_RESIDUAL', 'CS_FILLNA'
]


class CrossSectionalFactor(AbstractFactor):
    """
    基础横截面因子抽象类
    """
    def __hash__(self):
        return id(self)

    def execute(self, *factors):
        raise NotImplementedError

    @property
    def sub_factors(self):
        raise NotImplementedError

    @property
    def expr(self):
        return self

    @property
    def dependencies(self):
        return [self]


class UnaryCrossSectionalFactor(CrossSectionalFactor):
    """
    单元横截面因子类

    Parameters
    ----------
    func : function, 函数
    factor : rqfactor.interface.AbstractFactor
    args : 位置参数
    kwargs : 关键字参数

    Examples
    --------
    构造一个横截面因子

    >>> from rqfactor import Factor
    >>> def cummin(df, **kwargs):
    ...     return df.cummin(axis=1, **kwargs)
    >>> factor = UnaryCrossSectionalFactor(cummin, Factor('close'))
    >>> factor
    CrossSectional(cummin, Factor('close'))

    """
    def __init__(self, func, factor, *args, **kwargs):
        self._func = func
        self._factor = factor
        self._args = args
        self._kwargs = kwargs

    def __repr__(self):
        return 'CrossSectional({}, {!r})'.format(self._func.__name__, self._factor)

    def execute(self, *factors):
        return self._func(*(factors + self._args), **self._kwargs)

    @property
    def sub_factors(self):
        return [self._factor]

    @property
    def shift(self):
        return self._factor.shift


def rank(df, **kwargs):
    """
    横截面排名

    Parameters
    ----------
    df : pandas.DataFrame
    kwargs :
        * method: {'average', 'min', 'max', 'first', 'dense'}
            ** average: 使用分组平均排名
            ** min: 使用分组最小排名
            ** max: 使用分组最大排名
            ** first: 值在原始序列中出现的次序排名
            ** dense: 类似 'min', 但是分组之间排名总是增加1
        * ascending: boolean
            排名是否用升序

    Returns
    -------
    pandas.DataFrame
    """
    return df.rank(axis=1, pct=True, **kwargs)


def RANK(factor, method='average', ascending=True):
    """
    横截面排名

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    method : str, 默认 'average'
        * average: 使用分组平均排名
        * min: 使用分组最小排名
        * max: 使用分组最大排名
        * first: 值在原始序列中出现的次序排名
        * dense: 类似 'min', 但是分组之间排名总是增加1
    ascending : boolean, 默认 True
        是否用升序进行排名

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    if method not in {'average', 'min', 'max', 'first', 'dense'}:
        raise ValueError('invalid method value({}), valid: {}'.format(method, 'first, min, max, average, dense'))
    if not isinstance(ascending, bool):
        raise ValueError('invalid ascending value({}), should be True/False'.format(ascending))

    return UnaryCrossSectionalFactor(rank, factor, method=method, ascending=ascending)


def scale(df, to=1):
    """
    横截面缩放函数

    Parameters
    ----------
    df : pandas.DataFrame
    to : float, int, 默认 1
        缩放系数

    Returns
    -------
    pandas.DataFrame
    """
    with pd.option_context('mode.use_inf_as_na', True):
        return df.divide(df.abs().sum(axis=1), axis='index') * to


def SCALE(factor, to=1):
    """
    横截面缩放

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    to : float, int, 默认 1
        缩放系数

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    if to <= 0:
        raise ValueError('scale target should be greater than 0')

    return UnaryCrossSectionalFactor(scale, factor, to=to)


def demean(df):
    """
    横截面去平均函数

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """
    with pd.option_context('mode.use_inf_as_na', True):
        return df.subtract(df.mean(axis=1), axis='index')


def DEMEAN(factor):
    """
    横截面去平均

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    return UnaryCrossSectionalFactor(demean, factor)


def zscore(df):
    """
    横截面z-score函数

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """
    with pd.option_context('mode.use_inf_as_na', True):
        return df.subtract(df.mean(axis=1), axis='index').divide(df.std(axis=1), axis='index')


def CS_ZSCORE(factor):
    """
    横截面z-score

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    return UnaryCrossSectionalFactor(zscore, factor)


def quantile(df, bins=5, ascending=True):
    """
    横截面分为数函数

    Parameters
    ----------
    df : pandas.DataFrame
    bins : int, 默认 5
        分位数， 10为10份, 等等。 依此类推
    ascending : boolean, 默认 True
        升序 or 降序， 按照[bins, bins-1, ..., 1]

    Returns
    -------
    pandas.DataFrame
    """
    lables = list(range(1, bins+1))
    if not ascending:
        lables.reverse()

    return df.apply(lambda s: pd.qcut(s, bins, lables), axis='columns').astype(float)


def QUANTILE(factor, bins=5, ascending=True):
    """
    横截面分位数

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    bins : int, 默认 5
        分位数， 10为10份, 等等。 依此类推
    ascending : boolean, 默认 True
        升序 or 降序， 按照[bins, bins-1, ..., 1]

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    if bins <= 0:
        raise ValueError('bins should be greater than 0, got {}'.format(bins))

    return UnaryCrossSectionalFactor(quantile, factor, bins=bins, ascending=ascending)


def top(df, threshold=50, pct=False):
    """
    横截面截取排名最高（顶部）函数
    按照横截面rank之后截取排名最高的若干并设置为1，其他设置为0

    Parameters
    ----------
    df : pandas.DataFrame
    threshold : int or float, 默认 50(%)
        截取阈值
    pct : boolean, 默认 False
        是否按照百分比进行截取

    See also
    --------
    top : 截取底部

    Returns
    -------
    pandas.DataFrame
    """
    if pct:
        threshold /= 100.0

    return df.rank(axis=1, method='first', ascending=False, pct=pct).applymap(
        lambda e: 1 if e <= threshold else 0)


def bottom(df, threshold=50, pct=False):
    """
    横截面截取排名最低（底部）函数
    按照横截面rank之后截取排名最低的若干并设置为1，其他设置为0

    Parameters
    ----------
    df : pandas.DataFrame
    threshold : int or float, 默认 50(%)
        截取阈值
    pct : boolean, 默认 False
        是否按照百分比进行截取

    See also
    --------
    top : 截取顶部

    Returns
    -------
    pandas.DataFrame
    """
    if pct:
        threshold /= 100.0

    return df.rank(axis=1, method='first', ascending=True, pct=pct).applymap(
        lambda e: 1 if e <= threshold else 0)


def TOP(factor, threshold=50, pct=False):
    """
    横截面截取排名最高（顶部）
    按照横截面rank之后截取排名最高的若干并设置为1，其他设置为0

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    threshold : int or float, 默认 50(%)
        截取阈值
    pct : boolean, 默认 False
        是否按照百分比进行截取

    See also
    --------
    BOTTOM : 底部 N(%)

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    return UnaryCrossSectionalFactor(top, factor, threshold=threshold, pct=pct)


def BOTTOM(factor, threshold=50, pct=False):
    """
    横截面截取排名最低（底部）
    按照横截面rank之后截取排名最低的若干并设置为1，其他设置为0

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    threshold : int or float, 默认 50(%)
        截取阈值
    pct : boolean, 默认 False
        是否按照百分比进行截取


    See also
    --------
    TOP : 顶部 N(%)

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    return UnaryCrossSectionalFactor(bottom, factor, threshold=threshold, pct=pct)


def industry_neutralize(df, source='citics_2019'):
    """
    横截面行业中心化函数

    Parameters
    ----------
    df : pandas.DataFrame
    source : {'sws', 'citics', 'citics_2019', 'gildata'}, 默认 'citics_2019'
        * sws: 使用申万行业分类
        * citics: 使用中信行业分类
        * gildata: 使用聚源行业分类
        其他变化参见: doc(rqdatac.get_instrument_industry)
    Returns
    -------
    pandas.DataFrame
    """
    # should not, but ...
    import rqdatac
    latest_date = df.index[-1]
    industry_tag = rqdatac.get_instrument_industry(
        df.columns.tolist(), source=source, date=latest_date
    )['first_industry_name']
    indexes = defaultdict(list)
    for i, v in enumerate(industry_tag):
        indexes[v].append(i)

    result = df.copy()
    height = result.shape[0]
    result.values[np.isinf(result.values)] = np.nan
    for v in indexes.values():
        mean = np.nanmean(result.values[:, v], axis=1)
        result.values[:, v] -= mean.reshape((height, 1))

    return result.reindex(columns=df.columns)


def INDUSTRY_NEUTRALIZE(factor, source='citics_2019'):
    """
    横截面行业中心化

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    source : {'sws', 'citics', 'citics_2019', 'jy}, 默认 'citics_2019'
        * sws: 使用申万行业分类
        * citics: 使用中信行业分类
        * jy: 使用聚源行业分类

    Returns
    -------
    rqfactor.cross_sectional.UnaryCrossSectionalFactor
    """
    print('>>> industry nuetralize with source = citics 2019')
    assert source in {'sws', 'citics', 'citics_2019', 'jy'}
    return UnaryCrossSectionalFactor(industry_neutralize, factor, source)


class CombinedCrossSectionalFactor(CrossSectionalFactor):
    """
    组合多个因子为新的横截面因子类

    Parameters
    ----------
    func : function
    factors : rqfactor.interface.AbstractFactor

    Examples
    --------
    一个例子

    >>> from rqfactor import Factor
    >>> from functools import reduce
    >>> def add(*dfs):
    ...     return reduce(lambda x,y:x+y, dfs[1:], dfs[0])
    >>> factor = CombinedCrossSectionalFactor(add, Factor('close'), Factor('open'))
    >>> factor
    CrossSectional(add, (Factor('close'), Factor('open')))

    """
    def __init__(self, func, *factors):
        self._func = func
        self._factors = factors
        self._shift = max(factor.shift for factor in factors)

    @property
    def shift(self):
        return self._shift

    @property
    def sub_factors(self):
        return self._factors

    def execute(self, *args):
        return self._func(*args)

    def __repr__(self):
        return 'CrossSectional({}, {})'.format(self._func, tuple(self._factors))


def regression(Y, *X, add_const=True):
    """
    横截面拟合回归函数

    Parameters
    ----------
    Y : pandas.DataFrame
        拟合目标
    X : pandas.DataFrame
        拟合参数Xi
    add_const: boolean, 默认 True
        是否增加含常量部分

    Returns
    -------
    pandas.DataFrame
    """
    result = np.empty(Y.shape)
    result.fill(np.nan)

    for i in range(len(Y)):
        mask = np.isfinite(Y.values[i])
        for xi in X:
            mask &= np.isfinite(xi.values[i])

        rhs = list(xi.values[i][mask] for xi in X)
        if add_const:
            rhs += [np.ones(np.sum(mask))]
        x = np.vstack(rhs).T
        y = Y.values[i][mask]
        # http://blog.mmast.net/least-squares-fitting-numpy-scipy
        a = np.dot(np.linalg.pinv(np.dot(x.T, x)), np.dot(x.T, y))
        result[i][mask] = y - np.dot(x, a)

    return pd.DataFrame(result, index=Y.index, columns=Y.columns)


def CS_REGRESSION_RESIDUAL(Y, *X, add_const=True):
    """
    横截面拟合回归

    Parameters
    ----------
    Y : rqfactor.interface.AbstractFactor
        拟合目标
    X : rqfactor.interface.AbstractFactor
        拟合参数Xi
    add_const : boolean, 默认 True
        是否增加常量部分（即 X*theta=Y or X*theta+C=Y的问题)

    Examples
    --------
    一个例子

    >>> from rqfactor import Factor
    >>> Y = Factor('close')
    >>> X1 = Factor('open')
    >>> factor = CS_REGRESSION_RESIDUAL(Y, X1)
    >>> factor
    CrossSectional(functools.partial(regression, add_const=True), (Factor('close'), Factor('open')))

    Returns
    -------
    rqfactor.cross_sectional.CombinedCrossSectionalFactor
    """
    if not X:
        raise ValueError('CS_REGRESSION: at least one X required')

    wrapper = partial(regression, add_const=add_const)
    return CombinedCrossSectionalFactor(wrapper, Y, *X)


def fillna(df, source='citics_2019'):
    """
    横截面nan值填充，行业分组均值

    Parameters
    ----------
    df : pandas.DataFrame
    source : {'sws', 'citics', 'citics_2019', 'gildata'}, 默认 'citics_2019'
        * sws: 使用申万行业分类
        * citics: 使用中信行业分类
        * gildata: 使用聚源行业分类
        其他变化参加: doc(rqdatac.get_instrument_industry)
    Returns
    -------
    pandas.DataFrame
    """
    import rqdatac
    latest_date = df.index[-1]

    industry_tag = rqdatac.get_instrument_industry(
        df.columns.tolist(), source=source, date=latest_date
    )['first_industry_name']
    indexes = defaultdict(list)
    for i, v in enumerate(industry_tag):
        indexes[v].append(i)

    result = df.copy()
    result.values[np.isinf(result.values)] = np.nan
    for v in indexes.values():
        arr = result.values[:, v].T
        nan_index = np.isnan(arr)
        # https://www.geeksforgeeks.org/python-replace-nan-values-with-average-of-columns/ method 2
        result.values[:, v] = np.where(nan_index,
                                       np.ma.array(arr, mask=nan_index).mean(axis=0),
                                       arr).T
    return result


def CS_FILLNA(factor, source='citics_2019'):
    """
    横截面nan填充，使用行业分组均值进行填充

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    source : {'sws', 'citics', 'citics_2019', 'jy'}, 默认 'citics_2019'
        * sws: 使用申万行业分类
        * citics/citics_2019: 使用中信行业分类
        * jy: 使用聚源行业分类

    Returns
    -------
    rqfactor.cross_sectional.CombinedCrossSectionalFactor
    """
    assert source in {'sws', 'citics', 'citics_2019', 'jy'}
    return UnaryCrossSectionalFactor(fillna, factor, source)

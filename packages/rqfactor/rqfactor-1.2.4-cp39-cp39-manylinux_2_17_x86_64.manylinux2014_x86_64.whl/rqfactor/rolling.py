# -*- coding: utf-8 -*-
from itertools import chain
import numpy as np

from .interface import AbstractFactor, ShiftedFactor, BinaryCombinedFactor
from .utils import rolling_window


__all__ = [
    'COUNT',
    'TS_RANK',
    'EVERY', 'PRODUCT',
    'COV', 'COVARIANCE',
    'TS_REGRESSION', 'TS_ZSCORE',
    'TS_SKEW', 'TS_KURT', 'AVEDEV',
    'TS_ARGMAX', 'TS_ARGMIN',
    'CORR', 'CORRELATION',
    'MA', 'EMA', 'WMA', 'SMA',
    'STD', 'STDDEV', 'VAR',
    'DECAY_LINEAR', 'SLOPE', 'SUM',
    'TS_MIN', 'TS_MAX', 'HHV', 'LLV',
]


class RollingWindowFactor(AbstractFactor):
    """
    滑动窗口因子类

    Parameters
    ----------
    func : function
        函数
    window : int
        窗口大小
    factor : rqfactor.interface.AbstractFactor
    """
    def __init__(self, func, window, factor):
        assert isinstance(factor, AbstractFactor)
        self._func = func
        self._factor = factor
        self._window = window

    @property
    def dependencies(self):
        return self._factor.dependencies

    @property
    def expr(self):
        return self._func, (self._factor.expr, self._window)

    @property
    def shift(self):
        return self._window - 1 + self._factor.shift

    def __repr__(self):
        return '{}({!r}, {})'.format(self._func.__name__, self._factor, self._window)


def count(x, window):
    # force to bool
    x = x if x.dtype == bool else x.astype(np.bool)
    r = rolling_window(x, window)
    # np has its own bool type and np.sum can be used to count occurrence of True
    return np.sum(r, axis=1)


def COUNT(factor, window):
    """
    滑动真值计数

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(count, window, factor)


def ts_rank(x, window):
    r = rolling_window(x, window)  # 1-dim -> 2-dim
    rank = r.argsort(axis=-1).argsort(axis=-1)[:, -1]
    return rank / window


def TS_RANK(factor, window):
    """
    滑动排序（在时间序列上）

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(ts_rank, window, factor)


def EVERY(factor, window):
    """
    滑动计数全部为真

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.interface.BinaryCombinedFactor
    """
    return BinaryCombinedFactor(np.equal, COUNT(factor, window), window)


def product(s, window):
    return np.product(rolling_window(s, window), axis=1)


def PRODUCT(factor, window):
    """
    滑动乘积

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(product, window, factor)


class CombinedRollingWindowFactor(AbstractFactor):
    """
    组合滑动因子类

    Parameters
    ----------
    func : function
    window : int
    args : rqfactor.interface.AbstractFactor

    Note
    ----
    args中所有参数都必须为AbstractFactor的子类对象

    """
    def __init__(self, func, window, *args):
        assert all(isinstance(f, AbstractFactor) for f in args)
        max_shift = max(f.shift for f in args)

        def shift_if_need(arg):
            if arg.shift < max_shift:
                return ShiftedFactor(arg, max_shift - arg.shift)
            return arg

        self._func = func
        self._window = window
        self._factors = [shift_if_need(arg) for arg in args]
        self._shift = max_shift + window - 1

    @property
    def expr(self):
        args = [f.expr for f in self._factors]
        return self._func, tuple([self._window] + args)

    @property
    def shift(self):
        return self._shift

    @property
    def dependencies(self):
        return list(chain(*(f.dependencies for f in self._factors)))

    def __repr__(self):
        return '{}({})'.format(self._func.__name__, ', '.join(repr(f) for f in self._factors))


def covariance(window, a, b):
    ab = a * b
    r_a = rolling_window(a, window)
    r_b = rolling_window(b, window)
    r_ab = rolling_window(ab, window)
    return r_ab.mean(axis=1) - r_a.mean(axis=1) * r_b.mean(axis=1)


def COVARIANCE(a, b, window):
    """
    滑动协方差

    Parameters
    ----------
    a : rqfactor.interface.AbstractFactor
    b : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.CombinedRollingWindowFactor
    """
    return CombinedRollingWindowFactor(covariance, window, a, b)


# alias for COVARIANCE
COV = COVARIANCE


def regression(window, x, y):
    xy = x * y
    x2 = x * x
    r_x = rolling_window(x, window)
    r_y = rolling_window(y, window)
    r_xy = rolling_window(xy, window)
    r_x2 = rolling_window(x2, window)
    r_x_mean = r_x.mean(axis=1)
    r_y_mean = r_y.mean(axis=1)
    v1 = (r_xy.sum(axis=1) - r_x_mean*r_y_mean * window)
    v2 = (r_x2.sum(axis=1) - r_x_mean*r_x_mean * window)
    return v1 / v2


def TS_REGRESSION(Y, X, window):
    """
    滑动拟合回归

    Parameters
    ----------
    Y : rqfactor.interface.AbstractFactor
    X : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.CombinedRollingWindowFactor
    """
    return CombinedRollingWindowFactor(regression, window, X, Y)


def zscore(s, window):
    r_s = rolling_window(s, window)
    return (s[window-1:] - r_s.mean(axis=1)) / r_s.std(axis=1)


def TS_ZSCORE(factor, window):
    """
     滑动z分数

     Parameters
     ----------
     factor : rqfactor.interface.AbstractFactor
     window : int

     Returns
     -------
     rqfactor.rolling.RollingWindowFactor
     """
    return RollingWindowFactor(zscore, window, factor)


def skew(s, n):
    s3 = s*s*s
    r_s = rolling_window(s, n)
    r_s3 = rolling_window(s3, n)
    u = r_s.mean(axis=1)
    u_s3 = r_s3.mean(axis=1)
    std = r_s.std(axis=1, ddof=0)

    result = (u_s3 - 3*u*std*std - u*u*u) / (std*std*std)
    # https://stackoverflow.com/questions/37647961/how-does-pandas-calculate-skew
    if n > 2:
        c = ((n * (n-1))**0.5) / (n - 2)
        result = c * result
    return result


def TS_SKEW(factor, window):
    """
     滑动偏度

     Parameters
     ----------
     factor : rqfactor.interface.AbstractFactor
     window : int

     Returns
     -------
     rqfactor.rolling.RollingWindowFactor
     """
    return RollingWindowFactor(skew, window, factor)


def kurt(s, n):
    s2 = s * s
    s3 = s * s2
    s4 = s2 * s2
    r_s = rolling_window(s, n)
    u, std = r_s.mean(axis=1), r_s.std(axis=1, ddof=0)
    u2, u3 = rolling_window(s2, n).mean(axis=1), rolling_window(s3, n).mean(axis=1)
    u4 = rolling_window(s4, n).mean(axis=1)
    u_2, std_2 = u * u, std * std
    v = u4 - 3*u_2*u_2 - 4*u*u3 + 6*u_2*u2

    # https://en.wikipedia.org/wiki/Kurtosis G_2
    if n > 3:
        return (n+1)*n*n*v / ((n-1)*(n-2)*(n-3)) - 3*(n-1)*(n-1) / ((n-2)*(n-3))
    else:
        return v / (std_2 * std_2) - 3


def TS_KURT(factor, window):
    """
     滑动峰度

     Parameters
     ----------
     factor : rqfactor.interface.AbstractFactor
     window : int

     Returns
     -------
     rqfactor.rolling.RollingWindowFactor
     """
    return RollingWindowFactor(kurt, window, factor)


def avedev(s, window):
    r_s = rolling_window(s, window)
    return np.abs(r_s.T - r_s.mean(axis=1)).T.mean(axis=1)


def AVEDEV(factor, window):
    """
     滑动平均绝对离差

     Parameters
     ----------
     factor : rqfactor.interface.AbstractFactor
     window : int

     Returns
     -------
     rqfactor.rolling.RollingWindowFactor
     """
    return RollingWindowFactor(avedev, window, factor)


def ts_argmax(x, n):
    r = rolling_window(x, n)
    return r.argmax(axis=-1).astype(float)


def TS_ARGMAX(factor, n):
    """
    滑动最大值索引

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    See also
    --------
    TS_ARGMIN: vice versa

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(ts_argmax, n, factor)


def ts_argmin(x, n):
    r = rolling_window(x, n)
    return r.argmin(axis=-1).astype(float)


def TS_ARGMIN(factor, n):
    """
    滑动最小值索引

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    See also
    --------
    TS_ARGMAX: vice versa

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(ts_argmin, n, factor)


def correlation(window, a, b):
    ab = a * b
    r_a = rolling_window(a, window)
    r_b = rolling_window(b, window)
    r_ab = rolling_window(ab, window)
    std_a = r_a.std(axis=1, ddof=0)
    std_b = r_b.std(axis=1, ddof=0)
    return (r_ab.mean(axis=1) - r_a.mean(axis=1) * r_b.mean(axis=1)) / (std_a * std_b)


def CORRELATION(a, b, window):
    """
    滑动皮尔逊相关系数

    Parameters
    ----------
    a : rqfactor.interface.AbstractFactor
    b : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.CombinedRollingWindowFactor
    """
    return CombinedRollingWindowFactor(correlation, window, a, b)


# just an alias for CORRELATION
CORR = CORRELATION


def ma(x, n):
    return rolling_window(x, n).mean(axis=1)


def MA(factor, window):
    """
    简单移动平均

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(ma, window, factor)


SMA = MA


def ema(x, n):
    rx = rolling_window(x, n)
    alpha = 2.0 / (n + 1)
    weights = alpha * (1 - alpha) ** np.arange(n-1, -1, -1.)
    return (rx * weights).sum(axis=1)


def EMA(factor, window):
    """
    指数移动平均 (平滑系数=2)

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(ema, window, factor)


def wma(x, n):
    rx = rolling_window(x, n)
    weights = 2 * np.arange(1, n+1) / (n * (n+1))
    return (rx * weights).sum(axis=1)


def WMA(factor, window):
    """
    加权移动平均

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(wma, window, factor)


DECAY_LINEAR = WMA


def std(x, n):
    rx = rolling_window(x, n)
    return rx.std(axis=1)


def STD(factor, window):
    """
    移动标准差

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(std, window, factor)


STDDEV = STD


def var(x, n):
    rx = rolling_window(x, n)
    return rx.var(axis=1)


def VAR(factor, window):
    """
    移动方差

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(var, window, factor)


def slope(y, n):
    x = np.arange(n, dtype=float)
    sumx = x.sum()
    sumxsqr = n * (n-1) * (2 * n - 1) / 6
    divisor = sumx * sumx - n * sumxsqr
    ry = rolling_window(y, n)
    return (n * (ry * x).sum(axis=1) - ry.sum(axis=1) * sumx) / divisor


def SLOPE(factor, window):
    """
    滑动线性拟合斜率

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(slope, window, factor)


def sum(x, n):
    rx = rolling_window(x, n)
    return rx.sum(axis=1)


def SUM(factor, window):
    """
    滑动求和

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(sum, window, factor)


def ts_min(x, n):
    rx = rolling_window(x, n)
    return rx.min(axis=1)


def TS_MIN(factor, window):
    """
    滑动最小值

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(ts_min, window, factor)


def ts_max(x, n):
    rx = rolling_window(x, n)
    return rx.max(axis=1)


def TS_MAX(factor, window):
    """
    滑动最小值

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    window : int

    Returns
    -------
    rqfactor.rolling.RollingWindowFactor
    """
    return RollingWindowFactor(ts_max, window, factor)


HHV = TS_MAX
LLV = TS_MIN

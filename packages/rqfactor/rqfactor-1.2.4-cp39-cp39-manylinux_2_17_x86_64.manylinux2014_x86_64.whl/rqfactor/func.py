# -*- coding: utf-8 -*-
import numpy as np

from .interface import UnaryCombinedFactor, BinaryCombinedFactor, AbstractFactor, CombinedFactor
from .utils import FixShift, rolling_window
from .exception import RQFactorUserException
from ._dma import dma, dma_array

__all__ = [
    'AS_FLOAT', 'ABS', 'SIGN', 'LOG', 'EXP', 'EQUAL',
    'SIGNEDPOWER',
    'REF', 'DELAY', 'DELTA',
    'PCT_CHANGE',
    'MIN', 'FMIN', 'MAX', 'FMAX',
    'IF',
    'CROSS',
    'TS_FILLNA',
    'DMA', 'SMA_CN', 'EMA_CN',
]


ABS = abs


def as_float(s):
    """
    转为浮点数

    Parameters
    ----------
    s: array_like, pandas.Series, numpy.ndarray

    Returns
    -------
    array_like
    """
    return s if s.dtype == float else s.astype(float)


def AS_FLOAT(factor):
    """
    转换为浮点数

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor

    Returns
    -------
    rqfactor.interface.UnaryCombinedFactor
    """
    return UnaryCombinedFactor(as_float, factor)


def SIGN(factor):
    """
    求符号
    返回 x<0 : -1
        x=0 : 0
        x>0 : 1
        nan : nan

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor

    Returns
    -------
    rqfactor.interface.UnaryCombinedFactor
    """
    return UnaryCombinedFactor(np.sign, factor)


def LOG(factor):
    """
    自然对数（自然常数e为底的对数）

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor

    See also
    -------
    EXP: exponential


    Returns
    -------
    rqfactor.interface.UnaryCombinedFactor
    """
    return UnaryCombinedFactor(np.log, factor)


def EXP(factor):
    """
    自然常数e为底的幂运算

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor

    See also
    -------
    LOG: logarithm

    Returns
    -------
    rqfactor.interface.UnaryCombinedFactor
    """
    return UnaryCombinedFactor(np.exp, factor)


def EQUAL(left, right):
    """
    left == right

    Parameters
    ----------
    left : float, rqfactor.interface.AbstractFactor
    right : float, rqfactor.interface.AbstractFactor

    Returns
    -------
    float, rqfactor.interface.BinaryCombinedFactor
    """
    if not isinstance(left, AbstractFactor) and not isinstance(right, AbstractFactor):
        if left != left:
            return left
        if right != right:
            return right

        return left == right

    return BinaryCombinedFactor(np.equal, left, right)


def SIGNEDPOWER(x, e):
    """
    SIGN(x) * (ABS(x) ** e)

    Parameters
    ----------
    x : rqfactor.interface.AbstractFactor
    e : float, rqfactor.interface.AbstractFactor

    See also
    --------
    SIGN: give sign
    ABS: give absolutely value

    Returns
    -------
    rqfactor.interface.BinaryCombinedFactor
    """
    return SIGN(x) * (ABS(x) ** e)


class RefFactor(AbstractFactor):
    """
    对因子值在时间序列上进行平移处理的因子类（方向往前）

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    n : int
    """
    def __init__(self, factor, n):
        assert isinstance(factor, AbstractFactor)

        self._factor = factor
        self._n = n

    @staticmethod
    def _ref(s, n):
        return s[:-n]

    @property
    def expr(self):
        return self._ref, (self._factor.expr, self._n)

    @property
    def dependencies(self):
        return self._factor.dependencies

    @property
    def shift(self):
        return self._n + self._factor.shift

    def __repr__(self):
        return 'REF({!r}, {})'.format(self._factor, self._n)


def REF(factor, shift):
    """
    简单时间序列上的因子平移函数

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    shift : int
        大于或等于0，如果为0等价于factor

    Examples
    --------
    构造一个简单的平移类算子

    >>> from rqfactor import Factor
    >>> ref = REF(Factor('close'), 1) # 昨日收盘价
    >>> ref
    REF(Factor('close'), 1)
    >>> factor = Factor('close') / ref - 1 # 今日收益率
    >>> factor
    true_divide(subtract(shift(Factor('close'), 1), REF(Factor('close'), 1)), REF(Factor('close'), 1))

    Returns
    -------
    rqfactor.func.RefFactor
    """
    assert shift >= 0 and isinstance(shift, int)
    if shift == 0:
        return factor
    return RefFactor(factor, shift)


DELAY = REF     # DELAY is an alias to REF


def DELTA(x, d):
    """
    今日与d日前的值的差

    Parameters
    ----------
    x : rqfactor.interface.AbstractFactor
    d : int
        必须大于0

    Examples
    --------
    更简单的获取收益率的算子

    >>> from rqfactor import Factor
    >>> factor = DELTA(Factor('close'), 1) / REF(Factor('close'), 1)

    See also
    --------
    REF: 延期函数
    DELAY: REF别名函数

    Returns
    -------
    rqfactor.interface.BinaryCombinedFactor
    """
    return x - REF(x, d)


def PCT_CHANGE(factor, n):
    """
    当前值与n日前值的变化率（增长率）

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    n : int
        必须大于0

    See also
    --------
    REF: 延期函数
    DELAY: REF别名函数

    Returns
    -------
    rqfactor.interface.BinaryCombinedFactor
    """
    return factor / REF(factor, n) - 1


def MIN(left, right):
    """
    最小值

    Parameters
    ----------
    left : float, rqfactor.interface.AbstractFactor
    right : float, rqfactor.interface.AbstractFactor

    Returns
    -------
    float, rqfactor.interface.BinaryCombinedFactor
    """
    if not isinstance(left, AbstractFactor) and not isinstance(right, AbstractFactor):
        if left != left:
            return left
        if right != right:
            return right

        return left if left < right else right

    return BinaryCombinedFactor(np.minimum, left, right)


def FMIN(left, right):
    """
    最小值，尽可能忽略nan

    Parameters
    ----------
    left : float, rqfactor.interface.AbstractFactor
    right : float, rqfactor.interface.AbstractFactor

    Returns
    -------
    float, rqfactor.interface.BinaryCombinedFactor
    """
    if not isinstance(left, AbstractFactor) and not isinstance(right, AbstractFactor):
        if left != left:
            return right
        if right != right:
            return left
        return left if left < right else right

    return BinaryCombinedFactor(np.fmin, left, right)


def MAX(left, right):
    """
    最大值

    Parameters
    ----------
    left : float, rqfactor.interface.AbstractFactor
    right : float, rqfactor.interface.AbstractFactor

    Returns
    -------
    float, rqfactor.interface.BinaryCombinedFactor
    """
    if not isinstance(left, AbstractFactor) and not isinstance(right, AbstractFactor):
        if left != left:
            return left
        if right != right:
            return right
        return left if left > right else right

    return BinaryCombinedFactor(np.maximum, left, right)


def FMAX(left, right):
    """
    最大值，尽可能忽略nan

    Parameters
    ----------
    left : float, rqfactor.interface.AbstractFactor
    right : float, rqfactor.interface.AbstractFactor

    Returns
    -------
    float, rqfactor.interface.BinaryCombinedFactor
    """
    if not isinstance(left, AbstractFactor) and not isinstance(right, AbstractFactor):
        if left != left:
            return right
        if right != right:
            return left
        return left if left > right else right

    return BinaryCombinedFactor(np.fmax, left, right)


def IF(condition, true_value, false_value):
    """
    条件选择

    Parameters
    ----------
    condition : rqfactor.interface.AbstractFactor, boolean_like object
    true_value : float, rqfactor.interface.AbstractFactor
    false_value : float, rqfactor.interface.AbstractFactor

    Notes
    -----
    true_value与false_value至少一个应为rqfactor.interface.CombinedFactor

    Returns
    -------
    float, rqfactor.interface.CombinedFactor
    """
    if not isinstance(condition, AbstractFactor):
        return true_value if condition else false_value

    return CombinedFactor(np.where, condition, true_value, false_value)


def cross(s1, s2):
    """
    交叉对比函数

    Parameters
    ----------
    s1 : array_like
    s2 : array_like

    Returns
    -------
    array_like, boolean array
    """
    if not isinstance(s1, np.ndarray):
        s1 = np.repeat(s1, len(s2))
    elif not isinstance(s2, np.ndarray):
        s2 = np.repeat(s2, len(s1))

    r1 = s1[1:] > s2[1:]
    r2 = s1[:-1] <= s2[:-1]

    return r1 & r2


def CROSS(f1, f2):
    """
    交叉比较
    说明:
        比如对于两个数组 [l1, l2, ..., lN], [r1, r2, ..., rN]
        交叉比较的结果为:
        [(l1 <= r1) and (l2 > r2), (l2 <= r2) and (l3 > r3), ..., (lN-1 <= rN-1) and (lN > rN)]

    Parameters
    ----------
    f1 : float, rqfactor.interface.AbstractFactor
    f2 : float, rqfactor.interface.AbstractFactor

    Notes
    -----
    f1和f2应至少有一个为rqfactor.interface.AbstraceFactor

    Returns
    -------
    rqfactor.utils.FixShift
    """
    if not isinstance(f1, AbstractFactor) and not isinstance(f2, AbstractFactor):
        raise RQFactorUserException('CROSS: at least one factor expected, got two number: {} {}'.format(f1, f2))

    return FixShift(CombinedFactor(cross, f1, f2), 1)


def fillna_value(s, v):
    """
    nan值填充

    Parameters
    ----------
    s : array_like, input_array
    v : object
        填充的值

    Returns
    -------
    array_like
    """
    return np.where(np.isnan(s), v, s)


def fillna_mean(s, n):
    """
    滚动均值填充

    Parameters
    ----------
    s : array_like, input_array
    n : int
        窗口大小

    Returns
    -------
    array_like
    """
    mask = np.isnan(s[n-1:])
    if not mask.any():
        return s

    s_r = rolling_window(s, n)
    s_mean = np.nanmean(s_r, axis=1)
    s1 = s.copy()
    s1[n-1:][mask] = s_mean[mask]
    return s1


def fillna_forward(s, n):
    """
    向前填充

    Parameters
    ----------
    s : array_like, input_array
    n : int
        连续nan数量限制

    Returns
    -------
    array_like
    """
    flag = np.isnan(s)
    if not flag.any():
        return s

    r = np.arange(len(s))
    r1 = r.copy()
    r1[flag] = 0
    r2 = np.maximum.accumulate(r1)
    last_non_nan = r - r2
    good_nan = flag & (last_non_nan <= n)
    s1 = s.copy()
    s1[good_nan] = np.take(s, r2[good_nan])
    return s1


FILLNA_METHODS = {
    'value': fillna_value,
    'forward': fillna_forward,
    'MA': fillna_mean,
}


def TS_FILLNA(factor, nv, method='value'):
    """
    nan值填充

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    nv : float, int
        nv的取值意义参见method
    method: {'value', 'forward', 'MA'}, 默认 'value'
        * value: 统一将nan填充为nv
        * forward: 根据时间序列向前填充，最多连续不超过nv个nan
        * MA: 使用窗口的大小为nv的滑动窗口平均值填充

    Returns
    -------
    rqfactor.interface.UnaryCombinedFactor
    """
    if method not in FILLNA_METHODS:
        raise ValueError('TS_FILLNA: method should be one of {}, got {}'.format(
            list(FILLNA_METHODS.keys()), method))

    if method in ('forward', 'MA') and (not isinstance(nv, int) or nv <= 0):
        raise ValueError('TS_FILLNA: nv should be an int greater than 0, got {}'.format(nv))

    return UnaryCombinedFactor(FILLNA_METHODS[method], factor, nv)


def DMA(factor, alpha):
    """
    动态移动平均, 参数alpha
    递归公式:
        (1) 当alpha是一个浮点数
            Y[n] = X[n] * alpha + Y[n-1] * (1 - alpha)
        (2) 当alpha是一个序列
            Y[n] = X[n] * alpha[n] * Y[n-1] * (1 - alpha[n])

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    alpha : array_like

    Returns
    -------
    rqfactor.interface.CombinedFactor
    """
    if isinstance(alpha, AbstractFactor):
        return CombinedFactor(dma_array, factor, alpha)
    return CombinedFactor(dma, factor, float(alpha))


def SMA_CN(factor, N, M):
    """
    简单移动平均
    递归公式:
        Y[n] = X[n] * (M / N) + Y[n-1] * (1 - M / N)

    Parameters
    ----------
    factor: rqfactor.interface.AbstractFactor
    N: int
    M: int

    Returns
    -------
    rqfactor.interface.CombinedFactor
    """
    return DMA(factor, 1.0 * M / N)


def EMA_CN(factor, N):
    """
    指数移动平均
    递归公式:
        Y[n] = X[n] * (2 / (N + 1)) + Y[n-1] * (1 - 2 / (N + 1))

    Parameters
    ----------
    factor: rqfactor.interface.AbstractFactor
    N: int

    Returns
    -------
    rqfactor.interface.CombinedFactor
    """
    return DMA(factor, 2.0 / (N + 1))

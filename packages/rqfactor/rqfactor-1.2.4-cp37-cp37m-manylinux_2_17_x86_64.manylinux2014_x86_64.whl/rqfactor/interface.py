#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import chain

import numpy as np
import pandas as pd

import rqdatac
from .exception import RQFactorUserException, InvalidUserFactor


class AbstractFactor:
    @property
    def expr(self):
        raise NotImplementedError

    @property
    def dependencies(self):
        raise NotImplementedError

    @property
    def shift(self):
        raise NotImplementedError

    def __abs__(self):
        return UnaryCombinedFactor(np.abs, self)

    def __add__(self, other):
        return BinaryCombinedFactor(np.add, self, other)
    __radd__ = __add__

    def __sub__(self, other):
        return BinaryCombinedFactor(np.subtract, self, other)

    def __rsub__(self, other):
        return BinaryCombinedFactor(np.subtract, other, self)

    def __mul__(self, other):
        return BinaryCombinedFactor(np.multiply, self, other)
    __rmul__ = __mul__

    def __truediv__(self, other):
        return BinaryCombinedFactor(np.true_divide, self, other)

    def __rtruediv__(self, other):
        return BinaryCombinedFactor(np.true_divide, other, self)

    def __floordiv__(self, other):
        return BinaryCombinedFactor(np.floor_divide, self, other)

    def __rfloordiv__(self, other):
        return BinaryCombinedFactor(np.floor_divide, other, self)

    def __mod__(self, other):
        return BinaryCombinedFactor(np.mod, self, other)

    def __rmod__(self, other):
        return BinaryCombinedFactor(np.mod, other, self)

    def __pow__(self, other):
        return BinaryCombinedFactor(np.power, self, other)

    def __rpow__(self, other):
        return BinaryCombinedFactor(np.power, other, self)

    def __pos__(self):
        return self

    def __neg__(self):
        return UnaryCombinedFactor(np.negative, self)

    def __lt__(self, other):
        return BinaryCombinedFactor(np.less, self, other)

    def __le__(self, other):
        return BinaryCombinedFactor(np.less_equal, self, other)

    def __gt__(self, other):
        return BinaryCombinedFactor(np.greater, self, other)

    def __ge__(self, other):
        return BinaryCombinedFactor(np.greater_equal, self, other)

    # ==
    # def __eq__(self, other):
    #     return BinaryCombinedFactor(np.equal, self, other)

    def __ne__(self, other):
        return BinaryCombinedFactor(np.not_equal, self, other)

    def __and__(self, other):
        return BinaryCombinedFactor(np.logical_and, self, other)

    def __or__(self, other):
        return BinaryCombinedFactor(np.logical_or, self, other)

    def __xor__(self, other):
        return BinaryCombinedFactor(np.logical_xor, self, other)

    def __invert__(self):
        return UnaryCombinedFactor(np.logical_not, self)

    def __bool__(self):
        raise RQFactorUserException('please use IF instead')


class ConstantFactor(AbstractFactor):
    """
    常量因子类

    Parameters
    ----------
    value: number_like, int, float, str, object
    """
    def __init__(self, value):
        if isinstance(value, (pd.DataFrame, pd.Series)):
            self._value = value.values
            return
        if isinstance(value, np.ndarray):
            self._value = value
            return
        try:
            self._value = float(value)
        except ValueError:
            raise ValueError('invalid constant value {}'.format(value))

    @property
    def expr(self):
        return self._value

    @property
    def dependencies(self):
        return []

    @property
    def shift(self):
        return 0


class UnaryCombinedFactor(AbstractFactor):
    """
    单元组合因子类
    
    Parameters
    ----------
    func: function, 组合函数
    factor: rqfactor.interface.AbstractFactor
    args: object, 函数参数
    """
    def __init__(self, func, factor, *args):
        assert isinstance(factor, AbstractFactor), 'factor expected'
        self._func = func
        self._factor = factor
        self._args = args

    @property
    def shift(self):
        return self._factor.shift

    @property
    def expr(self):
        return self._func, tuple([self._factor.expr] + list(self._args))

    @property
    def dependencies(self):
        return self._factor.dependencies

    def __repr__(self):
        return '{}({!r})'.format(self._func.__name__, self._factor)


class ShiftedFactor(AbstractFactor):
    """
    移动因子类

    Parameters
    ----------
    factor: rqfactor.interface.AbstractFactor
    n: int
    """
    def __init__(self, factor, n):
        assert isinstance(factor, AbstractFactor)

        self._factor = factor
        self._n = n

    @property
    def shift(self):
        return self._factor.shift + self._n

    @property
    def dependencies(self):
        return self._factor.dependencies

    @staticmethod
    def _shift(series, n):
        if hasattr(series, 'values'):
            return series.values[n:]
        return series[n:]

    @property
    def expr(self):
        return self._shift, (self._factor.expr, self._n)

    def __repr__(self):
        return 'shift({!r}, {})'.format(self._factor, self._n)


class BinaryCombinedFactor(AbstractFactor):
    """
    二元组合因子类

    Parameters
    ----------
    func: function, 组合函数
    arg1: float, rqfactor.interface.AbstractFactor
    arg2: float, rqfactor.interface.AbstractFactor

    Notes
    -----
    arg1与arg2必须至少有一个参数为rqfactor.interface.AbstractFactor
    """
    def __init__(self, func, arg1, arg2):
        assert isinstance(arg1, AbstractFactor) or isinstance(arg2, AbstractFactor)

        self._func = func

        if isinstance(arg1, AbstractFactor) and isinstance(arg2, AbstractFactor):
            if arg1.shift > arg2.shift:
                self._arg2 = ShiftedFactor(arg2, arg1.shift - arg2.shift)
                self._arg1 = arg1
            elif arg1.shift < arg2.shift:
                self._arg1 = ShiftedFactor(arg1, arg2.shift - arg1.shift)
                self._arg2 = arg2
            else:
                self._arg1 = arg1
                self._arg2 = arg2

            self._shift = max(arg1.shift, arg2.shift)
        else:
            if isinstance(arg1, AbstractFactor):
                self._arg1 = arg1
                self._arg2 = ConstantFactor(arg2)
                self._shift = arg1.shift
            else:
                self._arg2 = arg2
                self._arg1 = ConstantFactor(arg1)
                self._shift = arg2.shift

    @property
    def expr(self):
        return self._func, (self._arg1.expr, self._arg2.expr)

    @property
    def dependencies(self):
        return self._arg1.dependencies + self._arg2.dependencies

    @property
    def shift(self):
        return self._shift

    def __repr__(self):
        return '{}({!r}, {!r})'.format(self._func.__name__, self._arg1, self._arg2)


class LeafFactor(AbstractFactor):
    """
    叶子节点基础抽象类
    """
    @property
    def expr(self):
        return self

    @property
    def dependencies(self):
        return [self]

    def __hash__(self):
        raise NotImplementedError

    @property
    def shift(self):
        return 0


class AbstractUserDefinedLeafFactor(LeafFactor):
    def execute(self, order_book_ids, start_date, end_date):
        raise NotImplementedError


class UserDefinedLeafFactor(AbstractUserDefinedLeafFactor):
    """
    用户自定义叶子节点因子类

    Parameters
    ----------
    name: str, 因子名
    func: function, 自定义算子
        返回对象必须是pandas.DataFrame，并且满足：
        （1）.index为交易日序列
         (2) .columns为股票列表

    Examples
    --------
    通过定义自定义算子构造一个因子

    >>> import rqdatac
    >>> def get_turnover_weekly(order_book_ids, start_date, end_date):
    ...     df = rqdatac.get_turnover_rate(order_book_ids, start_date, end_date, fields='week', expect_df=True)
    ...     return df['week'].unstack('order_book_id', 0)
    >>> factor = UserDefinedLeafFactor('turnover_rate_weekly', get_turnover_weekly)
    >>> factor
    UFactor(turnover_rate_weekly)
    """
    def __init__(self, name, func):
        self._name = name
        self._func = func
        self._func_name = func.__name__

    @property
    def name(self):
        return self._name

    def execute(self, order_book_ids, start_date, end_date):
        ret = self._func(order_book_ids, start_date, end_date)
        # 检查用户的自定义因子返回格式是否符合要求
        if not isinstance(ret, pd.DataFrame):
            raise InvalidUserFactor('function {}\'s returned value expect a pandas.DataFrame object, but got {}.'
                                    .format(self._func_name, type(ret)))
        if ret.empty:
            raise InvalidUserFactor('function {} returned an unexpect empty DataFrame.'.format(self._func_name))
        if not isinstance(ret.index, pd.DatetimeIndex):
            raise InvalidUserFactor('function {}\'s returned value index should be pandas.DatetimeIndex.'
                                    .format(self._func_name))

        tds = rqdatac.get_trading_dates(start_date, end_date)
        date_index = pd.to_datetime(tds)
        if date_index.shape != ret.index.shape or np.any(date_index != ret.index):
            raise InvalidUserFactor('function {}\'s returned value index mismatch, expect trading dates from {} to {}.'
                                    .format(self._func_name, start_date, end_date))
        if set(ret.columns.tolist()) != set(order_book_ids):
            raise InvalidUserFactor('function {}\'s returned value columns mismatch, expect order_book_ids as columns.'
                                    .format(self._func_name))
        return ret

    def __hash__(self):
        return id(self._func)

    def __repr__(self):
        return 'UFactor({})'.format(self._name)


class CombinedFactor(AbstractFactor):
    """
    组合因子类

    Parameters
    ----------
    func: function, 组合函数
    args: object, 一个或多个对象，至少有一个应为rqfactor.interface.AbstractFactor
    """
    def __init__(self, func, *args):
        self._func = func
        factors = [arg for arg in args if isinstance(arg, AbstractFactor)]
        assert factors
        self._shift = max(f.shift for f in factors)

        def shift_if_need(arg):
            if arg.shift < self._shift:
                return ShiftedFactor(arg, self._shift - arg.shift)
            return arg

        self._args = [shift_if_need(arg) if isinstance(arg, AbstractFactor) else ConstantFactor(arg)
                      for arg in args]

    @property
    def expr(self):
        return self._func, tuple(arg.expr for arg in self._args)

    @property
    def shift(self):
        return self._shift

    @property
    def dependencies(self):
        return list(chain(*(arg.dependencies for arg in self._args)))

    def __repr__(self):
        return '{}({})'.format(self._func.__name__, ', '.join(repr(f) for f in self._args))

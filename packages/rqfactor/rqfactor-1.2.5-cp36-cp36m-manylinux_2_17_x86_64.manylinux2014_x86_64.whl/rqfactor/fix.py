# -*- coding: utf-8 -*-
from .interface import AbstractFactor

__all__ = [
    'FIX',
]


class FixedFactor(AbstractFactor):
    """
    锁定因子值类

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    order_book_id : str
        股票代码

    Examples
    --------
    锁定因子

    >>> from rqfactor import Factor
    >>> factor = FixedFactor(Factor('close'), '000001.XSHE')  # 锁定平安银行的收盘价
    >>> factor
    FIX(Factor('close'), 000001.XSHE)

    # 现在我们计算一下因子
    >>> from rqfactor.engine_v2 import execute_factor
    >>> df = execute_factor(factor, ['000001.XSHE', '000002.XSHE', '000003.XSHE'], '20200101', '20200110')
    >>> df
                000001.XSHE  000002.XSHE
    2020-01-02    1735.5012    1735.5012
    2020-01-03    1767.3925    1767.3925
    2020-01-06    1756.0762    1756.0762
    2020-01-07    1764.3062    1764.3062
    2020-01-08    1713.8975    1713.8975
    2020-01-09    1727.2712    1727.2712
    2020-01-10    1716.9838    1716.9838

    我们发现，所有的

    """
    def __hash__(self):
        return id(self)

    def __init__(self, factor, order_book_id):
        self.factor = factor
        self.order_book_id = order_book_id

    def __repr__(self):
        return 'FIX({!r}, {})'.format(self.factor, self.order_book_id)

    @property
    def shift(self):
        return self.factor.shift

    @property
    def expr(self):
        return self

    @property
    def dependencies(self):
        return [self]


def FIX(factor, order_book_id):
    """
    创建一个锁定股票的因子对象

    Parameters
    ----------
    factor: rqfactor.interface.AbstractFactor
    order_book_id: str
        锁定的股票代码

    Returns
    -------
    rqfactor.fix.FixedFactor
    """
    if isinstance(factor, FixedFactor):
        raise ValueError('FIX: factor {} is already fixed'.format(factor))

    for f in factor.dependencies:
        if isinstance(f, FixedFactor):
            raise ValueError('FIX: factor {} is already fixed'.format(factor))

    return FixedFactor(factor, order_book_id)

# -*- coding: utf-8 -*-
import numpy as np


from .interface import AbstractFactor, LeafFactor
from .cross_sectional import CrossSectionalFactor
from .fix import FixedFactor


class FixShift(AbstractFactor):
    """
    修正偏移因子类

    Parameters
    ----------
    factor : rqfactor.interface.AbstractFactor
    shift : int
    """
    def __init__(self, factor, shift):
        self._factor = factor
        self._shift = shift

    @property
    def shift(self):
        return self._shift + self._factor.shift

    @property
    def expr(self):
        return self._factor.expr

    @property
    def dependencies(self):
        return self._factor.dependencies


def rolling_window(a, window):
    """
    滚动窗口

    Parameters
    ----------
    a: array_like
    window: int

    Returns
    -------
    array_like

    .. _Example rolling_window:
        http://stackoverflow.com/questions/6811183/rolling-window-for-1d-arrays-in-numpy
    """
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1], )
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def get_leaves(factor):
    if not isinstance(factor, AbstractFactor):
        raise TypeError('Unresolved type: {}'.format(type(factor)))
    leaves = set()
    queue = list(factor.dependencies)
    while queue:
        f = queue.pop(0)
        if isinstance(f, CrossSectionalFactor):
            for sf in f.sub_factors:
                queue.extend(sf.dependencies)
        elif isinstance(f, FixedFactor):
            queue.extend(f.factor.dependencies)
        else:
            assert isinstance(f, LeafFactor)
            leaves.add(f)
    return leaves


def get_fixed_order_book_ids(factor, order_book_ids):
    if not isinstance(factor, AbstractFactor):
        raise TypeError('Unresolved type: {}'.format(type(factor)))
    fixed = set()
    queue = list(factor.dependencies)
    while queue:
        f = queue.pop(0)
        if isinstance(f, CrossSectionalFactor):
            for sf in f.sub_factors:
                queue.extend(sf.dependencies)
        elif isinstance(f, FixedFactor):
            queue.extend(f.factor.dependencies)
            fixed.add(f)
        else:
            assert isinstance(f, LeafFactor)
    if not fixed:
        return []
    extra_ids = set()
    for f in fixed:
        if f.order_book_id not in order_book_ids:
            extra_ids.add(f.order_book_id)
    return sorted(extra_ids)


def is_cross_sectional(factor):
    if isinstance(factor, CrossSectionalFactor):
        return True

    queue = list(factor.dependencies)
    while queue:
        f = queue.pop(0)
        if isinstance(f, CrossSectionalFactor):
            return True
        if isinstance(f, FixedFactor):
            queue.extend(f.factor.dependencies)
            continue

    return False


def has_dma(expr):
    from rqfactor._dma import dma, dma_array
    if isinstance(expr, tuple):
        func, args = expr
        if func is dma or func is dma_array:
            return True
        return any(has_dma(arg) for arg in args)
    return False


def use_dma(factor):
    if isinstance(factor, CrossSectionalFactor):
        return any(use_dma(f) for f in factor.sub_factors)
    if isinstance(factor, FixedFactor):
        return use_dma(factor.factor)
    if isinstance(factor, LeafFactor):
        return False

    return has_dma(factor.expr)

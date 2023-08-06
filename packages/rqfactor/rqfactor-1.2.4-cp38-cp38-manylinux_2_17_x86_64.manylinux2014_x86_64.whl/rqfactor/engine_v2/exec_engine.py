# -*- coding: utf-8 -*-
#
# Copyright 2018 Ricequant, Inc
import numpy as np
import pandas as pd
import numbers
import warnings

import rqdatac

from rqfactor.interface import LeafFactor
from rqfactor.cross_sectional import CrossSectionalFactor
from rqfactor.fix import FixedFactor
from rqfactor.leaf import _Factor
from rqfactor.utils import get_leaves, use_dma, is_cross_sectional, get_fixed_order_book_ids

from .exec_context import PRICING_FACTORS, ThreadingExecContext, get_universe_mask


def ensure_end_date(end_date):
    date = pd.Timestamp(rqdatac.get_latest_trading_date())
    if end_date >= date:
        order_book_id = rqdatac.all_instruments('CS', date=date).order_book_id[0]
        if rqdatac.get_price(order_book_id, date, date, fields='volume') is None:
            prev_date = rqdatac.get_previous_trading_date(date)
            warnings.warn('volumes at {} is not available currently! fallback to date: {}!'.format(end_date, prev_date))
            return prev_date
        else:
            if end_date > date:
                warnings.warn('volumes after {} is not available currently! fallback to date: {}!'.format(date, date))
            return date
    return end_date


def execute_factor(factor, order_book_ids, start_date, end_date, universe=None, exec_context_class=None):
    if isinstance(factor, _Factor) and factor not in PRICING_FACTORS:
        # 类似 pe_ratio 这样的因子直接返回即可，不需要再计算了
        name = factor.name
        df = rqdatac.get_factor(order_book_ids, name, start_date, end_date, universe=universe, expect_df=True)
        return df[name].unstack('order_book_id')

    start_date, end_date = pd.Timestamp(start_date), pd.Timestamp(end_date)

    leaves = get_leaves(factor)
    if factor.shift > 0 or use_dma(factor):
        leaf_start_date = rqdatac.trading_date_offset(start_date, -factor.shift - 126)
    else:
        leaf_start_date = start_date

    # fallback end date if available
    end_date = ensure_end_date(end_date)

    if exec_context_class is None:
        exec_context_class = ThreadingExecContext
    fixed_order_book_ids = get_fixed_order_book_ids(factor, order_book_ids)
    exec_context = exec_context_class(
        leaves, order_book_ids + fixed_order_book_ids, leaf_start_date, end_date, universe=universe
    )

    universe_mask = get_universe_mask(order_book_ids, leaf_start_date, end_date, universe)
    setattr(exec_context, 'universe_mask', universe_mask)

    df = _exec_factor(factor, order_book_ids, exec_context)
    return df.loc[start_date:end_date]


def _exec_factor(factor, order_book_ids, exec_context):
    if isinstance(factor, CrossSectionalFactor):
        return _exec_cross_sectional(factor, order_book_ids, exec_context)

    for f in set(factor.dependencies):
        if isinstance(f, CrossSectionalFactor):
            exec_context.update(f, _exec_cross_sectional(f, order_book_ids, exec_context))
        elif isinstance(f, FixedFactor):
            exec_context.update(f, _exec_fixed(f, order_book_ids, exec_context))

    result = np.full((exec_context.ndays, len(order_book_ids)), np.nan, order='F')
    expr = factor.expr
    shift = factor.shift

    for i, order_book_id in enumerate(order_book_ids):
        mask = exec_context.get_mask_for(order_book_id)
        if mask.sum() <= shift:
            continue
        s = _exec_expr(expr, order_book_id, exec_context)
        indexes, = np.nonzero(mask)
        if isinstance(s, numbers.Real):
            result[indexes, i] = s
            continue

        result[indexes[-len(s):], i] = s

    return pd.DataFrame(index=exec_context.index, columns=order_book_ids, data=result)


def _exec_expr(expr, order_book_id, exec_context):
    if isinstance(expr, numbers.Real):
        return expr

    if isinstance(expr, (LeafFactor, CrossSectionalFactor, FixedFactor)):
        return exec_context.get_factor_value(expr, order_book_id)

    if isinstance(expr, tuple):
        func, args = expr
        return func(*[_exec_expr(arg, order_book_id, exec_context) for arg in args])

    return expr


def _exec_cross_sectional(factor, order_book_ids, exec_context):
    args = []
    for f in factor.sub_factors:
        args.append(_exec_factor(f, order_book_ids, exec_context))
    if exec_context.universe_mask is not None:
        return factor.execute(*[arg.where(exec_context.universe_mask) for arg in args])
    else:
        return factor.execute(*args)


def _exec_fixed(factor, order_book_ids, exec_context):
    if is_cross_sectional(factor.factor):
        df = _exec_cross_sectional(factor.factor, order_book_ids, exec_context)
        return df[factor.order_book_id]

    return _exec_expr(factor.factor.expr, factor.order_book_id, exec_context)

# -*- coding: utf-8 -*-
#
# Copyright 2018 Ricequant, Inc
from multiprocessing.pool import ThreadPool, AsyncResult

import pandas as pd
import numpy as np
import rqdatac

from rqfactor.leaf import Factor
from rqfactor.interface import AbstractUserDefinedLeafFactor
from rqfactor.fix import FixedFactor
from rqfactor.exception import RQFactorDataUnavailable

VOLUME_FACTOR = Factor('volume')

ADJUSTED_PRICING_FACTORS = {
    Factor('open'),
    Factor('close'),
    Factor('high'),
    Factor('low'),
    Factor('volume'),
}

TURNOVER_NUM_TRADES = {
    Factor('total_turnover'),
    Factor('num_trades'),
}

VOLUME_UNADJUSTED_FACTOR = Factor('volume_unadjusted')

UNADJUSTED_PRICING_FACTORS = {
    Factor('open_unadjusted'),
    Factor('close_unadjusted'),
    Factor('high_unadjusted'),
    Factor('low_unadjusted'),
    Factor('volume_unadjusted'),
}

PRICING_FACTORS = ADJUSTED_PRICING_FACTORS.union(UNADJUSTED_PRICING_FACTORS).union(TURNOVER_NUM_TRADES)


def _allocate_price_call(factors):
    adjusted = [f for f in factors if f in ADJUSTED_PRICING_FACTORS]
    unadjusted = [f for f in factors if f in UNADJUSTED_PRICING_FACTORS]
    either = [f for f in factors if f in TURNOVER_NUM_TRADES]

    if adjusted and not unadjusted:
        adjusted += either
        if VOLUME_FACTOR not in adjusted:
            adjusted.append(VOLUME_FACTOR)
        return VOLUME_FACTOR, adjusted, []

    if unadjusted and not adjusted:
        unadjusted += either
        if VOLUME_UNADJUSTED_FACTOR not in unadjusted:
            unadjusted.append(VOLUME_UNADJUSTED_FACTOR)
        return VOLUME_UNADJUSTED_FACTOR, [], unadjusted

    if VOLUME_FACTOR in adjusted:
        return VOLUME_FACTOR, adjusted, unadjusted + either

    if VOLUME_UNADJUSTED_FACTOR not in unadjusted:
        unadjusted.append(VOLUME_UNADJUSTED_FACTOR)
    return VOLUME_UNADJUSTED_FACTOR, adjusted, unadjusted + either


UNADJUSTED_FIELD_MAPPING = {
    'open_unadjusted': 'open',
    'close_unadjusted': 'close',
    'high_unadjusted': 'high',
    'low_unadjusted': 'low',
    'volume_unadjusted': 'volume',
    'total_turnover': 'total_turnover',
    'num_trades': 'num_trades',
}


def get_universe_mask(order_book_ids, start_date, end_date, universe):
    if universe is None or universe == 'all':
        return None

    data = rqdatac.index_components(universe, start_date=start_date, end_date=end_date)
    df = pd.DataFrame(data).T

    def apply_fun(s):
        sets = set(s)
        return pd.Series({i: i in sets for i in order_book_ids})

    mask = df.apply(apply_fun, axis=1)

    return mask


def _ensure_data_frame_get_factor(order_book_ids, factor, start_date, end_date, universe=None):
    df = rqdatac.get_factor(order_book_ids, factor, start_date, end_date, universe=universe, expect_df=True)
    if df is not None:
        return df[factor].unstack('order_book_id')


class ThreadingExecContext:
    pool = ThreadPool(4)

    def __init__(self, leaves, order_book_ids, start_date, end_date, universe=None):
        self.index = index = pd.to_datetime(rqdatac.get_trading_dates(start_date, end_date))

        non_pricing = [f for f in leaves if f not in PRICING_FACTORS]
        self._context = {
            f: self.pool.apply_async(
                _ensure_data_frame_get_factor,
                args=(order_book_ids, f.name, start_date, end_date, universe)
            )
            for f in non_pricing if not isinstance(f, AbstractUserDefinedLeafFactor)
        }
        self._context.update({
            f: self.pool.apply_async(f.execute, args=(order_book_ids, start_date, end_date))
            for f in leaves if isinstance(f, AbstractUserDefinedLeafFactor)
        })

        pricing = [f for f in leaves if f in PRICING_FACTORS]
        self._volume_factor, adjusted, unadjusted = _allocate_price_call(pricing)

        if adjusted:
            df = rqdatac.get_price(order_book_ids, start_date, end_date, frequency='1d', adjust_type='post_volume',
                                   fields=[f.name for f in adjusted], expect_df=True)
            for f in adjusted:
                self._context[f] = df[f.name].unstack('order_book_id', 0).reindex(index)

        if unadjusted:
            df = rqdatac.get_price(order_book_ids, start_date, end_date, frequency='1d', adjust_type='none',
                                   fields=[UNADJUSTED_FIELD_MAPPING[f.name] for f in unadjusted],
                                   expect_df=True)
            for f in unadjusted:
                self._context[f] = df[UNADJUSTED_FIELD_MAPPING[f.name]].unstack('order_book_id', 0).reindex(index)

        # a cache for get_mask
        self._mask_ob = self._mask = None

    @property
    def ndays(self):
        return len(self.index)

    def update(self, factor, value):
        self._context[factor] = value

    def get_mask_for(self, order_book_id):
        if self._mask_ob == order_book_id:
            return self._mask

        self._mask_ob = order_book_id
        df = self._context[self._volume_factor]
        try:
            self._mask = df[order_book_id].values > 0
        except KeyError:
            self._mask = np.repeat(False, self.ndays)

        return self._mask

    def get_factor_value(self, factor, order_book_id):
        df = self._context[factor]
        if isinstance(df, AsyncResult):
            df = df.get()
            self._context[factor] = df

        if df is None or isinstance(df, pd.DataFrame) and (df.empty or df.index[-1] != self.index[-1]):
            raise RQFactorDataUnavailable('factor {}@{} not available'.format(factor.name, self.index[-1].date()))

        mask = self.get_mask_for(order_book_id)

        if isinstance(factor, FixedFactor):  # here df is a simple numpy.ndarray
            v = df[mask]
        elif order_book_id in df:
            v = df[order_book_id].values[mask]
        else:
            v = np.full(mask.sum(), np.nan)

        return v[factor.shift:]

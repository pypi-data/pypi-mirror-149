import rqdatac
import logging
import pandas as pd
import numpy as np

from rqdatac.validators import ensure_date_int


class AnalysisDataSource:
    def __init__(self):
        pass

    @staticmethod
    def get_trading_dates(start, end):
        return pd.to_datetime(rqdatac.get_trading_dates(start, end))

    @staticmethod
    def is_st_stock(order_book_ids, date):
        date = ensure_date_int(date)
        data = rqdatac.client.get_client().execute('get_st_days', order_book_ids, date, date)
        return np.array([bool(data[i]) for i in order_book_ids])

    @staticmethod
    def get_close_price(order_book_ids, start_date, end_date):
        price = rqdatac.get_price(
            order_book_ids, start_date, end_date, fields='close', adjust_type='post', expect_df=True
        )
        if price is None:
            return pd.DataFrame()
        return price['close'].unstack('order_book_id')

    @staticmethod
    def is_new_stock(order_book_id, date):
        return (date - pd.Timestamp(rqdatac.instruments(order_book_id).listed_date)).days < 180

    @staticmethod
    def is_suspended(order_book_ids, date):
        d = pd.Timestamp(date)
        dateint = d.year * 10000 + d.month * 100 + d.day
        if isinstance(order_book_ids, str):
            order_book_ids = [order_book_ids]
        data = set(
            o for o, d in rqdatac.client.get_client().execute(
                'get_suspended_days', order_book_ids, dateint, dateint
            ).items() if d
        )
        return np.array([i in data for i in order_book_ids])

    def get_industry_tag(self, order_book_ids, date):
        date = pd.Timestamp(date)
        return rqdatac.get_instrument_industry(order_book_ids, source='citics_2019', date=date)['first_industry_name']

    @staticmethod
    def get_price_change_rate(stocks, start_date, end_date):
        if isinstance(stocks, str):
            stocks = [stocks]
        close = rqdatac.get_price(
            stocks, rqdatac.get_previous_trading_date(start_date), end_date, fields='close', adjust_type='post'
        )
        return close.pct_change(axis=0).iloc[1:]

    @staticmethod
    def get_combined_index_components(index_name, start_date, end_date):
        c = rqdatac.client.get_client()
        data = c.execute(
            '__internal__index_components',
            index_name=index_name,
            start_date=ensure_date_int(start_date),
            end_date=ensure_date_int(end_date),
        )
        components = set()
        if not data or pd.Timestamp(data[0]['trade_date']) > pd.Timestamp(start_date):
            components = set(rqdatac.index_components(index_name, start_date))

        for dic in data:
            components.update(dic['component_ids'])

        return sorted(components)

    @staticmethod
    def get_style_factor(stocks, date, factors):
        df = rqdatac.get_style_factor_exposure(stocks, date, date, factors)
        if df is None:
            logging.warning('got none style factors at date: {}, ignore.'.format(date))

        df.reset_index('date', drop=True, inplace=True)
        return df

    @staticmethod
    def get_market_cap(stocks, date):
        df = rqdatac.get_factor(stocks, 'market_cap', date, date, expect_df=True)
        return df['market_cap'].droplevel('date')

    def __getattr__(self, item):
        return getattr(rqdatac, item)

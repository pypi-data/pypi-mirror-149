# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import statsmodels.api as st


def neutralize(series, method, industry_tag=None, data=None):
    if industry_tag is not None:
        industry_tag = industry_tag.reindex(series.index)
    if data is not None:
        data = data.reindex(series.index)

    def _get_industry_df():
        industry = set(industry_tag.values)
        df = pd.DataFrame(index=series.index, columns=industry)
        df = df.apply(lambda s: (industry_tag == s.name).astype(np.int))
        return df

    if method == 'market':
        # data is market_cap data
        data = data.apply(np.log)
        ols = st.OLS(series, data, missing='drop')
        s = ols.fit().resid
    elif method == 'industry_market':
        data = data.apply(np.log)
        industry_df = _get_industry_df()
        exog = pd.concat([data, industry_df], axis=1)
        ols = st.OLS(series, exog, missing='drop')
        s = ols.fit().resid
    elif method == 'industry':
        ols = st.OLS(series, _get_industry_df(), hasconst=False, missing='drop')
        s = ols.fit().resid
    elif method == 'style':
        ols = st.OLS(series, data, missing='drop')
        s = ols.fit().resid
    elif method == 'industry_style':
        exog = pd.concat((data, _get_industry_df()), axis=1)
        ols = st.OLS(series, exog, hasconst=False, missing='drop')
        s = ols.fit().resid
    else:
        s = series
    return s.reindex(series.index)

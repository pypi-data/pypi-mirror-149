import numpy as np
from ..exception import InvalidArgument


def winsorize_std(series, n=3):
    mean, std = series.mean(), series.std()
    return series.clip(mean - std*n, mean + std*n)


def winsorize_percentile(series, left=0.025, right=0.975):
    lv, rv = np.percentile(series, [left*100, right*100])
    return series.clip(lv, rv)


def winsorize_mad(series, n=3):
    median = series.median()
    median_diff = (series - median).abs().median()
    return series.clip(median - median_diff * n, median + median_diff * n)


WINSORIZE_METHODS = {
    'std': winsorize_std,
    'percentile': winsorize_percentile,
    'mad': winsorize_mad,
    'none': lambda s: s,
}


def winsorize(series, how):
    if how not in WINSORIZE_METHODS:
        raise InvalidArgument('invalid winsorize method: {}. valid methods: {}'.format(
            how, list(WINSORIZE_METHODS.keys())))

    return WINSORIZE_METHODS[how](series)

# -*- coding: utf-8 -*-
from distutils.version import StrictVersion

import numpy as np
import pandas as pd
import rqdatac
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, Span, Range1d, LinearAxis
from bokeh.models import LinearColorMapper, ColorBar, BasicTicker, PrintfTickFormatter
from bokeh.palettes import Set1_5, Spectral5, Spectral6, Category20_20

import bokeh

if StrictVersion(bokeh.__version__) >= StrictVersion('0.12.10'):
    # bokeh 0.12.16 removed responsive
    def _figure(*args, **kwargs):
        return figure(*args, sizing_mode='scale_width', **kwargs)
else:
    def _figure(*args, **kwargs):
        return figure(*args, responsive=True, **kwargs)


# 箱形图
def factor_distribute(factors):
    q1 = factors.quantile(0.25, axis=1)
    q2 = factors.quantile(0.5, axis=1)
    q3 = factors.quantile(0.75, axis=1)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    outliers_x = []
    outliers_y = []

    outliers = factors[factors.gt(upper, axis='index') | factors.lt(lower, axis='index')]
    for x, series in outliers.iterrows():
        series = series.dropna()
        outliers_x.extend([x] * len(series))
        outliers_y.extend(series.values)

    bar_width = 0.7 * (q1.index[-1] - q1.index[0]).total_seconds() * 1000 / len(q1.index)
    line_width = 0.5 * bar_width

    source = ColumnDataSource({
        'index': q1.index.tolist(),
        'upper': upper.values,
        'lower': lower.values,
        'q1': q1.values,
        'q2': q2.values,
        'q3': q3.values,
    })

    fig = _figure(plot_width=600, plot_height=300, title=u'因子分布箱形图', x_axis_type='datetime')
    fig.xaxis.formatter = DatetimeTickFormatter(months='%Y-%m')
    fig.segment('index', 'upper', 'index', 'q3', line_color='black', source=source)
    fig.segment('index', 'lower', 'index', 'q1', line_color='black', source=source)
    fig.vbar(x='index', top='q3', bottom='q2', width=bar_width, fill_color='#E08E79', line_color='black', source=source)
    fig.vbar(x='index', top='q2', bottom='q1', width=bar_width, fill_color='#3B8686', line_color='black', source=source)
    fig.rect(x='index', y='lower', width=line_width, height=0.01, line_color='black', source=source)
    fig.rect(x='index', y='upper', width=line_width, height=0.01, line_color='black', source=source)
    fig.circle(outliers_x, outliers_y, size=6, color='#F38630', fill_alpha=0.6)

    fig.background_fill_color = "#EFE8E2"
    fig.ygrid.grid_line_color = "white"
    fig.grid.grid_line_width = 2
    fig.title.text_font_size = "12pt"
    return fig


TOOLS = "hover, save, pan, box_zoom, reset, wheel_zoom"


def factor_correlation(corr):
    fig = _figure(plot_width=600, plot_height=300, y_range=(0, 1.1), title=u'因子自相关性', tools=TOOLS)
    source = ColumnDataSource({
        'index': range(len(corr)),
        'correlation': np.array(corr),
    })
    fig.vbar(x='index', top='correlation', color='#3B8686', width=0.5, alpha=0.7, source=source)
    fig.select_one(HoverTool).tooltips = [(u"滞后期数", "@index"), (u'自相关系数', '@correlation')]

    fig.ygrid.grid_line_color = "white"
    fig.background_fill_color = "#EFE8E2"
    fig.title.text_font_size = "12pt"
    return fig


def factor_industry_distribute(distribute, title):
    data = distribute.mean(axis=1)
    source = ColumnDataSource({
        'index': range(1, len(data) + 1),
        'industry': data.index.tolist(),
        'value': data.values,
    })
    fig = _figure(plot_width=600, plot_height=300, title=title, x_range=(data.index.tolist()), tools=TOOLS)
    fig.vbar(x='index', top='value', color='firebrick', width=0.4, alpha=0.7, source=source)
    fig.xaxis.major_label_orientation = np.pi / 2
    fig.xaxis.major_label_overrides = dict(enumerate(data.index))
    fig.select_one(HoverTool).tooltips = [(u'申万一级', '@industry'), (u'因子值', '@value{0.0000}')]

    fig.ygrid.grid_line_color = "white"
    fig.background_fill_color = "#EFE8E2"
    fig.title.text_font_size = "12pt"
    return fig


MARKET_CAP_LABELS = {
    'smallest': u'超小型',
    'small': u'小型',
    'medium': u'中型',
    'large': u'大型',
    'largest': u'超大型'
}


def _ensure_column(df):
    # on bokeh 1.0.0, using such dataframe as ColumnDataSource will cause error
    if isinstance(df.columns, pd.CategoricalIndex):
        df = df.copy()
        df.columns = list(df.columns)
    df.index.name = 'index'
    return df


def factor_market_cap_distribute(distribute, title):
    fig = _figure(plot_width=600, plot_height=300, title=title, tools=TOOLS, x_axis_type='datetime')
    fig.xaxis.formatter = DatetimeTickFormatter(months='%Y-%m')

    source = ColumnDataSource(_ensure_column(distribute.T))
    for i, s in enumerate(distribute.index):
        fig.line(x='index', y=s, legend_label=MARKET_CAP_LABELS[s], line_width=2, color=Set1_5[i], source=source)

    hover_tool = fig.select_one(HoverTool)
    hover_tool.formatters = {'@index': 'datetime'}
    hover_tool.tooltips = [(u'日期', '@index{%Y-%m-%d}')] + [
        (MARKET_CAP_LABELS[n], '@' + n + '{0.0000}') for n in distribute.index]

    fig.xgrid.grid_line_color = "white"
    fig.ygrid.grid_line_color = "white"
    fig.background_fill_color = "#EFE8E2"
    fig.legend.location = "top_left"
    fig.legend.background_fill_alpha = 0.4
    fig.title.text_font_size = "12pt"

    return fig


# IC时间序列
def ic_series(series, title=u'IC 变化图', rolling=12):
    fig = _figure(plot_width=600, plot_height=300, title=title, tools=TOOLS, x_axis_type='datetime')
    fig.xaxis.formatter = DatetimeTickFormatter(months='%Y-%m')
    hover_tool = fig.select_one(HoverTool)
    hover_tool.formatters = {'@date': 'datetime'}
    hover_tool.tooltips = [
        (u'日期', '@date{%Y-%m-%d}'),
        (u'IC', '@value{0.0000}'),
    ]
    source = ColumnDataSource({
        'date': series.index,
        'value': series.values,
    })

    bar_width = 0.8 * (series.index[-1] - series.index[0]).total_seconds() * 1000 / len(series.index)
    fig.vbar(x='date', top='value', bottom=0, width=bar_width, legend_label='IC', source=source)
    if rolling:
        source.data['rolling'] = series.rolling(window=rolling).mean().values
        fig.line(x='date', y='rolling', legend_label=u'滚动IC(n={})'.format(rolling), color="firebrick", line_width=2, source=source)
        hover_tool.tooltips.append((u'滚动IC', '@rolling{0.0000}'))

    fig.xgrid.grid_line_color = "white"
    fig.ygrid.grid_line_color = "white"
    fig.background_fill_color = "#EFE8E2"
    fig.legend.location = "top_left"
    fig.legend.background_fill_alpha = 0.4
    fig.title.text_font_size = "12pt"
    return fig


HEATMAP_COLORS = [
    '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
    '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'
]


def ic_heatmap(series):
    s = series.groupby(by=lambda d: d.replace(day=1)).mean()
    source = ColumnDataSource({
        'year': [str(d.year) for d in s.index],
        'month': [str(d.month) for d in s.index],
        'ic': s.values,
    })

    mapper = LinearColorMapper(palette=HEATMAP_COLORS)
    fig = _figure(title=u'IC 热度图 ({}-{})'.format(s.index[0].year, s.index[-1].year),
                  x_range=sorted(set(str(d.month) for d in s.index), key=lambda m: int(m)),
                  y_range=sorted(set(str(d.year) for d in s.index)),
                  tools=TOOLS, toolbar_location='above', x_axis_location='below',
                  plot_width=600, plot_height=300)
    fig.rect(x='month', y='year', width=1, height=1, source=source,
             fill_color={'field': 'ic', 'transform': mapper}, line_color='white')

    color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(desired_num_ticks=len(HEATMAP_COLORS)),
                         formatter=PrintfTickFormatter(format='%.2f%%'),
                         label_standoff=6, major_label_text_font_size='5pt', border_line_color=None, location=(0, 0))
    fig.add_layout(color_bar, 'right')

    fig.select_one(HoverTool).tooltips = [('日期', u'@year年@month月'), ('IC值', '@ic{0.00}')]
    fig.xaxis.major_label_text_font_size = '10pt'
    fig.yaxis.major_label_text_font_size = '10pt'

    return fig


def ic_histogram(series):
    mu, sigma = series.mean(), series.std()
    hist, edges = np.histogram(series.dropna(), density=True, bins='auto')
    left, right = series.min() - 0.05, series.max() + 0.05

    x = np.linspace(left, right, 1000)
    pdf = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

    source_data = {
        "interval": [(round(edges[i], 3), round(edges[i + 1], 3)) for i in range(len(edges) - 1)],
        "point": np.linspace(pdf[0], pdf[-1], len(hist)),
        "hist": hist,
        "bottom": np.zeros(len(hist)),
        "left": edges[:-1],
        "right": edges[1:]
    }

    source_data_ = {
        "x": x,
        "pdf": pdf
    }

    source = ColumnDataSource(source_data)
    source_ = ColumnDataSource(source_data_)

    fig = _figure(plot_width=600, plot_height=300, title="IC频率分布图(mu={:.2f}, sigma={:.2f})".format(mu, sigma))
    fig.quad(top="hist", bottom="bottom", left="left", right="right", fill_color=Spectral6[-2], line_color="firebrick",
             alpha=0.7, source=source)
    fig.line(x="x", y="pdf", line_color="purple", line_width=2, alpha=0.7, source=source_)
    if mu == mu:
        # mu is not NaN
        mean_ic_data = Span(location=mu, dimension='height', line_color='white', line_dash='dashed', line_width=3)
        fig.add_layout(mean_ic_data)

    fig.add_tools(HoverTool(tooltips=[("IC", "(@interval)"), ("PDF", "@point{0.000}"), ("频率", "@hist")]))
    fig.background_fill_color = "#EFE8E2"
    fig.ygrid.grid_line_color = "white"
    fig.title.text_font_size = "12pt"
    return fig


def ic_industry_distribute(distribute, title):
    data = distribute
    source = ColumnDataSource({
        'index': range(1, len(data) + 1),
        'industry': data.index,
        'value': data.values,
    })

    fig = _figure(plot_width=600, plot_height=300, title=title, x_range=(data.index.tolist()), tools=TOOLS)

    fig.vbar(x='index', top='value', color='firebrick', width=0.4, alpha=0.7, source=source)
    fig.xaxis.major_label_orientation = np.pi / 2
    fig.xaxis.major_label_overrides = dict(enumerate(data.index))
    fig.select_one(HoverTool).tooltips = [(u'申万一级', '@industry'), (u'IC', '@value{0.0000}')]

    fig.xgrid.grid_line_color = "white"
    fig.ygrid.grid_line_color = "white"
    fig.background_fill_color = "#EFE8E2"
    fig.title.text_font_size = "12pt"
    return fig


def ic_decay(decay, title=u'IC衰减率'):
    fig = _figure(plot_width=600, plot_height=300, title=title, tools=TOOLS)

    source = ColumnDataSource({
        'period': decay.keys() + 1,
        'value': decay.values,
    })
    fig.vbar(x='period', top='value', bottom=0, width=0.5, color="purple", source=source)
    fig.select_one(HoverTool).tooltips = [(u'滞后期数', '@period'), (u'衰减率', '@value{0.0000}')]

    fig.ygrid.grid_line_color = "white"
    fig.background_fill_color = "#EFE8E2"
    fig.title.text_font_size = "12pt"
    return fig


def quantile_factor_returns(cumulative_returns, benchmark=None, title=u'分组累积收益分析'):
    fig = _figure(plot_width=600, plot_height=300, title=title, x_axis_type='datetime', tools=TOOLS)
    fig.xaxis.formatter = DatetimeTickFormatter(months='%Y-%m')

    cumulative_returns.index = cumulative_returns.index.astype(str)
    if benchmark is not None:
        _benchmark_name = getattr(rqdatac.instruments(benchmark.name), 'symbol', str(benchmark.name).replace(".", "_"))
        benchmark.name = "benchmark"
        cumulative_returns = cumulative_returns.append(benchmark)

    source = ColumnDataSource(_ensure_column(cumulative_returns.T))
    for i, quantile in enumerate(cumulative_returns.index):
        fig.line(x='index', y=quantile, legend_label=u'分组{}'.format(i + 1) if quantile.startswith('q') else f"基准（{_benchmark_name}）",
                 color=Category20_20[i], line_width=2,
                 source=source)

    hover_tool = fig.select_one(HoverTool)
    hover_tool.formatters = {'@index': 'datetime'}
    hover_tool.tooltips = [(u'日期', '@index{%Y-%m-%d}')] + [
        (u'分组{}'.format(i + 1) if q.startswith('q') else f"基准", '@' + q + '{0.0000}')
        for i, q in enumerate(cumulative_returns.index)
    ]

    fig.xgrid.grid_line_color = "white"
    fig.ygrid.grid_line_color = "white"
    fig.background_fill_color = "#EFE8E2"
    fig.legend.location = 'top_left'
    fig.legend.background_fill_alpha = 0.4
    fig.title.text_font_size = "12pt"
    return fig


def top_bottom_spread_returns(returns):
    fig = _figure(plot_width=600, plot_height=300, title=u'高低分组收益分析', x_axis_type='datetime', tools=TOOLS,
                  toolbar_location="above")
    fig.xaxis.formatter = DatetimeTickFormatter(months='%Y-%m')

    diff = returns.iloc[0] - returns.iloc[-1]
    cumulative = (diff + 1).cumprod() - 1

    left_ymin, left_ymax = min(0, diff.min() * 1.1), max(0, diff.max() * 1.1)
    right_ymin, right_ymax = min(0, cumulative.min() * 1.1), max(0, cumulative.max() * 1.1)

    source = ColumnDataSource({
        'date': diff.index,
        'diff': diff.values,
        'cumulative': cumulative.values,
    })

    width = 0.7 * (diff.index[-1] - diff.index[0]).total_seconds() * 1000 / len(diff.index)
    fig.vbar(x='date', top='diff', width=width, bottom=0, color=Spectral6[-1], alpha=0.7, legend_label=u'高低分组收益差值',
             source=source)

    fig.y_range = Range1d(left_ymin, left_ymax)
    fig.extra_y_ranges = {"Cumulative Returns": Range1d(right_ymin, right_ymax)}
    fig.add_layout(LinearAxis(y_range_name="Cumulative Returns"), "right")
    fig.line(x="date", y="cumulative", y_range_name="Cumulative Returns", legend_label=u'高低分组累积收益', color="navy",
             line_width=2, source=source)

    hover_tool = fig.select_one(HoverTool)
    hover_tool.formatters = {'@date': 'datetime'}
    hover_tool.tooltips = [(u'日期', '@date{%Y-%m-%d}'), (u'高低分组收益差值', '@diff{0.0000}'),
                           (u'高低分组累积收益', '@cumulative{0.0000}')]

    fig.background_fill_color = "#EFE8E2"
    fig.ygrid.grid_line_color = "white"
    fig.xgrid.grid_line_color = "white"
    fig.legend.location = "top_left"
    fig.legend.background_fill_alpha = 0.4
    fig.title.text_font_size = "12pt"
    return fig


def quantile_turnover(turnover, title=u'分组换手率'):
    fig = _figure(plot_width=600, plot_height=300, title=title, x_axis_type='datetime', tools=TOOLS)
    fig.xaxis.formatter = DatetimeTickFormatter(months='%Y-%m')

    turnover.index = turnover.index.astype(str)
    source = ColumnDataSource(_ensure_column(turnover.T))
    for i, q in enumerate(turnover.index):
        fig.line(x='index', y=q, legend_label=u'分组{}'.format(i + 1), color=Category20_20[i], line_width=2,
                 source=source)

    hover_tool = fig.select_one(HoverTool)
    hover_tool.formatters = {'@index': 'datetime'}
    hover_tool.tooltips = [(u'日期', '@index{%Y-%m-%d}')] + [
        (u'分组{}'.format(i + 1), '@' + q + '{0.0000}') for i, q in enumerate(turnover.index)
    ]

    fig.background_fill_color = "#EFE8E2"
    fig.ygrid.grid_line_color = "white"
    fig.xgrid.grid_line_color = "white"
    fig.legend.location = "top_left"
    fig.legend.background_fill_alpha = 0.4
    fig.title.text_font_size = "12pt"

    return fig

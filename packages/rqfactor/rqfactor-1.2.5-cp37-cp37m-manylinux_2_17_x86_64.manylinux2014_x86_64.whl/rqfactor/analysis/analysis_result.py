from scipy import stats
from bokeh import plotting, layouts, models
from bokeh.io import output_notebook, output_file
from rqfactor.analysis.plot import *

__all__ = ['ICAnalysisResult', 'QuantileReturnAnalysisResult', 'FactorReturnAnalysisResult']

USE_JUPYTER_NOTEBOOK = False
try:
    import IPython
    if type(IPython.get_ipython()).__module__.startswith('ipykernel.'):
        USE_JUPYTER_NOTEBOOK = True
except:
    pass


class ColorGenerator:
    """ 颜色生成器 """
    def __init__(self):
        self.idx = 0

    def nxt_color(self):
        c = Category20_20[self.idx]
        self.idx += 1
        return c


class BaseResult:
    fig_name = "AnalysisResult.html"    # 图像输出文件名称

    def _set_fig_name(self, name):
        """ 设置图像名称，初始化时进行设置，名称为管线步骤名称 """
        self.fig_name = '{}.html'.format(name)

    @staticmethod
    def new_figure(**kwargs):
        """ 生成统一figure """
        params = dict(
            plot_width=600, plot_height=300,
            x_axis_type='datetime', tools=TOOLS,
            sizing_mode='scale_width',
        )
        params.update(kwargs)

        fig = plotting.figure(**params)
        fig.xgrid.grid_line_color = "white"
        fig.ygrid.grid_line_color = "white"
        fig.background_fill_color = "#EFE8E2"
        fig.title.text_font_size = "12pt"
        if params['x_axis_type'] == 'datetime':
            fig.xaxis.formatter = DatetimeTickFormatter(months='%Y-%m')
        return fig

    def _figs(self, *args, **kwargs):
        """ 由子类继承，生成需要渲染展示的图像列表 """
        pass

    def show(self, *args, **kwargs):
        """ 图像展示 """
        figs = self._figs(*args, **kwargs)
        if figs is None:
            return
        if USE_JUPYTER_NOTEBOOK:
            output_notebook()
        else:
            output_file(self.fig_name)
        plotting.show(layouts.column(figs, sizing_mode='stretch_both'))


class ICAnalysisResult(BaseResult):
    """ IC检验结果 """
    def __init__(self, ic, ic_p_value, ic_decay, ic_industry_distribute, name):
        self.ic = ic
        self.ic_decay = ic_decay
        self.ic_industry_distribute = ic_industry_distribute
        self._ic_summary = None
        self._ic_p_value = ic_p_value
        self._set_fig_name(name)

    def rolling(self, window=12):
        """rolling ic"""
        return self.ic.rolling(window=window).mean()

    def summary(self):
        """ ic summary """
        if self._ic_summary is None:
            ic = self.ic.dropna()
            ic_p_value = self._ic_p_value
            t_stat, p_value = stats.ttest_1samp(ic, 0)
            result_dict = {
                'mean': ic.mean(),
                'std': ic.std(),
                'positive': np.sum(ic >= 0),
                'negative': np.sum(ic < 0),
                'significance': np.sum(ic_p_value < 0.01) / len(ic_p_value),
                'sig_positive': np.sum((ic > 0) & (ic_p_value < 0.01)) / len(ic),
                'sig_negative': np.sum((ic < 0) & (ic_p_value < 0.01)) / len(ic),
                't_stat': t_stat,
                'p_value': p_value,
                'skew': stats.skew(ic),
                'kurtosis': stats.kurtosis(ic),
                'ir': ic.mean() / ic.std(),
            }
            self._ic_summary = pd.DataFrame.from_dict(result_dict).T
        return self._ic_summary

    def _figs(self, rolling=None):
        """ 绘制结果 """
        figs = []
        for period in self.ic.columns:
            figs.append(ic_series(self.ic[period], title="IC 变化图 - {}".format(period), rolling=rolling))
            if self.ic_industry_distribute is not None:
                figs.append(ic_industry_distribute(self.ic_industry_distribute[period], title='IC行业分布 - {}'.format(period)))
            if self.ic_decay is not None:
                _decay = self.ic_decay[period].groupby(level='decay').mean()
                figs.append(ic_decay(_decay, title='IC衰减率 - {}'.format(period)))
        return figs


class QuantileReturnAnalysisResult(BaseResult):
    """ 分组收益率检验结果 """
    def __init__(
            self,
            quantile_turnover=None,
            quantile_returns=None,
            quantile_detail=None,
            benchmark_return=None,
            top_minus_bottom_returns=None,
            name=None,
    ):
        self.quantile_turnover = quantile_turnover
        self.quantile_returns = quantile_returns
        self.quantile_detail = quantile_detail
        self.benchmark_return = benchmark_return
        self.top_minus_bottom_returns = top_minus_bottom_returns
        self._set_fig_name(name)

    def _fig_top_minus_bottom_returns(self):
        fig = self.new_figure(title='分组多空收益率')
        cg = ColorGenerator()
        source = models.ColumnDataSource(self.top_minus_bottom_returns.reset_index())
        tooltips = [('日期', '@datetime{%Y-%m-%d}')]
        for period in self.top_minus_bottom_returns.columns:
            fig.line(x='datetime', y=period, color=cg.nxt_color(), source=source, legend_label=period, line_width=2)
            tooltips.append((period, '@' + period + '{0.0000}'))
        hover_tool = fig.select_one(HoverTool)
        hover_tool.formatters = {'@datetime': 'datetime'}
        hover_tool.tooltips = tooltips
        fig.legend.location = 'top_left'
        fig.legend.background_fill_alpha = 0.4
        return fig

    def _figs(self):
        """ 绘制结果 """
        figs = [
            self._fig_top_minus_bottom_returns()       # 分组多空收益率
        ]
        for period in self.quantile_returns.columns:
            to_series = self.quantile_turnover[period]
            figs.append(quantile_turnover(to_series.unstack('datetime'), title='分组换手率 - {}'.format(period)))
            qr = self.quantile_returns[period].unstack('datetime')
            figs.append(quantile_factor_returns(qr, benchmark=self.benchmark_return, title='分组累积收益分析 - {}'.format(period)))
        return figs


class FactorReturnAnalysisResult(BaseResult):
    """ 因子收益率检验结果 """
    def __init__(self, factor_returns=None, name=None):
        self.factor_returns = factor_returns
        self._mdd = None
        self._set_fig_name(name)

    def max_drawdown(self):
        """ 计算最大回撤 """
        if self._mdd is None:
            def _calc_mdd(x):
                ret_cum = np.exp(np.log1p(x).cumsum())
                max_ret = np.maximum.accumulate(ret_cum)
                return ((max_ret - ret_cum) / max_ret).max()
            self._mdd = self.factor_returns.apply(_calc_mdd)
        return self._mdd

    def std(self, ddof=1):
        """ 波动率 """
        return self.factor_returns.std(ddof=ddof)

    def _figs(self):
        """ 绘制因子检验收益率曲线 """
        fig = self.new_figure(title='因子收益率')
        cg = ColorGenerator()
        source = models.ColumnDataSource(self.factor_returns.reset_index())
        tooltips = [('日期', '@datetime{%Y-%m-%d}')]
        for period in self.factor_returns.columns:
            fig.line(x='datetime', y=period, legend_label=period, color=cg.nxt_color(), line_width=2, source=source)
            tooltips.append((period, '@' + period + '{0.0000}'))
        hover_tool = fig.select_one(HoverTool)
        hover_tool.formatters = {'@datetime': 'datetime'}
        hover_tool.tooltips = tooltips
        fig.legend.location = 'top_left'
        fig.legend.background_fill_alpha = 0.4
        return [fig]

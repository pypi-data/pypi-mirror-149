from datetime import datetime
from typing import Any, Dict, List, Optional, cast

import arrow
import click
import investor8_sdk
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from click.types import DateTime
from pandas import DataFrame
from plotly.subplots import make_subplots
from rich.console import Console

from i8_terminal.app.layout import get_plot_default_layout
from i8_terminal.app.plot_server import serve_plot
from i8_terminal.commands.financials import financials
from i8_terminal.common.cli import get_click_command_path, pass_command
from i8_terminal.common.utils import PlotType
from i8_terminal.types.metric_param_type import MetricParamType
from i8_terminal.types.period_type_param_type import PeriodTypeParamType
from i8_terminal.types.ticker_param_type import TickerParamType

from i8_terminal.common.metrics import find_similar_fin_metric, get_metrics_display_names  # isort:skip
from i8_terminal.types.chart_param_type import ChartParamType, get_chart_param_types  # isort:skip


def get_historical_financials_df(
    tickers: List[str], metrics: List[str], period_type: str, from_date: Optional[str], to_date: Optional[str]
) -> DataFrame:
    if not to_date:
        to_date = arrow.now().datetime.strftime("%Y-%m-%d")
    if not from_date:
        from_date = arrow.now().shift(years=-8 if period_type == "FY" else -4).datetime.strftime("%Y-%m-%d")
    hist_financials = investor8_sdk.MetricsApi().get_historical_metrics(
        tickers=",".join(tickers),
        metrics=",".join(metrics),
        period_type=period_type,
        from_date=from_date,
        to_date=to_date,
    )
    df = DataFrame.from_dict(
        {(i, j): hist_financials[i][j] for i in hist_financials.keys() for j in sorted(hist_financials[i].keys())}
    ).sort_index()
    df.index.name = f"Historical {' and '.join(get_metrics_display_names(metrics))}"
    return df


def create_fig(df: DataFrame, cmd_context: Dict[str, Any], matched_metrics: List[str], chart_type: str) -> go.Figure:
    vertical_spacing = 0.02
    layout = dict(
        title=cmd_context["plot_title"],
        autosize=True,
        hovermode="closest",
        legend=dict(font=dict(size=11), orientation="v"),
        margin=dict(b=20, l=50, r=65),
    )
    rows_num = len(matched_metrics)

    if rows_num == 2:
        row_width = [0.5, 0.5]
    else:
        row_width = [1]

    fig = make_subplots(
        rows=rows_num, cols=1, shared_xaxes=True, vertical_spacing=vertical_spacing, row_width=row_width
    )

    for m in matched_metrics:
        for idx, tk in enumerate(df[m].columns):
            if chart_type == "bar":
                fig.add_trace(
                    go.Bar(
                        x=df[m].index,
                        y=df[m][tk],
                        name=tk,
                        marker=dict(color=px.colors.qualitative.Plotly[idx]),
                        legendgroup=f"group{idx}",
                        showlegend=True if matched_metrics.index(m) == 0 else False,
                    ),
                    row=matched_metrics.index(m) + 1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=df[m].index,
                        y=df[m][tk],
                        name=tk,
                        marker=dict(color=px.colors.qualitative.Plotly[idx]),
                        legendgroup=f"group{idx}",
                        showlegend=True if matched_metrics.index(m) == 0 else False,
                    ),
                    row=matched_metrics.index(m) + 1,
                    col=1,
                )

    fig.update_traces(hovertemplate="%{y} %{x}")
    fig.update_xaxes(
        rangeslider_visible=False,
        spikemode="across",
        spikesnap="cursor",
    )

    fig.update_layout(
        **layout,
        **get_plot_default_layout(),
        legend_title_text=None,
        xaxis_title=None,
        yaxis_title=None,
    )

    # Add yaxis titles
    for idx, r in enumerate(np.cumsum(row_width)[::-1]):
        fig["layout"][f"yaxis{idx+1}"]["title"] = get_metrics_display_names(matched_metrics)[idx]

    fig.update_annotations(
        dict(
            font_size=10,
            font_color="#525252",
        )
    )
    fig.update_yaxes(
        title_font_size=10,
    )

    return fig


@financials.command()
@click.pass_context
@click.option("--tickers", "-k", type=TickerParamType(), required=True, help="Comma-separated list of tickers.")
@click.option(
    "--period_type",
    "-m",
    type=PeriodTypeParamType(),
    default="FY",
    help="Period by which you want to view the report. Possible values are `FY` for yearly, `Q` for quarterly, and `TTM` for TTM reports.",
)
@click.option("--metrics", "-m", type=MetricParamType(), default="basic_eps", help="Comma-separated list of metrics.")
@click.option("--from_date", "-f", type=DateTime(), help="Histotical financials from date.")
@click.option("--to_date", "-t", type=DateTime(), help="Histotical financials to date.")
@click.option(
    "--chart_type",
    "-c",
    type=ChartParamType([("bar", "Bar chart"), ("line", "Line chart")]),
    default="bar",
    help="Chart can be bar or line chart.",
)
@pass_command
def plot(
    ctx: click.Context,
    tickers: str,
    period_type: str,
    metrics: str,
    chart_type: str,
    from_date: Optional[datetime],
    to_date: Optional[datetime],
) -> None:
    """Compare and plot financials metrics of given companies. TICKERS is a comma seperated list of tickers.

    Examples:

    `i8 financials plot --period_type Q --metrics net_ppe --from_date 2020-05-01 --to_date 2022-05-01 --tickers AMD,INTC,QCOM --chart_type line`
    """
    metrics_list = metrics.replace(" ", "").split(",")
    matched_metrics = [find_similar_fin_metric(metric.replace("_", "")) for metric in metrics_list]
    if not matched_metrics:
        click.echo(
            f"`{metrics}` is not valid metrics name. See the list of valid financial metrics with the following command:\n`i8 metrics`"
        )
        return
    if len(matched_metrics) > 2:
        click.echo("You can enter up to 2 metrics.")
        return
    if not chart_type in [t[0] for t in get_chart_param_types()]:
        click.echo(f"`{chart_type}` is not valid chart type.")
        return
    command_path_parsed_options_dict = {"--metrics": ",".join(matched_metrics)}  # type: ignore
    if from_date:
        command_path_parsed_options_dict["--from_date"] = from_date.strftime("%Y-%m-%d")
    if to_date:
        command_path_parsed_options_dict["--to_date"] = to_date.strftime("%Y-%m-%d")
    command_path = get_click_command_path(ctx, command_path_parsed_options_dict)
    tickers_list = tickers.replace(" ", "").upper().split(",")
    if len(tickers_list) > 5:
        click.echo("You can enter up to 5 tickers.")
        return
    cmd_context = {
        "command_path": command_path,
        "tickers": tickers_list,
        "plot_type": PlotType.CHART.value,
    }

    console = Console()
    with console.status("Fetching data...", spinner="material") as status:
        df = get_historical_financials_df(
            tickers_list, matched_metrics, period_type, cast(str, from_date), cast(str, to_date)  # type: ignore
        )
        cmd_context["plot_title"] = df.index.name
        status.update("Generating plot...")
        fig = create_fig(df, cmd_context, matched_metrics, chart_type)  # type: ignore

    serve_plot(fig, cmd_context)

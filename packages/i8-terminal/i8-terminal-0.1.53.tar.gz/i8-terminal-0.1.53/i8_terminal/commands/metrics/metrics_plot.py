from datetime import datetime
from typing import Any, Dict, List, Optional, cast

import click
import investor8_sdk
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from click.types import DateTime
from pandas import DataFrame
from plotly.subplots import make_subplots
from rich.console import Console

from i8_terminal.app.layout import get_date_range, get_plot_default_layout
from i8_terminal.app.plot_server import serve_plot
from i8_terminal.commands.metrics import metrics
from i8_terminal.common.cli import get_click_command_path, pass_command
from i8_terminal.common.metrics import get_daily_metrics_display_names
from i8_terminal.common.utils import PlotType, get_period_code
from i8_terminal.types.daily_metric_param_type import DailyMetricParamType
from i8_terminal.types.price_period_param_type import PricePeriodParamType
from i8_terminal.types.ticker_param_type import TickerParamType


def get_historical_daily_metrics_df(
    tickers: List[str], period: str, from_date: Optional[str], to_date: Optional[str]
) -> Optional[DataFrame]:
    period_code = get_period_code(period)
    hist_daily_metrics = []
    if from_date:
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        for ticker in tickers:
            hist_daily_metrics.extend(
                investor8_sdk.MetricsApi().get_historical_daily_metrics(ticker, from_date=from_date, to_date=to_date)
            )
    else:
        for ticker in tickers:
            hist_daily_metrics.extend(
                investor8_sdk.MetricsApi().get_historical_daily_metrics(ticker, period=period_code)
            )
    if not hist_daily_metrics:
        return None
    df = DataFrame([d.to_dict() for d in hist_daily_metrics])
    df["date"] = pd.to_datetime(df["timestamp"], unit="s").dt.tz_localize("UTC")
    df = df.set_index("date")
    return df


def create_fig(
    df: DataFrame,
    period: str,
    cmd_context: Dict[str, Any],
    metrics: List[str],
    range_selector: bool = True,
) -> go.Figure:
    vertical_spacing = 0.02
    layout = dict(
        title=cmd_context["plot_title"],
        autosize=True,
        hovermode="closest",
        legend=dict(font=dict(size=11), orientation="v"),
        margin=dict(b=20, l=50, r=65),
    )
    rows_num = len(metrics)

    if rows_num == 2:
        row_width = [0.5, 0.5]
    else:
        row_width = [1]

    fig = make_subplots(
        rows=rows_num, cols=1, shared_xaxes=True, vertical_spacing=vertical_spacing, row_width=row_width
    )

    tickers = sorted(list(set(df["ticker"])))
    for m in metrics:
        for ticker, ticker_df in df.groupby("ticker"):
            fig.add_trace(
                go.Scatter(
                    x=ticker_df.index,
                    y=ticker_df[m],
                    name=ticker,
                    marker=dict(color=px.colors.qualitative.Plotly[tickers.index(ticker)]),
                    legendgroup=f"group{tickers.index(ticker)}",
                    showlegend=True if metrics.index(m) == 0 else False,
                ),
                row=metrics.index(m) + 1,
                col=1,
            )
    fig.update_traces(hovertemplate="%{y:.2f} %{x}")
    fig.update_xaxes(
        rangeslider_visible=False,
        spikemode="across",
        spikesnap="cursor",
    )

    if range_selector:
        fig.update_xaxes(rangeselector=get_date_range(get_period_code(period)))
    fig.update_layout(
        **layout,
        **get_plot_default_layout(),
        legend_title_text=None,
        xaxis_title=None,
        yaxis_title=None,
    )

    # Add yaxis titles
    for idx, r in enumerate(np.cumsum(row_width)[::-1]):
        fig["layout"][f"yaxis{idx+1}"]["title"] = get_daily_metrics_display_names(metrics)[idx]

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


@metrics.command()
@click.pass_context
@click.option("--tickers", "-k", type=TickerParamType(), required=True, help="Comma-separated list of tickers.")
@click.option(
    "--metrics",
    "-m",
    type=DailyMetricParamType(),
    default="pe_ratio_ttm",
    help="Comma-separated list of daily metrics.",
)
@click.option(
    "--period",
    "-p",
    type=PricePeriodParamType(),
    default="1Y",
    help="Historical price period.",
)
@click.option("--from_date", "-f", type=DateTime(), help="Histotical financials from date.")
@click.option("--to_date", "-t", type=DateTime(), help="Histotical financials to date.")
@pass_command
def plot(
    ctx: click.Context,
    tickers: str,
    metrics: str,
    period: str,
    from_date: Optional[datetime],
    to_date: Optional[datetime],
) -> None:
    """Compare and plot daily metrics of given companies. TICKERS is a comma seperated list of tickers.

    Examples:

    `i8 metrics plot --metrics pe_ratio_fy --period 5Y --tickers AMD,INTC,QCOM`
    """
    period = period.replace(" ", "").upper()
    metrics_list = metrics.replace(" ", "").split(",")
    if len(metrics_list) > 2:
        click.echo("You can enter up to 2 daily metrics.")
        return
    command_path_parsed_options_dict = {}
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
        df = get_historical_daily_metrics_df(tickers_list, period, cast(str, from_date), cast(str, to_date))
        cmd_context["plot_title"] = f"Historical daily {' and '.join(get_daily_metrics_display_names(metrics_list))}"
        status.update("Generating plot...")
        fig = create_fig(df, period, cmd_context, metrics_list, range_selector=False)

    serve_plot(fig, cmd_context)

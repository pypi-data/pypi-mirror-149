from typing import Optional, cast

import click
from click.types import DateTime
from pandas import DataFrame
from rich.console import Console

from i8_terminal.commands.price import price
from i8_terminal.common.cli import pass_command
from i8_terminal.common.formatting import get_formatter
from i8_terminal.common.layout import df2Table, format_df
from i8_terminal.common.price import get_historical_price_df
from i8_terminal.common.utils import get_period_code, validate_ticker
from i8_terminal.types.price_period_param_type import PricePeriodParamType
from i8_terminal.types.ticker_param_type import TickerParamType


def format_hist_price_df(df: DataFrame, target: str) -> DataFrame:
    formatters = {
        "open": get_formatter("price", target),
        "close": get_formatter("price", target),
        "low": get_formatter("price", target),
        "high": get_formatter("price", target),
        "volume": get_formatter("volume", target),
        "change_perc": get_formatter("perc", target),
    }
    col_names = {
        "open": "Open",
        "close": "Close",
        "low": "Low",
        "high": "High",
        "volume": "Volume",
        "change_perc": "Change (%)",
    }
    return format_df(df, col_names, formatters)


@price.command()
@click.option("--ticker", "-k", type=TickerParamType(), required=True, callback=validate_ticker, help="Company ticker.")
@click.option(
    "--period",
    "-p",
    type=PricePeriodParamType(),
    default="1M",
    help="Historical price period.",
)
@click.option("--from_date", "-f", type=DateTime(), help="Histotical price from date.")
@click.option("--to_date", "-t", type=DateTime(), help="Histotical price to date.")
@click.option("--export", "export_path", "-e", help="Filename to export the output to.")
@pass_command
def list(
    ticker: str, period: str, from_date: Optional[DateTime], to_date: Optional[DateTime], export_path: Optional[str]
) -> None:
    """Lists historical prices for the given TICKER."""
    period_code = get_period_code(period.replace(" ", "").upper())
    console = Console()
    with console.status("Fetching data...", spinner="material"):
        df = get_historical_price_df([ticker], period_code, cast(str, from_date), cast(str, to_date))

    if export_path:
        df_formatted = format_hist_price_df(df, "store")
        df_formatted.to_csv(export_path, index=False)
        # TODO: new function/module for storing the files and to check if path already exists
        console.print(f"Price list for ticker {ticker} is saved on: {export_path}")
    else:
        df_formatted = format_hist_price_df(df, "console")
        table = df2Table(df_formatted)
        console.print(table)

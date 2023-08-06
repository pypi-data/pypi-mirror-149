from typing import Any, Dict, List, Optional

import click
import investor8_sdk
import pandas as pd
from investor8_sdk.models.stock_info_master_dto import StockInfoMasterDto
from pandas import DataFrame
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from i8_terminal.commands.company import company
from i8_terminal.common.cli import pass_command
from i8_terminal.common.utils import export_data
from i8_terminal.config import APP_SETTINGS
from i8_terminal.types.ticker_param_type import TickerParamType

from i8_terminal.common.formatting import format_date, format_fyq, format_number  # isort:skip


def get_stock_infos_df(tickers: List[str], exportize: Optional[bool] = False) -> Optional[DataFrame]:
    stock_infos = []
    for ticker in tickers:
        try:
            resp = investor8_sdk.StockInfoApi().get_stock_info_master(ticker=ticker)
            if resp:
                stock_infos.append(resp)
        except Exception:
            continue
    if not stock_infos:
        return None
    return prepare_stock_infos_df(stock_infos, exportize)


def prepare_stock_infos_df(stock_infos: List[StockInfoMasterDto], exportize: Optional[bool]) -> DataFrame:
    available_stock_infos_dict = {
        "summary": {
            "name": {"display_name": "Name", "unit": "str"},
            "exchange": {"display_name": "Exchange", "unit": "str"},
            "sector": {"display_name": "Sector", "unit": "str"},
            "industry_group": {"display_name": "Industry", "unit": "str"},
            "market_cap": {"display_name": "Market Cap", "unit": "usd"},
            "pe_ratio_ttm": {"display_name": "P/E Ratio", "unit": "usdpershare"},
            "current_price": {"display_name": "Current Price", "unit": "usd"},
            "change_perc": {"display_name": "Change", "unit": "percentage"},
        },
        "financials": {
            "fyq": {"display_name": "FYQ", "unit": "fyq"},
            "operating_revenue": {"display_name": "Operating Revenue", "unit": "usd"},
            "total_revenue": {"display_name": "Total Revenue", "unit": "usd"},
            "total_grossprofit": {"display_name": "Total Gross Profit", "unit": "usd"},
            "other_income": {"display_name": "Other Income", "unit": "usd"},
            "net_income": {"display_name": "Net Income", "unit": "usd"},
            "basic_eps": {"display_name": "Basic EPS", "unit": "usdpershare"},
            "diluted_eps": {"display_name": "Diluted EPS", "unit": "usdpershare"},
            "filing_date": {"display_name": "Filing Date", "unit": "date"},
            "adjusted_basic_eps": {"display_name": "Adjusted Basic EPS", "unit": "usd"},
        },
        "price_returns": {
            "OneDay": {"display_name": "One Day", "unit": "percentage"},
            "OneWeek": {"display_name": "One Week", "unit": "percentage"},
            "OneMonth": {"display_name": "One Month", "unit": "percentage"},
            "ThreeMonth": {"display_name": "Three Month", "unit": "percentage"},
            "SixMonth": {"display_name": "Six Month", "unit": "percentage"},
            "YearToDate": {"display_name": "Year To Date", "unit": "percentage"},
            "OneYear": {"display_name": "One Year", "unit": "percentage"},
            "TwoYear": {"display_name": "Two Year", "unit": "percentage"},
            "FiveYear": {"display_name": "Five Year", "unit": "percentage"},
        },
    }
    stock_infos_dict: Dict[str, Dict[str, Any]] = {}
    for stock_info in stock_infos:
        ticker = stock_info.ticker
        stock_infos_dict[ticker] = {}
        for name, value in stock_info.summary.to_dict().items():
            if name in available_stock_infos_dict["summary"]:
                stock_infos_dict[ticker][
                    f"Summary-{available_stock_infos_dict['summary'][name]['display_name']}"
                ] = format_value(
                    value,
                    available_stock_infos_dict["summary"][name]["unit"],
                    exportize,
                    colorize=True if name == "change_perc" else False,
                )
        for name, value in stock_info.latest_financials.quarterly.to_dict().items():
            if name in available_stock_infos_dict["financials"]:
                stock_infos_dict[ticker][
                    f"Financials-{available_stock_infos_dict['financials'][name]['display_name']}"
                ] = format_value(value, available_stock_infos_dict["financials"][name]["unit"], exportize)
        for name, value in stock_info.price_returns.items():
            if name in available_stock_infos_dict["price_returns"]:
                stock_infos_dict[ticker][
                    f"Price Return-{available_stock_infos_dict['price_returns'][name]['display_name']}"
                ] = format_value(
                    value, available_stock_infos_dict["price_returns"][name]["unit"], exportize, colorize=True
                )
    df = DataFrame(stock_infos_dict.values(), index=stock_infos_dict.keys()).T
    df = df.where(pd.notnull(df), "-")
    df.index = df.index.set_names(["Name"])
    df = df.reset_index()
    df["Section"] = df["Name"].apply(lambda name: name.split("-")[0])
    df["Name"] = df["Name"].apply(lambda name: name.split("-")[1])

    return df


def format_value(value: Any, unit: str, exportize: Optional[bool], colorize: Optional[bool] = False) -> Any:
    if value is None:
        return "-"
    if unit == "str":
        return value
    elif unit == "date":
        return format_date(value)
    elif unit == "fyq":
        return format_fyq(value)
    else:
        return format_number(value, unit, humanize=True, exportize=exportize, colorize=colorize)  # type: ignore


def companies_df2tree(df: DataFrame, tickers: List[str]) -> Tree:
    col_width = 40
    plot_title = f"Comparison of {', '.join(tickers)}"
    plot_title = " and ".join(plot_title.rsplit(", ", 1))
    tree = Tree(Panel(plot_title, width=50))
    # Add header table to tree
    header_table = Table(width=50 + (col_width * (len(tickers) - 1)), show_lines=False, show_header=False, box=None)
    header_table.add_column(width=35, style="magenta")
    for p in tickers:
        header_table.add_column(width=col_width, justify="center", style="magenta")
    header_table.add_row("Ticker", *tickers)
    tree.add(header_table)

    for sec_name, sec_values in df.groupby("Section", sort=False):
        sec_branch = tree.add(f"[cyan]{sec_name}")
        for i, r in sec_values.iterrows():
            t = Table(width=46 + (col_width * (len(tickers) - 1)), show_lines=False, show_header=False, box=None)
            t.add_column(width=31)
            for tk in tickers:
                t.add_column(width=col_width, justify="center")
            t.add_row(r["Name"], *[f"{d}" for d in r[tickers].values])
            sec_branch.add(t)

    return tree


@company.command()
@click.option("--tickers", "-k", type=TickerParamType(), required=True, help="Comma-separated list of tickers.")
@click.option("--export", "export_path", "-e", help="Filename to export the output to.")
@pass_command
def compare(tickers: str, export_path: Optional[str]) -> None:
    console = Console()
    tickers_list = tickers.replace(" ", "").upper().split(",")
    with console.status("Fetching data...", spinner="material") as status:
        stock_infos_df = get_stock_infos_df(tickers_list, exportize=True if export_path else False)
        if stock_infos_df is None:
            status.stop()
            click.echo("No data found!")
            return
    if export_path:
        stock_infos_df.drop(columns=["Section"], inplace=True)  # type: ignore
        export_data(
            stock_infos_df,
            export_path,
            column_width=18,
            column_format=APP_SETTINGS["styles"]["xlsx"]["company"]["column"],
        )
    else:
        tree = companies_df2tree(stock_infos_df, tickers_list)
        console.print(tree)

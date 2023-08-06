import os
from typing import Dict, List, Optional, Tuple

import numpy as np
from investor8_sdk import MetricsApi
from pandas import DataFrame, read_csv

from i8_terminal.common.utils import is_cached_file_expired, similarity
from i8_terminal.config import APP_SETTINGS, SETTINGS_FOLDER


def get_indicators_list(indicator: Optional[str] = None) -> List[str]:
    indicators_dict = {
        "Momentum": ["MA5", "MA12", "MA26", "MA52", "EMA5", "EMA12", "EMA26", "EMA52"],
        "RSI": ["RSI_7D", "RSI_14D", "RSI_1M", "RSI_3M"],
        "Alpha": ["Alpha_1W", "Alpha_2W", "Alpha_1M", "Alpha_3M", "Alpha_6M", "Alpha_1Y", "Alpha_2Y", "Alpha_5Y"],
        "Beta": ["Beta_1W", "Beta_2W", "Beta_1M", "Beta_3M", "Beta_6M", "Beta_1Y", "Beta_2Y", "Beta_5Y"],
        "Volume": ["volume"],
    }
    if indicator:
        return indicators_dict.get(indicator, [""])
    else:
        return [item for sublist in indicators_dict.values() for item in sublist]


def find_similar_fin_metric(metric: str) -> Optional[str]:
    metrics_meta_data = get_all_metrics_df()[["metric_name", "name"]]
    best_match_similarity = 0.0
    best_match = ""
    for idx, m in metrics_meta_data.iterrows():
        sim = similarity(metric.upper(), m["metric_name"].upper())
        if sim > best_match_similarity:
            best_match_similarity = sim
            best_match = m["metric_name"]
    if best_match_similarity < APP_SETTINGS["metrics"]["similarity_threshold"]:
        return None
    return best_match.replace("_", "")


def find_similar_indicator(indicator: str) -> Optional[str]:
    default_indicators = {"RSI": "RSI_14D", "ALPHA": "Alpha_1Y", "BETA": "Beta_1Y", "VOLUME": "volume"}
    defualt_ind = default_indicators.get(indicator.upper())
    if defualt_ind:
        return defualt_ind
    indicators_list = get_indicators_list()
    best_match_similarity = 0.0
    best_match = ""
    for ind in indicators_list:
        sim = similarity(indicator.upper(), ind.upper())
        if sim > best_match_similarity:
            best_match_similarity = sim
            best_match = ind
    if best_match_similarity < APP_SETTINGS["metrics"]["similarity_threshold"]:
        return None

    return best_match


def get_all_metrics_df() -> DataFrame:
    metric_path = f"{SETTINGS_FOLDER}/metrics_metadata.csv"
    if os.path.exists(metric_path) and not is_cached_file_expired(metric_path):
        df = read_csv(metric_path)
    else:
        all_metrics = MetricsApi().get_list_financial_metrics_metadata()
        df = DataFrame([m.to_dict() for m in all_metrics])
        stat_code_mapping = {
            "income_statement": "inc",
            "cash_flow_statement": "cf",
            "balance_sheet_statement": "bs",
            "calculations": "calc",
        }
        df["tag_fullname"] = df.apply(lambda x: f"{x['tag']}_{stat_code_mapping[x['statement_code']]}", axis=1)
        df.to_csv(metric_path, index=False)

    return df


def get_metrics_display_names(metrics: List[str]) -> List[str]:
    all_metrics = get_all_metrics_df()[["metric_name", "name"]]
    all_metrics["metric_name"] = all_metrics["metric_name"].apply(lambda x: x.replace("_", ""))
    return list(set(all_metrics[all_metrics.metric_name.isin(metrics)]["name"]))


def get_all_daily_metrics() -> Dict[str, str]:
    return {
        "pe_ratio_fy": "P/E Ratio (FY)",
        "pe_ratio_ttm": "P/E Ratio (TTM)",
        "dividend_yield_fy": "Dividend Yield (FY)",
        "dividend_yield_ttm": "Dividend Yield (TTM)",
    }


def get_daily_metrics_display_names(metrics: List[str]) -> List[str]:
    all__daily_metrics = get_all_daily_metrics()
    return list(all__daily_metrics[metric] for metric in metrics)


def get_metric_info(name: str) -> Tuple[str, str, str]:
    all_metrics = get_all_metrics_df()
    metric = all_metrics.loc[all_metrics.metric_name == name].replace(np.nan, "", regex=True).to_dict("records")[0]
    return (
        metric["name"],
        metric["unit"],
        metric["short_description"]
        if "short_description" in metric.keys() and metric["short_description"]
        else "No Description",
    )

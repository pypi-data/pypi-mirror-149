from typing import List, Tuple

from i8_terminal.common.metrics import get_all_daily_metrics
from i8_terminal.types.auto_complete_choice import AutoCompleteChoice


def get_daily_metrics() -> List[Tuple[str, str]]:
    daily_metrics = get_all_daily_metrics()
    return [(name, display_name) for name, display_name in daily_metrics.items()]


class DailyMetricParamType(AutoCompleteChoice):
    name = "dailymetric"

    def get_suggestions(self, keyword: str, pre_populate: bool = True) -> List[Tuple[str, str]]:
        if not self.is_loaded:
            self.set_choices(get_daily_metrics())

        if pre_populate and keyword.strip() == "":
            return self._choices[: self.size]
        return self.search_keyword(keyword)

    def __repr__(self) -> str:
        return "DAILYMETRIC"

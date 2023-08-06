from tardis.clients.csv_client import ExchangeCSVClient
from tardis.database.client import ConstanceDBClient
from tardis.database.table import ConstanceDBTable
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import Optional, Tuple
import pandas as pd


class BaseTardisIngestor(ABC):
    def __init__(
        self,
        exchange: str,
        period_seconds: int,
        db_credentials: dict,
        tardis_api_key: str,
    ):
        self.tardis_client = ExchangeCSVClient(exchange, tardis_api_key)
        self.period = timedelta(seconds=period_seconds)
        self.db_client = ConstanceDBClient(**db_credentials)
        self.table = self._get_table(exchange, self.period)
        self.symbol = self._get_symbol()

    @abstractmethod
    def _get_table(self, exchange: str, period: timedelta) -> ConstanceDBTable:
        pass

    @abstractmethod
    def _get_symbol(self) -> str:
        pass

    @abstractmethod
    def _get_data(self, max_days: int) -> Optional[pd.DataFrame]:
        pass

    def _insert_data(self, data: pd.DataFrame):
        self.table.insert_data(data)

    def _get_sync_range(self, max_days: int) -> Tuple[datetime, datetime]:
        range_start, range_end = self.tardis_client.get_symbol_date_range(self.symbol)
        range_start = datetime(range_start.year, range_start.month, range_start.day)
        range_end = datetime(range_end.year, range_end.month, range_end.day)

        latest_time = self.table.get_latest_time()
        sync_start = latest_time + self.period if latest_time else range_start
        sync_end = min(sync_start + timedelta(days=max_days), range_end)
        return sync_start, sync_end

    def sync(self, max_days: int):
        new_data = self._get_data(max_days)
        if new_data is not None and len(new_data) > 0:
            self._insert_data(new_data)

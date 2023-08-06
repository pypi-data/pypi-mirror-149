from datetime import datetime
from typing import Optional
import pandas as pd
from sqlalchemy.engine import Engine


class ConstanceDBTable:
    TIME_COL = "timestamp"

    def __init__(self, engine: Engine, name: str):
        self._engine = engine
        self.name = name

    def get_latest_time(self) -> Optional[datetime]:
        result = pd.read_sql(
            f"SELECT {self.TIME_COL} FROM {self.name} ORDER BY {self.TIME_COL} DESC LIMIT 1",
            self._engine,
        )
        if len(result) > 0:
            return result.iloc[0, 0]

    def insert_data(self, data: pd.DataFrame):
        data = data.dropna()
        if data[self.TIME_COL].dtype != "datetime64[ns]":
            data[self.TIME_COL] = pd.to_datetime(data[self.TIME_COL], unit="us")
        data.to_sql(
            self.name,
            self._engine,
            if_exists="append",
            index=False,
            chunksize=1000,
            method="multi",
        )

import pandas as pd
from typing import Dict
from utils.random import random_string
from typing import List, Union


class Store:

    path: str

    def __init__(
        self, data: Dict[str, Union[List, pd.Series]], labels: pd.Series, path: str
    ):
        self.data = data
        self.labels = labels
        self.id = "store-" + random_string(5)
        self.path = path
        self.stats = dict()

    def get_data(self, id: str) -> pd.Series:
        return self.data[id].copy()

    def get_labels(self) -> pd.Series:
        return self.labels.copy()

    def set_data(self, id: str, data: Union[pd.Series, List]) -> None:
        self.data[id] = data

    def set_stats(self, id: str, stats: pd.Series) -> None:
        self.stats[id] = stats

    def get_all_stats(self) -> pd.DataFrame:
        return pd.concat(list(self.stats.values()), axis=1)

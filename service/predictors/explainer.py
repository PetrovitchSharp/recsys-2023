import os
from typing import List

import pandas as pd

from ..settings import ServiceConfig

data = {}


def load_explanation_data(cfg: ServiceConfig) -> None:
    """Get all data"""
    data["items_rating"] = pd.read_csv(os.path.join(cfg.explanation_data_path, "items_rating.csv"))
    data["all_users"] = pd.read_csv(os.path.join(cfg.explanation_data_path, "users.csv"))


def get_user_rating() -> pd.DataFrame:
    return data["items_rating"]


def get_all_users() -> List[int]:
    return data["all_users"]

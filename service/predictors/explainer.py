import os

import numpy as np
import pandas as pd

from ..settings import ServiceConfig

data = {}


def load_explanation_data(cfg: ServiceConfig) -> None:
    """Get data required to explain recos"""
    data["items_rating"] = pd.read_csv(os.path.join(cfg.explanation_data_path, "items_rating.csv"), index_col="item_id")
    data["all_users"] = pd.read_csv(os.path.join(cfg.explanation_data_path, "users.csv"))["user_id"].values


def get_items_rating() -> pd.DataFrame:
    """Get items rating dataframe"""
    return data["items_rating"]


def get_all_users() -> np.ndarray:
    """Get list of all existing users"""
    return data["all_users"]

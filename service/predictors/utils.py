import os
from typing import Any, List, Tuple

import pandas as pd
import yaml
from rectools import Columns
from rectools.dataset import Dataset

from ..settings import ServiceConfig


def get_data(dataset_name: str, global_cfg: ServiceConfig) -> Tuple[Dataset, List[int]]:
    """Get data for models trained without features"""
    df = pd.read_csv(os.path.join(global_cfg.dataset_path, dataset_name))
    dataset = Dataset.construct(df)
    users = df[Columns.User].unique()

    return dataset, users


def get_data_with_features(
    interactions_dataset_name: str,
    users_features_dataset_name: str,
    items_features_dataset_name: str,
    global_cfg: ServiceConfig,
) -> Tuple[Dataset, List[int]]:
    """Get data for models trained with features"""
    interactions = pd.read_csv(os.path.join(global_cfg.dataset_path, interactions_dataset_name))
    users_features = pd.read_csv(os.path.join(global_cfg.dataset_path, users_features_dataset_name))
    items_features = pd.read_csv(os.path.join(global_cfg.dataset_path, items_features_dataset_name))

    dataset = Dataset.construct(
        interactions_df=interactions,
        user_features_df=users_features,
        cat_user_features=["sex", "age", "income"],
        item_features_df=items_features,
        cat_item_features=[
            "genre",
            "content_type",
            "age_rating",
            "country",
            "release_year_bin",
        ],
    )

    users = interactions[Columns.User].unique()

    return dataset, users


def get_cold_user_predictions_from_offline(cold_dataset: str, global_cfg: ServiceConfig) -> pd.DataFrame:
    """Get offline recommendations for cold users"""
    df = pd.read_csv(os.path.join(global_cfg.dataset_path, cold_dataset))

    return df


def get_predictors_config(global_cfg: ServiceConfig) -> Any:
    """Get config"""
    with open(
        os.path.join(
            global_cfg.root_path,
            "service/predictors/predictors_config.yaml",
        ),
        encoding="ascii",
    ) as f:
        predictors_config = yaml.safe_load(f)
    return predictors_config

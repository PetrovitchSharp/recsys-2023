import os
import random
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import yaml
from rectools import Columns
from rectools.dataset import Dataset

from ..settings import get_config

app_config = get_config()
dataset_path = app_config.dataset_path


def get_data(dataset_name: str) -> Tuple[Dataset, List[int]]:
    """Get data for models trained without features"""
    df = pd.read_csv(os.path.join(dataset_path, dataset_name))
    dataset = Dataset.construct(df)
    users = df[Columns.User].unique()

    return dataset, users


def get_data_with_features(
    interactions_dataset_name: str,
    users_features_dataset_name: str,
    items_features_dataset_name: str,
) -> Tuple[Dataset, List[int]]:
    """Get data for models trained with features"""
    interactions = pd.read_csv(os.path.join(dataset_path, interactions_dataset_name))
    users_features = pd.read_csv(os.path.join(dataset_path, users_features_dataset_name))
    items_features = pd.read_csv(os.path.join(dataset_path, items_features_dataset_name))

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


def get_cold_user_predictions() -> List:
    """Get random ids to recommend"""
    reco = random.sample(range(1000), app_config.k_recs)
    return reco


def get_offline_recommendations(
    dataset_name: str,
) -> Tuple[pd.DataFrame, np.ndarray]:
    """Get offline recommendations of model"""
    df = pd.read_csv(os.path.join(dataset_path, dataset_name))

    users = df[Columns.User].unique()

    return df, users


def get_cold_user_predictions_from_offline(
    cold_dataset: str,
) -> pd.DataFrame:
    """Get offline recommendations for cold users"""
    df = pd.read_csv(os.path.join(dataset_path, cold_dataset))

    return df


def get_predictors_config() -> Dict:
    """Get config"""
    with open(
        os.path.join(
            app_config.root_path,
            "service/predictors/predictors_config.yaml",
        ),
        encoding="ascii",
    ) as f:
        config = yaml.safe_load(f)
    return config

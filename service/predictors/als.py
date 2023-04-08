import os
from typing import Any, List

import joblib
from rectools.models import ImplicitALSWrapperModel

from .base import BaseRecommender
from .utils import (
    get_cold_user_predictions_from_offline,
    get_data_with_features,
    get_predictors_config,
)

model_cfg = get_predictors_config()


class ALSRecommender(BaseRecommender):
    """Recommender based on Implicit ALS
    with nmslib ANN (online realization)"""

    def __init__(self) -> None:
        super().__init__()
        # Loading dataset with features and list of non-cold users
        self.dataset, self.users = get_data_with_features(
            model_cfg["als"]["interactions"],
            model_cfg["als"]["users_features"],
            model_cfg["als"]["items_features"],
        )
        # Loading recommendations for cold users
        self.cold_dataset = get_cold_user_predictions_from_offline(
            model_cfg["als"]["cold_dataset"]
        )

        self.model: ImplicitALSWrapperModel = self.load_model()

    def load_model(self) -> Any:
        # Loading base pretrained ALS models
        base_model = joblib.load(
            os.path.join(
                self.predictors_path, model_cfg["als"]["model_filename"]
            )
        )

        return base_model

    def recommend(self, user_id: int) -> List:
        if user_id in self.users:
            reco = self.model.recommend(
                users=[user_id],
                dataset=self.dataset,
                k=10,
                filter_viewed=True,
            ).item_id.to_list()
        else:
            reco = self.cold_dataset.item_id.to_list()

        return reco

    def __repr__(self) -> str:
        return f"""{type(self).__name__}(model={model_cfg["als"]["model_filename"]},
                    dataset={model_cfg["als"]["dataset"]})"""


def get_als_predictor() -> Any:
    return ALSRecommender()

import os
from typing import Any, List

import joblib
from rectools.models import ImplicitALSWrapperModel

from ..settings import get_config
from .base import BaseRecommender
from .utils import get_cold_user_predictions_from_offline, get_data_with_features, get_predictors_config

global_cfg = get_config()
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
        self.cold_dataset = get_cold_user_predictions_from_offline(model_cfg["als"]["cold_dataset"])

        self.user_ext_to_int_map = self.dataset.user_id_map.to_internal.to_dict()
        self.item_int_to_ext_map = self.dataset.item_id_map.to_external.to_dict()
        self.ui_csr = self.dataset.get_user_item_matrix()

        self.model: ImplicitALSWrapperModel = self.load_model()

    def load_model(self) -> Any:
        # Loading base pretrained ALS models
        base_model = joblib.load(os.path.join(global_cfg.predictors_path, model_cfg["als"]["model_filename"]))

        return base_model

    def recommend(self, user_id: int) -> List:
        if user_id in self.users:
            int_user_id = self.user_ext_to_int_map[user_id]
            rec = self.model.model.recommend(
                int_user_id,
                user_items=self.ui_csr,
                N=10,
                filter_already_liked_items=True,
            )
            reco = [self.item_int_to_ext_map[item_int_id] for (item_int_id, _) in rec]
        else:
            reco = self.cold_dataset.item_id.to_list()

        return reco

    def __repr__(self) -> str:
        return f"""{type(self).__name__}(model={model_cfg["als"]["model_filename"]},
                    dataset={model_cfg["als"]["dataset"]})"""


def get_als_predictor() -> Any:
    return ALSRecommender()

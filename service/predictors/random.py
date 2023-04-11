import random
from typing import Any, List

from .base import BaseRecommender
from .utils import get_predictors_config

model_cfg = get_predictors_config()


class RandomRecommender(BaseRecommender):
    def load_model(self) -> Any:
        random.seed(model_cfg["random"]["random_state"])

    def recommend(self, user_id: int) -> List:
        reco = random.sample(range(1000), self.k_recs)

        return reco

    def __repr__(self) -> str:
        return f"""{type(self).__name__}(model={model_cfg["random"]["model_filename"]},
                    dataset={model_cfg["random"]["dataset"]})"""


def get_random_predictor() -> Any:
    return RandomRecommender()

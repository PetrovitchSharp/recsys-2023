from ..api.exceptions import ModelNotFoundError
from ..settings import ServiceConfig
from .als import get_als_predictor
from .base import BaseRecommender
from .random import get_random_predictor

predictors = {}


def load_predictors(config: ServiceConfig) -> None:
    predictors["random"] = get_random_predictor(config)
    predictors["als"] = get_als_predictor(config)


def get_predictor(name: str) -> BaseRecommender:
    try:
        predictor = predictors[name]
    except KeyError as err:
        raise ModelNotFoundError(error_message=f"Model {name} not found") from err

    return predictor

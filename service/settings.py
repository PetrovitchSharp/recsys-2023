import os
from enum import Enum

from pydantic import BaseSettings


class AppMode(Enum):
    TEST = 0
    PROD = 1


class Config(BaseSettings):
    class Config:
        case_sensitive = False


class LogConfig(Config):
    level: str = "INFO"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        case_sensitive = False
        fields = {
            "level": {"env": ["log_level"]},
        }


class ServiceConfig(Config):
    service_name: str = "reco_service"
    k_recs: int = 10
    root_path = os.getcwd()
    predictors_path: str
    dataset_path: str

    log_config: LogConfig


def get_config(mode: AppMode) -> ServiceConfig:
    root_path = os.getcwd()

    if mode == AppMode.TEST:
        config = ServiceConfig(
            predictors_path=os.path.join(root_path, "tests/mock_data/predictors"),
            dataset_path=os.path.join(root_path, "tests/mock_data/dataset"),
            log_config=LogConfig(),
        )
    elif mode == AppMode.PROD:
        config = ServiceConfig(
            predictors_path=os.path.join(root_path, "service/data/predictors"),
            dataset_path=os.path.join(root_path, "service/data/dataset"),
            log_config=LogConfig(),
        )
    else:
        raise NotImplementedError()

    return config

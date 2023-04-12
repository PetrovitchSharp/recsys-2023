import os
from enum import Enum

from pydantic import BaseSettings


class ApplicationMode(Enum):
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
    root_path: str = os.getcwd()
    predictors_path: str = os.path.join(root_path, "service/data/predictors")
    dataset_path: str = os.path.join(root_path, "service/data/dataset")

    log_config: LogConfig


def get_config(app_mode: ApplicationMode) -> ServiceConfig:
    root_path: str = os.getcwd()

    if app_mode == ApplicationMode.TEST:
        cfg = ServiceConfig(
            predictors_path=os.path.join(root_path, "tests/mock_data/predictors"),
            dataset_path=os.path.join(root_path, "tests/mock_data/dataset"),
            log_config=LogConfig(),
        )
    elif app_mode == ApplicationMode.PROD:
        cfg = ServiceConfig(
            log_config=LogConfig(),
        )
    else:
        raise NotImplementedError()

    return cfg

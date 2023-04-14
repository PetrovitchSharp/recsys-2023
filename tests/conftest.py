# pylint: disable=redefined-outer-name
import os
from typing import Iterator

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import FastAPI
from starlette.testclient import TestClient

from service.api.app import create_app
from service.settings import ServiceConfig, get_config


@pytest.fixture
def set_env() -> Iterator[None]:
    monkeypatch = MonkeyPatch()
    root_path = os.getcwd()
    monkeypatch.setenv("PREDICTORS_PATH", os.path.join(root_path, "tests/mock_data/predictors"))
    monkeypatch.setenv("DATASET_PATH", os.path.join(root_path, "tests/mock_data/dataset"))

    yield

    monkeypatch.undo()


@pytest.fixture
def service_config(set_env: None) -> ServiceConfig:
    return get_config()


@pytest.fixture
def app(
    service_config: ServiceConfig,
) -> FastAPI:
    app = create_app(service_config)
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)

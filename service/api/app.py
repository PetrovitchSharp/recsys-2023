import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Dict

import uvloop
from fastapi import FastAPI

from ..log import app_logger, setup_logging
from ..predictors.constructor import load_predictors
from ..predictors.explainer import load_explanation_data
from ..settings import ServiceConfig
from .exception_handlers import add_exception_handlers
from .middlewares import add_middlewares
from .views import add_views

__all__ = ("create_app",)


def setup_asyncio(thread_name_prefix: str) -> None:
    uvloop.install()

    loop = asyncio.get_event_loop()

    executor = ThreadPoolExecutor(thread_name_prefix=thread_name_prefix)
    loop.set_default_executor(executor)

    def handler(_, context: Dict[str, Any]) -> None:
        message = "Caught asyncio exception: {message}".format_map(context)
        app_logger.warning(message)

    loop.set_exception_handler(handler)


def create_app(config: ServiceConfig) -> FastAPI:
    setup_logging(config)
    setup_asyncio(thread_name_prefix=config.service_name)

    app = FastAPI(debug=False, title="RecoService API", version="1.0.0")
    app.state.k_recs = config.k_recs
    app.state.root_path = config.root_path
    app.state.config = config

    load_predictors(config)
    load_explanation_data(config)
    add_views(app)
    add_middlewares(app)
    add_exception_handlers(app)

    return app

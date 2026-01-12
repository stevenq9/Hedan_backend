import os

from fastapi import FastAPI
from fastapi_injector import InjectorMiddleware, attach_injector
from injector import Injector
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.apps.game_api.modules import modules
from src.common.api.di import add_mediator, add_event_bus
from src.common.api.module_installer import install_modules
from src.common.infrastructure.logging.logging_middleware import log_request_response
from src.common.infrastructure.persistence.sqlalchemy.db import add_database


def create_fast_api_app() -> FastAPI:
    app = FastAPI(
        title="HEDAN Game API",
        docs_url=os.getenv("docs_url"),
        redoc_url=os.getenv("redoc_url")
    )
    injector = Injector()
    add_mediator(injector)
    add_event_bus(injector)
    add_database(injector)
    install_modules(injector, app, modules)
    app.add_middleware(InjectorMiddleware, injector=injector)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("GAME_URL")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_request_response)
    attach_injector(app, injector)
    return app

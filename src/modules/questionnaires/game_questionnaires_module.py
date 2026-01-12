from fastapi import FastAPI
from fastapi_injector import request_scope
from injector import Injector
from mediatr import Mediator

from src.common.api.router_installer import RouterInstaller
from src.common.mediator_setup import register_mediator_handlers
from src.common.module import Module
from src.modules.questionnaires.api.routers import game_routers
from src.modules.questionnaires.application.interactors.handlers import game_handlers
from src.modules.questionnaires.domain.test_session.test_session_repository_async import TestSessionRepositoryAsync
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.repositories.sql_alchemy_test_session_async import \
    SqlAlchemyTestSessionRepositoryAsync


class GameQuestionnairesModule(Module, RouterInstaller):
    @staticmethod
    def install(injector: Injector) -> None:
        GameQuestionnairesModule.__register_repositories(injector)
        register_mediator_handlers(injector.get(Mediator), game_handlers)

    @staticmethod
    def install_routers(fast_api_app: FastAPI):
        [fast_api_app.include_router(router) for router in game_routers]

    @staticmethod
    def __register_repositories(injector: Injector):
        injector.binder.bind(TestSessionRepositoryAsync, to=SqlAlchemyTestSessionRepositoryAsync, scope=request_scope)

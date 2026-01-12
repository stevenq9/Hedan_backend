from typing import cast

from fastapi import FastAPI
from fastapi_injector import request_scope
from injector import Injector
from mediatr import Mediator

from src.common.api.router_installer import RouterInstaller
from src.common.application.event_bus import EventBus
from src.common.event_bus_setup import register_event_bus_handlers
from src.common.infrastructure.bus.memory.in_memory_event_bus import InMemoryEventBus
from src.common.mediator_setup import register_mediator_handlers
from src.common.module import Module
from src.modules.questionnaires.api.routers import routers
from src.modules.questionnaires.application.integration_events_handlers.integration_events_handlers import \
    event_handlers
from src.modules.questionnaires.application.interactors.get_test_Session_by_id.get_test_Session_by_id_query_service import \
    TestSessionByIdQueryService
from src.modules.questionnaires.application.interactors.get_test_session_id.get_test_session_id_service import \
    TestSessionIdQueryService
from src.modules.questionnaires.application.interactors.get_test_session_list.get_test_session_list_query_service import \
    TestSessionListQueryService
from src.modules.questionnaires.application.interactors.handlers import handlers
from src.modules.questionnaires.domain.test_session.test_session_repository_async import TestSessionRepositoryAsync
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_get_test_session_by_id_query_service import \
    SqlAlchemyTestSessionByIdQueryService
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_get_test_session_list_query_service import \
    SqlAlchemyTestSessionListQueryService
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_test_session_query_service import \
    SqlAlchemyTestSessionQueryService
from src.modules.questionnaires.infrastructure.persistence.sqlalchemy.repositories.sql_alchemy_test_session_async import \
    SqlAlchemyTestSessionRepositoryAsync


class QuestionnairesModule(Module, RouterInstaller):
    @staticmethod
    def install(injector: Injector) -> None:
        QuestionnairesModule.__register_services_implementation(injector)
        register_mediator_handlers(injector.get(Mediator), handlers)
        register_event_bus_handlers(cast(InMemoryEventBus, injector.get(EventBus)), event_handlers)

    @staticmethod
    def install_routers(fast_api_app: FastAPI):
        [fast_api_app.include_router(router) for router in routers]

    @staticmethod
    def __register_services_implementation(injector: Injector):
        injector.binder.bind(TestSessionRepositoryAsync, to=SqlAlchemyTestSessionRepositoryAsync, scope=request_scope)
        injector.binder.bind(TestSessionIdQueryService, to=SqlAlchemyTestSessionQueryService, scope=request_scope)
        injector.binder.bind(TestSessionListQueryService, to=SqlAlchemyTestSessionListQueryService, scope=request_scope)
        injector.binder.bind(TestSessionByIdQueryService, to=SqlAlchemyTestSessionByIdQueryService, scope=request_scope)



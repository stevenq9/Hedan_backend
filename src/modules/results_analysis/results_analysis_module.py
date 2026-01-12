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
from src.modules.results_analysis.api.routers import routers
from src.modules.results_analysis.application.integration_events_handlers.integration_events_handlers import \
    web_app_event_handlers
from src.modules.results_analysis.application.interactors.get_test_response.get_tests_reports_query_service import \
    GetTestsReportsQueryService
from src.modules.results_analysis.application.interactors.handlers import handlers
from src.modules.results_analysis.domain.test_report.test_report_repository_async import TestReportRepositoryAsync
from src.modules.results_analysis.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_get_tests_resports_query_service import \
    SqlAlchemyGetTestsReportsQueryService
from src.modules.results_analysis.infrastructure.persistence.sqlalchemy.repositories.sql_alchemy_test_report_repository_async import \
    SqlAlchemyTestReportRepositoryAsync


class ResultsAnalysisModule(Module, RouterInstaller):
    @staticmethod
    def install(injector: Injector) -> None:
        ResultsAnalysisModule.__register_services_implementation(injector)
        register_mediator_handlers(injector.get(Mediator), handlers)
        register_event_bus_handlers(cast(InMemoryEventBus, injector.get(EventBus)), web_app_event_handlers)

    @staticmethod
    def install_routers(fast_api_app: FastAPI):
        [fast_api_app.include_router(router) for router in routers]

    @staticmethod
    def __register_services_implementation(injector: Injector):
        injector.binder.bind(GetTestsReportsQueryService, to=SqlAlchemyGetTestsReportsQueryService,
                             scope=request_scope)
        injector.binder.bind(TestReportRepositoryAsync, to=SqlAlchemyTestReportRepositoryAsync, scope=request_scope)

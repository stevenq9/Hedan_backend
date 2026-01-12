from typing import cast

from fastapi import FastAPI
from fastapi_injector import request_scope
from injector import Injector

from src.common.api.router_installer import RouterInstaller
from src.common.application.event_bus import EventBus
from src.common.event_bus_setup import register_event_bus_handlers
from src.common.infrastructure.bus.memory.in_memory_event_bus import InMemoryEventBus
from src.common.module import Module
from src.modules.results_analysis.api.routers import routers
from src.modules.results_analysis.application.integration_events_handlers.integration_events_handlers import \
    game_event_handlers, web_app_event_handlers
from src.modules.results_analysis.domain.test_report.test_report_repository_async import TestReportRepositoryAsync
from src.modules.results_analysis.infrastructure.persistence.sqlalchemy.repositories.sql_alchemy_test_report_repository_async import \
    SqlAlchemyTestReportRepositoryAsync


class GameResultsAnalysisModule(Module):
    @staticmethod
    def install(injector: Injector) -> None:
        GameResultsAnalysisModule.__register_repositories(injector)
        register_event_bus_handlers(cast(InMemoryEventBus, injector.get(EventBus)), game_event_handlers)

    @staticmethod
    def __register_repositories(injector: Injector):
        injector.binder.bind(TestReportRepositoryAsync, to=SqlAlchemyTestReportRepositoryAsync, scope=request_scope)

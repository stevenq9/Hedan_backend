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
from src.modules.patients.api.routers import routers
from src.modules.patients.application.integration_events_handlers.integration_events_handlers import event_handlers
from src.modules.patients.application.interactors.get_by_id_psychologist.get_by_id_psychologist_service import \
    GetByIdPsychologistService
from src.modules.patients.application.interactors.get_children.get_children_query_service import ChildrenQueryService
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_query_service import \
    PsychologistListQueryService
from src.modules.patients.application.interactors.handlers import handlers
from src.modules.patients.domain.child.child_repository_async import ChildRepositoryAsync
from src.modules.patients.domain.psychologist.psychologist_repository_async import PsychologistRepositoryAsync
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.child_model import ChildModel
from src.modules.patients.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_children_query_service import \
    SqlAlchemyChildrenQueryService
from src.modules.patients.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_get_by_id_psychologist_user_service import \
    SQLAlchemyGetByIdPsychologistUserService
from src.modules.patients.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_psychologist_list_query_service import \
    SqlAlchemyPsychologistListQueryService
from src.modules.patients.infrastructure.persistence.sqlalchemy.repositories.sql_alchemy_psychologist_repository_async import \
    SqlAlchemyPsychologistRepositoryAsync

ChildModel
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.psychologist_model import PsychologistModel

PsychologistModel
from src.modules.patients.infrastructure.persistence.sqlalchemy.repositories.sql_alchemy_child_repository_async import \
    SqlAlchemyChildRepositoryAsync


class PatientsModule(Module, RouterInstaller):
    @staticmethod
    def install(injector: Injector) -> None:
        PatientsModule.__register_services_implementation(injector)
        register_mediator_handlers(injector.get(Mediator), handlers)
        register_event_bus_handlers(cast(InMemoryEventBus, injector.get(EventBus)), event_handlers)

    @staticmethod
    def install_routers(fast_api_app: FastAPI):
        [fast_api_app.include_router(router) for router in routers]

    @staticmethod
    def __register_services_implementation(injector: Injector):
        injector.binder.bind(ChildrenQueryService, to=SqlAlchemyChildrenQueryService,
                             scope=request_scope)
        injector.binder.bind(ChildRepositoryAsync, to=SqlAlchemyChildRepositoryAsync, scope=request_scope)
        injector.binder.bind(PsychologistRepositoryAsync, to=SqlAlchemyPsychologistRepositoryAsync, scope=request_scope)
        injector.binder.bind(PsychologistListQueryService, to=SqlAlchemyPsychologistListQueryService,
                             scope=request_scope)
        injector.binder.bind(GetByIdPsychologistService, to=SQLAlchemyGetByIdPsychologistUserService,
                             scope=request_scope)

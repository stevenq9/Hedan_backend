from fastapi import FastAPI
from fastapi_injector import request_scope
from injector import Injector, singleton
from mediatr import Mediator

from src.common.api.router_installer import RouterInstaller
from src.common.mediator_setup import register_mediator_handlers
from src.common.module import Module
from src.modules.users_management.api.routers import routers
from src.modules.users_management.application.hashing.hashing_provider import HashingProvider
from src.modules.users_management.application.interactors.add_psychologist_user.create_psychologist_user_service import \
    CreatePsychologistUserService
from src.modules.users_management.application.interactors.handlers import handlers
from src.modules.users_management.application.interactors.login.credentials_service import CredentialsService
from src.modules.users_management.application.interactors.update_psychologist_user.update_psychologist_user_service import \
    UpdatePsychologistUserService
from src.modules.users_management.application.token.token_provider import TokenProvider
from src.modules.users_management.infrastructure.hashing.bcrypt_hashing_provider import BCryptHashingProvider
from src.modules.users_management.infrastructure.persistence.sqlalchemy.query_services.sql_alchemy_credentials_service import \
    SqlAlchemyCredentialsService
from src.modules.users_management.infrastructure.persistence.sqlalchemy.write_services.sql_alchemy_create_psychologist_user_service import \
    SqlAlchemyCreatePsychologistUserService
from src.modules.users_management.infrastructure.persistence.sqlalchemy.write_services.sql_alchemy_update_psychologist_user_service import \
    SqlAlchemyUpdatePsychologistUserService
from src.modules.users_management.infrastructure.token.jwt_token_provider import JwtTokenProvider


class UsersManagementModule(Module, RouterInstaller):
    @staticmethod
    def install(injector: Injector) -> None:
        UsersManagementModule.__register_providers(injector)
        UsersManagementModule.__register_write_services(injector)
        UsersManagementModule.__register_query_services(injector)
        register_mediator_handlers(injector.get(Mediator), handlers)

    @staticmethod
    def install_routers(fast_api_app: FastAPI):
        [fast_api_app.include_router(router) for router in routers]

    @staticmethod
    def __register_write_services(injector: Injector):
        injector.binder.bind(CreatePsychologistUserService, to=SqlAlchemyCreatePsychologistUserService,
                             scope=request_scope)
        injector.binder.bind(UpdatePsychologistUserService, to=SqlAlchemyUpdatePsychologistUserService,
                             scope=request_scope)

    @staticmethod
    def __register_providers(injector: Injector):
        injector.binder.bind(HashingProvider, to=BCryptHashingProvider, scope=singleton)
        injector.binder.bind(TokenProvider, to=JwtTokenProvider, scope=singleton)

    @staticmethod
    def __register_query_services(injector: Injector):
        injector.binder.bind(CredentialsService, to=SqlAlchemyCredentialsService, scope=request_scope)
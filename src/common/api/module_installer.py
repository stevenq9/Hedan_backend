from typing import Type, Union

from fastapi import FastAPI
from injector import Injector

from src.common.api.router_installer import RouterInstaller
from src.common.module import Module


def install_modules(
        injector: Injector,
        fast_api_app: FastAPI,
        modules: list[Union[Type[Module], Type[RouterInstaller]]]
) -> None:
    for module in modules:
        if issubclass(module, Module):
            module.install(injector)
        if issubclass(module, RouterInstaller):
            module.install_routers(fast_api_app)

from abc import ABC, abstractmethod

from fastapi import FastAPI
from injector import Injector


class Module(ABC):
    @staticmethod
    @abstractmethod
    def install(injector: Injector) -> None:
        ...

from fastapi import FastAPI
from abc import ABC, abstractmethod


class RouterInstaller(ABC):
    @staticmethod
    @abstractmethod
    def install_routers(fast_api_app: FastAPI):
        pass

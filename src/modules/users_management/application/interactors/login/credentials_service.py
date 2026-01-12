from abc import ABC

from src.common.application.query_service import QueryService


class CredentialsService(QueryService, ABC):
    ...

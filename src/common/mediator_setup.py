from typing import Union, Type

from mediatr import Mediator

from src.common.application.command_handler import CommandHandler
from src.common.application.query_handler import QueryHandler


def register_mediator_handlers(
        mediator: Mediator,
        handlers: list[Type[Union[CommandHandler, QueryHandler]]]
) -> None:
    [mediator.register_handler(handler) for handler in handlers]

from dataclasses import dataclass

from src.common.application.command import Command


@dataclass(frozen=True)
class SetTestTokenCommand(Command[None]):
    token: str
    test_session_id: int

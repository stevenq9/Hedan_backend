from dataclasses import dataclass

from src.common.application.command import Command


@dataclass(frozen=True)
class DeleteTestByIdCommand(Command[None]):
    psychologist_cedula: str
    test_session_id: int

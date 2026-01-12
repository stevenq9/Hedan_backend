from abc import ABC
from dataclasses import dataclass

from src.common.application.event import Event


@dataclass(frozen=True)
class IntegrationEvent(Event, ABC):
    ...

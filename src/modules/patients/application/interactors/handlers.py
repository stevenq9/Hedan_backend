from typing import Type, Union

from src.common.application.command_handler import CommandHandler
from src.common.application.query_handler import QueryHandler
from src.modules.patients.application.interactors.add_child.add_child_command_handler import AddChildCommandHandler
from src.modules.patients.application.interactors.get_by_id_psychologist.get_by_id_psychologist_query_handler import \
    GetByIdPsychologistQueryHandler
from src.modules.patients.application.interactors.get_children.get_children_query_hanlder import GetChildrenQueryHandler
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_list_query_handler import \
    GetPsychologistListQueryHandler

handlers: list[Type[Union[CommandHandler, QueryHandler]]] = [
    AddChildCommandHandler,
    GetPsychologistListQueryHandler,
    GetChildrenQueryHandler,
    GetByIdPsychologistQueryHandler
]

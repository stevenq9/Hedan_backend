from typing import Type, Union

from src.common.application.command_handler import CommandHandler
from src.common.application.query_handler import QueryHandler
from src.modules.results_analysis.application.interactors.get_test_response.get_tests_reports_query_hanlder import \
    GetTestsReportsQueryHandler

handlers: list[Type[Union[CommandHandler, QueryHandler]]] = [
    GetTestsReportsQueryHandler
]

from typing import Type, Union

from src.common.api.router_installer import RouterInstaller
from src.common.module import Module
from src.modules.questionnaires.game_questionnaires_module import GameQuestionnairesModule
from src.modules.results_analysis.game_results_analysis_module import GameResultsAnalysisModule

modules: list[Union[Type[Module], Type[RouterInstaller]]] = [
    GameQuestionnairesModule,
    GameResultsAnalysisModule
]

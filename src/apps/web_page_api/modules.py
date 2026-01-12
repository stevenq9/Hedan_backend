from typing import Type, Union

from src.common.api.router_installer import RouterInstaller
from src.common.module import Module
from src.modules.patients.patients_module import PatientsModule
from src.modules.questionnaires.questionnaires_module import QuestionnairesModule
from src.modules.results_analysis.results_analysis_module import ResultsAnalysisModule
from src.modules.users_management.users_management_module import UsersManagementModule

modules: list[Union[Type[Module], Type[RouterInstaller]]] = [
    PatientsModule,
    QuestionnairesModule,
    ResultsAnalysisModule,
    UsersManagementModule
]

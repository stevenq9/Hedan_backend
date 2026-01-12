from fastapi import APIRouter, Security
from fastapi_injector import Injected
from mediatr import Mediator

from src.common.api.authorization import psychologist_with_cedula
from src.common.domain.value_objects.cedula import Cedula
from src.common.infrastructure.token.access_security import access_security
from src.modules.results_analysis.application.interactors.get_test_response.get_tests_reports_query import \
    GetTestsReportsQuery

router = APIRouter(prefix="/results", tags=["results"],
                   dependencies=[Security(access_security)])


@router.get("/{psychologist_cedula}/test_reports", dependencies=[Security(psychologist_with_cedula)])
async def get_test_reports(psychologist_cedula: str, mediator: Mediator = Injected(Mediator)):
    query = GetTestsReportsQuery(
        psychologist_cedula=Cedula(psychologist_cedula)
    )
    return await mediator.send_async(query)

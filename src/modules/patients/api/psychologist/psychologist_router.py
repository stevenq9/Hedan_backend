from typing import List

from fastapi import APIRouter, Security
from fastapi_injector import Injected
from mediatr import Mediator

from src.common.api.authorization import admin_only, psychologist_with_cedula, psychologist_with_cedula_or_admin
from src.common.domain.value_objects.cedula import Cedula
from src.common.infrastructure.token.access_security import access_security
from src.modules.patients.api.psychologist.add_child_dto import AddChildDto
from src.modules.patients.application.interactors.add_child.add_child_command import AddChildCommand
from src.modules.patients.application.interactors.get_by_id_psychologist.get_by_id_psychologist_query import \
    GetByIdPsychologistQuery
from src.modules.patients.application.interactors.get_children.get_children_query import GetChildrenQuery
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_list_query import \
    GetPsychologistListQuery
from src.modules.patients.application.interactors.get_psychologists.get_psychologist_response import \
    GetPsychologistListResponse
from src.modules.patients.domain.child.scholar_grade import ScholarGrade

router = APIRouter(prefix="/psychologists", tags=["psychologists"],
                   dependencies=[Security(access_security)])


@router.get("/", response_model=List[GetPsychologistListResponse], dependencies=[Security(admin_only)])
async def get_psychologists(
        mediator: Mediator = Injected(Mediator),
) -> List[GetPsychologistListResponse]:
    query = GetPsychologistListQuery()
    return await mediator.send_async(query)


@router.post("/{psychologist_cedula}/children", dependencies=[Security(psychologist_with_cedula)])
async def add_child(psychologist_cedula: str, add_child_dto: AddChildDto, mediator: Mediator = Injected(Mediator)):
    command = AddChildCommand(
        name=add_child_dto.name,
        sex=add_child_dto.sex,
        birthdate=add_child_dto.birthdate,
        scholar_grade=ScholarGrade(add_child_dto.scholar_grade),
        test_sender=add_child_dto.test_sender,
        test_reason=add_child_dto.test_reason,
        psychologist_cedula=Cedula(psychologist_cedula)
    )
    return await mediator.send_async(command)


@router.get("/{psychologist_cedula}/children", dependencies=[Security(psychologist_with_cedula)])
async def get_children(psychologist_cedula: str, mediator: Mediator = Injected(Mediator)):
    query = GetChildrenQuery(
        cedula=Cedula(psychologist_cedula)
    )
    return await mediator.send_async(query)


@router.get("/{psychologist_cedula}", response_model=GetPsychologistListResponse,
            dependencies=[Security(psychologist_with_cedula_or_admin)])
async def get_psychologist_by_cedula(
        psychologist_cedula: str,
        mediator: Mediator = Injected(Mediator),
):
    query = GetByIdPsychologistQuery(cedula=psychologist_cedula)
    response = await mediator.send_async(query)
    return GetPsychologistListResponse(
        cedula=str(response.cedula),
        name=response.name,
        sex=response.sex,
        email=str(response.email)
    )

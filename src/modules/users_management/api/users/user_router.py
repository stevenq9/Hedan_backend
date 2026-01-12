from fastapi import APIRouter, Security
from fastapi_injector import Injected
from fastapi_jwt import JwtAuthorizationCredentials
from mediatr import Mediator
from starlette import status

from src.common.api.authorization import admin_only
from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.email import Email
from src.common.infrastructure.token.access_security import access_security
from src.modules.users_management.api.users.add_psychologist_user_dto import AddPsychologistUserDto
from src.modules.users_management.api.users.update_psychologist_user_dto import UpdatePsychologistUserDto
from src.modules.users_management.api.users.user_data_dto import UserDataDto
from src.modules.users_management.application.interactors.add_psychologist_user.add_psychologist_user_command import \
    AddPsychologistUserCommand
from src.modules.users_management.application.interactors.update_psychologist_user.update_psychologist_user_command import \
    UpdatePsychologistUserCommand

router = APIRouter(prefix="/users", tags=["users"],  dependencies=[Security(access_security)])


@router.post("/psychologists", status_code=status.HTTP_201_CREATED, dependencies=[Security(admin_only)])
async def add_psychologist_user(
        add_psychologist_user_dto: AddPsychologistUserDto,
        mediator: Mediator = Injected(Mediator),
):
    command = AddPsychologistUserCommand(
        cedula=Cedula(add_psychologist_user_dto.cedula),
        name=add_psychologist_user_dto.name,
        sex=add_psychologist_user_dto.sex,
        email=Email(add_psychologist_user_dto.email),
        password=add_psychologist_user_dto.password
    )
    await mediator.send_async(command)


@router.put("/psychologists/{cedula}", status_code=status.HTTP_200_OK, dependencies=[Security(admin_only)])
async def update_psychologist_user(
        cedula: str,
        update_psychologist_user_dto: UpdatePsychologistUserDto,
        mediator: Mediator = Injected(Mediator),
):
    command = UpdatePsychologistUserCommand(
        cedula=Cedula(cedula),
        name=update_psychologist_user_dto.name,
        sex=update_psychologist_user_dto.sex,
        email=Email(update_psychologist_user_dto.email),
        password=update_psychologist_user_dto.password,
        change_password=update_psychologist_user_dto.change_password
    )
    await mediator.send_async(command)


@router.get("/me", response_model=UserDataDto)
async def get_current_user_data(
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    cedula = None if not credentials.subject.keys().__contains__("cedula") else str(credentials["cedula"])
    return UserDataDto(
        cedula=cedula,
        role=str(credentials["role"]),
    )

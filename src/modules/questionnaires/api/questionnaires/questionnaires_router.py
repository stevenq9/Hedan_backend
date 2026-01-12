import os

from fastapi import HTTPException, Security

from fastapi import APIRouter
from fastapi_injector import Injected
from mediatr import Mediator

from src.common.api.authorization import psychologist_with_cedula, psychologist_only
from src.common.domain.value_objects.cedula import Cedula
from src.modules.questionnaires.api.questionnaires.test_session_dto import TestSessionDto
from src.modules.questionnaires.api.questionnaires_children.validate_token_dto import ValidateTokenDto
from src.modules.questionnaires.application.interactors.delete_test_by_id.delete_test_by_id_command import \
    DeleteTestByIdCommand
from src.modules.questionnaires.application.interactors.get_test_Session_by_id.get_test_Session_by_id_query import \
    GetTestSessionByIdQuery
from src.modules.questionnaires.application.interactors.get_test_session_id.get_test_session_id_query import \
    GetTestSessionIdQuery
from src.modules.questionnaires.application.interactors.get_test_session_list.get_test_session_list_query import \
    GetTestSessionListQuery
from src.modules.questionnaires.application.interactors.set_test_token.set_test_token_command import SetTestTokenCommand
from src.modules.questionnaires.application.interactors.validate_questionnaire_token.validate_questionnaire_token_query import \
    ValidateQuestionnaireTokenQuery
from src.modules.questionnaires.application.invitation_link.invitation_link_provider import InvitationLinkProvider

router = APIRouter(prefix="/questionnaires", tags=["Questionnaires"])


@router.get("/token/{child_id}/{psychologist_cedula}", dependencies=[Security(psychologist_with_cedula)])
async def get_token(child_id: int, psychologist_cedula: int, mediator: Mediator = Injected(Mediator)):
    try:
        # Get test session id for the child
        query = GetTestSessionIdQuery(
            child_id=child_id,
            pyschologist_cedula=str(psychologist_cedula)
        )
        test_session_id = await mediator.send_async(query)
        # Validate if the test session id exists
        if test_session_id is None:
            raise HTTPException(status_code=404, detail="Test session not found")
        else:
            # Generate invitation link
            token = InvitationLinkProvider.generate_token(test_session_id)
            # Save token into database
            stm = SetTestTokenCommand(
                token=token,
                test_session_id=test_session_id
            )
            await mediator.send_async(stm)
            # Return invitation link
            return f"{os.getenv("GAME_URL")}/?token={token}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{psychologist_cedula}/test_sessions", dependencies=[Security(psychologist_with_cedula)])
async def get_test_sessions(psychologist_cedula: int, mediator: Mediator = Injected(Mediator)):
    try:
        query = GetTestSessionListQuery(
            cedula=Cedula(str(psychologist_cedula))
        )
        return await mediator.send_async(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resultado/{test_id}")
async def get_test_result(test_id: int, mediator: Mediator = Injected(Mediator)):
    try:
        query = GetTestSessionByIdQuery(
            test_id=test_id
        )
        return await mediator.send_async(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{psychologist_cedula}/{test_session_id}", dependencies=[Security(psychologist_with_cedula)])
async def delete_test_by_id(psychologist_cedula: str, test_session_id: int, mediator: Mediator = Injected(Mediator)):
    try:
        query = DeleteTestByIdCommand(
            psychologist_cedula=psychologist_cedula,
            test_session_id=test_session_id
        )
        await mediator.send_async(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

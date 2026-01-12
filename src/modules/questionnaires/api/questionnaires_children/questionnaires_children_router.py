from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi_injector import Injected
from mediatr import Mediator

from src.modules.questionnaires.api.questionnaires_children.set_questionnaire_answers_dto import \
    SetQuestionnaireAnswersDto
from src.modules.questionnaires.api.questionnaires_children.validate_token_dto import ValidateTokenDto
from src.modules.questionnaires.application.interactors.set_test_answers.set_test_answers_command import \
    SetTestAnswersCommand
from src.modules.questionnaires.application.interactors.validate_questionnaire_token.validate_questionnaire_token_query import \
    ValidateQuestionnaireTokenQuery
from src.modules.questionnaires.domain.test_session.answer import Answer
from src.modules.questionnaires.domain.test_session.answer_set_already_set_error import AnswerSetAlreadySetError
from src.modules.questionnaires.domain.test_session.answers_set import AnswerSet
from src.modules.questionnaires.domain.test_session.question_id import QuestionId

router = APIRouter(prefix="/questionnaires", tags=["Questionnaires"])


@router.post("/validate-token", response_model=None)
async def validate_token(validate_token_dto: ValidateTokenDto, mediator: Mediator = Injected(Mediator)):
    query = ValidateQuestionnaireTokenQuery(
        token=validate_token_dto.token
    )
    if not await mediator.send_async(query):
        raise HTTPException(status_code=401, detail=None)


@router.patch("/answers")
async def set_questionnaire_answers(questionnaire_response: SetQuestionnaireAnswersDto,
                                    mediator: Mediator = Injected(Mediator)):
    command = SetTestAnswersCommand(
        token=questionnaire_response.token,
        answers=AnswerSet(answer_list=[Answer(
            question_id=QuestionId(answer_dto.question_id),
            value=answer_dto.answer,
            time_taken=timedelta(milliseconds=answer_dto.time_taken)
        ) for answer_dto in questionnaire_response.answers])
    )
    try:
        await mediator.send_async(command)
    except ValueError:
        raise HTTPException(status_code=404, detail="Test session not found")
    except AnswerSetAlreadySetError:
        raise HTTPException(status_code=409, detail="Test session already answered")

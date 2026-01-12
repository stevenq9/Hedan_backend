from src.common.application.query_handler import QueryHandler
from src.modules.questionnaires.application.interactors.validate_questionnaire_token.validate_questionnaire_token_query import \
    ValidateQuestionnaireTokenQuery
from src.modules.questionnaires.application.invitation_link.invitation_link_provider import InvitationLinkProvider


class ValidateQuestionnaireTokenQueryHandler(QueryHandler[ValidateQuestionnaireTokenQuery, bool]):
    async def handle(self, query: ValidateQuestionnaireTokenQuery) -> bool:
        return InvitationLinkProvider.validate_token(query.token)

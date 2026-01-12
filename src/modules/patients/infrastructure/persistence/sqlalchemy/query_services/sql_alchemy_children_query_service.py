from injector import Inject
from sqlalchemy import select, Sequence, Row
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.patients.application.interactors.get_children.get_children_query import GetChildrenQuery
from src.modules.patients.application.interactors.get_children.get_children_query_service import ChildrenQueryService
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.child_model import ChildModel
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.psychologist_model import PsychologistModel


class SqlAlchemyChildrenQueryService(ChildrenQueryService):
    def __init__(self, async_session_factory: Inject[async_sessionmaker[AsyncSession]]):
        self.__async_session_factory = async_session_factory

    async def execute_async(self, query: GetChildrenQuery) -> list[ChildModel]:
        async with self.__async_session_factory() as session:
            query = select(ChildModel).where(ChildModel.psychologist_cedula == str(query.cedula))
            result = (await session.execute(query)).scalars().all()
            children: list[ChildModel] = []
            for child in result:
                children.append(ChildModel(
                    id=child.id,
                    name=child.name,
                    sex=child.sex,
                    birthdate=child.birthdate,
                    scholar_grade=child.scholar_grade,
                    psychologist_cedula=child.psychologist_cedula)
                )
            return children

import os

from injector import Injector, singleton
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


def create_async_session() -> async_sessionmaker[AsyncSession]:
    url: str = os.getenv("DATABASE_URL")
    engine = create_async_engine(url)
    session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session


def add_database(injector: Injector):
    injector.binder.bind(async_sessionmaker[AsyncSession], to=create_async_session, scope=singleton)

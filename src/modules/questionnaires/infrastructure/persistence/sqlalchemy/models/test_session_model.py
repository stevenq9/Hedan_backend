from datetime import datetime

from sqlalchemy import DateTime, func, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.common.infrastructure.persistence.sqlalchemy.base import Base


class TestSessionModel(Base):
    __tablename__ = "test_sessions"
    __table_args__ = {"schema": "questionnaires"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    child_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    psychologist_cedula: Mapped[str]
    child_age: Mapped[int]
    scholar_grade: Mapped[int]
    child_sex: Mapped[str] = mapped_column(String(1))
    test_sender: Mapped[str]
    test_reason: Mapped[str]
    test_token: Mapped[str] = mapped_column(nullable=True)
    date_time_of_answer: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    answers: Mapped[list[dict]] = mapped_column(JSONB, default=None, nullable=True)
    test_results: Mapped[dict] = mapped_column(JSONB, default=None, nullable=True)
    calculate_test_results_time_taken: Mapped[int] = mapped_column(nullable=False)

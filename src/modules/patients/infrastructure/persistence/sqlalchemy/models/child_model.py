from datetime import datetime, date
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.infrastructure.persistence.sqlalchemy.base import Base

if TYPE_CHECKING:
    from src.modules.patients.infrastructure.persistence.sqlalchemy.models.psychologist_model import PsychologistModel


class ChildModel(Base):
    __tablename__ = "children"
    __table_args__ = {"schema": "patients"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    sex: Mapped[str] = mapped_column(String(1))
    birthdate: Mapped[date] = mapped_column(Date)
    scholar_grade: Mapped[int] = mapped_column(Integer)
    psychologist_cedula: Mapped[str] = mapped_column(ForeignKey("patients.psychologists.cedula"))
    psychologist: Mapped["PsychologistModel"] = relationship("PsychologistModel", back_populates="children")

    #join with table test_report to get chils's name
    #+test_reports = relationship("GetTestReportModel", back_populates="child")

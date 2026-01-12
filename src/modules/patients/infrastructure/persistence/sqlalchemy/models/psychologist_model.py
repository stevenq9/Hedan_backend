from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.infrastructure.persistence.sqlalchemy.base import Base

if TYPE_CHECKING:
    from src.modules.patients.infrastructure.persistence.sqlalchemy.models.child_model import ChildModel


class PsychologistModel(Base):
    __tablename__ = "psychologists"
    __table_args__ = {"schema": "patients"}

    cedula: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    sex: Mapped[str] = mapped_column(String(1))
    email: Mapped[str] = mapped_column(String(64))
    children: Mapped[List["ChildModel"]] = relationship("ChildModel", back_populates="psychologist")

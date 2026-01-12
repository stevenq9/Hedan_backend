from sqlalchemy.orm import Mapped, mapped_column

from src.common.infrastructure.persistence.sqlalchemy.base import Base

#class PsychologistModel(Base):
#    __tablename__ = "psychologists"
 #   __table_args__ = {"schema": "patients"}
#
 #   cedula: Mapped[str] = mapped_column(primary_key=True)
  #  name: Mapped[str]
   # sex: Mapped[str]
    #email: Mapped[str]

class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "users_management"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    psychologist_cedula: Mapped[str] = mapped_column(unique=True, index=True)

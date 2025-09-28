from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

from datetime import date
from typing import TYPE_CHECKING

import uuid

if TYPE_CHECKING:
    from src.modules.shared.models.user.user import User


class Customer(Base, AuditMixin):
    __tablename__ = "customer"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), unique=True)

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    birth_date: Mapped[date] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="customer", lazy="joined")

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

from typing import TYPE_CHECKING

import uuid

if TYPE_CHECKING:
    from src.modules.shared.models.user.user import User
    from src.modules.company.models.state import State
    from src.modules.company.models.company import Company


class Organization(Base, AuditMixin):
    __tablename__ = "organization"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), unique=True)

    name: Mapped[str] = mapped_column()
    register_code: Mapped[str] = mapped_column()
    state_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("state.id"))

    user: Mapped["User"] = relationship(back_populates="organization", lazy="joined")
    state: Mapped["State"] = relationship(back_populates="organizations", lazy="joined")
    companies: Mapped[list["Company"]] = relationship(
        back_populates="organization", lazy="selectin"
    )

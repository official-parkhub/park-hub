from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

from typing import TYPE_CHECKING

import uuid

from src.modules.company.models.organization import Organization

if TYPE_CHECKING:
    from src.modules.driver.models.customer import Customer


class User(Base, AuditMixin):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column()

    customer: Mapped["Customer"] = relationship(back_populates="user", lazy="joined")
    organization: Mapped["Organization"] = relationship(
        back_populates="user", lazy="joined", uselist=False
    )

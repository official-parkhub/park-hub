from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

from typing import TYPE_CHECKING


import uuid


if TYPE_CHECKING:
    from src.modules.company.models.company import Company


class CompanyImage(Base, AuditMixin):
    __tablename__ = "company_image"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    key: Mapped[str] = mapped_column(nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("company.id"), nullable=False
    )
    is_primary: Mapped[bool] = mapped_column(default=False, nullable=False)

    company: Mapped["Company"] = relationship(back_populates="images", lazy="joined")

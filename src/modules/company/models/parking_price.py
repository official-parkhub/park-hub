from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

from typing import TYPE_CHECKING

import uuid


if TYPE_CHECKING:
    from src.modules.company.models.company import Company


class ParkingPrice(Base, AuditMixin):
    __tablename__ = "parking_price"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("company.id"), nullable=False
    )

    week_day: Mapped[int] = mapped_column(nullable=False)
    start_hour: Mapped[int] = mapped_column(nullable=False)
    end_hour: Mapped[int] = mapped_column(nullable=False)
    price_cents: Mapped[int] = mapped_column(nullable=False)

    is_discount: Mapped[bool] = mapped_column(default=False, nullable=False)

    company: Mapped["Company"] = relationship(
        back_populates="parking_prices", lazy="joined"
    )

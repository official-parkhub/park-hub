from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

import uuid

from datetime import datetime


class VehicleEntrance(Base, AuditMixin):
    __tablename__ = "vehicle_entrance"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vehicle.id"), nullable=False
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("company.id"), nullable=False
    )

    entrance_date: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)

    hourly_rate: Mapped[int | None] = mapped_column(nullable=True)
    total_price: Mapped[int | None] = mapped_column(nullable=True)

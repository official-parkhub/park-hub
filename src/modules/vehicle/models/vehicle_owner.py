from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

import uuid


class VehicleOwner(Base, AuditMixin):
    __tablename__ = "vehicle_owner"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    name: Mapped[str] = mapped_column(nullable=False)
    vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vehicle.id"), nullable=False
    )
    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("customer.id"), nullable=False
    )

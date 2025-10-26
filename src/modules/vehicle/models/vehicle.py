from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

from src.core.database.audit import AuditMixin
from src.core.database.base import Base

import uuid

from src.modules.shared.enums.country import Country


class Vehicle(Base, AuditMixin):
    __tablename__ = "vehicle"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    plate: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    model: Mapped[str | None] = mapped_column(nullable=True)
    year: Mapped[int | None] = mapped_column(nullable=True)
    color: Mapped[str | None] = mapped_column(nullable=True)

    country: Mapped[Country] = mapped_column(Enum(Country))

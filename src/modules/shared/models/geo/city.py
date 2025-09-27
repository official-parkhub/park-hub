from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.audit import AuditMixin
from src.core.database.base import Base
from src.modules.shared.enums.country import Country

import uuid

if TYPE_CHECKING:
    from src.modules.management.models.company import Company
    from src.modules.shared.models.geo.state import State


class City(Base, AuditMixin):
    __tablename__ = "city"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    identification_code: Mapped[str | None]
    country: Mapped[Country] = mapped_column(Enum(Country))
    state_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("state.id"))
    name: Mapped[str]

    identification_code: Mapped[str | None]

    state: Mapped[State | None] = relationship(back_populates="cities", lazy="joined")
    companies: Mapped[list[Company]] = relationship(
        back_populates="city", lazy="joined"
    )

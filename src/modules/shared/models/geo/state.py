from sqlalchemy import UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.audit import AuditMixin
from src.core.database.base import Base
from src.modules.shared.enums.country import Country
from src.modules.shared.models.geo.city import City

import uuid


class State(Base, AuditMixin):
    __tablename__ = "state"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    country: Mapped[Country] = mapped_column(Enum(Country))
    name: Mapped[str] = mapped_column(unique=True)
    iso2_code: Mapped[str]

    __table_args__ = (UniqueConstraint("country", "iso2_code"),)

    cities: Mapped[list[City]] = relationship(back_populates="state")

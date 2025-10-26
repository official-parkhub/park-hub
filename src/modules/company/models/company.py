from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database.audit import AuditMixin
from src.core.database.base import Base


import uuid

from src.modules.company.models.company_image import CompanyImage
from src.modules.company.models.parking_exception import ParkingException
from src.modules.company.models.parking_price import ParkingPrice
from src.modules.company.models.organization import Organization
from src.modules.shared.models.geo.city import City


class Company(Base, AuditMixin):
    __tablename__ = "company"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organization.id"))
    city_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("city.id"))

    name: Mapped[str] = mapped_column()
    register_code: Mapped[str] = mapped_column(unique=True, index=True)
    address: Mapped[str] = mapped_column()
    postal_code: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)

    is_covered: Mapped[bool] = mapped_column(default=False, nullable=False)
    has_camera: Mapped[bool] = mapped_column(default=False, nullable=False)
    total_spots: Mapped[int] = mapped_column(nullable=False)
    has_charging_station: Mapped[bool] = mapped_column(default=False, nullable=False)

    organization: Mapped[Organization] = relationship(
        back_populates="companies", lazy="joined"
    )
    city: Mapped[City] = relationship(back_populates="companies", lazy="joined")
    parking_prices: Mapped[list[ParkingPrice]] = relationship(
        back_populates="company", lazy="selectin"
    )
    images: Mapped[list[CompanyImage]] = relationship(
        back_populates="company", lazy="selectin"
    )
    parking_exceptions: Mapped[list[ParkingException]] = relationship(
        back_populates="company", lazy="selectin"
    )

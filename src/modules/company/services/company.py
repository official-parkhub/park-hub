from sqlalchemy import select, func

from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.company.models.company import Company
from src.modules.company.models.parking_price import ParkingPrice
from src.modules.company.models.parking_exception import ParkingException
from src.modules.company.schemas.company.company import (
    CompanyListResponseSchema,
    CompanyWithTodayPricesSchema,
)
from src.modules.shared.models.geo.city import City

from sqlalchemy.orm import joinedload

from datetime import datetime, timezone


@dependable
class CompanyService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def list_companies(self, skip: int, limit: int) -> CompanyListResponseSchema:
        today_date = datetime.now(timezone.utc).date()
        weekday = today_date.weekday()

        exc_lat = (
            select(
                ParkingException.price_cents.label("exc_price"),
                ParkingException.start_hour.label("exc_start"),
                ParkingException.end_hour.label("exc_end"),
                ParkingException.is_discount.label("exc_discount"),
            )
            .where(
                ParkingException.company_id == Company.id,
                func.date(ParkingException.exception_date) == today_date,
                ParkingException.active,
            )
            .limit(1)
            .lateral("exc_lat")
        )

        price_lat = (
            select(
                ParkingPrice.price_cents.label("price_price"),
                ParkingPrice.start_hour.label("price_start"),
                ParkingPrice.end_hour.label("price_end"),
                ParkingPrice.is_discount.label("price_discount"),
            )
            .where(
                ParkingPrice.company_id == Company.id,
                ParkingPrice.week_day == weekday,
                ParkingPrice.active,
            )
            .order_by(ParkingPrice.start_hour)
            .limit(1)
            .lateral("price_lat")  # Creates another LATERAL subquery
        )

        today_price_cents = func.coalesce(
            exc_lat.c.exc_price, price_lat.c.price_price
        ).label("today_price_cents")
        today_start = func.coalesce(exc_lat.c.exc_start, price_lat.c.price_start).label(
            "today_start_hour"
        )
        today_end = func.coalesce(exc_lat.c.exc_end, price_lat.c.price_end).label(
            "today_end_hour"
        )
        today_is_discount = func.coalesce(
            exc_lat.c.exc_discount, price_lat.c.price_discount
        ).label("today_is_discount")

        stmt = (
            select(
                Company, today_price_cents, today_start, today_end, today_is_discount
            )
            .select_from(Company)
            .outerjoin(exc_lat, True)
            .outerjoin(price_lat, True)
            .options(
                joinedload(Company.city).joinedload(City.state),
                joinedload(Company.images),
            )
            .offset(skip)
            .limit(limit)
        )

        count_stmt = select(func.count()).select_from(Company)

        result = await self.db.execute(stmt)
        rows = result.all()
        total = (await self.db.execute(count_stmt)).scalar_one()

        data: list[CompanyWithTodayPricesSchema] = []
        for row in rows:
            company_obj = row[0]
            price_cents = row[1]
            start_hour = row[2]
            end_hour = row[3]
            is_discount = row[4]

            today_price = None
            if price_cents is not None:
                today_price = {
                    "start_hour": int(start_hour) if start_hour is not None else 0,
                    "end_hour": int(end_hour) if end_hour is not None else 0,
                    "price_cents": int(price_cents),
                    "is_discount": bool(is_discount)
                    if is_discount is not None
                    else False,
                }

            company_data = {
                "id": company_obj.id,
                "name": company_obj.name,
                "postal_code": company_obj.postal_code,
                "address": company_obj.address,
                "description": company_obj.description,
                "is_covered": company_obj.is_covered,
                "has_camera": company_obj.has_camera,
                "total_spots": company_obj.total_spots,
                "has_charging_station": company_obj.has_charging_station,
                "city": {
                    "id": company_obj.city.id,
                    "name": company_obj.city.name,
                    "identification_code": getattr(
                        company_obj.city, "identification_code", None
                    ),
                    "country": getattr(company_obj.city, "country", None),
                    "state": (
                        {
                            "id": company_obj.city.state.id,
                            "name": company_obj.city.state.name,
                            "country": getattr(company_obj.city.state, "country", None),
                            "iso2_code": getattr(
                                company_obj.city.state, "iso2_code", None
                            ),
                        }
                        if getattr(company_obj.city, "state", None)
                        else None
                    ),
                },
                "images": [
                    {"id": img.id, "url": img.url, "is_primary": img.is_primary}
                    for img in company_obj.images
                ],
                "today_parking_price": today_price,
            }

            data.append(CompanyWithTodayPricesSchema.model_validate(company_data))

        return CompanyListResponseSchema.model_validate(
            {"skip": skip, "limit": limit, "total": int(total), "data": data}
        )

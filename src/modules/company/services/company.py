import uuid
from fastapi import UploadFile
from src.core import errors
from sqlalchemy import insert, select

from src.core.bucket.session import (
    delete_file_object,
    get_presigned_url,
    upload_file_object,
)
from src.core.utils.base_service import BaseService
from src.core.utils.depends import dependable
from src.core.utils.request_context import RequestContext
from src.modules.company.models.company import Company
from src.modules.company.models.company_image import CompanyImage
from src.modules.company.schemas.company.company import (
    BaseCompanyImageSchema,
    CompleteCompanySchema,
)
from src.modules.company.schemas.company.company_price import (
    CompanyListResponseSchema,
    CompanyWithTodayPricesSchema,
)
from src.modules.company.schemas.company.create_company import CreateCompanySchema
from src.modules.company.services.company_price import CompanyPriceService
from src.modules.shared.enums.bucket import BucketNames
from src.modules.shared.models.geo.city import City

from sqlalchemy.orm import joinedload

from datetime import timedelta

from sqlalchemy.sql.expression import func

from src.modules.shared.schemas.city import BaseCitySchema


@dependable
class CompanyService(BaseService):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)

    async def list_companies(
        self,
        skip: int,
        limit: int,
        company_price_service: CompanyPriceService,
    ) -> CompanyListResponseSchema:
        companies_stmt = await self.db.execute(
            select(Company)
            .options(
                joinedload(Company.city),
                joinedload(Company.organization),
            )
            .where(Company.active)
            .offset(skip)
            .limit(limit)
        )
        companies = companies_stmt.scalars().all()
        total_companies_stmt = await self.db.execute(
            select(func.count()).where(Company.active)
        )
        total_companies = total_companies_stmt.scalars().first()

        data = []
        for company in companies:
            image = await self.get_main_company_image(company.id)
            data.append(
                CompanyWithTodayPricesSchema(
                    name=company.name,
                    postal_code=company.postal_code,
                    register_code=company.register_code,
                    address=company.address,
                    description=company.description,
                    is_covered=company.is_covered,
                    has_camera=company.has_camera,
                    total_spots=company.total_spots,
                    has_charging_station=company.has_charging_station,
                    id=company.id,
                    city=BaseCitySchema.model_validate(
                        company.city, from_attributes=True
                    ),
                    today_parking_price=await company_price_service.get_parking_price_reference(
                        company.id
                    ),
                    images=[image] if image else [],
                )
            )

        return CompanyListResponseSchema(
            total=total_companies,
            skip=skip,
            limit=limit,
            data=data,
        )

    async def get_company_by_id(self, company_id: str) -> CompleteCompanySchema:
        result = await self.db.execute(
            select(Company)
            .options(
                joinedload(Company.parking_prices),
                joinedload(Company.parking_exceptions),
                joinedload(Company.city),
                joinedload(Company.organization),
            )
            .where(Company.id == company_id, Company.active)
        )
        company = result.scalars().first()

        if not company:
            raise errors.ResourceNotFound(message="Company not found")

        return CompleteCompanySchema.model_validate(company, from_attributes=True)

    async def create_company(
        self,
        organization_id: str,
        create_company_schema: CreateCompanySchema,
    ) -> CompleteCompanySchema:
        city_stmt = await self.db.execute(
            select(City).where(City.id == create_company_schema.city_id)
        )
        existing_city = city_stmt.scalars().first()

        if not existing_city:
            raise errors.ResourceNotFound(message="City not found")

        company_stmt = await self.db.execute(
            select(Company).where(
                Company.register_code == create_company_schema.register_code
            )
        )
        existing_company = company_stmt.scalars().first()

        if existing_company:
            raise errors.InvalidOperation(
                message="Company already exists with this register code"
            )

        stmt = (
            insert(Company)
            .values(
                organization_id=organization_id,
                active=True,
                name=create_company_schema.name,
                address=create_company_schema.address,
                city_id=create_company_schema.city_id,
                register_code=create_company_schema.register_code,
                is_covered=create_company_schema.is_covered,
                has_camera=create_company_schema.has_camera,
                total_spots=create_company_schema.total_spots,
                has_charging_station=create_company_schema.has_charging_station,
                description=create_company_schema.description,
                postal_code=create_company_schema.postal_code,
            )
            .returning(Company)
        )

        result = await self.db.execute(stmt)
        company = result.scalars().first()

        return await self.get_company_by_id(company.id)

    async def add_company_image(
        self, company_id: str, is_primary: bool, file: UploadFile
    ) -> None:
        random_uuid = str(uuid.uuid4())
        stmt = (
            insert(CompanyImage)
            .values(
                company_id=company_id,
                is_primary=is_primary,
                key=f"{random_uuid}.{file.filename.split('.')[-1]}",
            )
            .returning(CompanyImage)
        )

        result = await self.db.execute(stmt)
        company_image = result.scalars().first()

        bucket_name = BucketNames.COMPANY_IMAGES
        await upload_file_object(
            bucket_name=bucket_name,
            object_name=company_image.key,
            file_object=file.file,
        )

        await self.db.commit()

    async def get_company_images(self, company_id: str) -> list[BaseCompanyImageSchema]:
        stmt = select(CompanyImage).where(
            CompanyImage.company_id == company_id, CompanyImage.active
        )
        result = await self.db.execute(stmt)
        company_images = result.scalars().all()

        bucket_name = BucketNames.COMPANY_IMAGES
        return [
            BaseCompanyImageSchema(
                id=company_image.id,
                is_primary=company_image.is_primary,
                url=await get_presigned_url(
                    bucket_name=bucket_name,
                    object_name=company_image.key,
                    expiration=timedelta(minutes=15).seconds,
                ),
            )
            for company_image in company_images
        ]

    async def get_main_company_image(
        self, company_id: str
    ) -> BaseCompanyImageSchema | None:
        stmt = (
            select(CompanyImage)
            .where(
                CompanyImage.company_id == company_id,
                CompanyImage.active,
            )
            .limit(1)
            .order_by(CompanyImage.is_primary.desc())
        )
        result = await self.db.execute(stmt)
        company_image = result.scalars().first()

        if not company_image:
            return None

        bucket_name = BucketNames.COMPANY_IMAGES
        return BaseCompanyImageSchema(
            id=company_image.id,
            is_primary=company_image.is_primary,
            url=await get_presigned_url(
                bucket_name=bucket_name,
                object_name=company_image.key,
                expiration=timedelta(minutes=15).seconds,
            ),
        )

    async def delete_company_image(
        self, company_id: str, company_image_id: str
    ) -> None:
        stmt = select(CompanyImage).where(
            CompanyImage.id == company_image_id,
            CompanyImage.company_id == company_id,
            CompanyImage.active,
        )
        result = await self.db.execute(stmt)
        company_image = result.scalars().first()

        if not company_image:
            raise errors.ResourceNotFound(message="Company image not found")

        company_image.active = False
        await delete_file_object(
            bucket_name=BucketNames.COMPANY_IMAGES,
            object_name=company_image.key,
        )
        await self.db.commit()

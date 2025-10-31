from fastapi import APIRouter
import uuid

from src.modules.company.dependencies.company_image import (
    DepAddCompanyImage,
    DepCompanyImages,
    DepRemoveCompanyImage,
)
from src.modules.company.dependencies.create_company import DepCreateCompany
from src.modules.company.dependencies.list_companies import DepListCompanies
from src.modules.company.schemas.company.company import (
    BaseCompanyImageSchema,
    CompleteCompanySchema,
)
from src.modules.company.services.company import CompanyService

router = APIRouter(
    prefix="/company",
    tags=["Company"],
)

image_router = APIRouter(
    prefix="/company/{company_id}/images",
    tags=["Company Images"],
)


@router.get("/list")
async def list_companies(
    result: DepListCompanies,
):
    """
    List all companies.
    """
    return result


@router.post("/", status_code=201)
async def create_company(
    response: DepCreateCompany,
) -> CompleteCompanySchema:
    """
    Create a new company.
    """
    return response


@router.get("/{company_id}")
async def get_company_by_id(
    company_id: uuid.UUID,
    company_service: CompanyService,
) -> CompleteCompanySchema:
    """
    Get a company by its ID.
    """
    return await company_service.get_company_by_id(str(company_id))


@image_router.get("/")
async def get_company_images(
    result: DepCompanyImages,
) -> list[BaseCompanyImageSchema]:
    """
    Get all images for a company.
    """
    return result


@image_router.post("/", status_code=204)
async def add_company_image(
    result: DepAddCompanyImage,
) -> None:
    """
    Add an image for a company.
    """
    return result


@image_router.delete("/{image_id}", status_code=204)
async def delete_company_image(
    result: DepRemoveCompanyImage,
) -> None:
    """
    Delete an image for a company.
    """
    return result

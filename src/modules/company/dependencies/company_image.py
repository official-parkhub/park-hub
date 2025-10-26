from typing import Annotated

from src.modules.company.schemas.company.company import BaseCompanyImageSchema
from src.modules.shared.dependencies.auth import DepCurrentUser

from fastapi import Depends, UploadFile
from src.modules.company.services.company import CompanyService

from src.core import errors


async def _get_company_images(
    _current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: str,
):
    return await company_service.get_company_images(company_id)


DepCompanyImages = Annotated[
    list[BaseCompanyImageSchema],
    Depends(_get_company_images),
]


async def _add_company_image(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: str,
    file: UploadFile,
    is_primary: bool = False,
):
    existing_company = await company_service.get_company_by_id(company_id)
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to add images to this company"
        )

    await company_service.add_company_image(company_id, is_primary, file)


async def _remove_company_image(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: str,
    image_id: str,
):
    existing_company = await company_service.get_company_by_id(company_id)
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to remove images from this company"
        )

    await company_service.delete_company_image(company_id, image_id)


DepRemoveCompanyImage = Annotated[
    None,
    Depends(_remove_company_image),
]

DepCompanyImages = Annotated[
    list[BaseCompanyImageSchema],
    Depends(_get_company_images),
]

DepAddCompanyImage = Annotated[
    None,
    Depends(_add_company_image),
]

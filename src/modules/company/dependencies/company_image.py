from typing import Annotated, TypeAlias
import uuid

from src.modules.company.schemas.company.company import BaseCompanyImageSchema
from src.modules.shared.dependencies.auth import DepCurrentUser

from fastapi import Depends, UploadFile
from src.modules.company.services.company import CompanyService

from src.core import errors


async def _get_company_images(
    _current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: uuid.UUID,
):
    return await company_service.get_company_images(str(company_id))


DepCompanyImages: TypeAlias = Annotated[
    list[BaseCompanyImageSchema],
    Depends(_get_company_images),
]


async def _add_company_image(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: uuid.UUID,
    file: UploadFile,
    is_primary: bool = False,
):
    existing_company = await company_service.get_company_by_id(str(company_id))
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to add images to this company"
        )

    await company_service.add_company_image(str(company_id), is_primary, file)


async def _remove_company_image(
    current_user: DepCurrentUser,
    company_service: CompanyService,
    company_id: uuid.UUID,
    image_id: uuid.UUID,
):
    existing_company = await company_service.get_company_by_id(str(company_id))
    if (
        not current_user.organization
        or current_user.organization.id != existing_company.organization_id
    ):
        raise errors.ForbiddenError(
            "You do not have permission to remove images from this company"
        )

    await company_service.delete_company_image(str(company_id), str(image_id))


DepRemoveCompanyImage: TypeAlias = Annotated[
    None,
    Depends(_remove_company_image),
]

DepAddCompanyImage: TypeAlias = Annotated[
    None,
    Depends(_add_company_image),
]

from fastapi import APIRouter

from src.modules.company.dependencies.list_companies import DepListCompanies

router = APIRouter(
    prefix="/company",
    tags=["Company"],
)


@router.get("/list")
async def list_companies(
    result: DepListCompanies,
):
    """
    List all companies.
    """
    return result

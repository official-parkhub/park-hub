from typing import Annotated

from src.modules.shared.dependencies.auth import DepCurrentUser

from fastapi import Depends


async def _list_companies(
    _current_user: DepCurrentUser,
    skip: int = 0,
    limit: int = 10,
):
    raise Exception("Function not implemented yet")


DepListCompanies = Annotated[
    dict[str, list[str]],
    Depends(_list_companies),
]

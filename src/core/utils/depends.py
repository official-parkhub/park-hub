from typing import Annotated

from fastapi import Depends


def dependable[T](cls: type[T]) -> type[T]:
    return Annotated[cls, Depends(cls)]

from typing import Any

from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class ApplicationError(Exception):
    KIND = "APPLICATION_ERROR"
    STATUS_CODE = 400

    def __init__(self, *, message: str | None = None, data: Any | None = None):
        self.message = message
        self.data = data

    def to_fastapi_response(self) -> Response:
        content = {"kind": self.KIND}
        if self.message:
            content["message"] = self.message
        if self.data:
            content["data"] = self.data
        return JSONResponse(status_code=self.STATUS_CODE, content=jsonable_encoder(content))


class UnavailableResource(ApplicationError):
    KIND = "UNAVAILABLE_RESOURCE"
    STATUS_CODE = 503

    def __init__(self, *, message: str = None):
        super().__init__(message=message)


class AuthenticationRequired(ApplicationError):
    KIND = "AUTHENTICATION_REQUIRED"
    STATUS_CODE = 401

    def __init__(self, *, message: str = None):
        super().__init__(message=message)


class AccessDenied(ApplicationError):
    KIND = "ACCESS_DENIED"
    STATUS_CODE = 403

    def __init__(self, *, message: str = None):
        super().__init__(message=message)


class InvalidOperation(ApplicationError):
    KIND = "INVALID_OPERATION"
    STATUS_CODE = 403

    def __init__(self, *, message: str = None):
        super().__init__(message=message)


class ResourceAlreadyExists(ApplicationError):
    KIND = "RESOURCE_ALREADY_EXISTS"
    STATUS_CODE = 409

    def __init__(self, *, message: str = None):
        super().__init__(message=message)


class ResourceNotFound(ApplicationError):
    KIND = "RESOURCE_NOT_FOUND"
    STATUS_CODE = 404

    def __init__(self, *, message: str = None):
        super().__init__(message=message)

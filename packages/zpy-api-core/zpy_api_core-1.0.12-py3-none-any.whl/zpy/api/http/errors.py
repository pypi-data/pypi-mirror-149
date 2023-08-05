from typing import Optional, List

from zpy.api.http.status_codes import HttpStatus


class ZError(Exception):
    """Base Error

    Args:
        Exception ([type]): [description]
    """

    def __init__(
            self, message: str, reason: str, details: Optional[List[str]], meta: Optional[dict] = None,
            parent_ex: Exception = None, *args: object
    ) -> None:
        super().__init__(message, *args)
        self.reason = reason
        self.message = message
        self.details = details
        self.metadata = meta
        self.internal_exception = parent_ex

    def add_detail(self, message: str) -> None:
        if self.details is None:
            self.details = []
        self.details.append(message)

    def set_metadata(self, value: dict):
        self.metadata = value

    def __str__(self):
        return f'[ZCE] - {self.message}\n\t  - {self.reason}'


class ZHttpError(ZError):
    """Http Base Error

    Args:
        ZError ([type]): [description]
    """

    def __init__(
            self,
            message: str = None,
            reason: str = None,
            details: Optional[List[str]] = None,
            status: HttpStatus = HttpStatus.INTERNAL_SERVER_ERROR,
            meta: Optional[dict] = None,
            parent_ex: Exception = None,
            *args: object
    ) -> None:
        super().__init__(message, reason, details, meta, parent_ex, *args)
        self.status = status


class BadRequest(ZHttpError):
    """BadRequest

    Args:
        ZError ([type]): [description]
    """

    def __init__(
            self,
            message: str = None,
            reason: str = None,
            details: Optional[List[str]] = None,
            meta: Optional[dict] = None,
            parent_ex: Exception = None,
            *args: object
    ) -> None:
        super().__init__(message, reason, details, HttpStatus.BAD_REQUEST, meta, parent_ex, *args)


class Unauthorized(ZHttpError):
    """Unauthorized

    Args:
        ZError ([type]): [description]
    """

    def __init__(
            self,
            message: str = None,
            reason: str = None,
            details: Optional[List[str]] = None,
            meta: Optional[dict] = None,
            parent_ex: Exception = None,
            *args: object
    ) -> None:
        super().__init__(message, reason, details, HttpStatus.UNAUTHORIZED, meta, parent_ex, *args)


class NotFound(ZHttpError):
    """BadRequest

    Args:
        ZError ([type]): [description]
    """

    def __init__(
            self,
            message: str = None,
            reason: str = None,
            details: Optional[List[str]] = None,
            meta: Optional[dict] = None,
            parent_ex: Exception = None,
            *args: object
    ) -> None:
        super().__init__(message, reason, details, HttpStatus.NOT_FOUND, meta, parent_ex, *args)


class UnprocessableEntity(ZHttpError):
    """UnprocessableEntity

    Args:
        ZError ([type]): [description]
    """

    def __init__(
            self,
            message: str = None,
            reason: str = None,
            details: Optional[List[str]] = None,
            meta: Optional[dict] = None,
            parent_ex: Exception = None,
            *args: object
    ) -> None:
        super().__init__(message, reason, details, HttpStatus.UNPROCESSABLE, meta, parent_ex, *args)

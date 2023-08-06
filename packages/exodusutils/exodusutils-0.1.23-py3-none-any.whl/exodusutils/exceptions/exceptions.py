from typing import Optional

from fastapi import HTTPException, status


class ExodusBadRequest(HTTPException):
    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ExodusNotFound(HTTPException):
    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ExodusForbidden(HTTPException):
    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ExodusMethodNotAllowed(HTTPException):
    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=detail)


class ExodusError(HTTPException):
    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )

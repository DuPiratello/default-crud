from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


# Raised when entity is not found
class NotFoundException(HTTPException):
    def __init__(self, entity: str = "Resource", entity_id: int | str = ""):
        detail = f"{entity} with id '{entity_id}' not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


# Raised when entity already exists
class AlreadyExistsException(HTTPException):
    def __init__(self, entity: str = "Resource", field: str = ""):
        detail = f"{entity} with {field} already exists"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


# Raised on invalid input or business rule violations
class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


# Global handler for unhandled exceptions
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse
from typing import Type, Dict, Any
from .auth import UserAlreadyExistsException, InvalidCredentialsException, TokenCredentialsException
from .user import UserNotFoundException
from .company import CompanyNotFoundException, CompanyAlreadyExistsException

EXCEPTION_MAP: Dict[Type[Exception], Dict[str, Any]] = {
    UserAlreadyExistsException: {"status_code": status.HTTP_400_BAD_REQUEST},
    InvalidCredentialsException: {"status_code": status.HTTP_400_BAD_REQUEST, "headers": {"WWW-Authenticate": "Bearer"}},
    UserNotFoundException: {"status_code": status.HTTP_404_NOT_FOUND},
    TokenCredentialsException: {"status_code": status.HTTP_401_UNAUTHORIZED},
    CompanyNotFoundException: {"status_code": status.HTTP_404_NOT_FOUND},
    CompanyAlreadyExistsException: {"status_code": status.HTTP_400_BAD_REQUEST}
}

async def generic_exception_handler(request: Request, exc: Exception):
    """Handles all custom exceptions based on EXCEPTION_MAP."""
    config = EXCEPTION_MAP.get(type(exc))
    if config:
        return JSONResponse(
            status_code=config["status_code"],
            content={"detail": getattr(exc, "message", str(exc))},
            headers=config.get("headers", None)
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"}
    )

def register_exception_handlers(app: FastAPI):
    """Registers all custom exceptions with FastAPI."""
    for exc_class in EXCEPTION_MAP.keys():
        app.add_exception_handler(exc_class, generic_exception_handler)

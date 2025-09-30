from pydantic import BaseModel, Field
from typing import Any, TypeVar, Generic

T = TypeVar('T')

class ResponseDTO(BaseModel, Generic[T]):
    message: str = Field(...)
    data: T | None = Field(default=None)
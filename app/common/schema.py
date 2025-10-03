from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import TypeVar, Generic
from datetime import datetime

T = TypeVar('T')

class CommonBaseModel(BaseModel, Generic[T]):
    class Config:
        #alias_generator=to_camel
        model_config = ConfigDict(
            #alias_generator=to_camel,
            populate_by_name=True,
            from_attributes=True,
            str_strip_whitespace=True,
            extra="forbid"
        )

class PaginationDTO(CommonBaseModel, BaseModel):
    """
    DTO to hold pagination metadata for hybrid (time + cursor) pagination.
    """
    limit: int = Field(..., gt=0, description="Number of items requested per page")
    total: int = Field(..., ge=0, description="Total number of items within the date range")
    next_cursor: str | None = Field(
        default=None, description="Cursor (ObjectId) for the next page, or None if no more pages"
    )
    start_date: datetime | None = Field(
        default=None, description="Start of the time window used for filtering"
    )
    end_date: datetime | None = Field(
        default=None, description="End of the time window used for filtering"
    )
    
    
class ResponseDTO(CommonBaseModel, Generic[T]):   
    """
    Standard API response wrapper with optional pagination metadata.
    """
    message: str | None = Field(default=None, description="Human-readable response message")
    data: T | None = Field(default=None, description="The actual payload")
    status_code: int = Field(..., description="HTTP status code of the response")
    pagination: PaginationDTO | None = Field(
        default=None, description="Pagination metadata if the response is paginated"
    )

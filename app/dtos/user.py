from pydantic import Field, field_validator, field_serializer
from datetime import datetime, timezone
from app.common.schema import CommonBaseModel
from app.exceptions.user import UserInvalidBirthdayException

class UserUpdate(CommonBaseModel):
    first_name: str | None = Field(
        default=None,
        title="First Name",
        description="The user's given name."
    )
    last_name: str | None = Field(
        default=None,
        title="Last Name",
        description="The user's family name or surname."
    )
    birthday: datetime | None = Field(
        default=None,
        title="Birthday",
        description="The user's date of birth."
    )
    
    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, v):
        if v:
            now = datetime.now(timezone.utc)
            if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
                v = v.replace(tzinfo=timezone.utc)
            if v.date() >= now.date():
                raise UserInvalidBirthdayException()
        return v

    
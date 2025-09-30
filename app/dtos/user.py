from pydantic import BaseModel, Field
from datetime import datetime

class UserUpdate(BaseModel):
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
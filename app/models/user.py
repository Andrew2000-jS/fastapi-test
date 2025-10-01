from pydantic import Field, field_validator
from beanie import before_event, Update
from datetime import datetime
from app.common.model import CommonDocument

class User(CommonDocument):
    """
        User document representing a person in the system.

        Stores basic personal information including first name, last name, and birthday.
    """
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        title="First Name",
        description="The user's first name. Must be between 2 and 50 characters."
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        title="Last Name",
        description="The user's last name. Must be between 2 and 50 characters."
    )
    birthday: datetime | None = Field(default=None)

    class Settings:
        name = "users"
    
    @before_event(Update)
    async def capitalize_names(self):
        """
            Capitalize the first letter of the user's first name or last name 
            before updating the document in the database.

            This method is triggered automatically before an update operation. 
            - If `first_name` is present, it capitalizes the first letter.
            - If `first_name` is not present but `last_name` is, it capitalizes the first letter of `last_name`.
        """
        if self.first_name:
            self.first_name = self.first_name.capitalize()
        elif self.last_name:
            self.last_name = self.last_name.capitalize()
        
    @field_validator("birthday")
    def validate_birthday(cls, v: datetime) -> datetime:
        """
            Validate the user's birthday field.
        """
        if v and v > datetime.now():
            raise ValueError("Birthday cannot be in the future.")
        return v

from pydantic import Field, EmailStr
from app.common.schema import CommonBaseModel

class BaseAuth(CommonBaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=20,
        title="Username",
        description="The new username for the account. Must be unique and contain between 3 and 50 characters.."
    )
    password: str = Field(
        ..., 
        min_length=6, 
        title="Password", 
        description="The new password for the account. Must be at least 6 characters long."
    )
    email: EmailStr = Field(
        ...,
        title="Email Address",
        description="The new email address associated with the account."
    )

class AuthCreate(BaseAuth):
    pass
    
class AuthUpdate(CommonBaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        title="Username",
        description="The new username for the account. Must be unique and contain between 3 and 50 characters."
    )
    password: str | None = Field(
        default=None,
        min_length=6,
        title="Password",
        description="The new password for the account. Must be at least 6 characters long."
    )
    email: EmailStr | None = Field(
        default=None,
        title="Email Address",
        description="The new email address associated with the account."
    )


class Token(CommonBaseModel):
    access_token: str = Field(
        ...,
        title="Access Token",
        description="The JWT access token used to authenticate API requests."
    )
    token_type: str = Field(
        ...,
        title="Token Type",
        description="The type of the token provided, typically 'Bearer'."
    )
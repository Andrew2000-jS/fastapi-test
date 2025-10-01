from beanie import Link, Indexed, before_event, Delete
from typing import Annotated
from pydantic import Field, EmailStr
from .user import User
from app.common.model import CommonDocument
from app.dtos.auth import BaseAuth

class Auth(CommonDocument):
    """
        Auth document representing user authentication credentials.
        
        Stores the username, password, email, and a link to the related User document.
    """
    username: Annotated[str, Indexed(unique=True)] = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    email: EmailStr = Field(...)
    user: Link[User]
    
    class Settings:
        name = "auth"

    @classmethod
    def from_dto(cls, data: BaseAuth, user: User) -> "Auth":
        """
        Create an Auth document instance from a BaseAuth DTO and a linked User.

        Args:
            data (BaseAuth): The DTO containing auth information.
            user (User): The linked User document.

        Returns:
            Auth: A new Auth document instance populated with the DTO data and linked user.
        """
        return cls(
            username=data.username,
            password=data.password,
            email=data.email,
            user=user  # type: ignore
        )

    @classmethod
    def to_dto(cls, auth: "Auth") -> BaseAuth:
        """
        Convert an Auth document instance into a BaseAuth DTO.

        Args:
            auth (Auth): The Auth document instance to convert.

        Returns:
            BaseAuth: A data transfer object containing the auth information.
        """
        return BaseAuth(
            username=auth.username,
            password=auth.password,
            email=auth.email
        )
        
    @before_event(Delete)
    async def delete_related_user(self):
        """
            Delete the linked User document before deleting this Auth document.

            This ensures that when an Auth instance is removed, the associated User is
            also removed to maintain data integrity.
        """  
        if self.user:
            await self.user.delete() # type: ignore

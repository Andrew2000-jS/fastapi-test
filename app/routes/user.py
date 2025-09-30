from fastapi import APIRouter, Body, status
from typing import Annotated
from app.dtos.user import UserUpdate
from app.dtos.common import ResponseDTO
from app.conf.security import auth_dependency
from app.models.user import User
from app.exceptions.user import UserNotFoundException
from datetime import datetime

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.patch("/", status_code=status.HTTP_200_OK, response_model=ResponseDTO)
async def update_user(body: Annotated[UserUpdate, Body()], crr_auth: auth_dependency):
    user = await User.get(crr_auth.user.id) # type: ignore
    if not user:
        raise UserNotFoundException()
    
    await user.update({
        "$set": {
            User.first_name: body.first_name if body.first_name else user.first_name,
            User.last_name: body.last_name if body.last_name else user.last_name,
            User.birthday: body.birthday if body.birthday else user.birthday
        }
    })
    
    return ResponseDTO(message="User updated Successfully")

@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(crr_auth: auth_dependency):
    await crr_auth.delete()
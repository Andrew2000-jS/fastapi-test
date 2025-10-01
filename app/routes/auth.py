from fastapi import APIRouter, Body, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from app.conf.security import PasswordService, AuthService, TokenService
from app.models.auth import Auth
from app.models.user import User
from app.dtos.auth import AuthCreate, Token
from app.common.schema import ResponseDTO
from app.conf.consts import ACCESS_TOKEN_EXPIRE_MINUTES
from app.exceptions.auth import UserAlreadyExistsException, InvalidCredentialsException

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])

@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ResponseDTO[None])
async def register(body: Annotated[AuthCreate, Body(...)]):
    existing_auth = await Auth.find_one(Auth.username == body.username)
    if existing_auth:
        raise UserAlreadyExistsException(body.username)
    
    try:
        user = User()
        await user.insert()
        body.password = PasswordService.hash_password(body.password)
        new_auth = Auth.from_dto(data=body, user=user)
        await new_auth.insert()
        response = ResponseDTO(
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED
        )
        return response.model_dump(by_alias=True)
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token | None:
    auth = await AuthService.authenticate_user(username=form_data.username, password=form_data.password)
    if not auth:
        raise InvalidCredentialsException()
    try:
        data = {"sub": auth.username}
        token_exp = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = TokenService.create_access_token(data, expires_delta=token_exp)
        return Token(access_token=token, token_type="bearer")
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something was wrong")

        
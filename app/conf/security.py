import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.models.auth import Auth
from app.models.user import User
from datetime import timedelta, datetime, timezone
from typing import Annotated, Any
from fastapi import Depends
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from .consts import SECRET_KEY, ALGORITHM
from app.exceptions.auth import TokenCredentialsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class PasswordService:
    """Handles password hashing and verification."""
    _pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(plain_password, hashed_password)

class TokenService:
    """Handles token managament."""
    
    @classmethod
    def create_access_token(cls, data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @classmethod
    def decode_access_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[str(ALGORITHM)])
            return payload
        except ExpiredSignatureError:
            raise TokenCredentialsException()
        except InvalidTokenError:
            raise TokenCredentialsException()
    
class AuthService:
    """Handles authentication."""

    @classmethod
    async def get_user_auth(cls, username: str) -> Auth | None:
        return await Auth.find_one(Auth.username == username)

    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Auth | None:
        auth = await cls.get_user_auth(username)
        if not auth:
            return None
        if not PasswordService.verify_password(password, auth.password):
            return None
        return auth

    @classmethod
    async def get_current_auth(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> Auth:
        payload = TokenService.decode_access_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise TokenCredentialsException()
        auth = await cls.get_user_auth(username)
        if not auth:
            raise TokenCredentialsException()
        await auth.fetch_link(Auth.user)
        return auth

auth_dependency = Annotated[Auth, Depends(AuthService.get_current_auth)]    
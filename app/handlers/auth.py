from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import Response

from ..decorators import handle_mongo_exceptions
from ..mongo import DoesNotExistError
from ..schemas.auth import TokenPair, AccessToken, RefreshToken
from ..schemas.users import User
from ..mongo.users_crud import get_user, create_user
from ..services.auth import (
    CredentialsException,
    create_jwt_token_pair,
    refresh_access_token,
)
from ..services.encrypt import validate_password

router = APIRouter(prefix="/auth", tags=["auth"])


# Регистрация пользователя
@router.post("/register")
@handle_mongo_exceptions
def register(user: User):
    """Регистрация нового пользователя"""
    try:
        get_user(username=user.username)
    except DoesNotExistError:
        create_user(user)
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )


@router.post("/token", response_model=TokenPair)
def get_tokens(user: User):
    """Получение пары JWT"""
    try:
        user_model = get_user(username=user.username)
    except DoesNotExistError:
        raise CredentialsException

    if not validate_password(user.password, user_model.password):
        raise CredentialsException

    return create_jwt_token_pair(user_id=user_model.id)


@router.post("/token/refresh", response_model=AccessToken)
def refresh(token: RefreshToken):
    """Получение нового access token через refresh token"""
    return AccessToken(accessToken=refresh_access_token(token.refresh_token))

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..decorators import handle_mongo_exceptions
from ..mongo.passed_questions_crud import get_user_passed_question_list
from ..mongo.users_crud import (
    get_user,
    update_user,
    get_all_raw_users,
    change_user_password,
)
from ..mongo.questions_crud import get_all_question_groups
from ..schemas.users import MinimalUser, User, SelfUser, UpdateUser, Password
from ..schemas.passed_questions import PassedQuestionsDetail
from ..schemas.questions import MinimalQuestionGroup
from ..services.auth import get_current_user
from ..services.cache import CacheService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[MinimalUser])
async def get_myself_user_view(user: User = Depends(get_current_user)):
    """Список всех пользователей"""
    if user.is_superuser:
        return await get_all_raw_users()
    else:
        raise HTTPException(
            status_code=403, detail="У вас нет прав для просмотра списка пользователей"
        )


@router.get("/myself", response_model=SelfUser)
async def get_myself_user_view(user: User = Depends(get_current_user)):
    """Данные пользователя, который авторизован"""
    return user.model_dump(by_alias=True)


@router.patch("/myself", response_model=SelfUser)
@handle_mongo_exceptions
async def update_myself_user_view(
    updated_user: UpdateUser, user: User = Depends(get_current_user)
):
    """Обновить данные пользователя, который авторизован"""
    await update_user(user_id=user.id, new_data=updated_user)
    await CacheService().delete(f"user:{user.id}")
    return user.model_dump(by_alias=True)


@router.patch("/myself/password", status_code=status.HTTP_200_OK)
@handle_mongo_exceptions
async def update_myself_password_view(
    passwd: Password, user: User = Depends(get_current_user)
):
    """Обновить данные пользователя, который авторизован"""
    await change_user_password(user_id=user.id, new_password=passwd.password)
    await CacheService().delete(f"user:{user.id}")


@router.get("/{username}", response_model=MinimalUser)
@handle_mongo_exceptions
async def get_user_view(username: str):
    """Данные пользователя"""
    user = await get_user(username=username)
    return user.model_dump(by_alias=True)


@router.get("/{user_id}/questions", response_model=list[MinimalQuestionGroup])
@handle_mongo_exceptions
async def get_user_questions_view(user_id: str):
    """Тесты, которые создал пользователь"""
    return await get_all_question_groups(filter_={"user_id": ObjectId(user_id)})


@router.get("/{user_id}/passed-questions", response_model=list[PassedQuestionsDetail])
@handle_mongo_exceptions
async def get_user_passed_questions_view(user_id: str):
    """История прохождений тестов пользователя"""
    return await get_user_passed_question_list(user_id)

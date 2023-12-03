from bson import ObjectId
from fastapi import APIRouter, Depends

from ..decorators import handle_mongo_exceptions
from ..mongo.passed_questions_crud import get_user_passed_question_list
from ..mongo.users_crud import get_user, update_user
from ..mongo.questions_crud import get_all_question_groups
from ..schemas.users import MinimalUser, User, SelfUser, UpdateUser
from ..schemas.passed_questions import PassedQuestionsDetail
from ..schemas.questions import MinimalQuestionGroup
from ..services.auth import get_current_user

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/myself", response_model=SelfUser)
async def get_user_view(user: User = Depends(get_current_user)):
    """Данные пользователя, который авторизован"""
    return user.model_dump(by_alias=True)


@router.patch("/myself", response_model=SelfUser)
@handle_mongo_exceptions
async def update_user_view(updated_user: UpdateUser, user: User = Depends(get_current_user)):
    """Обновить данные пользователя, который авторизован"""
    await update_user(user_id=user.id, new_data=updated_user)
    return user.model_dump(by_alias=True)


@router.get("/{user_id}", response_model=MinimalUser)
@handle_mongo_exceptions
async def get_user_view(user_id: str):
    """Данные пользователя"""
    return await get_user(_id=user_id)


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

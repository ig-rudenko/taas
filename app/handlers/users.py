from bson import ObjectId
from fastapi import APIRouter

from ..mongo.passed_questions_crud import get_user_passed_question_list
from ..mongo.users_crud import get_user
from ..mongo.questions_crud import get_all_question_groups
from ..schemas.users import MinimalUser
from ..schemas.passed_questions import PassedQuestion
from ..schemas.questions import MinimalQuestionGroup


router = APIRouter(prefix="/user", tags=["users"])


@router.get("/{user_id}", response_model=MinimalUser)
def get_user_view(user_id: str):
    """Данные пользователя"""
    return get_user(_id=user_id)


@router.get("/{user_id}/questions", response_model=list[MinimalQuestionGroup])
def get_user_questions_view(user_id: str):
    """Тесты, которые создал пользователь"""
    return get_all_question_groups(filter_={"user_id": ObjectId(user_id)})


@router.get("/{user_id}/passed-questions", response_model=list[PassedQuestion])
def get_user_view(user_id: str):
    """История прохождений тестов пользователя"""
    return get_user_passed_question_list(user_id)

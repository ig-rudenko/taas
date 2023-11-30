from bson import ObjectId
from fastapi import APIRouter

from ..mongo.users_crud import get_user
from ..mongo.questions_crud import get_all_question_groups
from ..schemas.users import MinimalUser
from ..schemas.questions import MinimalQuestionGroup


router = APIRouter(prefix="/user", tags=["users"])


@router.get("/{user_id}", response_model=MinimalUser)
def get_user_view(user_id: str):
    return get_user(_id=user_id)


@router.get("/{user_id}/questions", response_model=list[MinimalQuestionGroup])
def get_user_view(user_id: str):
    return get_all_question_groups(filter_={"user_id": ObjectId(user_id)})

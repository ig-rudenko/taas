from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from ..mongo.questions_crud import (
    get_all_question_groups,
    get_question_group,
    create_question_group,
    update_question_group,
    delete_question_group,
)
from ..decorators import handle_mongo_exceptions
from ..schemas.users import User
from ..services.auth import get_current_user
from ..services.permissions import has_permission_to_question_group
from ..services.validate_questions import validate_questions, ValidateException
from ..schemas.questions import (
    QuestionGroup,
    CreateUpdateQuestionGroup,
    QuestionGroupResult,
    FullQuestionGroup,
    MinimalQuestionGroup,
)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/groups", response_model=list[MinimalQuestionGroup])
def list_question_groups_view():
    return get_all_question_groups(limit=100)


@router.post(
    "/groups", response_model=FullQuestionGroup, status_code=status.HTTP_201_CREATED
)
def create_question_group_view(
    question: CreateUpdateQuestionGroup, user: User = Depends(get_current_user)
):
    return create_question_group(question, user.id)


@router.get("/group/{group_id}", response_model=QuestionGroup)
@handle_mongo_exceptions
def question_group_view(group_id: str):
    return get_question_group(group_id)


@router.put("/group/{group_id}")
@handle_mongo_exceptions
def update_question_group_view(
    group_id: str,
    question: CreateUpdateQuestionGroup,
    user: User = Depends(get_current_user),
):
    if not has_permission_to_question_group(
        user_id=user.id, question_group_id=group_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this question group.",
        )

    update_question_group(group_id, question)


@router.delete("/group/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_mongo_exceptions
def delete_question_group_view(group_id: str, user: User = Depends(get_current_user)):
    if not has_permission_to_question_group(
        user_id=user.id, question_group_id=group_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this question group.",
        )

    delete_question_group(group_id)


@router.post("/validate", response_model=QuestionGroupResult)
@handle_mongo_exceptions
def validate_question_group_view(question_group_data: FullQuestionGroup):
    try:
        return validate_questions(question_group_data)
    except ValidateException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

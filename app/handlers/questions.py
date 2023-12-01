from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from ..mongo.questions_crud import (
    get_all_question_groups,
    get_question_group,
    create_question_group,
    update_question_group,
    delete_question_group,
)
from ..mongo.passed_questions_crud import (
    create_passed_question,
    get_last_passed_question,
)
from ..decorators import handle_mongo_exceptions
from ..schemas.users import User
from ..services.auth import get_current_user
from ..services.permissions import (
    check_permission_to_question_group,
    check_permission_to_take_question_group,
)
from ..services.validate_questions import validate_questions, ValidateException
from ..schemas.questions import (
    QuestionGroup,
    CreateQuestionGroup,
    UpdateQuestionGroup,
    QuestionGroupResult,
    FullQuestionGroup,
    MinimalQuestionGroup,
    ValidateQuestionGroup,
)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/groups", response_model=list[MinimalQuestionGroup])
def list_question_groups_view():
    return get_all_question_groups()


@router.post(
    "/groups", response_model=FullQuestionGroup, status_code=status.HTTP_201_CREATED
)
def create_question_group_view(
    question: CreateQuestionGroup, user: User = Depends(get_current_user)
):
    return create_question_group(question, user.id)


@router.get("/group/{group_id}", response_model=QuestionGroup)
@handle_mongo_exceptions
def question_group_view(group_id: str, user: User = Depends(get_current_user)):
    check_permission_to_question_group(user.id, group_id, "view")
    return get_question_group(group_id)


@router.get("/group/{group_id}/full-access", response_model=FullQuestionGroup)
@handle_mongo_exceptions
def question_group_full_view(group_id: str, user: User = Depends(get_current_user)):
    check_permission_to_question_group(user.id, group_id, "full-access")
    return get_question_group(group_id)


@router.put("/group/{group_id}")
@handle_mongo_exceptions
def update_question_group_view(
    group_id: str, question: UpdateQuestionGroup, user: User = Depends(get_current_user)
):
    check_permission_to_question_group(user.id, group_id, "update")
    update_question_group(group_id, question)


@router.delete("/group/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_mongo_exceptions
def delete_question_group_view(group_id: str, user: User = Depends(get_current_user)):
    check_permission_to_question_group(user.id, group_id, "delete")
    delete_question_group(group_id)


@router.post("/validate", response_model=QuestionGroupResult)
@handle_mongo_exceptions
def validate_question_group_view(
    question_group_data: ValidateQuestionGroup, user: User = Depends(get_current_user)
):
    """
    Проверяет переданную пользователем группу вопросов (тест).
    Если за последний час пользователь уже проходил данный тест, то вернется ошибка `403`.
    """
    check_permission_to_take_question_group(
        user_id=user.id, question_group_id=question_group_data.id
    )
    try:
        validated_question_group = validate_questions(question_group_data)
    except ValidateException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    else:
        create_passed_question(user_id=user.id, question_group=validated_question_group)
        return validated_question_group

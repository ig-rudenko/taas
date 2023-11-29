from fastapi import APIRouter, HTTPException
from starlette import status

from ..crud import (
    get_all_question_groups,
    get_question_group,
    create_question_group,
    update_question_group,
    delete_question_group,
)
from ..decorators import handle_mongo_exceptions
from ..service.validate_questions import validate_questions, ValidateException
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
def create_question_group_view(question: CreateUpdateQuestionGroup):
    return create_question_group(question)


@router.get("/group/{group_id}", response_model=QuestionGroup)
@handle_mongo_exceptions
def question_group_view(group_id: str):
    return get_question_group(group_id)


@router.put("/group/{group_id}")
@handle_mongo_exceptions
def update_question_group_view(group_id: str, question: CreateUpdateQuestionGroup):
    update_question_group(group_id, question)


@router.delete("/group/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_mongo_exceptions
def delete_question_group_view(group_id: str):
    delete_question_group(group_id)


@router.post("/validate", response_model=QuestionGroupResult)
@handle_mongo_exceptions
def validate_question_group_view(question_group_data: FullQuestionGroup):
    try:
        return validate_questions(question_group_data)
    except ValidateException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

from datetime import datetime, timedelta
from typing import Literal

from bson import ObjectId
from fastapi import HTTPException
from starlette import status

from ..mongo import mongodb, DoesNotExistError
from ..mongo.passed_questions_crud import get_last_passed_question
from ..mongo.questions_crud import get_question_group


async def check_permission_to_question_group(
    user_id: str,
    question_group_id: str,
    action: Literal["view", "update", "delete", "full-access"],
) -> None:
    """
    Проверка полномочий пользователя взаимодействовать с группой вопросов (тестом).
    :param user_id: Идентификатор пользователя.
    :param question_group_id: Идентификатор группы вопросов (теста).
    :param action: Название действия.
    """
    if action == "view":
        await check_permission_to_take_question_group(user_id, question_group_id)
        return

    result = await mongodb.questions_collection.find_one(
        {"_id": ObjectId(question_group_id)}, {"user_id": 1}
    )
    if result is None:
        raise DoesNotExistError

    if not str(result.get("user_id")) == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not have permission to {action} this question group.",
        )


async def check_permission_to_take_question_group(
    user_id: str, question_group_id: str
) -> None:
    """
    Проверка права на получение пользователем группы вопросов (теста).
    Проходить тест можно только раз в час.
    :param user_id: Идентификатор пользователя.
    :param question_group_id: Идентификатор группы вопросов (теста).
    """
    try:
        last = await get_last_passed_question(
            user_id=user_id, question_group_id=question_group_id
        )
    except DoesNotExistError:
        pass

    else:
        question_group = await get_question_group(question_group_id)
        if (
            question_group.timeout_minutes
            and last.created_at
            > datetime.now() - timedelta(minutes=question_group.timeout_minutes)
        ):
            time_elapsed = last.created_at - (
                datetime.now() - timedelta(minutes=question_group.timeout_minutes)
            )
            seconds = time_elapsed.total_seconds()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Данный тест повторно вы сможете пройти через"
                f" {int(seconds / 60)} мин. {int(seconds % 60)} c.",
            )

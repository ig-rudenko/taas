from datetime import datetime, timedelta

from fastapi import HTTPException
from starlette import status

from app.mongo.questions_crud import get_question_group
from app.schemas.questions import FullQuestionGroup
from app.schemas.users import User
from app.services.cache import CacheService


async def get_testing_group(user: User, group_id: str) -> dict:
    group = await get_question_group(group_id)

    group_data = group.model_dump(by_alias=True)
    # Если для теста нет ограничения по времени.
    if group.completion_time_minutes == 0:
        group_data["completionTimeMinutes"] = -1
        return group_data

    cache_key = _get_cache_key(user, group_id)

    test_started_data = await CacheService().get(cache_key)
    if test_started_data is None:
        await CacheService().set(
            cache_key,
            _create_started_test_data(group),
            expire=group.timeout_minutes * 60 + group.completion_time_minutes * 60,
        )
        group_data["completionTimeSeconds"] = group.completion_time_minutes * 60
        return group_data

    else:
        await validate_question_group_time_not_expired(user, group_id)
        group_data["completionTimeSeconds"] = int(
            (test_started_data["expired"] - datetime.now()).total_seconds()
        )
        return group_data


async def validate_question_group_time_not_expired(user: User, group_id: str) -> None:
    group = await get_question_group(group_id)
    if group.completion_time_minutes == 0:
        return

    cache_key = _get_cache_key(user, group_id)
    test_started_data = await CacheService().get(cache_key)
    if test_started_data is not None and test_started_data["expired"] <= datetime.now():
        time_elapsed: timedelta = test_started_data["next_try"] - datetime.now()
        seconds = time_elapsed.total_seconds()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Данный тест повторно вы сможете пройти через"
            f" {int(seconds / 60)} мин. {int(seconds % 60)} c.",
        )


def _create_started_test_data(group: FullQuestionGroup) -> dict:
    return {
        "time_start": datetime.now(),
        "expired": datetime.now() + timedelta(minutes=group.completion_time_minutes),
        "next_try": datetime.now()
        + timedelta(minutes=group.timeout_minutes + group.completion_time_minutes),
    }


def _get_cache_key(user: User, group_id: str) -> str:
    return f"start_test:user:{user.id}:question_group:{group_id}"

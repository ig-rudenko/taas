from datetime import datetime, timedelta

from app.schemas.open_questions import OpenQuestionSchema
from app.schemas.questions import FullQuestionGroup
from app.schemas.users import User
from app.services.cache import CacheService


def _get_cache_key(user: User) -> str:
    return f"{user.id}:open_questions"


async def set_question_group_is_open(user: User, group: FullQuestionGroup) -> None:
    """
    Отмечает в кеше, что пользователь начал проходить тест.
    """
    cache = CacheService()
    now = datetime.now().astimezone()
    timeout_seconds = group.timeout_minutes * 60 + group.completion_time_minutes * 60

    data = OpenQuestionSchema(
        startTime=now,
        expireTime=now + timedelta(minutes=group.completion_time_minutes),
        nextTryTime=now + timedelta(seconds=timeout_seconds),
        finishedTime=None,
    )

    open_questions: dict[str, OpenQuestionSchema] | None = await cache.get(_get_cache_key(user))
    if open_questions is None:
        # Если еще нет в кеше, то создаем новый.
        await cache.set(_get_cache_key(user), {group.id: data}, expire=timeout_seconds)

    else:
        # Если уже были другие тесты, то добавляем этот тест в кеш.
        open_questions[group.id] = data
        await cache.set(_get_cache_key(user), open_questions, expire=timeout_seconds)


async def set_question_group_is_finished(user: User, group: FullQuestionGroup) -> None:
    """
    Отмечает в кеше, что пользователь завершил проходить тест.
    """
    cache = CacheService()
    now = datetime.now().astimezone()
    timeout_seconds = group.timeout_minutes * 60 + group.completion_time_minutes * 60

    open_questions: dict[str, OpenQuestionSchema] | None = await cache.get(_get_cache_key(user))
    if open_questions is None or group.id not in open_questions:
        return

    open_questions[group.id].finished_time = now
    await cache.set(_get_cache_key(user), open_questions, expire=timeout_seconds)


async def get_user_open_question_groups(user: User) -> dict[str, OpenQuestionSchema]:
    """Возвращает все тесты (из кеша), которые пользователь проходил недавно."""
    cache = CacheService()
    open_questions: dict[str, OpenQuestionSchema] | None = await cache.get(_get_cache_key(user))
    if open_questions is None:
        return {}
    return open_questions

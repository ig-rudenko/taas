from datetime import datetime, timedelta

import pymongo
from bson import ObjectId

from .mongo import mongodb, DoesNotExistError
from ..schemas.questions import QuestionGroupResult
from ..schemas.passed_questions import PassedQuestion, PassedQuestionsDetail


async def get_last_passed_question(
    user_id: str, question_group_id: str
) -> PassedQuestion:
    """
    Возвращает последний результат прохождения группы вопросов (теста).
    :param user_id: Идентификатор пользователя.
    :param question_group_id: Идентификатор группы вопросов (теста).
    """
    record = await mongodb.passed_questions.find_one(
        {
            "user_id": ObjectId(user_id),
            "question_group_id": ObjectId(question_group_id),
        },
        sort=[("created_at", pymongo.DESCENDING)],
    )
    if record is None:
        raise DoesNotExistError
    record = _format_passed_question(record)
    return PassedQuestion(**record)


async def get_passed_question(_id: str) -> PassedQuestion:
    record = await mongodb.passed_questions.find_one({"_id": ObjectId(_id)})
    record = _format_passed_question(record)
    return PassedQuestion(**record)


async def get_user_passed_question_list(user_id: str) -> list[PassedQuestionsDetail]:
    """
    Возвращает список всех решений пользователем групп вопросов (теста).
    Сортировка от новых записей к первым.
    """

    pipeline = [
        {
            "$lookup": {
                "from": "questions",
                "localField": "question_group_id",
                "foreignField": "_id",
                "as": "question_group_data"
            }
        },
        {
            "$unwind": "$question_group_data"
        },
        {
            "$match": {"user_id": ObjectId(user_id)}
        },
        {
            "$sort": {"created_at": pymongo.DESCENDING}
        },
        {
            "$project": {
                "_id": 1,
                "question_group_id": 1,
                "user_id": 1,
                "created_at": 1,
                "total_score": 1,
                "user_score": 1,
                "question_group_name": "$question_group_data.name"
            }
        }
    ]

    records = mongodb.passed_questions.aggregate(pipeline)

    return [PassedQuestionsDetail(**_format_passed_question(r)) async for r in records]


async def create_passed_question(
    user_id: str, question_group: QuestionGroupResult
) -> PassedQuestion:
    """
    Создает новую запись о прохождении пользователем группы вопросов (теста).
    :param user_id: Идентификатор пользователя.
    :param question_group: Проверенная группа вопросов (тестов).
    :return: Запись результата прохождения.
    """
    data = {
        "user_id": ObjectId(user_id),
        "question_group_id": ObjectId(question_group.id),
        "created_at": datetime.now(),
        "total_score": question_group.total_score,
        "user_score": question_group.user_score,
    }
    result = await mongodb.passed_questions.insert_one(data)
    return await get_passed_question(result.inserted_id)


def _format_passed_question(record):
    record["_id"] = str(record["_id"])
    record["user_id"] = str(record["user_id"])
    record["question_group_id"] = str(record["question_group_id"])
    return record

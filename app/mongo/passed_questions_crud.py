from datetime import datetime, timedelta

import pymongo
from bson import ObjectId

from .mongo import mongodb
from ..schemas.questions import QuestionGroupResult
from ..schemas.passed_questions import PassedQuestion


def get_last_passed_question(user_id: str, question_group_id: str) -> PassedQuestion:
    """
    Возвращает последний результат прохождения группы вопросов (теста).
    :param user_id: Идентификатор пользователя.
    :param question_group_id: Идентификатор группы вопросов (теста).
    """
    record = mongodb.passed_questions.find_one(
        {
            "user_id": ObjectId(user_id),
            "question_group_id": ObjectId(question_group_id),
        },
        sort=[("created_at", pymongo.DESCENDING)],
    )
    record = _format_passed_question(record)
    return record


def get_passed_question(_id: str) -> PassedQuestion:
    record = mongodb.passed_questions.find_one({"id": ObjectId(_id)})
    record = _format_passed_question(record)
    return PassedQuestion(**record)


def get_user_passed_question_list(
    user_id: str, question_group_id: str
) -> list[PassedQuestion]:
    """
    Возвращает список всех решений пользователем конкретной группы вопросов (теста).
    Сортировка от новых записей к первым.
    """
    records = mongodb.passed_questions.find(
        {"user_id": ObjectId(user_id), "question_group_id": ObjectId(question_group_id)}
    ).sort("created_at", pymongo.DESCENDING)
    formatted_records = []
    for record in records:
        record = _format_passed_question(record)
        formatted_records.append(PassedQuestion(**record))
    return formatted_records


def create_passed_question(
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
    inserted_id = mongodb.passed_questions.insert_one(data).inserted_id
    return get_passed_question(inserted_id)


def _format_passed_question(record):
    record["_id"] = str(record["_id"])
    record["user_id"] = str(record["user_id"])
    record["question_group_id"] = str(record["question_group_id"])
    return record

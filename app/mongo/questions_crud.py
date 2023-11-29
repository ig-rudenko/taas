from bson import ObjectId

from app.mongo import mongodb, DoesNotExistError
from app.schemas.questions import CreateUpdateQuestionGroup


def get_all_question_groups(limit: int = 100) -> list[dict]:
    result = []
    records = mongodb.questions_collection.find({}, {"_id": 1, "name": 1}).limit(limit)
    for question in records:
        question["_id"] = str(question["_id"])
        result.append(question)
    return result


def get_question_group(group_id: str) -> dict:
    question_group = mongodb.questions_collection.find_one({"_id": ObjectId(group_id)})
    if question_group is None:
        raise DoesNotExistError("Question group does not exist")
    question_group["_id"] = str(question_group["_id"])
    question_group["user_id"] = str(question_group["user_id"])
    return question_group


def create_question_group(
    question_group: CreateUpdateQuestionGroup, user_id: str
) -> dict:
    data = question_group.model_dump()
    data.update({"user_id": ObjectId(user_id)})

    inserted_id = mongodb.questions_collection.insert_one(data).inserted_id
    return get_question_group(inserted_id)


def update_question_group(
    group_id: str, question_group: CreateUpdateQuestionGroup
) -> None:
    matched_count = mongodb.questions_collection.update_one(
        filter={"_id": ObjectId(group_id)},
        update={"$set": question_group.model_dump()},
    ).matched_count
    if matched_count == 0:
        raise DoesNotExistError("Question group does not exist")


def delete_question_group(group_id: str) -> None:
    deleted_count = mongodb.questions_collection.delete_one(
        {"_id": ObjectId(group_id)}
    ).deleted_count
    if deleted_count == 0:
        raise DoesNotExistError("Question group does not exist")

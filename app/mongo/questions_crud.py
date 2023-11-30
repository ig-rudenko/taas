from bson import ObjectId

from app.mongo import mongodb, DoesNotExistError
from app.schemas.questions import (
    CreateQuestionGroup,
    UpdateQuestionGroup,
    MinimalQuestionGroup,
)


def get_all_question_groups(filter_=None) -> list[MinimalQuestionGroup]:
    if filter_ is None:
        filter_ = {}

    result = []
    records = mongodb.questions_collection.find(
        filter_,
        {
            "_id": 1,
            "name": 1,
            "user_id": 1,
            "tags": 1,
            "created_at": 1,
            "updated_at": 1,
        },
    )
    for question in records:
        question["_id"] = str(question["_id"])
        question["user_id"] = str(question["user_id"])
        result.append(question)
    return result


def get_question_group(group_id: str) -> dict:
    question_group = mongodb.questions_collection.find_one({"_id": ObjectId(group_id)})
    if question_group is None:
        raise DoesNotExistError("Question group does not exist")
    question_group["_id"] = str(question_group["_id"])
    question_group["user_id"] = str(question_group["user_id"])
    return question_group


def create_question_group(question_group: CreateQuestionGroup, user_id: str) -> dict:
    data = question_group.model_dump()
    data.update({"user_id": ObjectId(user_id)})

    inserted_id = mongodb.questions_collection.insert_one(data).inserted_id
    return get_question_group(inserted_id)


def update_question_group(group_id: str, question_group: UpdateQuestionGroup) -> None:
    record = get_question_group(group_id)
    new_data = question_group.model_dump()
    new_data.update({"created_at": record["created_at"]})

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

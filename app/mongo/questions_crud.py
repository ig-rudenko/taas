from datetime import datetime

import pymongo
from bson import ObjectId

from app.mongo import mongodb, DoesNotExistError
from app.schemas.questions import (
    CreateQuestionGroup,
    UpdateQuestionGroup,
    MinimalQuestionGroup,
    FullQuestionGroup,
)


async def get_all_question_groups(filter_=None) -> list[MinimalQuestionGroup]:
    if filter_ is None:
        filter_ = {}

    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "userId",
                "foreignField": "_id",
                "as": "userData",
            }
        },
        {"$unwind": "$userData"},
        {"$match": filter_},
        {"$sort": {"createdAt": pymongo.DESCENDING}},
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "userId": 1,
                "tags": 1,
                "description": 1,
                "createdAt": 1,
                "updatedAt": 1,
                "timeoutMinutes": 1,
                "completionTimeMinutes": 1,
                "username": "$userData.username",
            }
        },
    ]

    result = []

    async for question in mongodb.questions_collection.aggregate(pipeline):
        question["_id"] = str(question["_id"])
        question["userId"] = str(question["userId"])
        result.append(question)
    return result


async def get_question_group(group_id: str) -> FullQuestionGroup:
    question_group = await mongodb.questions_collection.find_one(
        {"_id": ObjectId(group_id)}
    )
    if question_group is None:
        raise DoesNotExistError("Question group does not exist")
    question_group["_id"] = str(question_group["_id"])
    question_group["userId"] = str(question_group["userId"])
    return FullQuestionGroup(**question_group)


async def create_question_group(
    question_group: CreateQuestionGroup, user_id: str
) -> FullQuestionGroup:
    data = question_group.model_dump(by_alias=True)
    data.update({"userId": ObjectId(user_id)})
    data.update({"createdAt": datetime.now()})
    data.update({"updatedAt": datetime.now()})

    result = await mongodb.questions_collection.insert_one(data)
    return await get_question_group(result.inserted_id)


async def update_question_group(
    group_id: str, question_group: UpdateQuestionGroup
) -> None:
    record = await get_question_group(group_id)
    new_data = question_group.model_dump(by_alias=True)
    new_data.update({"createdAt": record.created_at})
    new_data.update({"updatedAt": datetime.now()})

    result = await mongodb.questions_collection.update_one(
        filter={"_id": ObjectId(group_id)},
        update={"$set": new_data},
    )
    if result.matched_count == 0:
        raise DoesNotExistError("Question group does not exist")


async def delete_question_group(group_id: str) -> None:
    result = await mongodb.questions_collection.delete_one({"_id": ObjectId(group_id)})
    if result.deleted_count == 0:
        raise DoesNotExistError("Question group does not exist")

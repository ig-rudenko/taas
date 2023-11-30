from bson import ObjectId

from ..mongo import mongodb, DoesNotExistError


def has_permission_to_question_group(user_id: str, question_group_id: str) -> bool:
    result = mongodb.questions_collection.find_one(
        {"_id": ObjectId(question_group_id)}, {"user_id": 1}
    )
    if result is None:
        raise DoesNotExistError

    return str(result.get("user_id")) == user_id

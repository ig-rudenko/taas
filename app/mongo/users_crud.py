from bson import ObjectId

from ..schemas.users import User, CreateUser
from ..services.encrypt import encrypt_password
from .mongo import mongodb, DoesNotExistError


def get_user(**kwargs) -> User:
    if kwargs.get("_id") is not None:
        kwargs["_id"] = ObjectId(kwargs["_id"])

    user_data = mongodb.users_collection.find_one(kwargs)
    if user_data is None:
        raise DoesNotExistError
    user_data["_id"] = str(user_data["_id"])
    return User(**user_data)


def create_user(user: CreateUser) -> User:
    user.password = encrypt_password(user.password)
    inserted_id = mongodb.users_collection.insert_one(user.model_dump()).inserted_id
    return get_user(_id=inserted_id)

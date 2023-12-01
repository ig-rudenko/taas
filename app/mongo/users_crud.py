from bson import ObjectId

from ..schemas.users import User, CreateUser
from ..services.encrypt import encrypt_password
from .mongo import mongodb, DoesNotExistError


async def get_user(**kwargs) -> User:
    if kwargs.get("_id") is not None:
        kwargs["_id"] = ObjectId(kwargs["_id"])

    user_data = await mongodb.users_collection.find_one(kwargs)
    if user_data is None:
        raise DoesNotExistError
    user_data["_id"] = str(user_data["_id"])
    return User(**user_data)


async def create_user(user: CreateUser) -> User:
    user.password = encrypt_password(user.password)
    result = await mongodb.users_collection.insert_one(user.model_dump())
    return await get_user(_id=result.inserted_id)

from bson import ObjectId

from .mongo import mongodb, DoesNotExistError
from ..schemas.users import User, CreateUser, UpdateUser
from ..services.encrypt import encrypt_password


async def get_all_raw_users() -> list:
    users = []
    async for user in mongodb.users_collection.find():
        user['_id'] = str(user['_id'])
        users.append(user)
    return users


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
    user_data = user.model_dump()
    user_data.update({"is_superuser": False, "can_create_tests": False})
    result = await mongodb.users_collection.insert_one(user_data)
    return await get_user(_id=result.inserted_id)


async def update_user(user_id: str, new_data: UpdateUser) -> None:
    result = await mongodb.users_collection.update_one(
        filter={"_id": ObjectId(user_id)},
        update={"$set": new_data.model_dump()},
    )
    if result.matched_count == 0:
        raise DoesNotExistError("User does not exist")


async def change_user_password(user_id: str, new_password: str) -> None:
    result = await mongodb.users_collection.update_one(
        filter={"_id": ObjectId(user_id)},
        update={"$set": {"password": encrypt_password(new_password)}},
    )
    if result.matched_count == 0:
        raise DoesNotExistError("User does not exist")

from functools import wraps

from bson.errors import InvalidId
from fastapi import HTTPException
from starlette import status

from app.mongo import DoesNotExistError


def handle_mongo_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DoesNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except InvalidId as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return wrapper

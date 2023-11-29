from fastapi import APIRouter

from ..mongo.users_crud import get_user
from ..schemas.users import MinimalUser


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=MinimalUser)
def get_user_view(user_id: str):
    return get_user(_id=user_id)

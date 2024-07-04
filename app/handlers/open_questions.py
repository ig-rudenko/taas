from fastapi import APIRouter, Depends

from app.schemas.open_questions import OpenQuestionSchema
from app.schemas.users import User
from app.services.auth import get_current_user
from app.services.open_questions import get_user_open_question_groups

router = APIRouter(prefix="/open_questions", tags=["open_questions"])


@router.get("/", response_model=dict[str, OpenQuestionSchema])
async def get_open_questions(user: User = Depends(get_current_user)):
    return await get_user_open_question_groups(user)

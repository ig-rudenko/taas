from datetime import datetime

from pydantic import BaseModel


class PassedQuestion(BaseModel):
    user_id: str
    question_group_id: str
    created_at: datetime
    total_score: int
    user_score: int

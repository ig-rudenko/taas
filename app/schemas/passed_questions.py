from datetime import datetime

from pydantic import BaseModel, Field


class PassedQuestion(BaseModel):
    user_id: str = Field(..., alias="userId")
    question_group_id: str = Field(..., alias="questionGroupId")
    created_at: datetime = Field(..., alias="createdAt")
    total_score: int = Field(..., alias="totalScore")
    user_score: int = Field(..., alias="userScore")


class PassedQuestionsDetail(PassedQuestion):
    question_group_name: str = Field(..., alias="questionGroupName")

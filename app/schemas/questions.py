from datetime import datetime

from pydantic import BaseModel, Field


class Answer(BaseModel):
    text: str = Field(..., max_length=1024)


class FullAnswer(Answer):
    is_valid: bool = Field(default=False)


class AnswerResul(Answer):
    is_valid: bool
    true_valid: bool


class Question(BaseModel):
    text: str = Field(..., max_length=2048)
    answers: list[Answer]
    image: str = Field(default="", max_length=1024)


class ValidateQuestion(Question):
    answers: list[FullAnswer]


class FullQuestion(Question):
    answers: list[FullAnswer]
    explanation: str = Field(default="", max_length=2048)


class QuestionResult(FullQuestion):
    answers: list[AnswerResul]


class QuestionGroupToPass(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    questions: list[Question]
    description: str
    completion_time_seconds: int = Field(
        default=0, description="Время для прохождения теста"
    )


class UpdateQuestionGroup(BaseModel):
    name: str = Field(..., max_length=256)
    tags: list[str]
    questions: list[FullQuestion]
    description: str = Field(default="", max_length=2048)
    timeout_minutes: int = Field(
        default=0, description="Время для повторного прохождения"
    )
    completion_time_minutes: int = Field(
        default=0, description="Время для прохождения теста"
    )


class CreateQuestionGroup(UpdateQuestionGroup):
    pass


class FullQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    user_id: str
    tags: list[str]
    questions: list[FullQuestion]
    description: str
    timeout_minutes: int = Field(
        default=0, description="Время для повторного прохождения"
    )
    completion_time_minutes: int = Field(
        default=0, description="Время для прохождения теста"
    )
    created_at: datetime
    updated_at: datetime


class ValidateQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    questions: list[ValidateQuestion]


class MinimalQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    user_id: str
    username: str
    description: str
    created_at: datetime
    updated_at: datetime
    timeout_minutes: int = Field(..., description="Время для повторного прохождения")
    completion_time_minutes: int = Field(..., description="Время для прохождения теста")
    tags: list[str]


class QuestionGroupResult(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    tags: list[str]
    description: str
    timeout_minutes: int = Field(..., description="Время для повторного прохождения")
    completion_time_minutes: int = Field(..., description="Время для прохождения теста")
    created_at: datetime
    updated_at: datetime
    questions: list[QuestionResult]
    total_score: int
    user_score: int

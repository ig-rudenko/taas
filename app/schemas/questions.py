from datetime import datetime

from pydantic import BaseModel, Field


class Answer(BaseModel):
    text: str = Field(..., max_length=1024)


class FullAnswer(Answer):
    is_valid: bool = Field(default=False, alias="isValid")


class AnswerResul(Answer):
    is_valid: bool = Field(default=False, alias="isValid")
    true_valid: bool = Field(default=False, alias="trueValid")


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
        default=0,
        description="Время для прохождения теста",
        alias="completionTimeSeconds",
    )


class UpdateQuestionGroup(BaseModel):
    name: str = Field(..., max_length=256)
    tags: list[str]
    questions: list[FullQuestion]
    description: str = Field(default="", max_length=2048)
    timeout_minutes: int = Field(
        default=0,
        description="Время для повторного прохождения",
        alias="timeoutMinutes",
    )
    completion_time_minutes: int = Field(
        default=0,
        description="Время для прохождения теста",
        alias="completionTimeMinutes",
    )


class CreateQuestionGroup(UpdateQuestionGroup):
    pass


class FullQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    user_id: str = Field(..., alias="userId")
    tags: list[str]
    questions: list[FullQuestion]
    description: str
    timeout_minutes: int = Field(
        default=0,
        description="Время для повторного прохождения",
        alias="timeoutMinutes",
    )
    completion_time_minutes: int = Field(
        default=0,
        description="Время для прохождения теста",
        alias="completionTimeMinutes",
    )
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class ValidateQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    questions: list[ValidateQuestion]


class MinimalQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    user_id: str = Field(..., alias="userId")
    username: str
    description: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    timeout_minutes: int = Field(
        ...,
        description="Время для повторного прохождения",
        alias="timeoutMinutes",
    )
    completion_time_minutes: int = Field(
        ...,
        description="Время для прохождения теста",
        alias="completionTimeMinutes",
    )
    tags: list[str]


class QuestionGroupResult(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    tags: list[str]
    description: str
    timeout_minutes: int = Field(
        ..., description="Время для повторного прохождения", alias="timeoutMinutes"
    )
    completion_time_minutes: int = Field(
        ..., description="Время для прохождения теста", alias="completionTimeMinutes"
    )
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    questions: list[QuestionResult]
    total_score: int = Field(..., alias="totalScore")
    user_score: int = Field(..., alias="userScore")

from datetime import datetime

from pydantic import BaseModel, Field


class Answer(BaseModel):
    text: str


class CreateAnswer(Answer):
    is_valid: bool = Field(default=False)


class AnswerStatus(Answer):
    is_valid: bool
    true_valid: bool


class Question(BaseModel):
    text: str
    answers: list[Answer]
    image: str = Field(default="")


class QuestionStatus(BaseModel):
    text: str
    answers: list[AnswerStatus]
    image: str = Field(default="")
    explanation: str = Field(default="")


class CreateQuestion(Question):
    explanation: str = Field(default="")
    answers: list[CreateAnswer]


class QuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    user_id: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    questions: list[Question]


class UpdateQuestionGroup(BaseModel):
    name: str
    tags: list[str]
    questions: list[CreateQuestion]
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Название группы тестов",
                "tags": ["python", "easy"],
                "questions": [
                    {
                        "text": "Описание вопроса",
                        "image": "https://www.example.com/images/img.png",
                        "answers": [
                            {"text": "Вариант ответа 1", "is_valid": True},
                            {"text": "Вариант ответа 2"},
                        ],
                        "explanation": "Объяснение верного ответа.",
                    }
                ],
            }
        }


class CreateQuestionGroup(UpdateQuestionGroup):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class FullQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    user_id: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    questions: list[CreateQuestion]


class ValidateQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    questions: list[Question]


class MinimalQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    tags: list[str]


class QuestionGroupResult(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    questions: list[QuestionStatus]
    total_score: int
    user_score: int

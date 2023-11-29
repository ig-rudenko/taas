import uuid

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
    explanation: str = Field(default="")


class QuestionStatus(BaseModel):
    text: str
    answers: list[AnswerStatus]
    image: str = Field(default="")
    explanation: str = Field(default="")


class CreateQuestion(Question):
    answers: list[CreateAnswer]


class QuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    questions: list[Question]


class CreateUpdateQuestionGroup(BaseModel):
    name: str
    questions: list[CreateQuestion]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Название группы тестов",
                "questions": [
                    {
                        "text": "Описание вопроса",
                        "answers": [{"text": "Вариант ответа", "is_valid": True}],
                        "image": "https://www.example.com/images/img.png",
                        "explanation": "Объяснение верного ответа.",
                    }
                ],
            }
        }


class FullQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    questions: list[CreateQuestion]


class MinimalQuestionGroup(BaseModel):
    id: str = Field(..., alias="_id")
    name: str


class QuestionGroupResult(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    questions: list[QuestionStatus]
    total_score: int
    user_score: int

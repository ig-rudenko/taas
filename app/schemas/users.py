from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator


class CreateUser(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    email: EmailStr
    surname: str = Field(default="", max_length=100)
    first_name: str = Field(default="", max_length=100)
    last_name: str = Field(default="", max_length=100)
    registration_date: datetime = Field(default_factory=datetime)

    @field_validator("username")
    def username_alphanumeric(cls, v):
        """
        Проверка, что username состоит только из буквенно-цифровых символов.
        """
        if not v.isalnum():
            raise ValueError("Must be alphanumeric")
        return v

    @field_validator("password")
    def password_length(cls, v):
        """
        Проверка, что пароль имеет длину не менее 8 символов.
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("registration_date")
    def set_registration_date(cls, v):
        """
        Установка даты регистрации на текущую дату при создании пользователя.
        """
        return v or datetime.now()


class User(CreateUser):
    id: str = Field(..., alias="_id")


class MinimalUser(BaseModel):
    username: str
    email: EmailStr
    surname: str
    first_name: str
    last_name: str

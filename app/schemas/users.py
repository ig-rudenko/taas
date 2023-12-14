from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator


class UpdateUser(BaseModel):
    surname: str = Field(default="", max_length=100)
    first_name: str = Field(default="", max_length=100, alias="firstName")
    last_name: str = Field(default="", max_length=100, alias="lastName")


class Password(BaseModel):
    password: str = Field(..., max_length=100)

    @field_validator("password")
    def password_length(cls, v):
        """
        Проверка, что пароль имеет длину не менее 8 символов.
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class CreateUser(Password):
    username: str = Field(..., max_length=100)
    surname: str = Field(default="", max_length=100)
    first_name: str = Field(default="", max_length=100, alias="firstName")
    last_name: str = Field(default="", max_length=100, alias="lastName")
    email: EmailStr
    registration_date: datetime = Field(
        default_factory=datetime.now, alias="registrationDate"
    )

    @field_validator("username")
    def username_alphanumeric(cls, v):
        """
        Проверка, что username состоит только из буквенно-цифровых символов.
        """
        if not v.isalnum():
            raise ValueError("Must be alphanumeric")
        return v

    @field_validator("registration_date")
    def set_registration_date(cls, v):
        """
        Установка даты регистрации на текущую дату при создании пользователя.
        """
        return v or datetime.now()


class User(CreateUser):
    id: str = Field(..., alias="_id")
    is_superuser: bool = Field(..., alias="isSuperuser")
    can_create_tests: bool = Field(..., alias="canCreateTests")


class UserCredentials(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)


class MinimalUser(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    surname: str
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    registration_date: datetime = Field(..., alias="registrationDate")


class SelfUser(MinimalUser):
    email: EmailStr
    is_superuser: bool = Field(..., alias="isSuperuser")
    can_create_tests: bool = Field(..., alias="canCreateTests")

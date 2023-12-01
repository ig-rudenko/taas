import pytest
from httpx import AsyncClient

from app.main import app, startup_mongo
from app.mongo.mongo import mongodb
from app.services.encrypt import validate_password
from app.handlers.questions import router


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        app.include_router(router)
        yield client


async def clear_db():
    await mongodb.users_collection.drop()
    await mongodb.questions_collection.drop()
    await mongodb.passed_questions.drop()
    mongodb.shutdown()


@pytest.mark.asyncio
async def test_create_user_invalid_data(client):
    client = await anext(client)
    url = "/api/v1/auth/register"

    # Нет email
    response = await client.post(url, json={"username": "igor", "password": "password"})
    assert response.status_code == 422

    # Неверный email
    response = await client.post(url, json={"email": "123123", "password": "password"})
    assert response.status_code == 422

    # Нет password
    response = await client.post(url, json={"username": "igor"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user(client):
    client = await anext(client)
    user_data = {
        "username": "igor",
        "password": "password",
        "email": "igor@email.com",
        "first_name": "igor",
        "surname": "igor_surname",
        "last_name": "igor_lastname",
    }
    url = "/api/v1/auth/register"

    try:
        startup_mongo()

        response = await client.post(url, json=user_data)
        response_data = response.json()

        assert response.status_code == 201, "Response should be 201"
        assert (
            response_data.get("registration_date") is not None
        ), "Не вернулась дата регистрации пользователя `registration_date`"

        db_user = await mongodb.users_collection.find_one({"username": "igor"})
        assert db_user is not None, "Пользователь не добавился в mongodb"

        # Проверяем правильность переданных полей
        for attr in user_data.keys():
            if attr == "password":
                assert validate_password(
                    user_data[attr], db_user[attr]
                ), "Пароль должен быть зашифрован"
            else:
                assert user_data[attr] == db_user[attr]

    finally:
        await clear_db()


@pytest.mark.asyncio
async def test_get_jwt(client):
    client = await anext(client)
    user_data = {
        "username": "igor",
        "password": "password",
        "email": "igor@email.com",
    }
    try:
        startup_mongo()

        await client.post("/api/v1/auth/register", json=user_data)
        response = await client.post("/api/v1/auth/token", json=user_data)
        assert response.status_code == 200, "Response should be 200"

        tokens = response.json()

        assert tokens.get("accessToken") is not None, "Не вернулся access token."
        assert tokens.get("refreshToken") is not None, "Не вернулся refresh token."

    finally:
        await clear_db()


@pytest.mark.asyncio
async def test_refresh_token(client):
    client = await anext(client)
    user_data = {
        "username": "igor",
        "password": "password",
        "email": "igor@email.com",
    }
    try:
        startup_mongo()

        await client.post("/api/v1/auth/register", json=user_data)
        response = await client.post("/api/v1/auth/token", json=user_data)
        tokens = response.json()
        response = await client.post(
            "/api/v1/auth/token/refresh",
            json={"refreshToken": tokens.get("refreshToken")},
        )
        assert response.status_code == 200, "Response should be 200"

        new_token = response.json()

        assert new_token.get("accessToken") is not None, "Не вернулся access token."

    finally:
        await clear_db()

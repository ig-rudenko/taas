import os

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo.server_api import ServerApi


class MongoDatabase:
    def __init__(self):
        self._client = None
        self._db = None
        self._questions_collection = None
        self._users_collection = None
        self._passed_questions = None

    def init(self):
        uri = os.environ.get("MONGODB_URI")
        database_name = os.environ.get("MONGODB_DATABASE")
        if uri is None or database_name is None:
            raise Exception(
                "MONGODB_URI and MONGODB_DATABASE environment variables are required"
            )

        # Create a new client and connect to the server
        self._client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
        self._db: AsyncIOMotorDatabase = self._client[database_name]

        self._questions_collection: AsyncIOMotorCollection = self._db.get_collection(
            "questions"
        )
        self._users_collection: AsyncIOMotorCollection = self._db.get_collection(
            "users"
        )
        self._passed_questions: AsyncIOMotorCollection = self._db.get_collection(
            "passed_questions"
        )

    @property
    def questions_collection(self) -> AsyncIOMotorCollection:
        if self._questions_collection is None:
            raise Exception("Questions collection not initialized")
        return self._questions_collection

    @property
    def users_collection(self) -> AsyncIOMotorCollection:
        if self._users_collection is None:
            raise Exception("Users collection not initialized")
        return self._users_collection

    @property
    def passed_questions(self) -> AsyncIOMotorCollection:
        if self._passed_questions is None:
            raise Exception("Passed questions collection not initialized")
        return self._passed_questions

    def shutdown(self):
        if self._client is not None:
            self._client.close()


class DoesNotExistError(Exception):
    pass


mongodb = MongoDatabase()

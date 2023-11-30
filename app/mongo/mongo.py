import os

from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
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

        # Create a new client and connect to the server
        self._client = MongoClient(uri, server_api=ServerApi("1"))
        self._db: Database = self._client.taas

        self._questions_collection: Collection = self._db.get_collection("questions")
        self._users_collection: Collection = self._db.get_collection("users")
        self._passed_questions: Collection = self._db.get_collection("passed_questions")

    @property
    def questions_collection(self) -> Collection:
        if self._questions_collection is None:
            raise Exception("Questions collection not initialized")
        return self._questions_collection

    @property
    def users_collection(self) -> Collection:
        if self._users_collection is None:
            raise Exception("Users collection not initialized")
        return self._users_collection

    @property
    def passed_questions(self) -> Collection:
        if self._passed_questions is None:
            raise Exception("Passed questions collection not initialized")
        return self._passed_questions

    def shutdown(self):
        if self._client is not None:
            self._client.close()


class DoesNotExistError(Exception):
    pass


mongodb = MongoDatabase()

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

    def init(self):
        uri = os.environ.get("MONGODB_URI")

        # Create a new client and connect to the server
        self._client = MongoClient(uri, server_api=ServerApi("1"))
        self._db: Database = self._client.taas

        self._questions_collection: Collection = self._db.get_collection("questions")

    @property
    def questions_collection(self) -> Collection:
        if self._questions_collection is None:
            raise Exception("Questions collection not initialized")
        return self._questions_collection

    def shutdown(self):
        if self._client is not None:
            self._client.close()


class DoesNotExistError(Exception):
    pass


mongodb = MongoDatabase()

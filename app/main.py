from fastapi import FastAPI

from .handlers import questions
from .mongo import mongodb

app = FastAPI()

app.include_router(questions.router)


@app.on_event("startup")
def startup_mongo():
    mongodb.init()


@app.on_event("shutdown")
def startup_mongo():
    mongodb.shutdown()

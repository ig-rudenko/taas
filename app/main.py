from fastapi import FastAPI

from .handlers import questions, auth, users
from .mongo import mongodb

app = FastAPI()

app.include_router(questions.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.on_event("startup")
def startup_mongo():
    mongodb.init()


@app.on_event("shutdown")
def startup_mongo():
    mongodb.shutdown()

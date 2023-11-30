from fastapi import FastAPI

from .handlers import questions, auth, users
from .mongo import mongodb

app = FastAPI(
    title="Tests as a Service",
    version="0.1.0",
)

app.include_router(prefix="/api/v1", router=auth.router)
app.include_router(prefix="/api/v1", router=questions.router)
app.include_router(prefix="/api/v1", router=users.router)


@app.on_event("startup")
def startup_mongo():
    mongodb.init()


@app.on_event("shutdown")
def startup_mongo():
    mongodb.shutdown()

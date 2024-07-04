import os

from fastapi import FastAPI

from .handlers import questions, auth, users, healthcheck, open_questions
from .mongo import mongodb
from .services.cache import CacheService

app = FastAPI(
    title="Tests as a Service",
    version="0.1.0",
    servers=[{"url": "http://localhost:8000", "description": "Development Server"}],
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(prefix="/api/v1", router=auth.router)
app.include_router(prefix="/api/v1", router=questions.router)
app.include_router(prefix="/api/v1", router=users.router)
app.include_router(prefix="/api/v1", router=open_questions.router)
app.include_router(router=healthcheck.router)


@app.on_event("startup")
def startup_mongo():
    mongo_uri = os.environ.get("MONGODB_URI")
    database_name = os.environ.get("MONGODB_DATABASE")
    if mongo_uri is None or database_name is None:
        raise Exception(
            "MONGODB_URI and MONGODB_DATABASE environment variables are required"
        )
    mongodb.init(mongo_uri, database_name)

    # init cache
    CacheService()


@app.on_event("shutdown")
def shutdown_mongo():
    mongodb.shutdown()

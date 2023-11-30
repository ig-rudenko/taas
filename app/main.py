from fastapi import FastAPI

from .handlers import questions, auth, users, healthcheck
from .mongo import mongodb

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
app.include_router(router=healthcheck.router)


@app.on_event("startup")
def startup_mongo():
    mongodb.init()


@app.on_event("shutdown")
def startup_mongo():
    mongodb.shutdown()

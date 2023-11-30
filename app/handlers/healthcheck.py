from pydantic import BaseModel, Field
from fastapi import APIRouter


router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


class Pong(BaseModel):
    message: str = Field(default="pong")


@router.get("/", response_model=Pong)
def ping():
    return {"message": "pong"}

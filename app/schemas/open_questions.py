from datetime import datetime

from pydantic import BaseModel, Field


class OpenQuestionSchema(BaseModel):
    start_time: datetime = Field(alias="startTime")
    expire_time: datetime = Field(alias="expireTime")
    next_try_time: datetime = Field(alias="nextTryTime")

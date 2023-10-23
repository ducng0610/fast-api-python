"""Train Schemas"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TrainInputModel(BaseModel):
    name: str
    cost: float
    weight: float
    volume: float
    ready_to_book: Optional[bool] = False


class TrainResponseModel(TrainInputModel):
    id: int
    booked_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

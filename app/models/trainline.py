"""Trainline Schemas"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TrainlineInputModel(BaseModel):
    name: str


class TrainlineResponseModel(TrainlineInputModel):
    id: int
    occupied_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

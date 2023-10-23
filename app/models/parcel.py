"""Parcel Schemas"""
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ParcelInputModel(BaseModel):
    weight: float
    volume: float


class ParcelResponseModel(ParcelInputModel):
    id: int
    train_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ParcelFillResponseModel(BaseModel):
    assigned_items: int
    total_cost: float

"""Router for trainline management"""
import logging
from typing import List

from fastapi import APIRouter

from app.db import TrainLine, database
from app.models.trainline import TrainlineInputModel, TrainlineResponseModel

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/trainlines", response_model=List[TrainlineResponseModel])
async def list_trainlines():
    logger.info("Getting all availabel train lines")

    query = TrainLine.select().order_by("name")

    return await database.fetch_all(query)


@router.post(
    "/trainlines", response_model=TrainlineResponseModel, status_code=201
)
async def add_trainline(trainline: TrainlineInputModel):
    logger.info("Adding a new train line")

    request_data = trainline.model_dump()
    request_data.update(occupied_at=None)
    query = TrainLine.insert().values(request_data)
    new_id = await database.execute(query)

    return {**request_data, "id": new_id}

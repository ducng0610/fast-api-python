"""Routers for train management"""
import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from app.db import Train, database
from app.models.train import TrainInputModel, TrainResponseModel

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/trains", response_model=List[TrainResponseModel])
async def list_trains():
    logger.info("Getting all trains")

    query = Train.select().where(Train.c.booked_at == None).order_by("name")

    return await database.fetch_all(query)


@router.get("/trains/{train_id}", response_model=TrainResponseModel)
async def get_train(train_id: int):
    logger.info("Getting train information by id")

    query = Train.select().where(Train.c.id == train_id)
    train = await database.fetch_one(query)

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    return train


@router.post("/trains", response_model=TrainResponseModel, status_code=201)
async def add_train(train: TrainInputModel):
    logger.info("Adding a new train")

    request_data = train.model_dump()
    query = Train.insert().values(request_data)
    new_id = await database.execute(query)

    return {**request_data, "id": new_id}


@router.post(
    "/trains/book",
    response_model=List[TrainResponseModel],
    summary="Book the trains that are filled (Used by Post Master)",
)
async def book_train():
    logger.info("Book trains that are ready")
    query = Train.select().where(
        Train.c.ready_to_book == True,
        Train.c.booked_at == None,
    )
    ready_to_book_trains = await database.fetch_all(query)
    train_ids = [t.id for t in ready_to_book_trains]

    query = (
        Train.update()
        .where(Train.c.id.in_(train_ids))
        .values(
            booked_at=datetime.utcnow(),
        )
    )
    await database.execute(query)
    return await database.fetch_all(
        Train.select().where(Train.c.id.in_(train_ids))
    )

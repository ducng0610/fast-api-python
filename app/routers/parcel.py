"""Routers for parcel management"""
import logging
from typing import List

from fastapi import APIRouter, HTTPException

from app.db import Parcel, Train, database
from app.models.parcel import (
    ParcelFillResponseModel,
    ParcelInputModel,
    ParcelResponseModel,
)
from app.services.parcel_assignment import AssignmentService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/parcels", response_model=List[ParcelResponseModel])
async def list_parcels():
    logger.info("Getting all parcels")

    query = Parcel.select().order_by("id")

    return await database.fetch_all(query)


@router.post("/parcels", response_model=ParcelResponseModel, status_code=201)
async def add_parcel(parcel: ParcelInputModel):
    logger.info("Adding a new parcel")

    request_data = parcel.model_dump()
    query = Parcel.insert().values(request_data)
    new_id = await database.execute(query)

    return {**request_data, "id": new_id}


@router.post(
    "/parcels/fill",
    response_model=ParcelFillResponseModel,
    summary="Fill parcels to trains (Used by Post Master)",
)
async def fill_parcels():
    logger.info("Adding a new parcel")

    parcel_query = (
        Parcel.select().where(Parcel.c.train_id == None).order_by("id")
    )
    parcels = await database.fetch_all(parcel_query)

    train_query = Train.select().where(
        Train.c.ready_to_book == False,
        Train.c.booked_at == None,
    )
    trains = await database.fetch_all(train_query)

    assigned_info, cost = AssignmentService(trains, parcels).process()
    assigned_items = 0

    for train_id, parcel_ids in assigned_info.items():
        q = (
            Parcel.update()
            .where(Parcel.c.id.in_(parcel_ids))
            .values(train_id=train_id)
        )
        await database.execute(q)
        assigned_items += len(parcel_ids)

    await database.execute(
        Train.update()
        .where(Train.c.id.in_([t.id for t in trains]))
        .values(ready_to_book=True)
    )

    return {"assigned_items": assigned_items, "total_cost": cost}

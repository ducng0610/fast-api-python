from datetime import datetime
from typing import Callable
from unittest.mock import Mock, patch

import pytest
from httpx import AsyncClient

from app.db import Parcel, Train, database


@pytest.mark.anyio
async def test_create_parcel(async_client: AsyncClient):
    data = {
        "weight": 200.00,
        "volume": 10.00,
    }
    resp = await async_client.post("/parcels", json=data)
    new_train = resp.json()

    assert resp.status_code == 201
    assert new_train["weight"] == data["weight"]
    assert new_train["volume"] == data["volume"]


@pytest.mark.anyio
async def test_get_all_parcels(
    async_client: AsyncClient, sample_parcel: Callable
):
    parcel1 = await sample_parcel(
        {
            "weight": 500.00,
            "volume": 20.00,
        }
    )
    parcel2 = await sample_parcel(
        {
            "weight": 200.00,
            "volume": 10.00,
        }
    )

    resp = await async_client.get("/parcels")
    data = resp.json()

    assert resp.status_code == 200
    assert len(data) == 2
    assert {
        "id": parcel1.id,
        "weight": 500.00,
        "volume": 20.00,
        "train_id": None,
    } in data
    assert {
        "id": parcel2.id,
        "weight": 200.00,
        "volume": 10.00,
        "train_id": None,
    } in data


@pytest.mark.anyio
@patch("app.routers.parcel.AssignmentService")
async def test_fill_all_parcels(
    mock_svc: Mock,
    async_client: AsyncClient,
    sample_parcel: Callable,
    sample_train: Callable,
):
    train1 = await sample_train(
        {
            "name": "Percy",
            "cost": 120.00,
            "weight": 500.00,
            "volume": 20.00,
            "ready_to_book": True,
            "booked_at": datetime.utcnow(),
        }
    )
    train2 = await sample_train(
        {
            "name": "Thomas",
            "cost": 100.00,
            "weight": 200.00,
            "volume": 10.00,
            "ready_to_book": False,
            "booked_at": None,
        }
    )
    parcel1 = await sample_parcel(
        {
            "weight": 500.00,
            "volume": 20.00,
        }
    )
    parcel2 = await sample_parcel(
        {
            "weight": 200.00,
            "volume": 10.00,
        }
    )
    await sample_parcel(
        {
            "weight": 300.00,
            "volume": 10.00,
            "train_id": train1.id,
        }
    )

    # mock_svc.configure_mock(**{'process.return_value': ({train2.id: [parcel1.id, parcel2.id]}, 100.0)})
    mock_svc().process.return_value = {
        train2.id: [parcel1.id, parcel2.id]
    }, 100.0
    resp = await async_client.post("/parcels/fill")
    data = resp.json()

    parcels = await database.fetch_all(
        Parcel.select().where(Parcel.c.train_id == train2.id)
    )
    updated_train = await database.fetch_one(
        Train.select().where(Train.c.id == train2.id)
    )

    assert data["assigned_items"] == 2
    assert data["total_cost"] == 100.00
    assert len(parcels) == 2

    assert updated_train.ready_to_book is True

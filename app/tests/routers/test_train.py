from datetime import datetime
from typing import Callable
from unittest.mock import Mock, patch

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_train(async_client: AsyncClient):
    data = {
        "name": "Thomas",
        "cost": 100.00,
        "weight": 200.00,
        "volume": 10.00,
    }
    resp = await async_client.post("/trains", json=data)
    new_train = resp.json()

    assert resp.status_code == 201
    assert new_train["name"] == data["name"]
    assert new_train["cost"] == data["cost"]
    assert new_train["weight"] == data["weight"]
    assert new_train["volume"] == data["volume"]


@pytest.mark.anyio
async def test_retrieve_train(
    async_client: AsyncClient, sample_train: Callable
):
    train = await sample_train(
        {
            "name": "Percy",
            "cost": 120.00,
            "weight": 500.00,
            "volume": 20.00,
        }
    )
    resp = await async_client.get(f"/trains/{train.id}")
    data = resp.json()

    assert resp.status_code == 200
    assert data["name"] == train.name
    assert data["cost"] == train.cost
    assert data["weight"] == train.weight
    assert data["volume"] == train.volume


@pytest.mark.anyio
async def test_get_all_available_trains(
    async_client: AsyncClient, sample_train: Callable
):
    train1 = await sample_train(
        {
            "name": "Percy",
            "cost": 120.00,
            "weight": 500.00,
            "volume": 20.00,
            "ready_to_book": False,
        }
    )
    train2 = await sample_train(
        {
            "name": "Thomas",
            "cost": 100.00,
            "weight": 200.00,
            "volume": 10.00,
            "ready_to_book": False,
        }
    )

    resp = await async_client.get("/trains")
    data = resp.json()

    assert resp.status_code == 200
    assert len(data) == 2
    assert {
        "id": train1.id,
        "name": "Percy",
        "cost": 120.00,
        "weight": 500.00,
        "volume": 20.00,
        "booked_at": None,
        "ready_to_book": False,
    } in data
    assert {
        "id": train2.id,
        "name": "Thomas",
        "cost": 100.00,
        "weight": 200.00,
        "volume": 10.00,
        "booked_at": None,
        "ready_to_book": False,
    } in data


@pytest.mark.anyio
@patch("app.routers.train.datetime")
async def test_book_train(
    mock_dt: Mock, async_client: AsyncClient, sample_train: Callable
):
    booked_at = datetime.utcnow()
    mock_dt.utcnow.return_value = booked_at
    await sample_train(
        {
            "name": "Percy",
            "cost": 120.00,
            "weight": 500.00,
            "volume": 20.00,
            "ready_to_book": False,
            "booked_at": datetime.utcnow(),
        }
    )
    train2 = await sample_train(
        {
            "name": "Thomas",
            "cost": 100.00,
            "weight": 200.00,
            "volume": 10.00,
            "ready_to_book": True,
            "booked_at": None,
        }
    )

    resp = await async_client.post("/trains/book")
    data = resp.json()

    assert resp.status_code == 200
    assert {
        "id": train2.id,
        "name": "Thomas",
        "cost": 100.00,
        "weight": 200.00,
        "volume": 10.00,
        "ready_to_book": True,
        "booked_at": booked_at.isoformat(),
    } in data

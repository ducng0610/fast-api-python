from typing import Callable

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_trainline(async_client: AsyncClient):
    data = {"name": "A"}
    resp = await async_client.post("/trainlines", json=data)
    new_train = resp.json()

    assert resp.status_code == 201
    assert new_train["name"] == data["name"]
    assert new_train["occupied_at"] is None


@pytest.mark.anyio
async def test_get_all_trainlines(
    async_client: AsyncClient, sample_trainline: Callable
):
    line1 = await sample_trainline({"name": "A"})
    line2 = await sample_trainline({"name": "B"})

    resp = await async_client.get("/trainlines")
    data = resp.json()

    assert resp.status_code == 200
    assert len(data) == 2
    assert {
        "id": line1.id,
        "name": "A",
        "occupied_at": None,
    } in data
    assert {
        "id": line2.id,
        "name": "B",
        "occupied_at": None,
    } in data

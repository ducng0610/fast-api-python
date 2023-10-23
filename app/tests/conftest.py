import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.db import Parcel, Train, TrainLine, database
from app.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncClient:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac


@pytest.fixture
async def sample_trainline():
    async def create_trainline(data: dict):
        query = TrainLine.insert().values(data)
        new_id = await database.execute(query)
        return await database.fetch_one(
            TrainLine.select().where(TrainLine.c.id == new_id)
        )

    return create_trainline


@pytest.fixture
async def sample_train():
    async def create_train(data: dict):
        query = Train.insert().values(data)
        new_train_id = await database.execute(query)
        return await database.fetch_one(
            Train.select().where(Train.c.id == new_train_id)
        )

    return create_train


@pytest.fixture
async def sample_parcel():
    async def create_parcel(data: dict):
        query = Parcel.insert().values(data)
        new_parcel_id = await database.execute(query)
        return await database.fetch_one(
            Parcel.select().where(Parcel.c.id == new_parcel_id)
        )

    return create_parcel

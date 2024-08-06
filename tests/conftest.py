import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ad_looper.main import app
from apps.common.dependencies import get_db
from database.models import Base

SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://demian:test@localhost:5432/ad_looper_test"
)

# Create an async engine and sessionmaker for test database
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def db_override():
    # Create all tables in the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_db] = db_override

    yield TestClient(app)

    app.dependency_overrides.clear()

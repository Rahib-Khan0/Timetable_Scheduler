import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from db.base import Base

load_dotenv()

# Example environment-based database URL
DATABASE_URL = os.getenv("DATABASE_URL",)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def tenant_session(schema_name: str):
    """
    Async context manager to get a DB session with search_path set to the tenant schema.
    """
    async with AsyncSessionLocal() as session:
        await session.execute(text(f'SET search_path TO "{schema_name}"'))
        try:
            yield session
        finally:
            await session.close()


# Schema and table creation
async def create_schema_if_not_exists(schema_name: str):
    async with engine.begin() as conn:
        await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))

async def create_tables_in_schema(schema_name: str):
    async with engine.begin() as conn:
        await conn.execute(text(f'SET search_path TO "{schema_name}"'))
        await conn.run_sync(Base.metadata.create_all)

async def refresh_schema(schema_name: str):
    async with AsyncSessionLocal() as session:  # open a real session
        await session.execute(text(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE'))
        await session.commit()

    await create_schema_if_not_exists(schema_name)
    await create_tables_in_schema(schema_name)



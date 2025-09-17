# api/admin.py
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from db.base import Base
from db.models import *  # import all your models

router = APIRouter(prefix="/admin", tags=["Admin"])

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/Timetable_Scheduler"
engine = create_async_engine(DATABASE_URL, echo=True)

@router.post("/reset_dwarka")
async def reset_dwarka():
    async with engine.begin() as conn:
        # Drop schema and all tables
        await conn.execute(text('DROP SCHEMA IF EXISTS dwarka CASCADE'))
        await conn.execute(text('CREATE SCHEMA dwarka'))

        # Recreate tables according to models
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    return {"status": "success", "message": "DWARKA schema reset and tables recreated successfully."}



from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.session import get_session
from db.models import DepartmentSem
from services.dataFetcher.raw_data_loader import fetch_raw_data
from services.engine.Build_Scheduler import build_scheduler
from services.engine.Diagnose_Infeasibility import diagnose_infeasibility
from services.engine.diagnose_infeasibilty_global import diagnose_infeasibility_global
from services.engine.organize_data import organize_for_scheduler

router = APIRouter(
    prefix="/api",
    tags=["Raw Data"]
)

@router.get("/raw-data")
async def get_raw_data(
    session: AsyncSession = Depends(get_session)
):
    """
    Return raw unprocessed data for ALL department-semester combinations.
    Automatically collects dep_sem_ids from DB.
    """
    # 🧠 Fetch all dep_sem_ids from DB
    result = await session.execute(select(DepartmentSem.id))
    dep_sem_ids = [row[0] for row in result.fetchall()]

    # 🧪 Use raw_data_loader with that list
    raw_data = await fetch_raw_data(session, dep_sem_ids)

    # 🪄 Serialize everything safely
    def serialize(obj):
        if isinstance(obj, list):
            return [serialize(o) for o in obj]
        if isinstance(obj, tuple):
            return [serialize(o) for o in obj]
        # If it is a SQLAlchemy Row object
        if hasattr(obj, "_mapping"):
            return {k: serialize(v) for k, v in obj._mapping.items()}
        # If it is a dict
        if isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        # If it is a datetime / time object
        import datetime
        if isinstance(obj, (datetime.date, datetime.time, datetime.datetime)):
            return obj.isoformat()
        return obj

    return {key: serialize(value) for key, value in raw_data.items()}



@router.get("/org_data")
async def get_raw_data(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(DepartmentSem.id))
    dep_sem_ids = [row[0] for row in result.fetchall()]
    raw_data = await fetch_raw_data(session, dep_sem_ids)
    org_data = organize_for_scheduler(raw_data)
    return org_data


@router.get("/timetable/dummy")
async def get_timetable_data_dummy(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(DepartmentSem.id))
    dep_sem_ids = [row[0] for row in result.fetchall()]
    raw_data = await fetch_raw_data(session, dep_sem_ids)
    org_data = organize_for_scheduler(raw_data)

    # Run diagnostics
    issues = diagnose_infeasibility(org_data)
    if any(issues.values()):
        return {"status": "unsolvable", "reasons": issues}
    else:
        print("\n\n\nno issues\n\n")

    # Try scheduler
    timetable = build_scheduler(org_data)
    if timetable["status"] == "INFEASIBLE":
        return {"status": "infeasible", "reasons": diagnose_infeasibility_global(org_data)}
    return {"timetable": timetable}



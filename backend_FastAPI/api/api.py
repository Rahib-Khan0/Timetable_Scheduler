
from services.engine.Build_Scheduler import build_scheduler
from services.engine.Diagnose_Infeasibility import diagnose_infeasibility
from services.engine.diagnose_infeasibilty_global import diagnose_infeasibility_global
from services.engine.organize_data import organize_for_scheduler
from fastapi import APIRouter, Depends
from sqlalchemy import select
from core.depedencies import get_current_user
from db.session import tenant_session
from db.models import DepartmentSem
from services.dataFetcher.raw_data_loader import fetch_raw_data



router = APIRouter(
    prefix="/api",
    tags=["API"]
)

router = APIRouter()

@router.get("/raw-data")
async def get_raw_data(
    current_user=Depends(get_current_user)
):
    """
    Return raw unprocessed data for ALL department-semester combinations of the current institute.
    Automatically collects dep_sem_ids from tenant schema.
    """

    # ✅ Get tenant session for current institute
    async with tenant_session(current_user["institute_code"]) as session:
        # 🧠 Fetch all dep_sem_ids from tenant schema
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
        if hasattr(obj, "_mapping"):
            return {k: serialize(v) for k, v in obj._mapping.items()}
        if isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        import datetime
        if isinstance(obj, (datetime.date, datetime.time, datetime.datetime)):
            return obj.isoformat()
        return obj

    return {key: serialize(value) for key, value in raw_data.items()}




@router.get("/org_data")
async def get_raw_data(current_user=Depends(get_current_user)):
    """
    Get organized raw data for the current user's institute schema.
    """
    # 🔐 Get session for user's tenant schema
    async with tenant_session(current_user["institute_code"]) as session:
        # 🎯 Get department-semester IDs
        result = await session.execute(select(DepartmentSem.id))
        dep_sem_ids = [row[0] for row in result.fetchall()]

        # 🧪 Fetch raw data
        raw_data = await fetch_raw_data(session, dep_sem_ids)

        # 🧠 Organize for scheduler
        org_data = organize_for_scheduler(raw_data)

    return org_data


@router.get("/timetable/dummy")
async def get_timetable_data_dummy(current_user=Depends(get_current_user)):
    """
    Runs scheduling diagnostics and dummy timetable generation for current institute.
    """
    async with tenant_session(current_user["institute_code"]) as session:
        # Fetch all dep_sem_ids
        result = await session.execute(select(DepartmentSem.id))
        dep_sem_ids = [row[0] for row in result.fetchall()]

        # Load and organize raw data
        raw_data = await fetch_raw_data(session, dep_sem_ids)
        org_data = organize_for_scheduler(raw_data)

        # Run diagnostics
        issues = diagnose_infeasibility(org_data)
        if any(issues.values()):
            return {"status": "unsolvable", "reasons": issues}

        # Try to build timetable
        timetable = build_scheduler(org_data)
        if timetable["status"] == "INFEASIBLE":
            return {
                "status": "infeasible",
                "reasons": diagnose_infeasibility_global(org_data)
            }

        return {"status": "solved", "timetable": timetable}



from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Timetable, Course, Faculty, Rooms, DepartmentSem
import calendar

# Optional: map day integers to names
DAY_NAMES = list(calendar.day_name)  # ["Monday", "Tuesday", ..., "Sunday"]

async def get_pretty_timetable(version_id: int, session: AsyncSession):
    # Step 1: Fetch all timetable entries for this version
    result = await session.execute(
        select(Timetable)
        .where(Timetable.version_id == version_id)
        .options(
            # Eager load relationships to avoid multiple DB hits
            selectinload(Timetable.course),
            selectinload(Timetable.faculty),
            selectinload(Timetable.room),
            selectinload(Timetable.department_sem),
        )
    )
    entries = result.scalars().all()

    # Step 2: Build pretty timetable structure
    pretty = {}

    for entry in entries:
        dep = entry.department_sem.department
        sem = entry.department_sem.sem
        depsem_name = f"{dep.upper()} SEM {sem}"

        day_name = DAY_NAMES[entry.day]
        slot = entry.slot

        course_code = entry.course.course_code
        course_type = entry.component_type
        faculty_name = entry.faculty.name
        room_name = entry.room.name
        group_info = f" (Group {entry.group_no})" if entry.group_no > 1 else ""

        class_desc = f"{course_code} ({course_type}) - {faculty_name} - {room_name}{group_info}"

        pretty.setdefault(depsem_name, {}).setdefault(day_name, {})[slot] = class_desc

    return pretty

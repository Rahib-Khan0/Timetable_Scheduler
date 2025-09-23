from db.models import Timetable, TimetableVersion
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

async def store_solution_in_db(session: AsyncSession, timetable_data, components, faculty, version_name="Auto-Generated"):
    """
    Store a single complete timetable as one version.
    """
    if not timetable_data:
        return None

    # 1️⃣ Create new timetable version
    version = TimetableVersion(
        name=version_name,
        created_at=datetime.utcnow(),
        is_final=False
    )
    session.add(version)
    await session.flush()  # get version.id

    # 2️⃣ Add timetable entries
    for entry in timetable_data:
        if "room_id" not in entry or "faculty_code" not in entry:
            continue  # skip incomplete entries

        t = Timetable(
            day=entry["day"],
            slot=entry["slot"],
            room_id=entry["room_id"],
            faculty_id=faculty[entry["faculty_code"]]["faculty_id"],
            course_id=entry["course_id"],
            dep_sem_id=entry["dep_sem_id"],
            component_type=entry["type"],
            group_no=entry["group"],
            version_id=version.id,
            course_component_id=entry["component_id"],
            locked=False
        )

        session.add(t)

    await session.commit()
    return version.id

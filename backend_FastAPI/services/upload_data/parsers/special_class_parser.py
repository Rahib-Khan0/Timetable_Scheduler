import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DepartmentSem, Course, Faculty, Rooms, SpecialClass
from sqlalchemy.future import select

async def parse_special_classes(df: pd.DataFrame, session : AsyncSession):
    for _, row in df.iterrows():
        dept = row['Department'].strip()
        sem = int(row['Semester'])

        # Find dep_sem
        stmt = await session.execute(select(DepartmentSem).where(
            DepartmentSem.department == dept,
            DepartmentSem.semester == sem
        ))
        dep_sem = stmt.scalar_one_or_none()
        if not dep_sem:
            continue

        # Lookup course
        stmt = await session.execute(select(Course).where(Course.code == row['Course Code'].strip()))
        course = stmt.scalar_one_or_none()
        if not course:
            continue

        # Lookup faculty
        stmt = await session.execute(select(Faculty).where(Faculty.code == row['Faculty Code'].strip()))
        faculty = stmt.scalar_one_or_none()

        # Lookup room
        stmt = await session.execute(select(Rooms).where(Rooms.code == row['Room Name'].strip()))
        room = stmt.scalar_one_or_none()

        if not faculty or not room:
            continue

        sc = SpecialClass(
            dep_sem_id=dep_sem.id,
            course_id=course.id,
            faculty_id=faculty.id,
            room_id=room.id,
            day=int(row['Day']),
            slot=int(row['Slot'])
        )
        session.add(sc)
    await session.commit()

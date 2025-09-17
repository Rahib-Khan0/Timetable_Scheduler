# services/raw_data_loader.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import (
    DepartmentSem,
    DepSemCourse,
    Course,
    Faculty,
    Rooms,
    SpecialClass, CourseComponent
)

async def fetch_raw_data(session: AsyncSession, dep_sem_ids: list[int]) -> dict:
    """
    Fetch all raw data from the database needed for scheduling for a given list of department-semester IDs.
    """
    data = {}

    # Department-Semester rows
    result = await session.execute(
        select(DepartmentSem).where(DepartmentSem.id.in_(dep_sem_ids))
    )
    data["department_sem"] = result.scalars().all()

    # DepSemCourse + Course
    result = await session.execute(
        select(DepSemCourse, Course)
        .join(Course, DepSemCourse.course_id == Course.course_id)
        .where(DepSemCourse.dep_sem_id.in_(dep_sem_ids))
    )
    data["dep_sem_course"] = result.all()  # (DepSemCourse, Course)

    # CourseComponents (linked to DepSemCourse)
    dep_sem_course_ids = [dsc.id for dsc, _ in data["dep_sem_course"]]
    if dep_sem_course_ids:
        result = await session.execute(
            select(CourseComponent).where(
                CourseComponent.dep_sem_course_id.in_(dep_sem_course_ids)
            )
        )
        data["course_components"] = result.scalars().all()
    else:
        data["course_components"] = []

    # Faculty (global)
    result = await session.execute(select(Faculty))
    data["faculty"] = result.scalars().all()

    # Rooms (global)
    result = await session.execute(select(Rooms))
    data["rooms"] = result.scalars().all()

    # Special classes (per dep_sem)
    result = await session.execute(
        select(SpecialClass).where(SpecialClass.dep_sem_id.in_(dep_sem_ids))
    )
    data["special_classes"] = result.scalars().all()

    return data

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession


async def parse_dep_sem_courses(df: pd.DataFrame, session: AsyncSession):
    from db.models import DepSemCourse

    for _, row in df.iterrows():
        dsc = DepSemCourse(
            dep_sem_id=int(row['DepSemID']),
            course_id=int(row['CourseID']),
            type=row['Type'].lower(),  # "lecture", "lab", or "both"
            weekly_classes=int(row['Weekly Classes']),
            group_no=int(row['Group No']),
            room_type=row['Room Type'].lower()
        )
        session.add(dsc)
    await session.commit()

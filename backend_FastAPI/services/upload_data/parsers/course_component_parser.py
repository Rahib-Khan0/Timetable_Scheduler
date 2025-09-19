import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import CourseComponent

async def parse_course_components(df: pd.DataFrame, session: AsyncSession):


    for _, row in df.iterrows():
        component = CourseComponent(
            dep_sem_course_id=int(row['DepSemCourseID']),
            component_type=row['Component Type'].lower(),  # "lecture" or "practical"
            faculty_id=int(row['FacultyID']),
            weekly_classes=int(row['Weekly Classes']),
            group_no=int(row['Group No'])
        )
        session.add(component)
    await session.commit()

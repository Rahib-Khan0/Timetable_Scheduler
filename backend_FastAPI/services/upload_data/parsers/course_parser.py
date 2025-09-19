import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession


async def parse_courses(df: pd.DataFrame, session: AsyncSession):
    from db.models import Course

    for _, row in df.iterrows():
        course = Course(
            code=row['Code'],
            name=row['Name'],
            credits=float(row['Credits'])  # if fractional credits supported
        )
        session.add(course)
    await session.commit()

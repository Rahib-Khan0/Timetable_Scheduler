import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

async def parse_department_sem(df: pd.DataFrame, session: AsyncSession):
    from db.models import DepartmentSem

    for _, row in df.iterrows():
        room_prefs = row.get('Room Preferences', '[]')
        room_prefs = eval(room_prefs) if isinstance(room_prefs, str) else room_prefs

        dep_sem = DepartmentSem(
            department=row['Department'],
            semester=int(row['Semester']),
            room_preferences=room_prefs
        )
        session.add(dep_sem)
    await session.commit()

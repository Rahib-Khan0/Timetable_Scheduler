import pandas as pd

from db.models import DepartmentSem

async def parse_department_sem(df: pd.DataFrame, session):
    for _, row in df.iterrows():
        lecture_prefs = str(row.get("Lecture Room Preference", "")).split(",")
        lab_prefs = str(row.get("Lab Room Preference", "")).split(",")

        all_prefs = [r.strip() for r in lecture_prefs + lab_prefs if r.strip()]

        dep_sem = DepartmentSem(
            department=row['Department'].strip(),
            semester=int(row['Semester']),
            room_preferences=all_prefs
        )
        session.add(dep_sem)
    await session.commit()

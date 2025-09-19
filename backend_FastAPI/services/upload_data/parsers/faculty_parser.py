from db.models import Faculty
import json

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

async def parse_faculty(df: pd.DataFrame, session):
    for _, row in df.iterrows():
        # Parse availability from Mon–Fri columns
        availability = {}
        for day in DAYS:
            slots = str(row.get(day, "")).strip()
            if slots:
                availability[day] = [int(x) for x in slots.split(',') if x.strip().isdigit()]

        faculty = Faculty(
            code=row['Faculty Code'].strip(),
            name=row['Faculty Name'].strip(),
            max_per_week=int(row['Max Per Week']),
            max_per_day=int(row['Max Per Day']),
            availability=json.dumps(availability)
        )
        session.add(faculty)
    await session.commit()

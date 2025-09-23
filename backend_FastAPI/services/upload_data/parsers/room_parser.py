import pandas as pd
from db.models import Rooms
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

async def parse_rooms(df: pd.DataFrame, session):
    for _, row in df.iterrows():
        availability = {}
        for day in DAYS:
            slots = str(row.get(day, "")).strip()
            if slots:
                availability[day] = [int(x) for x in slots.split(',') if x.strip().isdigit()]

        room = Rooms(
            name=row['Room Name'].strip(),
            type=row['Room Type'].lower().strip(),  # lab or classroom
            capacity=int(row['Capacity']),
            availability=availability
        )
        session.add(room)
    await session.commit()

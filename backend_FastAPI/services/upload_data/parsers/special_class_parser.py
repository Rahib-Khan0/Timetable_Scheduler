import pandas as pd
from sqlalchemy.future import select

from db.models import DepartmentSem, Course, Faculty, Rooms, SpecialClass


async def parse_special_classes(df: pd.DataFrame, session):
    print("\n🔍 Starting to parse Special Classes")
    for _, row in df.iterrows():
        try:
            dept = row['Department'].strip()
            sem = int(row['Semester'])
            course_code = row['Course Code'].strip()
            faculty_code = row['Faculty Code'].strip()
            room_name = row['Room Name'].strip()
            day = int(row['Day'])
            slot = int(row['Slot'])

            # Lookup dep_sem
            stmt = await session.execute(select(DepartmentSem).where(
                DepartmentSem.department == dept,
                DepartmentSem.semester_no == sem
            ))
            dep_sem = stmt.scalar_one_or_none()
            if not dep_sem:
                print(f"No DepartmentSem found for {dept} - Sem {sem}")
                continue

            # Lookup course
            stmt = await session.execute(select(Course).where(Course.course_code == course_code))
            course = stmt.scalar_one_or_none()
            if not course:
                print(f"Course not found: {course_code}")
                continue

            # Lookup faculty
            stmt = await session.execute(select(Faculty).where(Faculty.faculty_code == faculty_code))
            faculty = stmt.scalar_one_or_none()
            if not faculty:
                print(f"Faculty not found: {faculty_code}")
                continue

            # Lookup room
            stmt = await session.execute(select(Rooms).where(Rooms.name == room_name))
            room = stmt.scalar_one_or_none()
            if not room:
                print(f"Room not found: {room_name}")
                continue

            # ✅ Create entry
            sc = SpecialClass(
                dep_sem_id=dep_sem.id,
                course_id=course.id,
                faculty_code=faculty.faculty_code,
                room_id=room.id,
                day_of_week=day,
                slot=slot
            )
            session.add(sc)
            print(f"Added SpecialClass: {dept}, Sem {sem}, {course_code}, Day {day}, Slot {slot}")

        except Exception as e:
            print(f" Error while processing row: {row}")
            import traceback
            traceback.print_exc()

    await session.commit()
    print("Special classes committed.\n")

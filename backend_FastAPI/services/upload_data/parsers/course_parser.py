import pandas as pd
from db.models import Course, DepartmentSem, DepSemCourse, CourseComponent
from sqlalchemy.future import select

async def parse_courses(df: pd.DataFrame, session):
    course_cache = {}
    depsem_cache = {}

    for _, row in df.iterrows():
        # 1. DepartmentSem
        dept = row['Department'].strip()
        sem = int(row['Semester'])
        dep_sem_key = f"{dept}-{sem}"
        if dep_sem_key not in depsem_cache:
            stmt = await session.execute(
                select(DepartmentSem).where(
                    DepartmentSem.department == dept,
                    DepartmentSem.sem == sem
                )
            )
            dep_sem = stmt.scalar_one_or_none()
            if not dep_sem:
                continue
            depsem_cache[dep_sem_key] = dep_sem
        else:
            dep_sem = depsem_cache[dep_sem_key]

        # 2. Course
        course_code_excel = row['Course Code'].strip()
        if course_code_excel not in course_cache:
            stmt = await session.execute(
                select(Course).where(Course.course_code == course_code_excel)
            )
            course = stmt.scalar_one_or_none()
            if not course:
                course = Course(
                    course_code=course_code_excel,
                    name=row['Course Name'].strip()
                )
                session.add(course)
                await session.flush()
            course_cache[course_code_excel] = course
        else:
            course = course_cache[course_code_excel]

        # 3. DepSemCourse
        stmt = await session.execute(
            select(DepSemCourse).where(
                DepSemCourse.dep_sem_id == dep_sem.id,
                DepSemCourse.course_id == course.course_id
            )
        )
        dsc = stmt.scalar_one_or_none()
        if not dsc:
            dsc = DepSemCourse(
                dep_sem_id=dep_sem.id,
                course_id=course.course_id
            )
            session.add(dsc)
            await session.flush()

        # 4. CourseComponent
        faculty_code = str(row.get('Faculty Code')).strip() if row.get('Faculty Code') else None

        weekly_classes = int(row['Weekly Classes']) if pd.notna(row['Weekly Classes']) else 0
        group_no = int(row.get('Group No')) if pd.notna(row.get('Group No')) else 1

        component = CourseComponent(
            dep_sem_course_id=dsc.id,
            component_type=row['Component Type'].lower(),
            weekly_classes=weekly_classes,
            group_no=group_no,
            room_type=row['Room Type'].lower(),
            faculty_code=faculty_code
        )
        session.add(component)

    await session.commit()

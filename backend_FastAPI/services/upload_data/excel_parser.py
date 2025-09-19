from io import BytesIO
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from services.upload_data.parsers import *

async def process_excel_file(file_bytes: bytes, session: AsyncSession):
    workbook = pd.read_excel(BytesIO(file_bytes), sheet_name=None)

    if 'Faculty' in workbook:
        await parse_faculty(workbook['Faculty'], session)

    if 'Rooms' in workbook:
        await parse_rooms(workbook['Rooms'], session)

    if 'DepartmentSem' in workbook:
        await parse_department_sem(workbook['DepartmentSem'], session)

    if 'Courses' in workbook:
        await parse_courses(workbook['Courses'], session)

    if 'DepSemCourses' in workbook:
        await parse_dep_sem_courses(workbook['DepSemCourses'], session)

    if 'CourseComponents' in workbook:
        await parse_course_components(workbook['CourseComponents'], session)

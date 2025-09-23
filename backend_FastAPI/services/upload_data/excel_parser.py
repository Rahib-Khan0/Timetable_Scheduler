from io import BytesIO
import pandas as pd
import traceback  # ✅ for detailed error trace
from sqlalchemy.ext.asyncio import AsyncSession

from services.upload_data.parsers import (
    parse_faculty,
    parse_rooms,
    parse_department_sem,
    parse_courses,
    parse_special_classes
)

async def process_excel_file(file_bytes: bytes, session: AsyncSession):
    try:
        # Load all sheets
        excel_data = pd.read_excel(BytesIO(file_bytes), sheet_name=None)

        print("\n\n\n[Excel Sheets Loaded]")
        print(excel_data.keys())  # Show sheet names
        print("\n\n\n")

        if 'Faculty' in excel_data:
            await parse_faculty(excel_data['Faculty'], session)

        if 'Rooms' in excel_data:
            await parse_rooms(excel_data['Rooms'], session)

        if 'Programs' in excel_data:
            await parse_department_sem(excel_data['Programs'], session)

        if 'Courses' in excel_data:
            await parse_courses(excel_data['Courses'], session)

        if 'Special Classes' in excel_data:
            await parse_special_classes(excel_data['Special Classes'], session)

    except Exception as e:
        print("❌ Error while processing Excel file")
        traceback.print_exc()  # ✅ print full error to terminal
        raise RuntimeError(f"Excel processing failed: {str(e)}") from e

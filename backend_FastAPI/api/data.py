from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.depedencies import get_current_user
from services.upload_data.excel_parser import  process_excel_file
from db.session import get_session, tenant_session, refresh_schema

router = APIRouter(prefix="/data", tags=["DATA_FILES"])

@router.post("/upload/excel_file")
async def upload_excel(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):

    async with tenant_session(current_user["institute_code"]) as session:

        # 1. Check file type
        if not file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(status_code=400, detail="Only Excel files are allowed.")

        # 2. remove all data from current schema tables
        await refresh_schema(current_user["institute_code"])



        # 2. Read file contents and process
        try:
            contents = await file.read()
            await process_excel_file(contents, session)
            return {"message": "File processed and data stored successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")



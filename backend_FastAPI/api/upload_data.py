from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.upload_data.excel_parser import  process_excel_file
from db.session import get_session

router = APIRouter()

@router.post("/upload-excel")
async def upload_excel(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    # 1. Check file type
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed.")

    # 2. Read file contents and process
    try:
        contents = await file.read()
        await process_excel_file(contents, session)
        return {"message": "File processed and data stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

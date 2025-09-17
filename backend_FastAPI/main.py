from fastapi import FastAPI

from api import api, drop, auth
from api.api import router as api_router  # ✅ Correct import

# from  import timetable, auth

app = FastAPI(title="Intelligent Timetable Scheduler")

# Include routes
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(timetable.router, prefix="/timetable", tags=["timetable"])
app.include_router(api_router)
app.include_router(drop.router)

app.include_router(auth.router)
@app.get("/")
def root():
    return {"message": "Welcome to Timetable Scheduler"}

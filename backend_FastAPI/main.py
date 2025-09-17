from fastapi import FastAPI

from api import raw_data, drop

# from  import timetable, auth

app = FastAPI(title="Intelligent Timetable Scheduler")

# Include routes
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(timetable.router, prefix="/timetable", tags=["timetable"])
app.include_router(raw_data.router)
app.include_router(drop.router)
@app.get("/")
def root():
    return {"message": "Welcome to Timetable Scheduler"}

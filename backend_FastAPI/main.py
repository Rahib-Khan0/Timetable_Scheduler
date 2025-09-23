from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from api import router as api_router

# from  import timetable, auth

app = FastAPI(title="Intelligent Timetable Scheduler")

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
@app.get("/")
def root():
    return {"message": "Welcome to Timetable Scheduler"}



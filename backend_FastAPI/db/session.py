from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Example environment-based database URL
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql+asyncpg://postgres:postgres@localhost:5432/timetable_db"
# )

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/Timetable_Scheduler"
engine = create_async_engine(DATABASE_URL)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,       # Set to False in production
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# FastAPI dependency to inject DB session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

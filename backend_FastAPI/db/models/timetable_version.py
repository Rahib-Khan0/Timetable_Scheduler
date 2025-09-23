from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from db.base import Base  # assuming you use Base = declarative_base()


# If using schema-per-institute (e.g., dwarka), you can set dynamically or hardcode here
class TimetableVersion(Base):
    __tablename__ = "timetable_version"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # e.g., "Draft 1", "Final", etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_final = Column(Boolean, default=False)

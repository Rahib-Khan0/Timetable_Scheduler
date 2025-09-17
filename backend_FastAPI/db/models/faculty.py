from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from db.base import Base  # <-- use the shared Base

class Faculty(Base):
    __tablename__ = "faculty"
    __table_args__ = {'schema': 'dwarka'}

    faculty_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    faculty_code = Column(String(50), unique=True, nullable=False)
    availability = Column(JSON, default={})
    max_per_week = Column(Integer, default=10)
    max_per_day = Column(Integer, default=3)

    course_components = relationship("CourseComponent", back_populates="faculty")

    timetable_entries = relationship("Timetable", back_populates="faculty")

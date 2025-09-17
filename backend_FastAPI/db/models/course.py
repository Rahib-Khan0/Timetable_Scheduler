from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base  # <-- use the shared Base

class Course(Base):
    __tablename__ = "course"
    __table_args__ = {'schema': 'dwarka'}

    course_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    course_code = Column(String(50), unique=True, nullable=False)

    dep_sem_courses = relationship("DepSemCourse", back_populates="course")
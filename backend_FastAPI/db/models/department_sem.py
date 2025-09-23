from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from db.base import Base  # <-- use the shared Base

class DepartmentSem(Base):
    __tablename__ = "department_sem"


    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    department = Column(String(50), nullable=False)
    sem = Column(Integer, nullable=False)
    room_preference = Column(JSON, default={})

    dep_sem_courses = relationship("DepSemCourse", back_populates="dep_sem")
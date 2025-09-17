from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base  # <-- use the shared Base

class DepSemCourse(Base):
    __tablename__ = "dep_sem_course"
    __table_args__ = {"schema": "dwarka"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dep_sem_id = Column(Integer, ForeignKey("dwarka.department_sem.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("dwarka.course.course_id", ondelete="CASCADE"))

    dep_sem = relationship("DepartmentSem", back_populates="dep_sem_courses")
    course = relationship("Course", back_populates="dep_sem_courses")
    components = relationship("CourseComponent", back_populates="dep_sem_course", cascade="all, delete-orphan")
    timetable_entries = relationship("Timetable", back_populates="dep_sem_course", cascade="all, delete-orphan")

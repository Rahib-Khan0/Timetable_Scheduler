from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class CourseComponent(Base):
    __tablename__ = "course_component"


    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dep_sem_course_id = Column(Integer, ForeignKey("dep_sem_course.id", ondelete="CASCADE"), nullable=False)

    component_type = Column(String(20), nullable=False)  # lecture or practical
    faculty_code = Column(String(50), ForeignKey("faculty.faculty_code", ondelete="CASCADE"), nullable=False)

    weekly_classes = Column(Integer, nullable=False, default=0)
    group_no = Column(Integer, nullable=False, default=1)
    room_type = Column(String(20), nullable=False)  # classroom or lab

    dep_sem_course = relationship("DepSemCourse", back_populates="components")
    faculty = relationship("Faculty", back_populates="course_components")
    timetable_entries = relationship("Timetable", back_populates="course_component", cascade="all, delete-orphan")



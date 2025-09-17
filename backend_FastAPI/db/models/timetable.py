from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from db.base import Base  # <-- use the shared Base

class Timetable(Base):
    __tablename__ = "timetable"
    # __table_args__ = {'schema': 'dwarka'}  <-- remove this

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dep_sem_course_id = Column(Integer, ForeignKey("dep_sem_course.id", ondelete="CASCADE"))
    course_component_id = Column(Integer, ForeignKey("course_component.id", ondelete="CASCADE"))
    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    faculty_id = Column(Integer, ForeignKey("faculty.faculty_id"))
    day_of_week = Column(Integer, CheckConstraint("day_of_week BETWEEN 1 AND 7"), nullable=False)
    slot = Column(Integer, nullable=False)
    is_locked = Column(Boolean, default=False)

    dep_sem_course = relationship("DepSemCourse", back_populates="timetable_entries")
    course_component = relationship("CourseComponent", back_populates="timetable_entries")
    room = relationship("Rooms", back_populates="timetable_entries")
    faculty = relationship("Faculty", back_populates="timetable_entries")
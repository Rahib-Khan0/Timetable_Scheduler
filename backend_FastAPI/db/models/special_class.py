from sqlalchemy import Column, Integer, String, Time, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from db.base import Base

class SpecialClass(Base):
    __tablename__ = 'special_class'

    special_class_id = Column(Integer, primary_key=True, autoincrement=True)
    dep_sem_id = Column(Integer, ForeignKey('department_sem.id', ondelete='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.course_id', ondelete='CASCADE'), nullable=False)
    faculty_code = Column(String(50), ForeignKey('faculty.faculty_code', ondelete='CASCADE'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.room_id', ondelete='CASCADE'), nullable=False)
    day_of_week = Column(Integer, CheckConstraint('day_of_week BETWEEN 1 AND 7'), nullable=False)
    slot = Column(Integer, nullable=False)


    # # Optional: relationships (if you want to easily access related objects)
    # department_sem = relationship("DepartmentSem", backref="special_classes")
    # course = relationship("Course", backref="special_classes")
    # faculty = relationship("Faculty", backref="special_classes")
    # room = relationship("Rooms", backref="special_classes")

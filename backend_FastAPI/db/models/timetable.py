from sqlalchemy import Column, Integer, ForeignKey, Boolean, Enum, String
from db.base import Base
from sqlalchemy.orm import relationship

class Timetable(Base):
    __tablename__ = "timetable"
      # ← schema-per-institute

    id = Column(Integer, primary_key=True)

    day = Column(Integer, nullable=False)   # 0 = Monday, 1 = Tuesday...
    slot = Column(Integer, nullable=False)  # Slot number (e.g., 1 = 9AM)

    course_component_id = Column(Integer, ForeignKey("course_component.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.faculty_id"), nullable=False)
    dep_sem_id = Column(Integer, ForeignKey("department_sem.id"), nullable=False)


    component_type = Column(String, nullable=False)  # "Lecture" or "Lab"
    group_no = Column(Integer, nullable=False, default=1)

    version_id = Column(Integer, ForeignKey("timetable_version.id"), nullable=False)
    locked = Column(Boolean, default=False)

    # Relationships (optional but useful)
    room = relationship("Rooms")
    faculty = relationship("Faculty")
    course = relationship("Course")
    department_sem = relationship("DepartmentSem")
    version = relationship("TimetableVersion")
    course_component = relationship("CourseComponent")


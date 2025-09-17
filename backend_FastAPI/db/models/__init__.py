from db.base import Base

from .course import Course
from .department_sem import DepartmentSem
from .dep_sem_course import DepSemCourse
from .faculty import Faculty
from .rooms import Rooms
from .special_class import SpecialClass
from .timetable import Timetable
from .CourseComponent import CourseComponent

__all__ = [
    "Base",
    "Course",
    "DepartmentSem",
    "DepSemCourse",
    "Faculty",
    "Rooms",
    "CourseComponent",
    "SpecialClass",
    "Timetable",
]

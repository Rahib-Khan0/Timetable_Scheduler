

from collections import defaultdict
from typing import Dict, Any

def organize_for_scheduler(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    organized = {}

    # ----------------------------
    # Department-Semester mapping
    # ----------------------------
    dep_sem_by_id = {
        d.id: {
            "id": d.id,
            "department": d.department,
            "sem": d.sem,
            "room_preference": d.room_preference or {}
        }
        for d in raw_data.get("department_sem", [])
    }
    organized["dep_sem_by_id"] = dep_sem_by_id

    # ----------------------------
    # Faculty mapping (by code + by id)
    # ----------------------------
    faculty_by_code = {
        f.faculty_code: {
            "faculty_id": f.faculty_id,
            "faculty_code": f.faculty_code,
            "name": f.name,
            "availability": f.availability or {},
            "max_per_week": f.max_per_week,
            "max_per_day": f.max_per_day,
        }
        for f in raw_data.get("faculty", [])
    }
    faculty_by_id = {v["faculty_id"]: v for v in faculty_by_code.values()}
    organized["faculty_by_code"] = faculty_by_code
    organized["faculty_by_id"] = faculty_by_id

    # ----------------------------
    # Rooms mapping
    # ----------------------------
    rooms_by_id = {
        r.room_id: {
            "room_id": r.room_id,
            "name": r.name,
            "type": r.type,
            "capacity": r.capacity,
            "availability": r.availability or {}
        }
        for r in raw_data.get("rooms", [])
    }
    organized["rooms_by_id"] = rooms_by_id

    # ----------------------------
    # Courses mapping
    # ----------------------------
    course_by_id = {
        c.Course.course_id: {
            "course_id": c.Course.course_id,
            "name": c.Course.name,
            "course_code": c.Course.course_code
        }
        for c in raw_data.get("dep_sem_course", [])
    }
    organized["course_by_id"] = course_by_id

    # ----------------------------
    # DepSemCourse mapping
    # ----------------------------
    dep_sem_course_by_id = {}
    dep_sem_course_list_by_dep_sem = defaultdict(list)
    for dsc, course in raw_data.get("dep_sem_course", []):
        dep_sem_course_by_id[dsc.id] = {
            "id": dsc.id,
            "dep_sem_id": dsc.dep_sem_id,
            "course_id": dsc.course_id
        }
        dep_sem_course_list_by_dep_sem[dsc.dep_sem_id].append(dsc.id)
    organized["dep_sem_course_by_id"] = dep_sem_course_by_id
    organized["dep_sem_course_list_by_dep_sem"] = dep_sem_course_list_by_dep_sem

    # ----------------------------
    # Course Components mapping (schedulable units)
    # ----------------------------
    components_by_id = {}
    components_by_dep_sem_course = defaultdict(list)
    components_by_dep_sem = defaultdict(list)

    for comp in raw_data.get("course_components", []):
        comp_dict = {
            "id": comp.id,
            "dep_sem_course_id": comp.dep_sem_course_id,
            "component_type": comp.component_type,
            "faculty_code": comp.faculty_code,
            "weekly_classes": comp.weekly_classes,
            "group_no": comp.group_no,
            "room_type": comp.room_type,
        }
        components_by_id[comp.id] = comp_dict
        components_by_dep_sem_course[comp.dep_sem_course_id].append(comp_dict)

        dep_sem_id = dep_sem_course_by_id[comp.dep_sem_course_id]["dep_sem_id"]
        components_by_dep_sem[dep_sem_id].append(comp_dict)

    organized["components_by_id"] = components_by_id
    organized["components_by_dep_sem_course"] = components_by_dep_sem_course
    organized["components_by_dep_sem"] = components_by_dep_sem



    # ----------------------------
    # Enriched dep_sem_course details (course + components)
    # ----------------------------
    dep_sem_course_details = defaultdict(list)
    for dsc, course in raw_data.get("dep_sem_course", []):
        dep_sem_course_details[dsc.dep_sem_id].append({
            "dep_sem_course_id": dsc.id,
            "course_id": dsc.course_id,
            "course_code": course.course_code,
            "course_name": course.name,
            "components": components_by_dep_sem_course.get(dsc.id, [])
        })
    organized["dep_sem_course_details"] = dep_sem_course_details

    # ----------------------------
    # Special Classes mapping
    # ----------------------------
    special_classes_by_dep_sem = defaultdict(list)
    special_classes = []  # flat list
    for sc in raw_data.get("special_classes", []):
        sc_dict = {
            "special_class_id": sc.special_class_id,
            "dep_sem_id": sc.dep_sem_id,
            "course_id": sc.course_id,
            "faculty_code": sc.faculty_code,
            "room_id": sc.room_id,
            "day_of_week": sc.day_of_week,
            "slot": sc.slot,
        }
        special_classes_by_dep_sem[sc.dep_sem_id].append(sc_dict)
        special_classes.append(sc_dict)

    organized["special_classes_by_dep_sem"] = special_classes_by_dep_sem
    organized["special_classes"] = special_classes

    return organized




from collections import defaultdict

def diagnose_infeasibility_global(org_data: dict) -> list:
    """
    Diagnose infeasibility reasons for timetable scheduling.
    org_data should contain:
        - faculties: list of dicts {faculty_id, name, max_load, courses}
        - courses: list of dicts {course_id, name, duration, faculty_id, students, department}
        - rooms: list of dicts {room_id, capacity}
        - time_slots: list of available slots
    Returns:
        List of strings describing possible infeasibility reasons
    """

    reasons = []

    faculties = org_data.get("faculties", [])
    courses = org_data.get("courses", [])
    rooms = org_data.get("rooms", [])
    time_slots = org_data.get("time_slots", [])

    # --- 1. No rooms or no timeslots ---
    if not rooms:
        reasons.append("No rooms available for scheduling.")
    if not time_slots:
        reasons.append("No time slots defined in the input.")

    # --- 2. Faculty Overload ---
    faculty_load = defaultdict(int)
    for c in courses:
        faculty_load[c["faculty_id"]] += c.get("duration", 1)

    for f in faculties:
        max_load = f.get("max_load", len(time_slots))  # default to all slots if not defined
        if faculty_load[f["faculty_id"]] > max_load:
            reasons.append(
                f"Faculty '{f['name']}' is overloaded: requires {faculty_load[f['faculty_id']]} "
                f"slots but max load is {max_load}."
            )

    # --- 3. Room capacity vs course enrollment ---
    max_room_capacity = max([r.get("capacity", 0) for r in rooms], default=0)
    for c in courses:
        if c.get("students", 0) > max_room_capacity:
            reasons.append(
                f"Course '{c['name']}' has {c['students']} students but no room can fit more than {max_room_capacity}."
            )

    # --- 4. Faculty missing / mismatch ---
    faculty_ids = {f["faculty_id"] for f in faculties}
    for c in courses:
        if c["faculty_id"] not in faculty_ids:
            reasons.append(f"Course '{c['name']}' requires faculty_id {c['faculty_id']} which does not exist.")

    # --- 5. Not enough time slots for all sessions ---
    total_required_slots = sum(c.get("duration", 1) for c in courses)
    if total_required_slots > len(time_slots) * len(rooms):
        reasons.append(
            f"Total required sessions ({total_required_slots}) exceed available slots "
            f"({len(time_slots) * len(rooms)})."
        )

    # --- 6. Duplicate or conflicting input data ---
    seen_courses = set()
    for c in courses:
        if c["course_id"] in seen_courses:
            reasons.append(f"Duplicate course entry found: course_id {c['course_id']}.")
        seen_courses.add(c["course_id"])

    seen_rooms = set()
    for r in rooms:
        if r["room_id"] in seen_rooms:
            reasons.append(f"Duplicate room entry found: room_id {r['room_id']}.")
        seen_rooms.add(r["room_id"])

    # --- 7. Department-semester consistency (optional) ---
    for c in courses:
        if "department" not in c:
            reasons.append(f"Course '{c['name']}' is missing department information.")
        if "semester" not in c:
            reasons.append(f"Course '{c['name']}' is missing semester information.")

    # If no specific reason found, return generic
    if not reasons:
        reasons.append("Infeasible due to conflicting constraints not captured by simple checks.")

    return reasons

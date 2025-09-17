def diagnose_infeasibility(organized):
    """
    Diagnose infeasibility by checking constraints outside the solver.
    Returns a dict of issues grouped by type (faculty, rooms, components, specials).
    """

    num_days = 5
    num_slots = 6

    components = organized["components_by_id"]
    faculty = organized["faculty_by_code"]
    rooms = organized["rooms_by_id"]
    special_classes = organized.get("special_classes_by_dep_sem", {})

    issues = {"faculty": [], "rooms": [], "components": [], "special_classes": []}

    # -------------------------------
    # Faculty-level checks
    # -------------------------------
    for fcode, f in faculty.items():
        availability = f.get("availability", {})
        total_available = sum(len(slots) for slots in availability.values())

        if total_available == 0:
            issues["faculty"].append(
                f"Faculty {f['name']} ({fcode}) has no availability at all."
            )

        if f.get("max_per_week", 0) == 0:
            issues["faculty"].append(
                f"Faculty {f['name']} ({fcode}) has max_per_week=0."
            )

    # -------------------------------
    # Room-level checks
    # -------------------------------
    for rid, r in rooms.items():
        availability = r.get("availability", {})
        total_available = sum(len(slots) for slots in availability.values())

        if total_available == 0:
            issues["rooms"].append(
                f"Room {r['name']} (type {r['type']}) has no available slots."
            )

    # -------------------------------
    # Component-level checks
    # -------------------------------
    for cid, comp in components.items():
        feasible_vars = 0
        required_slots = comp["weekly_classes"]

        for d in range(1, num_days + 1):
            for s in range(1, num_slots + 1):
                for rid, room in rooms.items():
                    # Check room type match
                    if room["type"] != comp["room_type"]:
                        continue

                    # Faculty availability
                    fcode = comp["faculty_code"]
                    available = faculty[fcode]["availability"]
                    if str(d) not in available or s not in available[str(d)]:
                        continue

                    # Room availability
                    available = room["availability"]
                    if str(d) not in available or s not in available[str(d)]:
                        continue

                    feasible_vars += 1

        if feasible_vars < required_slots:
            issues["components"].append(
                f"Component {cid} ({comp['component_type']}) "
                f"requires {required_slots} slots, but only {feasible_vars} feasible."
            )

    # -------------------------------
    # Special classes checks
    # -------------------------------
    for dep_id, specials in special_classes.items():
        for sc in specials:
            fcode = sc["faculty_code"]
            rid = sc["room_id"]
            d = sc["day_of_week"]
            s = sc["slot"]

            # Check faculty availability
            f_avail = faculty.get(fcode, {}).get("availability", {})
            if str(d) not in f_avail or s not in f_avail[str(d)]:
                issues["special_classes"].append(
                    f"Special class {sc['special_class_id']} → Faculty {fcode} "
                    f"not available at day {d}, slot {s}."
                )

            # Check room availability
            r_avail = rooms.get(rid, {}).get("availability", {})
            if str(d) not in r_avail or s not in r_avail[str(d)]:
                issues["special_classes"].append(
                    f"Special class {sc['special_class_id']} → Room {rid} "
                    f"not available at day {d}, slot {s}."
                )

            # Check component existence
            cid_list = [
                c for c, comp in components.items()
                if comp["faculty_code"] == sc["faculty_code"]
                and organized["dep_sem_course_by_id"][comp["dep_sem_course_id"]]["course_id"] == sc["course_id"]
            ]
            if not cid_list:
                issues["special_classes"].append(
                    f"Special class {sc['special_class_id']} → No matching component "
                    f"for course {sc['course_id']} with faculty {fcode}."
                )

    return issues

from ortools.sat.python import cp_model
from sqlalchemy.ext.asyncio import AsyncSession

from services.engine.store_solutions_in_DB import store_solution_in_db


async def build_scheduler(organized, session : AsyncSession):
    """
    Build and solve timetable using OR-Tools CP-SAT Solver.
    Special classes are pre-assigned and removed from solver variables.
    """
    model = cp_model.CpModel()

    # ------------------------------
    # Parameters
    # ------------------------------
    num_days = 5
    num_slots = 6

    components = organized["components_by_id"].copy()  # copy so we can modify
    faculty = organized["faculty_by_code"]
    rooms = organized["rooms_by_id"]
    dep_sem_course = organized["dep_sem_course_by_id"]
    special_classes = organized["special_classes_by_dep_sem"]
    dep_sem_by_id = organized["dep_sem_by_id"]

    timetable_fixed = []

    # ------------------------------
    # Pre-assign Special Classes
    # ------------------------------
    for dep_id, specials in special_classes.items():
        for sc in specials:
            # Find matching component
            cid_list = [
                c for c, comp in components.items()
                if comp["faculty_code"] == sc["faculty_code"] and
                   dep_sem_course[comp["dep_sem_course_id"]]["course_id"] == sc["course_id"]
            ]

            if not cid_list:
                # No matching component → infeasible special class
                return {
                    "status": "INFEASIBLE",
                    "reason": f"Special class {sc['special_class_id']} has no matching component"
                }

            cid = cid_list[0]  # assume one match
            comp = components[cid]

            # Validate room type
            room = rooms.get(sc["room_id"])
            if not room or room["type"] != comp["room_type"]:
                return {
                    "status": "INFEASIBLE",
                    "reason": f"Special class {sc['special_class_id']} room type mismatch"
                }

            # Pre-assign into timetable
            timetable_fixed.append({
                "component_id": cid,
                "course_id": dep_sem_course[comp["dep_sem_course_id"]]["course_id"],
                "faculty": faculty[comp["faculty_code"]]["name"],
                "day": sc["day_of_week"],
                "slot": sc["slot"],
                "room": room["name"],
                "type": comp["component_type"],
                "group": comp["group_no"],
            })

            # Reduce required weekly classes by 1
            comp["weekly_classes"] -= 1
            if comp["weekly_classes"] < 0:
                return {
                    "status": "INFEASIBLE",
                    "reason": f"Special class {sc['special_class_id']} exceeds weekly requirement"
                }

            # If weekly_classes now 0, remove this component from solver
            if comp["weekly_classes"] == 0:
                del components[cid]

    # ------------------------------
    # Decision Variables
    # ------------------------------
    x = {}
    for cid, comp in components.items():
        for d in range(1, num_days + 1):
            for s in range(1, num_slots + 1):
                for rid, room in rooms.items():
                    if room["type"] == comp["room_type"]:
                        x[cid, d, s, rid] = model.NewBoolVar(
                            f"x_c{cid}_d{d}_s{s}_r{rid}"
                        )

    # ------------------------------
    # Constraints (same as before)
    # ------------------------------
    # Weekly Class Count
    for cid, comp in components.items():
        vars_for_c = [var for key, var in x.items() if key[0] == cid]
        model.Add(sum(vars_for_c) == comp["weekly_classes"])

    # Room Conflicts
    for d in range(1, num_days + 1):
        for s in range(1, num_slots + 1):
            for rid in rooms:
                vars_in_slot = [var for (c, dd, ss, rr), var in x.items() if dd == d and ss == s and rr == rid]
                if vars_in_slot:
                    model.Add(sum(vars_in_slot) <= 1)

    # Faculty Conflicts
    for fcode in faculty:
        for d in range(1, num_days + 1):
            for s in range(1, num_slots + 1):
                vars_for_faculty = [
                    var for (c, dd, ss, rr), var in x.items()
                    if dd == d and ss == s and components[c]["faculty_code"] == fcode
                ]
                if vars_for_faculty:
                    model.Add(sum(vars_for_faculty) <= 1)

    # Faculty Availability
    for cid, comp in components.items():
        fcode = comp["faculty_code"]
        available = faculty[fcode]["availability"]
        for d in range(1, num_days + 1):
            d_str = str(d)
            for s in range(1, num_slots + 1):
                if d_str not in available or s not in available[d_str]:
                    for rid in rooms:
                        var = x.get((cid, d, s, rid))
                        if var is not None:
                            model.Add(var == 0)

    # Room Availability
    for rid, room in rooms.items():
        available = room["availability"]
        for d in range(1, num_days + 1):
            d_str = str(d)
            for s in range(1, num_slots + 1):
                if d_str not in available or s not in available[d_str]:
                    for cid, comp in components.items():
                        var = x.get((cid, d, s, rid))
                        if var is not None:
                            model.Add(var == 0)

    # ------------------------------
    # Solve
    # ------------------------------

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30  # time limit
    solver.parameters.num_search_workers = 1  # deterministic
    solver.parameters.random_seed = 42  # reproducible

    result = solver.Solve(model)

    if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        timetable = timetable_fixed.copy()  # include pre-assigned special classes

        for (c, d, s, rid), var in x.items():
            if solver.Value(var) == 1:
                comp = components[c]
                fcode = comp["faculty_code"]
                timetable.append({
                    "component_id": c,
                    "course_id": dep_sem_course[comp["dep_sem_course_id"]]["course_id"],
                    "faculty_code": fcode,
                    "day": d,
                    "slot": s,
                    "room_id": rid,
                    "type": comp["component_type"],
                    "group": comp["group_no"],
                    "dep_sem_id": dep_sem_course[comp["dep_sem_course_id"]]["dep_sem_id"]
                })

        # Store this timetable as one version in DB
        version_id = await store_solution_in_db(session, timetable, components, faculty, version_name="Auto-generated")

        return {
            "status": solver.StatusName(result),
            "version_id": version_id,
            "timetable": timetable
        }

    # No feasible solution
    return {"status": solver.StatusName(result), "timetable": None}

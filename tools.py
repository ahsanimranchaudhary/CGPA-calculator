COURSES = {
    1: [("MS-251",   "Probability & Statistics",                        3.0),
        ("GE-160",   "Applications of ICT",                             3.0),
        ("GE-169",   "Applied Physics",                                 3.0),
        ("GE-167",   "Discrete Structures",                             3.0),
        ("HQ-001",   "Quran Translation - I",                           0.5),
        ("GE-190",   "Functional English",                              3.0)],
    2: [("CC-112",   "Programming Fundamentals",                        3.0),
        ("CC-112-L", "Programming Fundamentals Lab",                    1.0),
        ("CC-110",   "Digital Logic Design",                            2.0),
        ("CC-110-L", "Digital Logic Design Lab",                        1.0),
        ("MS-252",   "Linear Algebra",                                  3.0),
        ("GE-191",   "Expository Writing",                              3.0),
        ("GE-163",   "Islamic Studies",                                 2.0),
        ("HQ-002",   "Quran Translation - II",                          0.5)],
    3: [("CC-211",   "Object Oriented Programming",                     3.0),
        ("CC-211-L", "Object Oriented Programming Lab",                 1.0),
        ("CC-215",   "Database Systems",                                3.0),
        ("CC-215-L", "Database Systems Lab",                            1.0),
        ("CC-210",   "Computer Organization & Assembly Language",       3.0),
        ("GE-162",   "Calculus & Analytical Geometry",                  3.0),
        ("GE-192",   "Introduction to Management",                      2.0),
        ("HQ-003",   "Quran Translation - III",                         0.5)],
    4: [("CC-213",   "Data Structures",                                 3.0),
        ("CC-213-L", "Data Structures Lab",                             1.0),
        ("CC-312",   "Information Security",                            3.0),
        ("CC-214",   "Computer Networks",                               3.0),
        ("CC-212",   "Software Engineering",                            3.0),
        ("DC-220",   "Advanced Database Management Systems",            3.0),
        ("HQ-004",   "Quran Translation - IV",                          0.5)],
    5: [("CC-313",   "Analysis of Algorithms",                          3.0),
        ("CC-310",   "Artificial Intelligence",                         3.0),
        ("DC-320",   "Theory of Automata and Formal Languages",         3.0),
        ("DC-321",   "Human Computer Interaction",                      3.0),
        ("DC-322",   "Computer Architecture",                           3.0),
        ("EC-330",   "Web Technologies / Elective",                     3.0),
        ("HQ-005",   "Quran Translation - V",                           0.5)],
    6: [("CC-311",   "Operating Systems",                               3.0),
        ("EC-333",   "Mobile Application Development / Elective",       3.0),
        ("EC-324",   "Software Construction & Development / Elective",  3.0),
        ("EC-335",   "Machine Learning / Elective",                     3.0),
        ("EC-334",   "Game Design and Development / Elective",          3.0),
        ("MS-253",   "Multivariable Calculus",                          3.0),
        ("HQ-006",   "Quran Translation - VI",                          0.5)],
    7: [("CC-411",   "Final Year Project - I",                          2.0),
        ("DC-328",   "Parallel & Distributed Computing",                3.0),
        ("EC-345",   "Computer Vision / Elective",                      3.0),
        ("EC-425",   "Software Quality Engineering / Elective",         3.0),
        ("MS-254",   "Technical and Business Writing",                  3.0),
        ("GE-263",   "Entrepreneurship",                                2.0),
        ("GE-262",   "Professional Practices",                          2.0),
        ("HQ-007",   "Quran Translation - VII",                         0.5)],
    8: [("CC-412",   "Final Year Project - II",                         4.0),
        ("DC-421",   "Compiler Construction",                           3.0),
        ("UE-272",   "Introduction to Marketing",                       3.0),
        ("GE-168",   "Ideology and Constitution of Pakistan",           2.0),
        ("GE-363",   "Civics and Community Engagement",                 2.0),
        ("HQ-008",   "Quran Translation - VIII",                        0.5)],
}

def marks_to_grade(marks:int) ->float | str:
    """Use this tool to convert student's raw marks (0-100) into GRADE POINTS (0.0-4.0)."""
    if marks >= 85: return 4.0
    elif marks >= 80: return 3.7
    elif marks >= 75: return 3.3
    elif marks >= 70: return 3.0
    elif marks >= 65: return 2.7
    elif marks >= 61: return 2.3
    elif marks >= 58: return 2.0
    elif marks >= 55: return 1.7
    elif marks >= 50: return 1.0
    else: return 0.0
    
def calculate_semester_gpa(grade_points:list[float],credit_hours: list[float])->float | str:
    """Use this tool to calculate a single semester's GPA by weighting grade points against credit hours."""
    if len(grade_points) != len(credit_hours):
        return "Error: The number of grade points and credit hours must be the same."
    total_credit_hours = sum(credit_hours)
    if total_credit_hours == 0:
        return "Error: Total credit hours cannot be zero."
    weighted_sum = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    gpa = weighted_sum / total_credit_hours
    return round(gpa, 2);

def calculate_new_cgpa(current_cgpa: float, completed_credit_hours: float, semester_gpa: float, semester_credit_hours: float) -> float | str:
    """Use this tool to project what a student's total CGPA will be after completing one additional semester."""
    total_ch = completed_credit_hours + semester_credit_hours
    if total_ch == 0:
        return "Error: total credit hours cannot be zero."
    return (current_cgpa * completed_credit_hours + semester_gpa * semester_credit_hours) / total_ch

def required_gpa_for_target(target_cgpa: float, current_cgpa: float, completed_credit_hours: float, remaining_credit_hours: float) -> float | str:
    """Use this tool to determine the GPA a student needs over their remaining credit hours to hit a specific target CGPA."""
    if remaining_credit_hours == 0:
        return "Error: remaining credit hours cannot be zero."
    required_gpa = (target_cgpa * (completed_credit_hours + remaining_credit_hours) - current_cgpa * completed_credit_hours) / remaining_credit_hours
    return required_gpa

def get_semester_courses(semester: int) -> str:
    """Use this tool when you need to look up the exact courses and credit hours for a specific semester number (1-8)."""
    if semester < 1 or semester > 8:
        return "Error: semester must be between 1 and 8."
    courses = COURSES.get(semester, [])
    return "\n".join([f"{code}: {title} ({ch} CH)" for code, title, ch in courses])

def get_remaining_credit_hours(current_semester: int) -> float | str:
    """Use this tool to calculate the total number of graded credit hours a student has left until graduation after a given semester."""
    if current_semester < 0 or current_semester > 8:
        return "Error: semester must be between 0 and 8."
    remaining_hours = 0.0
    for sem in range(current_semester + 1, 9):
        courses = COURSES.get(sem, [])
        remaining_hours += sum(ch for code, title, ch in courses)
        
    return remaining_hours

def save_report(filename: str, content: str) -> str:
    """Use this tool to save a GPA calculation report or graduation plan to a file. Return a confirmation message."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully saved report to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

def check_unreachable_target(current_semester: int, current_cgpa: float, target_cgpa: float) -> str:
    """Evaluate target CGPA feasibility iteratively across remaining semesters given current semester and CGPA."""
    # Automatically calculate completed credit hours up to the prior semester
    completed_ch = 0.0
    for sem in range(1, current_semester):
        completed_ch += sum(ch for _, _, ch in COURSES.get(sem, []))
    
    results = [f"Completed Credit Hours (Semesters 1 to {current_semester-1}): {completed_ch} CH\n"]
    
    for sem_offset in range(1, 9 - current_semester + 1):
        target_sem = current_semester + sem_offset - 1
        window_ch = 0
        for s in range(current_semester, target_sem + 1):
            window_ch += sum(ch for _, _, ch in COURSES.get(s, []))
        
        req_gpa = (target_cgpa * (completed_ch + window_ch) - current_cgpa * completed_ch) / window_ch
        
        horizon_name = f"Semesters {current_semester} to {target_sem}" if sem_offset > 1 else f"Semester {current_semester} only"
        
        if req_gpa > 4.0:
            results.append(f"- **{horizon_name}** ({window_ch} CH): Required GPA = **{req_gpa:.2f}** ❌ (Impossible)")
        else:
            results.append(f"- **{horizon_name}** ({window_ch} CH): Required GPA = **{req_gpa:.2f}** ✔️ (Achievable)")
            break
            
    return "\n".join(results)


pucit_tools = [
    marks_to_grade,
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    get_semester_courses,
    get_remaining_credit_hours,
    save_report,
    check_unreachable_target
]
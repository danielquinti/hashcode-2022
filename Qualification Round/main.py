import os


class Project:
    def __init__(self, name, required_days, score, expiration, skills):
        self.name = name
        self.required_days = required_days
        self.score = score
        self.expiration = expiration
        self.required_skills = skills
        self.employees = []
        self.active = False
        self.over = False
        self.start_date = None
        self.finish_date = None


class Employee:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        self.working = False


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level


def parse_skills(file, n_skills):
    skills = []
    for i in range(n_skills):
        name, level = file.readline().split()
        level = int(level)
        skills.append(Skill(name, level))
    return skills


def parse_employees(file, n_employees):
    employees = []
    for i in range(n_employees):
        name, n_skills = file.readline().split()
        n_skills = int(n_skills)
        skills = parse_skills(file, n_skills)
        employees.append(Employee(name, skills))
    return employees


def parse_projects(file, n_projects):
    projects = []
    for i in range(n_projects):
        project_attrs = file.readline().split()
        name = project_attrs[0]
        required_days, score, expiration, n_skills = [int(item) for item in project_attrs[1:]]
        skills = parse_skills(file, n_skills)
        projects.append(
            Project(
                name,
                required_days,
                score,
                expiration,
                skills
            )
        )
    return projects


def parse_info(file):
    n_employees, n_projects = file.readline().split()
    n_employees = int(n_employees)
    n_projects = int(n_projects)
    employees = parse_employees(file, n_employees)
    projects = parse_projects(file, n_projects)
    return employees, projects


def score_employees_by_project(selected_employees, project):
    for employee in selected_employees:
        for employee_skill in employee.skills:
            for project_skill in project.required_skills:
                if employee_skill.name == project_skill.name and project_skill.name:
                    score = project_skill.level - employee_skill.level
                    if employee.score < score:
                        employee.score = score
                else:
                    score = project_skill.level
                    if employee.score < score:
                        employee.score = score


def find_available_employee_by_skill(employees, skill, project):
    selected_employees = []
    for employee in employees:
        if employee.working == False:
            for employee_skill in employee.skills:
                if employee_skill.name == skill.name and employee_skill.level >= skill.level:
                    selected_employees.append(employee)
    score_employees_by_project(selected_employees, project)
    # order the selected employees by score
    selected_employees.sort(key=lambda x: x.score, reverse=True)
    return selected_employees[0] if selected_employees else []


def find_mentor_by_skill(project, skill):
    for employee in project.employees:
        for employee_skill in employee.skills:
            if employee_skill.name == skill.name and employee_skill.level >= skill.level:
                return employee
    return False


def find_available_mentee_by_skill(employees, skill, project):
    selected_employees = []
    for employee in employees:
        if employee.working == False:
            for employee_skill in employee.skills:
                if employee_skill.name == skill.name and employee_skill.level >= skill.level - 1:
                    if find_mentor_by_skill(project, skill):
                        selected_employees.append(employee)
    score_employees_by_project(selected_employees, project)
    # order the selected employees by score
    selected_employees.sort(key=lambda x: x.score, reverse=True)
    return selected_employees[0] if selected_employees else []


def can_do(project, employees):
    selected_employees = []
    for skill in project.required_skills:
        employee = find_available_employee_by_skill(employees, skill, project)  # should order the candidate employees properly
        if employee:
            selected_employees.append(employee)
        else:
            mentee = find_available_mentee_by_skill(employees, skill, project)
            if mentee:
                selected_employees.append(mentee)
            else:
                return False
    return True


def available_employees(employees):
    ret = []
    for employee in employees:
        if employee.working:
            ret.append(employee)
    return ret


def score_project(project, curr_day):
    delta = (project.expiration - (curr_day + project.required_days))
    if delta > 0:
        project.stimated_score = project.score
    else:
        project.stimated_score = project.score - delta


def assign_employees_to_feasible(employees, project, day):
    for skill in project.required_skills:
        employee = find_available_employee_by_skill(employees, skill,
                                                    project)  # should order the candidate employees properly
        if employee:
            project.employees.append(employee)
            employee.working = True
            project.skills.append((employee, skill))
        else:
            mentee = find_available_mentee_by_skill(employees, skill, project)
            if mentee:
                project.employees.append(mentee)
                mentee.working = True
                project.skills.append((mentee, skill))
    project.active = True
    project.start_date = day
    project.finish_date = day + project.required_days


def assign_employees(employees, projects, day):
    while available_employees(employees):  # also exit if there are no feasible projects
        feasible = []
        unfeasible = []
        for project in projects:
            if not project.active:
                if can_do(project, employees):
                    feasible.append(project)
                    score_project(project, day)
                else:
                    unfeasible.append(project)
        if not feasible: break
        assign_employees_to_feasible(employees, feasible[0])


def compute_day(day):
    # Check if any active project has finished
    # For every finished project
    # Mark project as finished and not active
    # Reward employees' skills
    # Free employee
    for project in projects:
        if project.active and project.finish_date == day:
            project.active = False
            project.over = True
            for employee in project.employees:
                employee.working = False
            for project_skill in project.skills:
                rol = project_skill[0]
                skill = project_skill[1]
                for rol_skill in rol.skills:
                    if rol_skill.name == skill.name:
                        if rol_skill.level == skill.level or rol_skill.level == skill.level - 1:
                            rol_skill.level += 1


def projects_not_over(employees, projects):
    for project in projects:
        if not project.active:
            if can_do(project, employees):
                return True
            if not project.over or project.active:
                return True
    return False


def run_projects(employees, projects):
    day = 0
    while (projects_not_over(employees, projects)) and day <= 100:
        assign_employees(employees, projects, day)
        compute_day(day)
        day += 1
        print(f"day {day}")
    print("A")


if __name__ == '__main__':
    folder = "input_data"
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as file:
            employees, projects = parse_info(file)
        run_projects(employees, projects)
        exit(0)

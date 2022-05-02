def _sorting_key(application, exam_score_index):
    """The key function to be used in application sorting.
    Returns the greater of the department score and the admission exam score, and the full applicant name."""
    return min(-float(application[exam_score_index]), -float(application[6])), application[0] + application[1]


class AdmissionSimulator:
    def __init__(self):
        self.departments = [  # Used to increase readability in the methods' loops.
            'Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics'
        ]
        self.applications = []
        self.rejected_applications = []
        self.department_max = 0
        self.department_capacities = {
            'Biotech': 0,
            'Chemistry': 0,
            'Engineering': 0,
            'Mathematics': 0,
            'Physics': 0
        }
        self.department_sorting_lists = {
            'Biotech': [],
            'Chemistry': [],
            'Engineering': [],
            'Mathematics': [],
            'Physics': []
        }
        self.accepted_applications = {
            'Biotech': [],
            'Chemistry': [],
            'Engineering': [],
            'Mathematics': [],
            'Physics': []
        }
        self.application_score_indices = {  # The index in the applications of the exam score for that department.
            'Biotech': -3,
            'Chemistry': 3,
            'Engineering': -2,
            'Mathematics': 4,
            'Physics': -1
        }

    def give_accepted_applicants(self):
        """Gives the admission decision for a set of applicants."""
        self._set_department_max()
        self._set_department_capacities()
        self._set_applications()
        self._update_application_scores()

        for _ in range(3):
            self._application_round()

        for department in self.departments:
            self._sort_applications(department, "accepted list")

        self._output_admitted_applicants()
        return

    def _set_department_max(self):
        """Takes as input the max capacity of the departments, sets as an integer."""
        self.department_max = int(input())
        return

    def _set_department_capacities(self):
        """Sets the initial department capacities to match the department max."""
        self.department_capacities = {department: self.department_max for department in self.accepted_applications}
        return

    def _set_applications(self):
        """Formats the list of applications. The prefs represent department priorities on the application.
        Uses format [first name, last name, phys score, chem score, math score, comp sci score, pref1, pref2, pref3]."""
        with open('applicants.txt', 'r') as applications:
            for application in applications.readlines():
                application.rstrip()
                self.applications.append(application.split())
        return

    def _update_application_scores(self):
        """Appends the three needed average scores to the end of the application (reconciles <indices> attribute)."""
        for application in self.applications:
            biotech_score = float((int(application[3]) + int(application[2])) / 2)  # Necessary average for Biotech
            physics_score = float((int(application[4]) + int(application[2])) / 2)  # Necessary average for Physics
            engineering_score = float((int(application[4]) + int(application[5])) / 2)  # Necessary average for Eng
            application += [biotech_score, engineering_score, physics_score]
        return

    def _application_round(self):
        """One complete round of admittance based on the applications' foremost department preference."""
        self._distribute_applications()

        for department in self.departments:
            self._sort_applications(department, 'sorting list')
            self._update_accepted_applications(department)
            self._update_department_capacities(department)

        self._remove_departments()
        return

    def _distribute_applications(self):
        """Divides applications into their foremost preferred department application sorting list."""
        for application in self.applications[:]:
            preferred_department = application[7]
            self.applications.remove(application)
            self.department_sorting_lists[preferred_department].append(application)
        return

    def _sort_applications(self, department, application_list):
        """Sorts current round applications first by the appropriate exam score(s), then by full name."""
        exam_score_index = self.application_score_indices[department]
        if application_list == 'sorting list':
            self.department_sorting_lists[department].sort(key=lambda app: _sorting_key(app, exam_score_index))
        elif application_list == 'accepted list':
            self.accepted_applications[department].sort(key=lambda app: _sorting_key(app, exam_score_index))
        return

    def _update_accepted_applications(self, department):
        """Updates the accepted application list for the given department"""
        if len(self.department_sorting_lists[department]) <= self.department_capacities[department]:
            self.accepted_applications[department] += self.department_sorting_lists[department]
        else:
            capacity = self.department_capacities[department]
            self.accepted_applications[department] += self.department_sorting_lists[department][:capacity]
            self.applications += self.department_sorting_lists[department][capacity:]

        self.department_sorting_lists[department].clear()
        return

    def _update_department_capacities(self, department):
        """Updates the remaining capacity of the given department."""
        self.department_capacities[department] = self.department_max - len(self.accepted_applications[department])
        return

    def _remove_departments(self):
        """Removes the department preference in applications for the previous round of acceptance."""
        for application in self.applications:
            del application[7]
        return

    def _output_admitted_applicants(self):
        """Creates files for each department's accepted applicants and their scores."""
        for department in self.departments:
            exam_score_index = self.application_score_indices[department]
            with open(f'{department}.txt', 'w') as accepted_department_applicants:
                for application in self.accepted_applications[department]:
                    applicant = f'{application[0]} {application[1]} '
                    applicant_score = max(float(application[exam_score_index]), float(application[6]))
                    accepted_department_applicants.write(applicant + str(applicant_score) + '\n')
        return


test = AdmissionSimulator()
test.give_accepted_applicants()

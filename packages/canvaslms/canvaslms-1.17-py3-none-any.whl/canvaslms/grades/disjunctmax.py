"""
Module that summarizes an assignment group by disjunctive maximum.

Disjunctive maximum means: 

  1) At least one assignment must have a non-F grade.
  2) If there are more than one assignment with a non-F grade, we take the 
     maximum as the grade. A--E are valued higher than P. The grade F is valued 
     the lowest.
"""

import datetime as dt

def summarize(user, assignments_list):
  """Extracts user's submissions for assignments in assingments_list to 
  summarize results into one grade and a grade date. Summarize by disjunctive 
  maximum."""

  grades = []
  recent_date = dt.date(year=1970, month=1, day=1)

  for assignment in assignments_list:
    submission = assignment.get_submission(user)
    grade = submission.grade

    if grade is None:
      grade = "F"

    grades.append(grade)

    grade_date = submission.submitted_at or submission.graded_at

    if not grade_date:
      grade_date = recent_date
    else:
      grade_date = dt.date.fromisoformat(grade_date.split("T")[0])

    if grade_date > recent_date:
      recent_date = grade_date

  return (grade_max(grades), recent_date)
def grade_max(grades):
  """Takes a list of A--E/P--F grades, returns the maximum."""
  num_grades = map(grade_to_int, grades)
  max_grade = max(num_grades)
  return int_to_grade(max_grade)

def grade_to_int(grade):
  grade_map = {"F": -1, "P": 0, "E": 1, "D": 2, "C": 3, "B": 4, "A": 5}
  return grade_map[grade]

def int_to_grade(int_grade):
  grade_map_inv = {-1: "F", 0: "P", 1: "E", 2: "D", 3: "C", 4: "B", 5: "A"}
  return grade_map_inv[int_grade]

def summarize_group(assignments_list, users_list):
  """Summarizes a particular set of assignments (assignments_list) for all
  users in users_list"""

  for user in users_list:
    grade, grade_date = summarize(user, assignments_list)
    yield (user, grade, grade_date)

"""
Module that summarizes an assignment group by conjunctive average.

Conjunctive average means: 

  1) We need all assignments to have a non-F grade.
  2) If there are A--F assignments present, we will compute the average of 
     those grades. For instance; an A and a C will result in a B; an A and a B 
     will result in an A, but an A with two Bs will become a B (standard 
     rounding).
"""

import datetime as dt

def summarize(user, assignments_list):
  """Extracts user's submissions for assignments in assingments_list to 
  summarize results into one grade and a grade date. Summarize by conjunctive 
  average."""

  pf_grades = []
  a2e_grades = []
  recent_date = dt.date(year=1970, month=1, day=1)

  for assignment in assignments_list:
    submission = assignment.get_submission(user)
    grade = submission.grade

    if grade is None:
      grade = "F"

    if grade in "ABCDE":
      a2e_grades.append(grade)
    else:
      pf_grades.append(grade)

    grade_date = submission.submitted_at or submission.graded_at

    if not grade_date:
      grade_date = recent_date
    else:
      grade_date = dt.date.fromisoformat(grade_date.split("T")[0])

    if grade_date > recent_date:
      recent_date = grade_date

  if not all(map(lambda x: x == "P", pf_grades)):
    return ("F", recent_date)

  if a2e_grades:
    return (a2e_average(a2e_grades), recent_date)
  return ("P", recent_date)
def a2e_average(grades):
  """Takes a list of A--E grades, returns the average."""
  num_grades = map(grade_to_int, grades)
  avg_grade = round(sum(num_grades)/len(grades))
  return int_to_grade(avg_grade)

def grade_to_int(grade):
  grade_map = {"E": 1, "D": 2, "C": 3, "B": 4, "A": 5}
  return grade_map[grade]

def int_to_grade(int_grade):
  grade_map_inv = {1: "E", 2: "D", 3: "C", 4: "B", 5: "A"}
  return grade_map_inv[int_grade]

def summarize_group(assignments_list, users_list):
  """Summarizes a particular set of assignments (assignments_list) for all
  users in users_list"""

  for user in users_list:
    grade, grade_date = summarize(user, assignments_list)
    yield (user, grade, grade_date)

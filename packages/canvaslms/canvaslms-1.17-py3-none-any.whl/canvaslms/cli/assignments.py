import argparse
import canvasapi
import canvaslms.cli.courses as courses
import canvaslms.hacks.canvasapi
import csv
import pydoc
import pypandoc
import re
import sys

def add_assignment_option(parser, ungraded=True):
  try:
    courses.add_course_option(parser)
  except argparse.ArgumentError:
    pass

  if ungraded:
    parser.add_argument("-U", "--ungraded", action="store_true",
      help="Filter only assignments with ungraded submissions.")

  parser.add_argument("-a", "--assignment",
    required=False, default=".*",
    help="Regex matching assignment title or Canvas identifier, "
      "default: '.*'")

  parser.add_argument("-A", "--assignment-group",
    required=False, default="",
    help="Regex matching assignment group title or Canvas identifier.")

def process_assignment_option(canvas, args):
  course_list = courses.process_course_option(canvas, args)
  assignments_list = []

  for course in course_list:
    try:
      ungraded = args.ungraded
    except AttributeError:
      ungraded = False

    all_assignments = list(filter_assignments([course],
      args.assignment,
      ungraded=ungraded))

    try:
      assignm_grp_regex = args.assignment_group
    except AttributeError:
      print("default to .* for group")
      assignm_grp_regex = ".*"

    assignment_groups = filter_assignment_groups(course, assignm_grp_regex)

    for assignment_group in assignment_groups:
      assignments_list += list(filter_assignments_by_group(
          assignment_group, all_assignments))
  return list(assignments_list)
def assignments_command(config, canvas, args):
  output = csv.writer(sys.stdout, delimiter=args.delimiter)
  assignment_list = process_assignment_option(canvas, args)
  for assignment in assignment_list:
    output.writerow([assignment.assignment_group.name, assignment.name])
def filter_assignment_groups(course, regex):
  """Returns all assignment groups of course whose name matches regex"""
  name = re.compile(regex)
  return filter(
    lambda group: name.search(group.name),
    course.get_assignment_groups())
def filter_assignments_by_group(assignment_group, assignments):
  """Returns elements in assignments that are part of assignment_group"""
  for assignment in assignments:
    if assignment.assignment_group_id == assignment_group.id:
      assignment.assignment_group = assignment_group
      yield assignment
def assignment_command(config, canvas, args):
  assignment_list = process_assignment_option(canvas, args)
  for assignment in assignment_list:
    pydoc.pager(format_assignment(assignment))
def format_assignment(assignment):
  """Returns an assignment formatted for the terminal"""
  instruction = pypandoc.convert_text(
    assignment.description, "md", format="html")

  return f"""# {assignment.name}

{instruction}

URL: {assignment.html_url}
Submissions: {assignment.submissions_download_url}"""
def list_assignments(assignments_containers, ungraded=False):
  """Lists all assignments in all assignments containers (courses or 
  assignement groups)"""
  for container in assignments_containers:
    if isinstance(container, canvasapi.course.Course):
      course = container
    elif isinstance(container, canvasapi.assignment.AssignmentGroup):
      assignment_group = container
      course = assignment_group.course

    if ungraded:
      assignments = container.get_assignments(bucket="ungraded")
    else:
      assignments = container.get_assignments()

    for assignment in assignments:
      try:
        assignment.course = course
      except NameError:
        pass

      try:
        assignment.assignment_group = assignment_group
      except NameError:
        pass

      yield assignment

def list_ungraded_assignments(assignments_containers):
  return list_assignments(assignments_containers, ungraded=True)
def filter_assignments(assignments_containers, regex, ungraded=False):
  """Returns all assignments from assignments_container whose
  title matches regex"""
  p = re.compile(regex)
  for assignment in list_assignments(assignments_containers, ungraded=ungraded):
    if p.search(assignment.name):
      yield assignment
    elif p.search(str(assignment.id)):
      yield assignment

def add_command(subp):
  """Adds the subcommands assignments and assignment to argparse parser subp"""
  add_assignments_command(subp)
  add_assignment_command(subp)

def add_assignments_command(subp):
  """Adds the assignments subcommand to argparse parser subp"""
  assignments_parser = subp.add_parser("assignments",
      help="Lists assignments of a course",
      description="Lists assignments of a course. "
        "Output, CSV-format: <assignment group> <assignment name>")
  assignments_parser.set_defaults(func=assignments_command)
  add_assignment_option(assignments_parser)

def add_assignment_command(subp):
  """Adds the assignment subcommand to argparse parser subp"""
  assignment_parser = subp.add_parser("assignment",
      help="Lists assignment details",
      description="Lists assignment details")
  assignment_parser.set_defaults(func=assignment_command)
  add_assignment_option(assignment_parser)

import canvaslms.hacks.canvasapi
import csv
import re
import sys

def courses_command(config, canvas, args):
  """Prints the users list of courses in CSV format to stdout"""
  output = csv.writer(sys.stdout, delimiter=args.delimiter)

  course_list = filter_courses(canvas, args.regex)
  for course in course_list:
    output.writerow([
      course.course_code,
      course.name,
      course.start_at,
      course.end_at
    ])
def filter_courses(canvas, regex):
  courses = canvas.get_courses()
  p = re.compile(regex)
  for course in courses:
    if p.search(course.name):
      yield course
    elif p.search(course.course_code):
      yield course
    elif p.search(str(course.id)):
      yield course
def add_course_option(parser):
  """Adds the -c option to argparse parser to filter out courses"""
  parser.add_argument("-c", "--course", required=False, default=".*",
    help="Regex matching courses on title, course code or Canvas ID, "
      "default: '.*'")

def process_course_option(canvas, args):
  """Processes -c option, returns a list of courses"""
  course_list = filter_courses(canvas, args.course)
  return list(course_list)

def add_command(subp):
  """Adds the subcomand and its options to argparse subparser subp"""
  courses_parser = subp.add_parser("courses",
    help="Lists your courses",
    description="Lists your courses. Output, CSV-format: "
      "<course-code> <course-name> <start-time> <end-time>")
  courses_parser.set_defaults(func=courses_command)
  courses_parser.add_argument("regex",
    default=".*", nargs="?",
    help="Regex for filtering courses, default: '.*'")

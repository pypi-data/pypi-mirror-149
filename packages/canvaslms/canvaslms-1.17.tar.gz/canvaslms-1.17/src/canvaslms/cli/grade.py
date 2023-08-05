import canvaslms.cli.submissions as submissions
import webbrowser

def grade_command(config, canvas, args):
  submission_list = submissions.process_submission_options(canvas, args)
  results = {}
  if args.grade:
    results["submission"] = {"posted_grade": args.grade}
  if args.message:
    results["comment"] = {"text_comment": args.message}
  if not args.grade and not args.message:
    for submission in submission_list:
      webbrowser.open(submissions.speedgrader(submission))
  else:
    for submission in submission_list:
      submission.edit(**results)

def add_command(subp):
  """Adds grade command to the argparse subparser subp"""
  grade_parser = subp.add_parser("grade",
    help="Grades assignments (hic sunt dracones!)",
    description="Grades assignments. ***Hic sunt dracones [here be dragons]***: "
      "the regex matching is very powerful, "
      "be certain that you match what you think!")
  grade_parser.set_defaults(func=grade_command)
  submissions.add_submission_options(grade_parser)
  grade_options = grade_parser.add_argument_group(
    "arguments to set the grade and/or comment, "
    "if none given, opens SpeedGrader")
  grade_options.add_argument("-g", "--grade",
    help="The grade to set for the submissions")
  grade_options.add_argument("-m", "--message",
    help="A comment to the student")

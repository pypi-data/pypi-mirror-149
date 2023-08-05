"""A command-line interface for the Canvas LMS."""

import appdirs
import argcomplete, argparse
from canvasapi import Canvas
import canvaslms.cli.login
import os
import sys

import canvaslms.cli.login
import canvaslms.cli.courses
import canvaslms.cli.users
import canvaslms.cli.assignments
import canvaslms.cli.submissions
import canvaslms.cli.grade
import canvaslms.cli.results

dirs = appdirs.AppDirs("canvaslms", "dbosk@kth.se")

def err(rc, msg):
  """Prints msg to stderr, prints a stack trace and
  exits with rc as return code"""
  print(f"{sys.argv[0]}: error: {msg}", file=sys.stderr)
  sys.exit(rc)

def warn(msg):
  """Prints msg to stderr"""
  print(f"{sys.argv[0]}: {msg}", file=sys.stderr)
def read_configuration(config_file):
  """Returns a dictionary containing the configuration"""
  config = {}

  try:
    with open(config_file, "r") as file:
      config.update(json.load(file))
  except FileNotFoundError:
    pass
  if "canvas" not in config:
    config["canvas"] = {}

  if "CANVAS_SERVER" in os.environ:
    config["canvas"]["host"] = os.environ["CANVAS_SERVER"]

  if "CANVAS_TOKEN" in os.environ:
    config["canvas"]["access_token"] = os.environ["CANVAS_TOKEN"]

  return config
def update_config_file(config, config_file):
  """Updates the config file by writing the config dictionary back to it"""
  with open(config_file, "w") as fd:
    json.dump(config, fd)

def main():
  argp = argparse.ArgumentParser(
    description="Scriptable Canvas LMS",
    epilog="Web: https://github.com/dbosk/canvaslms")

  subp = argp.add_subparsers(
    title="commands",
    dest="command",
    required=True)

  argp.add_argument("-f", "--config-file",
    default=f"{dirs.user_config_dir}/config.json",
    help="Path to configuration file "
      f"(default: {dirs.user_config_dir}/config.json) "
      "or set CANVAS_SERVER and CANVAS_TOKEN environment variables.")
  argp.add_argument("-d", "--delimiter",
    default="\t",
    help="Sets the delimiter for CSV output, the default is the tab character")
  canvaslms.cli.login.add_command(subp)
  canvaslms.cli.courses.add_command(subp)
  canvaslms.cli.users.add_command(subp)
  canvaslms.cli.assignments.add_command(subp)
  canvaslms.cli.submissions.add_command(subp)
  canvaslms.cli.grade.add_command(subp)
  canvaslms.cli.results.add_command(subp)

  argcomplete.autocomplete(argp)
  args = argp.parse_args()

  config = read_configuration(args.config_file)

  hostname, token = canvaslms.cli.login.load_credentials(config)

  if not (hostname and token):
    err(1, "No hostname or token, run 'canvaslms login'")

  canvas = Canvas(hostname, token)

  if args.func:
    args.func(config, canvas, args)

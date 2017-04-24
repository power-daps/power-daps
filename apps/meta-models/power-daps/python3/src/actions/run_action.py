import common
from actions import deps_action, unit_test_action, package_action

class RunAction():
  name = "run"

  def __init__(self):
    return

  def run(self):
    common.print_raw("blueee!!!")

def action():
   return RunAction()

def run():
    common.print_raw("yowzah!!!")
    return 0, ""


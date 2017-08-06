import common
from actions import deps_action, unit_test_action, package_action

class DefaultAction():
  name = "default"

  def __init__(self):
    return

  def run(self):
    common.stop_if_failed(*deps_action.action().run())
    common.stop_if_failed(*unit_test_action.action().run())
    return 0, ""

def action():
   return DefaultAction()

def print_actions():
    actions = dict()
    f = open("/Users/ppendse/src/power-daps/apps/dap/config/actions.csv", "r")
    try:
        raw_actions = f.read().split("\n")
        raw_actions.remove("ACTION,TYPE,DEPENDENCY,VERSION")
        for raw_action in raw_actions:
            if len(raw_action.split(",")) == 4:
                (action, type, dependency, version) = tuple(raw_action.split(","))
                if action in actions:
                    actions[action].append([type, dependency, version])
                else:
                    actions[action] = list()
                    actions[action].append([type, dependency, version])
        for action in iter(actions):
            print_raw(" --- " + action)
            for dep in iter(actions[action]):
                print_raw("      --- " + dep[0] + ", " + dep[1])
    finally:
        f.close()


import common
import yaml
from actions import deps_action, unit_test_action, package_action

class DefaultAction():
  name = "default"
  default_actions_file_location = common.actions_file_location()

  def __init__(self, actions_file_location = ""):
    self.set_actions_file_location(actions_file_location)
    return

  def run(self):
    deps = dict()
    with open(self.actions_file_location) as f:
      actions_file_contents = f.read()
      for stage in yaml.load(actions_file_contents).items():
        for action in stage[1]:
          print(action)
          common.stop_if_failed(*self.action_for(action).run())
    f.closed
    return 0, ""

  def action_for(self, action_name):
    actions = dict()
    actions["deps"] = deps_action.action()
    actions["unit_test"] = unit_test_action.action()

    return actions[action_name]

  def set_actions_file_location(self, actions_file_location):
    if actions_file_location:
      self.actions_file_location = actions_file_location
    else:
      self.actions_file_location = DefaultAction.default_actions_file_location

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


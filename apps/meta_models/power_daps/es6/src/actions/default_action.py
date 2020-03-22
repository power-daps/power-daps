from dap_core import common
import yaml
from actions import deps_action, unit_test_action, package_action


class DefaultAction:
  name = "default"
  default_actions_file_location = common.actions_file_location()

  def __init__(self, actions_file_location = ""):
    self.set_actions_file_location(actions_file_location)
    return

  def run(self):
    common.print_verbose("Running " + self.name + " action")

    with open(self.actions_file_location) as f:
      actions_file_contents = f.read()
      for stage in yaml.load(actions_file_contents, Loader=yaml.SafeLoader).items():
        for an_action in stage[1]:
          common.stop_if_failed(*self.action_for(an_action).run())
    f.closed
    return 0, ""

  def action_for(self, action_name):
    actions = dict()
    actions["deps"] = deps_action.action()
    actions["unit_test"] = unit_test_action.action()
    actions["package"] = package_action.action()

    return actions[action_name]

  def set_actions_file_location(self, actions_file_location):
    if actions_file_location:
      self.actions_file_location = actions_file_location
    else:
      self.actions_file_location = DefaultAction.default_actions_file_location


def action():
   return DefaultAction()



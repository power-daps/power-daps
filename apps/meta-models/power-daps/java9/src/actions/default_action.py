import common
import yaml
from meta_model import MetaModel
from no_action_error import NoActionError


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
      for stage in yaml.load(actions_file_contents).items():
        for an_action in stage[1]:
          common.stop_if_failed(*self.action_for(an_action).run())
    f.closed
    return 0, ""

  def action_for(self, action_name):
    meta_model = MetaModel("power-daps/java9")
    the_actions = list(filter(lambda a: a.name==action_name, meta_model.actions()))
    the_actions
    if the_actions:
      return the_actions[0]
    else:
      return NoActionError(action_name)

  def set_actions_file_location(self, actions_file_location):
    if actions_file_location:
      self.actions_file_location = actions_file_location
    else:
      self.actions_file_location = DefaultAction.default_actions_file_location


def action():
  return DefaultAction("./actions.yml")



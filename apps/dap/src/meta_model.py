import os, inspect, sys, importlib, glob
import common

class MetaModel:
  n = ""

  def __init__(self, name="power-daps/python3"):
    self.n = name

  def name(self):
    return self.n

  def load_actions_from_dir(self, dir):
    common.print_verbose("Looking for actions in " + dir)
    if os.path.isdir(dir) is not True:
      common.exit_with_error_message("Meta-model '" + self.name() + "' not found in '" + dir + "'")

    elif os.path.isdir(os.path.join(dir, "actions")) is not True:
      common.exit_with_error_message("Meta-model '" + self.name() + "' found but no actions found")

    elif len(self.actions_found_in(dir + "/actions")) == 0:
      common.exit_with_error_message("No actions found in '" + dir + "/actions'")

    if dir not in sys.path:
      sys.path.insert(0, dir)

    actions = []
    #for action in ["default", "deps", "unit_test", "package", "run"]:

    for action in self.actions_found_in(dir + "/actions"):
      action_module = importlib.import_module("actions." + action + "_action")
      actions.append(action_module.action())
    
    return actions


  def actions_dir(self):
    ret_val = os.path.realpath(
      os.path.abspath(
        os.path.join(
          os.path.split(
            inspect.getfile(
              inspect.currentframe()
            ))[0],
          "../../meta-models/" + self.name() + "/src")))
    return ret_val

  def actions(self):
    return self.load_actions_from_dir(self.actions_dir())

  def actions_found_in(self, dir):
    return [os.path.split(path)[-1].replace("_action.py", "") for path in glob.glob(dir + "/*_action.py")]

  def template_for_action(self, action_name):
    return os.path.join(self.actions_dir(), "..", "templates", action_name)


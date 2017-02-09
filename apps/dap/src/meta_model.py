import os, inspect, sys, importlib
import common

class MetaModel:
  n = ""

  def __init__(self, name):
    self.n = name

  def name(self):
    return self.n

  def load_actions_from_dir(self, dir):
    if dir not in sys.path:
      sys.path.insert(0, dir)


    actions = []
    for action in ["default"]:
      action_module = importlib.import_module("actions." + action + "_action")
      actions.append(action_module.DefaultAction())
    
    return actions


  def actions_dir(self):
    return os.path.realpath(
      os.path.abspath(
        os.path.join(
          os.path.split(
            inspect.getfile(
              inspect.currentframe()
            ))[0],
          "../../meta-models/" + self.name() + "/src")))

  def actions(self):
    return self.load_actions_from_dir(self.actions_dir())

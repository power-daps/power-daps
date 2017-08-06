import os
import common
import dap_action
from actions import deps_action, unit_test_action, package_action

class DefaultAction():
  name = "default"
    
  def run(self):
    for action_name in ["deps", "unit_test", "package"]:
      dap_action.run(action_name)
    return 0, ""
   
def action():
   return DefaultAction()



import os
import common
from actions import deps_action, unit_test_action, package_action

class DefaultAction():
  name = "default"
  
  def __init__(self):
    return
    
  def run(self):
    common.print_raw("blueee!!!")
   
def action():
   return DefaultAction()

def run():
    common.stop_if_failed(*deps_action.run())
    common.stop_if_failed(*unit_test_action.run())
    common.stop_if_failed(*package_action.run())

    return 0, ""


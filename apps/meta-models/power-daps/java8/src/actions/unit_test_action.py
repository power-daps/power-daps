import os
import common

class UnitTestAction():
  name = "unit_test"
  
  def __init__(self):
    return
    
  def run(self):
    common.print_raw("blueee!!!")
   
def action():
   return UnitTestAction()

def run():
  return 0, ""

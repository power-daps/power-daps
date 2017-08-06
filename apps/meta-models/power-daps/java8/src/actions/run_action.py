import os
import common

class RunAction():
  name = "run"
  
  def __init__(self):
    return
    
  def run(self):
    common.print_raw("Hello World!")
    return 0, ""
   
def action():
   return RunAction()

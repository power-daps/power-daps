import os
import common

class RunAction():
  name = "run"
  
  def __init__(self):
    return
    
  def run(self):
    common.print_raw("blueee!!!")
   
def action():
   return RunAction()

def run():
  print('Hello World!')
  return 0, ""

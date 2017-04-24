import os
import common

class DepsAction():
  name = "deps"
  
  def __init__(self):
    return
    
  def run(self):
    common.print_raw("blueee!!!")
   
def action():
   return DepsAction()

def run():
  return 0, "" 

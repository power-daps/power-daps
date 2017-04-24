import os
import common

class PackageAction():
  name = "package"
  
  def __init__(self):
    return
    
  def run(self):
    common.print_raw("blueee!!!")
   
def action():
   return PackageAction()

def run():
  return 0, ""

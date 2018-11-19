import os
import common

class CreateAction():
  name = "create"

  def run(self):
    common.print_raw("blueee!!!")
    return 0, ""
   
def action():
   return CreateAction()

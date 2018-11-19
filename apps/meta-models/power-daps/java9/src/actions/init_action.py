import common

class InitAction():
  name = "init"

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    common.print_raw("blueee!!!")
    return 0, ""

def action():
  return InitAction()

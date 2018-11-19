import common

class InitAction():
  name = "run"

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    common.print_raw("blueee!!!")
    return 0, ""

def action():
  return InitAction()

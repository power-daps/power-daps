import common

class NoActionError:
  action_name = "un-specified"
  def __init__(self, action_name = "un-specified"):
    self.action_name = action_name
    return

  def run(self):
    common.print_error("Action '" + self.action_name + "' not found")

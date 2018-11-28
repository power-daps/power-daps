import common

class NoActionError:
  action_name = "un-specified"
  def __init__(self, action_name = "un-specified"):
    self.action_name = action_name
    return

  def run(self):
    error_message = "Action '" + self.action_name + "' not found"
    common.print_error(error_message)
    return 1, error_message
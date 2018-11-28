import common


class UnitTestAction:
  name = "unit_test"

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    return 0, ""


def action():
  return UnitTestAction()

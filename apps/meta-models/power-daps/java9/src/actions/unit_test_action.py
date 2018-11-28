import common


class CompileAction:
  name = "compile"

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    return 0, ""


def action():
  return CompileAction()

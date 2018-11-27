import common
import glob

from meta_model import MetaModel

class InitAction():
  name = "init"

  def run(self):
    common.print_verbose("Running " + self.name + " action")

    files_to_copy = glob.glob(MetaModel(common.meta_model()).template_for_action(self.name) + "/*", recursive=False)
    command_to_run = ['/bin/cp', "-R", *files_to_copy, '.']

    common.run_command(command_to_run)
    common.print_raw("Initialized new Java 9 application.")

    return 0, ""

def action():
  return InitAction()

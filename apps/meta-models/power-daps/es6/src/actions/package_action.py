import os
from dap_core import common
import glob

class PackageAction():
  name = "package"

  def __init__(self):
    return

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    common.stop_if_failed(*common.run_command(["/bin/rm", "-rf", "dist"]))
    return common.run_command(["npx", "webpack-cli"])

def action():
   return PackageAction()


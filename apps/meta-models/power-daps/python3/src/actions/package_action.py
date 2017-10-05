import os
import common
import glob

class PackageAction():
  name = "package"

  def __init__(self):
    return

  def run(self):
    common.stop_if_failed(*common.run_command(["/bin/rm", "-rf", "dist/dap"]))
    return common.run_command([self.pyinstaller(),
                        "--noconfirm", "--log-level=WARN",
                        common.power_daps_dir() + "dap.spec"])

  def pyinstaller(self):
    rc, pyinstaller_path = common.run_command(["which", "pyinstaller"])
    return pyinstaller_path.rstrip()

def action():
   return PackageAction()


import os
import common
import glob

class PackageAction():
  name = "package"

  def __init__(self):
    return

  def run(self):
    common.stop_if_failed(*common.run_command(["/bin/rm", "-rf", "dist/dap"]))
    return common.run_command([common.app_dir() + "deps/bin/pyinstaller",
                        "--noconfirm", "--log-level=WARN",
                        common.power_daps_dir() + "dap.spec"])

def action():
   return PackageAction()


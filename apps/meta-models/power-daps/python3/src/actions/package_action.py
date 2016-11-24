import os
import common
import glob

def run():
    common.stop_if_failed(*common.run_command(["/bin/rm", "-rf", "dist/dap"]))
    return common.run_command([common.app_dir() + "deps/bin/pyinstaller",
                        "--noconfirm", "--log-level=WARN",
                        "--onefile", "--nowindow",
                        "--paths=apps/meta-models/power-daps/python3/src",
                        "--hidden-import=actions",
                        "apps/dap/src/dap.py"])



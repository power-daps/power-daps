import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src/actions")))


if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

if actions_dir not in sys.path:
    sys.path.insert(0, actions_dir)

import common, package_action

class TestPackageAction(unittest.TestCase):
  def test_run(self):
    common.run_command = MagicMock()
    command = [common.app_dir() + "deps/bin/pyinstaller",
                        "--noconfirm", "--log-level=WARN",
                        "--onefile", "--nowindow",
                        "--paths=apps/meta-models/power-daps/python3/src",
                        "--hidden-import=actions",
                        "apps/dap/src/dap.py"]
    package_action.run()
    common.run_command.assert_called_with(command)

if __name__ == '__main__':
    unittest.main()

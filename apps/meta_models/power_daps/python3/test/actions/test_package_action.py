#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
# 
#  This file is part of power-daps.
# 
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, inspect
import unittest
from unittest.mock import MagicMock

dap_src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../../dap_core/src")))
src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src/power_daps/python3/actions")))


if dap_src_dir not in sys.path:
    sys.path.insert(0, dap_src_dir)

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

if actions_dir not in sys.path:
    sys.path.insert(0, actions_dir)

import package_action
from shutil import which
from dap_core import common


class TestPackageAction(unittest.TestCase):
  def test_run(self):
    action = package_action.action()
    action.list_of_package_dirs = MagicMock(return_value=["."])
    common.run_command = MagicMock()
    # command = [common.app_dir() + "deps/bin/pyinstaller",
    #                    "--noconfirm", "--log-level=WARN",
    #           common.power_daps_dir() + "dap.spec"]
    # action.pyinstaller = MagicMock(return_value=common.app_dir() + "deps/bin/pyinstaller")
    command = [which('python3'), 'setup.py', 'sdist', 'bdist_wheel']
    action.run()
    common.run_command.assert_called_with(command)

if __name__ == '__main__':
    unittest.main()

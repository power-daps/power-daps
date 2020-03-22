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

dap_core_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../dap_core/src")))
src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if dap_core_dir not in sys.path:
     sys.path.insert(0, dap_core_dir)

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

from dap_core import common, dap
from power_daps.java8.actions import default_action

dap_command_path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../../bin/dap")))
dap_create = [dap_command_path, "--quiet", "--meta-model", "power_daps/java8", "create"]
dap_default = [dap_command_path, "--quiet", "--meta-model", "power_daps/java8"]
dap_run = [dap_command_path, "--quiet", "--meta-model", "power_daps/java8", "run"]

class TestMetaModel(unittest.TestCase):
  def test_create(self):
    exit_code = 0
    exit_code, output = common.run_command(dap_create)
    self.assertEqual(exit_code, 0)
  
  def test_default(self):
    exit_code = 0
    exit_code, output = common.run_command(dap_default)
    self.assertEqual(exit_code, 0)
  
  def test_run(self):
    exit_code = 0
    exit_code, output = common.run_command(dap_run)
    self.assertEqual(exit_code, 0)
    self.assertEqual(output, "Hello World!\n")

  def test_default_runs_default(self):
    mocked_default_action = default_action.DefaultAction()
    mocked_default_action.run = MagicMock("run method")
    default_action.action = MagicMock("default_action.action")
    default_action.action.return_value = mocked_default_action
  
    dap.main("error", "power_daps/java8", ["default"])

    mocked_default_action.run.assert_called()


if __name__ == '__main__':
  unittest.main()
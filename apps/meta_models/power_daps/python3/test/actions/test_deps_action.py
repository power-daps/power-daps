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

import deps_action
from dap_core import common


def Any(cls):
    class Any(cls):
        def __eq__(self, other):
            return True
    return Any()

class TestDepsAction(unittest.TestCase):
  def test_run_with_default_dependencies(self):
    self.ensure_default_dependencies_file()
    common.run_command = MagicMock(return_value=(0, ""))
    command = ['/usr/local/bin/pip3', '-q', 'install', Any(str), Any(str)]
    deps_action.action().run()
    common.run_command.assert_called_with(command)
    self.ensure_empty_dependencies_file()

  def test_run_with_empty_dependencies_file(self):
    self.ensure_empty_dependencies_file()
    common.run_command = MagicMock()
    deps_action.action().run()
    assert not common.run_command.called
    self.ensure_empty_dependencies_file()

  def test_run_with_empty_default_dependencies_file(self):
    self.ensure_empty_default_dependencies_file()
    common.run_command = MagicMock()
    deps_action.action().run()
    assert not common.run_command.called
    self.ensure_empty_dependencies_file()

  def ensure_empty_dependencies_file(self):
    open("dependencies.yml", 'w').close()

  def ensure_default_dependencies_file(self):
    dependencies_file = open("dependencies.yml", 'w')
    dependencies_file.write("default:\n  pyyaml:\n    version: latest\n    installer: pip3\n")
    dependencies_file.close()

  def ensure_empty_default_dependencies_file(self):
    dependencies_file = open("dependencies.yml", 'w')
    dependencies_file.write("default:\n")
    dependencies_file.close()

if __name__ == '__main__':
    unittest.main()

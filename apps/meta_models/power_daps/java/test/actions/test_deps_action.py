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

dap_src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../../dap_core/src")))
src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src/power_daps/java/actions")))


if dap_src_dir not in sys.path:
  sys.path.insert(0, dap_src_dir)

if src_dir not in sys.path:
  sys.path.insert(0, src_dir)

if actions_dir not in sys.path:
  sys.path.insert(0, actions_dir)

import deps_action


class TestDepsAction(unittest.TestCase):
  def test_other_details_of_a_dependency_come_through(self):
    self.ensure_dependencies_file_with_jar_dependency()
    deps = deps_action.action().load_dependencies("dependencies.yml")

    self.assertEqual(deps.dependencies_for("default")[0].details, {"group_id": "org.mockito"})
    self.ensure_empty_dependencies_file()

  def ensure_empty_dependencies_file(self):
    open("dependencies.yml", 'w').close()

  def ensure_dependencies_file_with_jar_dependency(self):
    dependencies_file = open("dependencies.yml", 'w')
    dependencies_file.write("default:\n  mockito-core:\n    version: 1.10.19\n    installer: jar\n    group_id: org.mockito\n")
    dependencies_file.close()

if __name__ == '__main__':
  unittest.main()

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

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from dap import dependencies


class TestDependencies(unittest.TestCase):
  def test_turns_content_of_dapfile_into_dependencies(self):
    dapfile_contents = """
a_stage:
  a_dep:
    version: '1.2'
    installer: 'pip3'
    """
    expected_dependency = dependencies.Dependency(name ='a_dep', version ='1.2', installer ='pip3')

    deps = dependencies.Dependencies(dapfile_contents)

    self.assertCountEqual(deps.dependencies_for('a_stage'), [expected_dependency])

  def test_turns_content_of_dapfile_into_multiple_dependencies(self):
    dapfile_contents = """
a_stage:
  a_dep:
    version: '1.2'
    installer: 'pip3'

  b_dep:
    version: 'latest'
    installer: 'pip3'
    """

    expected_dependency_a = dependencies.Dependency(name ='a_dep', version ='1.2', installer ='pip3')
    expected_dependency_b = dependencies.Dependency(name ='b_dep', version ='latest', installer ='pip3')
    deps = dependencies.Dependencies(dapfile_contents)

    self.assertCountEqual(deps.dependencies_for('a_stage'), [expected_dependency_a, expected_dependency_b])
    self.assertEqual(deps.dependencies_for('a_stage')[0].version, "1.2")
    self.assertEqual(deps.dependencies_for('a_stage')[1].version, "latest")


  def test_turns_content_of_dapfile_into_multiple_dependencies_for_multiple_stages(self):
    dapfile_contents = """
a_stage:
  a_dep:
    version: '1.2'
    installer: 'pip3'

  b_dep:
    version: 'latest'
    installer: 'pip3'

b_stage:
  c_dep:
    version: 'c_version'
    installer: 'pip3'

  d_dep:
    version: 'd_version'
    installer: 'pip3'
    """

    deps = dependencies.Dependencies(dapfile_contents)

    self.assertEqual(deps.dependencies_for('a_stage')[0].version, "1.2")
    self.assertEqual(deps.dependencies_for('a_stage')[1].version, "latest")
    self.assertEqual(deps.dependencies_for('b_stage')[0].version, "c_version")
    self.assertEqual(deps.dependencies_for('b_stage')[1].version, "d_version")

  def test_other_details_of_a_dependency_come_through(self):
    dapfile_contents = """
a_stage:
  a_dep:
    version: '1.2'
    installer: 'jar'
    group_id: 'org.a_dep'
    """
    expected_dependency = dependencies.Dependency(\
      name = 'a_dep', version = '1.2', installer = 'jar', details={'group_id': 'org.a_dep'})

    deps = dependencies.Dependencies(dapfile_contents)

    self.assertCountEqual(deps.dependencies_for('a_stage'), [expected_dependency])

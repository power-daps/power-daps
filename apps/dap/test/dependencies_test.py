import os, sys, inspect
import unittest

from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


import dependencies


class TestDependencies(unittest.TestCase):
  def test_turns_content_of_dapfile_into_dependencies(self):
    dapfile_contents = """
a_stage:
  a_dep:
    version: '1.2'
    installer: 'pip3'
    """
    expected_dependency = dependencies.Dependency(name = 'a_dep', version = '1.2', installer = 'pip3')

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

    expected_dependency_a = dependencies.Dependency(name = 'a_dep', version = '1.2', installer = 'pip3')
    expected_dependency_b = dependencies.Dependency(name = 'b_dep', version = 'latest', installer = 'pip3')
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

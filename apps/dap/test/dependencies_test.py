import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

import common
import dependencies

class TestDependencies(unittest.TestCase):
  def test_turns_content_of_dapfile_into_dependencies(self):
    dapfile_contents = """
a_stage:
  a_dep:
    version: '1.2',
    installer: 'pip3'
    """

    expected_dependency = dependencies.Dependency(name = 'a_dep', version = '1.2', installer = 'pip3')

    deps = dependencies.Dependencies(dapfile_contents)

    self.assertCountEqual(deps.dependencies_for('a_stage'), [expected_dependency])

  def test_turns_content_of_dapfile_into_multiple_dependencies(self):
    dapfile_contents = """
a_stage:
  a_dep:
    version: '1.2',
    installer: 'pip3'

  b_dep:
    version: 'latest',
    installer: 'pip3'
    """

    expected_dependency_a = dependencies.Dependency(name = 'a_dep', version = '1.2', installer = 'pip3')
    expected_dependency_b = dependencies.Dependency(name = 'b_dep', version = 'latest', installer = 'pip3')
    deps = dependencies.Dependencies(dapfile_contents)

    self.assertCountEqual(deps.dependencies_for('a_stage'), [expected_dependency_a])
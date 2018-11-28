import os, sys, inspect, subprocess
import unittest
from unittest.mock import MagicMock

dap_src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../../dap/src")))
src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src/actions")))


if dap_src_dir not in sys.path:
  sys.path.insert(0, dap_src_dir)

if src_dir not in sys.path:
  sys.path.insert(0, src_dir)

if actions_dir not in sys.path:
  sys.path.insert(0, actions_dir)

import common, deps_action


class TestDepsAction(unittest.TestCase):
  def test_other_details_of_a_dependency_come_through(self):
    self.ensure_dependencies_file_with_jar_dependency()
    common.run_command = MagicMock()
    deps_action.action().run()
    assert not common.run_command.called
    self.ensure_empty_dependencies_file()

  def ensure_empty_dependencies_file(self):
    open("dependencies.yml", 'w').close()

  def ensure_dependencies_file_with_jar_dependency(self):
    dependencies_file = open("dependencies.yml", 'w')
    dependencies_file.write("default:\n  mockito-core:\n    version: 1.10.19\n    installer: jar\n    group_id: org.mockito\n")
    dependencies_file.close()

if __name__ == '__main__':
  unittest.main()

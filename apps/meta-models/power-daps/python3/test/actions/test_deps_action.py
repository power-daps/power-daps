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

def Any(cls):
    class Any(cls):
        def __eq__(self, other):
            return True
    return Any()

class TestDepsAction(unittest.TestCase):
  def test_run_with_default_dependencies(self):
    self.ensure_default_dependencies_file()
    common.run_command = MagicMock()
    command = ['/usr/local/bin/pip3', '-q', 'install', Any(str)]
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

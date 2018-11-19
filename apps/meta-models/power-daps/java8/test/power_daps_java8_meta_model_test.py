import os, sys, inspect
import unittest
from unittest.mock import MagicMock

common_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../dap/src")))
src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if common_dir not in sys.path:
     sys.path.insert(0, common_dir)

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

import common, dap, dap_action
from actions import unit_test_action, deps_action, package_action, default_action

dap_command_path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../../bin/dap")))
dap_create = [dap_command_path, "--quiet", "--meta-model", "power-daps/java8", "create"]
dap_default = [dap_command_path, "--quiet", "--meta-model", "power-daps/java8"]
dap_run = [dap_command_path, "--quiet", "--meta-model", "power-daps/java8", "run"]

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
  
    dap.main("error", "power-daps/java8", ["default"])

    mocked_default_action.run.assert_called()


if __name__ == '__main__':
  unittest.main()

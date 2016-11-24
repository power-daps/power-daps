import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

import common
     
actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../meta-models/" + common.meta_model() + "/src")))

if actions_dir not in sys.path:
     sys.path.insert(0, actions_dir)

import dap
from actions import unit_test_action, deps_action, package_action

class TestDap(unittest.TestCase):
  def test_main_runs_action_in_the_right_order(self):
    unit_test_action.run = MagicMock()
    deps_action.run = MagicMock()
    package_action.run = MagicMock()

    dap.main("blah")

    unit_test_action.run.assert_called_with()
    deps_action.run.assert_called_with()
    package_action.run.assert_called_with()

if __name__ == '__main__':
    unittest.main()

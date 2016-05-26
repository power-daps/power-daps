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
from actions import unit_test_action, deps_action

class TestDap(unittest.TestCase):
  def test_main_runs_the_unit_test_action(self):
    unit_test_action.run = MagicMock()
    dap.main("blah")
    unit_test_action.run.assert_called_with()

def test_main_runs_the_deps_action(self):
    deps_action.run = MagicMock()
    dap.main("blah")
    deps_action.run.assert_called_with()

if __name__ == '__main__':
    unittest.main()

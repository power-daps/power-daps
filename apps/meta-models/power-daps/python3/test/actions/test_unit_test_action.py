import os, sys, inspect, glob
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

import common, unit_test_action

class TestRunTestAction(unittest.TestCase):
  def test_run(self):
    glob.iglob = MagicMock(return_value = ["../test"])
    common.run_command = MagicMock(return_value = (0, ""))
    unit_test_action.action().run()
    assert common.run_command.called

if __name__ == '__main__':
    unittest.main()

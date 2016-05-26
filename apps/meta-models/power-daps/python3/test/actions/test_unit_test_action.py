import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src/actions")))


if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

if actions_dir not in sys.path:
    sys.path.insert(0, actions_dir)

import common, unit_test_action

class TestRunTestAction(unittest.TestCase):
  def test_run(self):
    common.run_command = MagicMock()
    command = ['/usr/local/bin/python3', '-m', 'unittest', 'test/*.py', 'test/**/*.py']
    unit_test_action.run()
    assert common.run_command.called

if __name__ == '__main__':
    unittest.main()

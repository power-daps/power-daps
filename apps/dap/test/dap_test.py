import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

import dap
from actions import run_test

class TestDap(unittest.TestCase):
  def test_main_runs_the_test_action(self):
    run_test.run = MagicMock()
    dap.main("blah")
    run_test.run.assert_called_with()


if __name__ == '__main__':
    unittest.main()

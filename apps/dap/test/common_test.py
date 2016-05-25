import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

import common

class TestCommon(unittest.TestCase):
  def test_print_info(self):
    common.print_raw = MagicMock()
    s = 'hello world'
    common.print_info(s)
    common.print_raw.assert_called_with('INFO: hello world')

if __name__ == '__main__':
    unittest.main()

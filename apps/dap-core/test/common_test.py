#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
# 
#  This file is part of power-daps.
# 
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

from dap_core import common


class TestCommon(unittest.TestCase):
  def test_print_info(self):
    common.set_log_level("info")
    common.print_raw = MagicMock()
    s = 'hello world'
    common.print_info(s)
    common.print_raw.assert_called_with('INFO: hello world')

  def test_meta_model(self):
    common.set_meta_model(None)
    s = 'blah'
    os.getenv = MagicMock(return_value = s)

    self.assertEqual(common.meta_model(), s)
    os.getenv.assert_called_with("POWER_DAPS_META_MODEL", "power-daps/python3")

  def test_stop_if_failed(self):
    orig_exit = sys.exit
    sys.exit = MagicMock()
    # continue when there are no failures
    common.stop_if_failed() # assume success
    common.stop_if_failed(common.SUCCESS)
    common.stop_if_failed(common.SUCCESS, "abcd")

    # exit if failed
    common.stop_if_failed(common.FAILED, "error string")
    sys.exit.assert_called_with(common.FAILED)
    sys.exit = orig_exit

  def test_continue_if_failed(self):
    # continue when there are no failures
    common.continue_if_failed() # assume success
    common.continue_if_failed(common.SUCCESS)
    common.continue_if_failed(common.SUCCESS, "abcd")

    # continue if failed
    common.continue_if_failed(common.FAILED, "error string")

    # but save exit code for later
    self.assertEqual(common.exit_code(), common.FAILED)

if __name__ == '__main__':
    unittest.main()

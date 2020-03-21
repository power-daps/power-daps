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

from dap_core import common, dap

actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../meta-models/" + common.meta_model() + "/src")))

if actions_dir not in sys.path:
     sys.path.insert(0, actions_dir)

from actions import default_action, deps_action
from unittest.mock import patch



class TestDap(unittest.TestCase):
  def test_main_gets_action_in_the_right_order(self):
    with patch('actions.default_action.action'):
      mocked_default_action = self.mock_default_action()

      dap.main("error", "power-daps/python3", ["default"])

      mocked_default_action.run.assert_called()

  def test_main_gets_and_runs_action(self):
    with patch('actions.default_action.action'):
      action = self.mock_default_action()
    
      dap.main("error", "power-daps/python3", ["default"])

      action.run.assert_called_with()

  def test_main_runs_only_the_specified_action(self):
    with patch('actions.default_action.action'):
      with patch('actions.deps_action.action'):
        deps_action = self.mock_deps_action()
        default_action = self.mock_default_action()
        
        dap.main("error", "power-daps/python3", ["deps"])
        
        deps_action.run.assert_called_with()
        default_action.run.assert_not_called()


  def mock_default_action(self):
    action = default_action.DefaultAction()
    action.run = MagicMock()
    default_action.action = MagicMock()
    default_action.action.return_value = action
    return action


  def mock_deps_action(self):
    action = deps_action.DepsAction()
    action.run = MagicMock()
    deps_action.action = MagicMock()
    deps_action.action.return_value = action
    return action

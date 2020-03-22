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

import os, inspect, sys

dap_core_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../dap_core/src")))
src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../src")))

if dap_core_dir not in sys.path:
  sys.path.insert(0, dap_core_dir)

if src_dir not in sys.path:
  sys.path.insert(0, src_dir)

from dap_core import common, dap_action
# from power_daps.java8.actions import deps_action, unit_test_action, package_action

class DefaultAction():
  name = "default"
    
  def run(self):
    for action_name in ["deps", "unit_test", "package"]:
      dap_action.run(action_name)
    return 0, ""
   
def action():
   return DefaultAction()


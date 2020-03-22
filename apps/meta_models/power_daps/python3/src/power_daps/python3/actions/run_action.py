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

from dap_core import common
from actions import deps_action, unit_test_action, package_action

class RunAction():
  name = "run"

  def __init__(self):
    return

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    common.print_raw("blueee!!!")
    return 0, ""
    
def action():
   return RunAction()

def run():
    common.print_raw("yowzah!!!")
    return 0, ""

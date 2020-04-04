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

from shutil import which
from dap_core import common
from power_daps.rust.cargo_command import CargoCommand

class UnitTestAction:
  name = "unit_test"

  def __init__(self, source_dir="test", target_dir="target/test"):
    self.source_dir = source_dir
    self.target_dir = target_dir

  def run(self):
    common.print_info("Running " + self.name + " action")
    common.run_command_in_shell('mkdir -p ' + self.target_dir)

    return CargoCommand('test').run()


  def verbose_flag(self):
    if(common.LOG_LEVEL == "verbose"):
      return "-v"
    else:
      return ""


def action():
  return UnitTestAction()

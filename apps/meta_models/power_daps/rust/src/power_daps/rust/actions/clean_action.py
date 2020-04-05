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

import pathlib
from dap_core import common
from  dap_core.base_actions.dap_action_base  import DapActionBase


class CleanAction(DapActionBase):

  def run(self):
    super().run()
    self.delete_dirs_named("**/target")
    self.delete_dirs_named("**/dist")
    self.delete_dirs_named("**/build")
    self.delete_dirs_named("**/*.egg-info")
    return 0, ""

  def delete_dirs_named(self, dir_name):
    common.print_verbose("Found " + str(len(self.dirs_named(dir_name))) + " dirs named " + dir_name)
    for dir in self.dirs_named(dir_name):
      common.print_verbose("Deleting dir " + dir)
      common.stop_if_failed(*common.run_command(["/bin/rm", "-rf", dir]))

  def dirs_named(self, dir_name):
    return [str(p.absolute()) for p in pathlib.Path(".").glob(dir_name)]


def action():
  return CleanAction()


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

import os
from dap_core import common
import glob

class UploadPackageAction():
  name = "upload_package"

  def __init__(self):
    return

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    common.stop_if_failed(*common.run_command(["/bin/rm", "-rf", "dist/dap"]))
    return common.run_command(['/usr/local/bin/python3', '-m', 'twine', 'upload', '--repository-url', 'https://test.pypi.org/legacy/', 'dist/*'])

def action():
  return UploadPackageAction()

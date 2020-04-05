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
from dap_core.util import git_util, template_util, str_util
import os, sys, pathlib, shutil

from dap_core.meta_model import MetaModel


class InitAction:
  name = "init"

  def run(self):
    common.print_info("Running " + self.name + " action")
    project_dir = '.'
    project_name = os.getcwd().split('/')[-1]

    template_util.check_that_name_does_not_have_dashes(project_name)
    template_util.copy_template_files_to(project_dir, common.action_name(self))

    template_util.find_and_replace_in_file_names_and_content(project_dir, {
      "PROJECT_NAME": project_name,
      "PROJECT_CAMELIZED_NAME": str_util.camelize(project_name)})

    git_util.setup_git(project_dir)
    common.print_raw("Initialized new Python 3 application.")

    return 0, ""


def action():
  return InitAction()

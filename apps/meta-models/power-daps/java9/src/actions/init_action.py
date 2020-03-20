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

import common
import glob
import os, pathlib

from meta_model import MetaModel

class InitAction():
  name = "init"

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    project_dir = '.'
    project_name = os.getcwd().split('/')[-1]

    files_to_copy = [str(p) for p in pathlib.Path(MetaModel(common.meta_model()).template_for_action(self.name)).glob("*")]
    # files_to_copy = glob.glob(MetaModel(common.meta_model()).template_for_action(self.name) + "/*", recursive=False)
    command_to_run = ['/bin/cp', "-R", *files_to_copy, project_dir]
    common.run_command(command_to_run)

    files_to_rename = [str(p) for p in pathlib.Path(project_dir).glob("*PROJECT_NAME*")]
    for file_to_rename in files_to_rename:
      rename_command = ['/bin/mv', file_to_rename, file_to_rename.replace("PROJECT_NAME", project_name)]
      common.run_command(rename_command)

    files_to_search_and_replace_within = [str(p) for p in pathlib.Path(project_dir).glob(".idea/*.xml")]
    for f in files_to_search_and_replace_within:
        sed_command = ['/usr/bin/sed', '-ie', "s/PROJECT_NAME/" + project_name + "/g", f]
        common.run_command(sed_command)

    git_init_command = ['/usr/bin/git', 'init']
    common.run_command(git_init_command)

    git_add_command = ['/usr/bin/git', 'add', '.']
    common.run_command(git_add_command)

    git_commit_command = ['/usr/bin/git', 'commit', '-m', 'Initial commit']
    common.run_command(git_commit_command)

    common.print_raw("Initialized new Java 9 application.")

    return 0, ""

def action():
  return InitAction()

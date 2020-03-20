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

    self.copy_template_files_to(project_dir)
    self.rename_files(project_dir, "PROJECT_NAME", project_name)
    self.setup_git(project_dir)

  def copy_template_files_to(self, destination):
    files_to_copy = [str(p) for p in pathlib.Path(MetaModel(common.meta_model()).template_for_action(self.name)).glob("*")]
    command_to_run = ['/bin/cp', "-R", *files_to_copy, destination]
    common.run_command(command_to_run)

  def rename_files(self, dir, str_to_find, str_to_replace_with):
    files_to_rename = [str(p) for p in pathlib.Path(dir).glob("*" + str_to_find + "*")]
    for file_to_rename in files_to_rename:
      rename_command = ['/bin/mv', file_to_rename, file_to_rename.replace(str_to_find, str_to_replace_with)]
      common.run_command(rename_command)

    files_to_search_and_replace_within = [str(p) for p in pathlib.Path(dir).glob(".idea/*.xml")]
    for f in files_to_search_and_replace_within:
        sed_command = ['/usr/bin/sed', '-ie', "s/" + str_to_find + "/" + str_to_replace_with + "/g", f]
        common.run_command(sed_command)


  def setup_git(self, dir):
    os.chdir(dir)

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

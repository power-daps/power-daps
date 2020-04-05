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

import os, shutil
from dap_core import common


def setup_git(dir):
  git_init(dir)
  add_to_git(dir)


def git_init(dir):
  os.chdir(dir)
  git_path = shutil.which('git')
  git_init_command = [git_path, 'init']
  common.run_command(git_init_command)


def add_to_git(dir):
  os.chdir(dir)
  git_path = shutil.which('git')
  git_add_command = [git_path, 'add', '.']
  common.run_command(git_add_command)

  git_commit_command = [git_path, 'commit', '-m', 'Initialized with power_daps template ' + common.meta_model()]
  common.run_command(git_commit_command)

  return 0, ""

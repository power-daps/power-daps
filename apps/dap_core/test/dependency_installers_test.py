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

import os, sys, shutil, inspect
import unittest

from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
  sys.path.insert(0, src_dir)

from dap_core import common

from dap_core.dependency_installers import PipInstaller
from dap_core.jar_dependency_installer import MavenCentralInstaller
from pathlib import Path

class TestPipInstaller(unittest.TestCase):
  def test_runs_the_right_command_to_install_latest_dependency(self):
    installer = PipInstaller()
    common.run_command = MagicMock(return_value=(0, ""))
    command = ['/usr/local/bin/pip3', '-q', 'install', 'some_name']
    installer.install("some_name")
    common.run_command.assert_called_with(command)

  def test_runs_without_version_when_version_is_specified_as_latest(self):
    installer = PipInstaller()
    common.run_command = MagicMock(return_value=(0, ""))
    command = ['/usr/local/bin/pip3', '-q', 'install', 'some_name']
    installer.install("some_name", "latest")
    common.run_command.assert_called_with(command)

  def test_runs_command_with_version_number_if_specified(self):
    installer = PipInstaller()
    common.run_command = MagicMock(return_value=(0, ""))
    command = ['/usr/local/bin/pip3', '-q', 'install', 'some_name==1.0']
    installer.install("some_name", "1.0")
    common.run_command.assert_called_with(command)

  def test_runs_command_with_version_number_even_if_it_is_a_float(self):
    installer = PipInstaller()
    common.run_command = MagicMock(return_value=(0, ""))
    command = ['/usr/local/bin/pip3', '-q', 'install', 'some_name==1.0']
    installer.install("some_name", 1.0)
    common.run_command.assert_called_with(command)


class TestMavenCentralInstaller(unittest.TestCase):
  def test_knows_the_right_remote_location_to_fetch_jar_from(self):
    expected_location = self.base_url + self.group_id_with_slashes + "/" + self.artifact_id + "/" + self.version + "/" + self.artifact_id + "-" + self.version + "." + self.file_extension
    installer = MavenCentralInstaller(self.base_url)
    self.assertEqual(expected_location, installer.remote_location(self.group_id, self.artifact_id, self.version, self.file_extension))

  def test_knows_the_right_remote_location_to_fetch_pom_from(self):
    self.file_extension = "pom"
    expected_location = self.base_url + self.group_id_with_slashes + "/" + self.artifact_id + "/" + self.version + "/" + self.artifact_id + "-" + self.version + "." + self.file_extension
    installer = MavenCentralInstaller(self.base_url)
    self.assertEqual(expected_location, installer.remote_location(self.group_id, self.artifact_id, self.version, self.file_extension))

  def test_knows_the_right_remote_location_to_fetch_a_different_jar(self):
    self.group_id = "c.d.e"
    self.group_id_with_slashes = "c/d/e"
    self.artifact_id = "blah"
    self.version = "3.0"

    expected_location = self.base_url + self.group_id_with_slashes + "/" + self.artifact_id + "/" + self.version + "/" + self.artifact_id + "-" + self.version + "." + self.file_extension
    installer = MavenCentralInstaller(self.base_url)
    self.assertEqual(expected_location, installer.remote_location(self.group_id, self.artifact_id, self.version, self.file_extension))

  def test_knows_the_right_location_location_to_put_a_jar(self):
    expected_location = "/".join(["lib", "java", self.group_id_with_slashes, self.artifact_id, self.version, self.artifact_id]) + "-" + self.version + "." + self.file_extension
    installer = MavenCentralInstaller(self.base_url)
    self.assertEqual(expected_location, installer.local_location(self.group_id, self.artifact_id, self.version, self.file_extension))

  def test_knows_whether_the_dependency_has_already_been_downloaded(self):
    installer = MavenCentralInstaller(self.base_url)
    self.ensure_dir_tree_does_not_exist(self.tmp_dir)

    self.assertFalse(installer.has_already_been_downloaded(self.group_id, self.artifact_id, self.version, self.file_extension))

    self.ensure_dependency_exists_in_dir(self.tmp_dir, self.dependency_file_name)
    installer.local_location = MagicMock(return_value=self.tmp_dependency_location)

    self.assertTrue(installer.has_already_been_downloaded(self.group_id, self.artifact_id, self.version, self.file_extension))

    self.ensure_dir_tree_does_not_exist(self.tmp_dir)

  def test_fetches_when_dependency_has_not_already_been_downloaded(self):
    installer = MavenCentralInstaller(self.base_url)
    self.ensure_dir_tree_does_not_exist(self.tmp_dir)
    installer.local_location = MagicMock(side_effect=self.change_local_location_by_extension_in_mock)
    installer.fetch = MagicMock()

    installer.install(self.artifact_id, self.version, {"group_id": self.group_id})

    installer.fetch.assert_called()

  def test_does_not_fetch_when_dependency_has_already_been_downloaded(self):
    installer = MavenCentralInstaller(self.base_url)
    self.ensure_dependency_exists_in_dir(self.tmp_dir, self.dependency_file_name)
    installer.local_location = MagicMock(return_value=self.tmp_dependency_location)
    installer.fetch = MagicMock()

    installer.install("something.jar", "0.0", {"group_id": "blah"})

    installer.fetch.assert_not_called()

    self.ensure_dir_tree_does_not_exist(self.tmp_dir)

  def ensure_dependency_exists_in_dir(self, dir_name, dep_file_name):
    dependency_location = dir_name + "/" + dep_file_name
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    Path(dependency_location).touch()

  def ensure_dir_tree_does_not_exist(self, dir_name):
    shutil.rmtree(dir_name, ignore_errors=True)

  def change_local_location_by_extension_in_mock(self, group_id, artifact_id, version, file_extension):
    if file_extension == "jar":
      return self.tmp_dependency_location
    elif file_extension == "pom":
      return self.tmp_pom_location
    else:
      return ""

  def setUp(self):
    self.base_url = "base_url/stuff="
    self.group_id = "a.b.c"
    self.group_id_with_slashes = "a/b/c"
    self.artifact_id = "something"
    self.version = "1.0"
    self.file_extension = "jar"
    self.dependency_file_name = self.artifact_id + "." + self.file_extension
    self.tmp_dir = "../../../build/tmp"
    self.tmp_dependency_location = self.tmp_dir + "/" + self.dependency_file_name
    self.tmp_pom_location = self.tmp_dir + "/" + self.artifact_id + "." + "pom"

  def tearDown(self) -> None:
    self.ensure_dir_tree_does_not_exist(self.tmp_dir)
    self.ensure_dir_tree_does_not_exist("lib")

if __name__ == '__main__':
  unittest.main()

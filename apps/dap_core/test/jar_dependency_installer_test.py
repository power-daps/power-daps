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

import os, sys, shutil, inspect, io
import unittest
from xml.etree import ElementTree

from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
  sys.path.insert(0, src_dir)

from dap_core.jar_dependency_installer import JarDependency, JarDependencyMetadata, Pom
from pathlib import Path


class TestPom(unittest.TestCase):
  def test_knows_its_relative_remote_location(self):
    expected_location = self.group_id_with_slashes + "/" + self.artifact_id + "/" + self.version + "/" + self.artifact_id + "-" + self.version + "." + self.file_extension
    pom = Pom(self.group_id, self.artifact_id, self.version)
    self.assertEqual(expected_location, pom.relative_remote_location())

  def test_knows_its_version_if_specified(self):
    pom = Pom(self.group_id, self.artifact_id, "1.1.1")
    self.assertEqual("1.1.1", pom.version)

  def test_knows_its_local_location(self):
    expected_location = "/".join(["lib", "java", self.group_id_with_slashes, self.artifact_id, self.version, self.artifact_id]) + "-" + self.version + "." + self.file_extension
    pom = Pom(self.group_id, self.artifact_id, self.version)
    self.assertEqual(expected_location, pom.local_location())

  def test_finds_dependencies_in_pom(self):
    jd = JarDependency(self.group_id, self.artifact_id, self.version)
    jd.pom.pom_file = MagicMock(return_value=io.StringIO(junit_shortened_pom_with_dependencies()))
    expected_dependencies = [
      JarDependency("org.hamcrest", "hamcrest-core", "1.3"),
      JarDependency("org.hamcrest", "hamcrest-library", "1.3")
    ]
    self.assertEqual(expected_dependencies, jd.dependencies())

  def ensure_dependency_exists_in_dir(self, dir_name, dep_file_name):
    dependency_location = dir_name + "/" + dep_file_name
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    Path(dependency_location).touch()

  def ensure_dir_tree_does_not_exist(self, dir_name):
    shutil.rmtree(dir_name, ignore_errors=True)

  def setUp(self):
    self.group_id = "a.b.c"
    self.group_id_with_slashes = "a/b/c"
    self.artifact_id = "something"
    self.version = "1.0"
    self.file_extension = "pom"
    self.dependency_file_name = self.artifact_id + "." + self.file_extension
    self.tmp_dir = "../../../build/tmp"
    self.tmp_dependency_location = self.tmp_dir + "/" + self.dependency_file_name
    self.tmp_pom_location = self.tmp_dir + "/" + self.artifact_id + "." + "pom"

  def tearDown(self) -> None:
    self.ensure_dir_tree_does_not_exist(self.tmp_dir)
    self.ensure_dir_tree_does_not_exist("lib")


class TestJarDependency(unittest.TestCase):

  def test_two_instances_with_same_group_id_artifiact_id_and_version_are_equal(self):
    one = JarDependency("a", "b", "c")
    two = JarDependency("a", "b", "c")
    self.assertEqual(one, two)


class TestJarDependencyMetadata:
  def test_parses_metadata_to_get_latest_version(self):
    metadata = JarDependencyMetadata("a", "b")
    stub_metadata_xml = io.StringIO(junit_short_metadata())
    metadata.metadata_file = MagicMock(return_value=stub_metadata_xml)
    self.assertEqual("4.13", metadata.latest_version())


def junit_short_metadata():
    return """<?xml version="1.0" encoding="UTF-8"?>
      <metadata>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <versioning>
          <latest>4.13</latest>
          <release>4.13</release>
          <versions>
            <version>3.7</version>
            <version>4.13</version>
          </versions>
          <lastUpdated>x</lastUpdated>
        </versioning>
      </metadata>
    """


def junit_shortened_pom_with_dependencies():
  return """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <dependencies>
        <dependency>
            <groupId>org.hamcrest</groupId>
            <artifactId>hamcrest-core</artifactId>
            <version>1.3</version>
        </dependency>

        <dependency>
            <groupId>org.hamcrest</groupId>
            <artifactId>hamcrest-library</artifactId>
            <version>1.3</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
    """


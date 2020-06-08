
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
import os, re, io
from xml.etree import ElementTree

from dap_core import common
import urllib.request


class MavenCentralInstaller:
  # https://search.maven.org/remotecontent?filepath=
  def __init__(self, base_url="https://repo1.maven.org/maven2/", lib_dir="lib"):
    self.base_url = base_url
    self.lib_dir = lib_dir
    self.latest_versions_cache = {}
    return

  def install(self, name, version, details):
    if not self.has_already_been_downloaded(details["group_id"], name, version, "jar"):
      self.install_file(name, version, details, "jar")
      self.install_file(name, version, details, "pom")
      self.install_transitive_dependencies(name, version, details, "pom")

  def install_transitive_dependencies(self, name, version, details, extension):
    if self.local_pom_exists(details["group_id"], name, version):
      namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
      tree = ElementTree.parse(self.local_location(details["group_id"], name, version, "pom"))
      root = tree.getroot()

      deps = root.findall("./xmlns:dependencies/xmlns:dependency", namespaces=namespaces)
      for d in deps:
        version = "latest"
        groupId = d.find("xmlns:groupId", namespaces=namespaces).text
        artifactId = d.find("xmlns:artifactId", namespaces=namespaces).text
        version_elem = d.find("xmlns:version", namespaces=namespaces)
        if version_elem is not None:
          if self.value_references_variable(version_elem.text):
            version_var_name = re.findall("\$\{(.*?)\}", version_elem.text)[0]
            common.print_verbose("Looking for property " + version_var_name)
            props = root.findall("./xmlns:properties", namespaces=namespaces)
            for el in props[0].iter():
              if el.tag == "{http://maven.apache.org/POM/4.0.0}" + version_var_name:
                version = el.text
                common.print_verbose("Found property " + version_var_name + " = " + version)
          else:
            version = version_elem.text
        self.install(artifactId, version, {"group_id": groupId})

  def value_references_variable(self, value):
    return value.startswith("${")

  def install_file(self, name, version, details, extension):
    remote_loc = self.remote_location(details["group_id"], name, version, extension)
    local_lib_dir = self.local_lib_directory(details["group_id"], name, version)
    local_loc = self.local_location(details["group_id"], name, version, extension)
    if not self.has_already_been_downloaded(details["group_id"], name, version, extension):
      common.print_info("Downloading " + remote_loc + " to " + local_loc)
      common.run_command(["mkdir", "-p", local_lib_dir])
      self.fetch(remote_loc, local_loc)
    else:
      common.print_verbose("Dependency found at " + local_loc)
    return 0, ""

  def remote_location(self, group_id, artifact_id, version, file_extension):
    group_id_with_slashes = group_id.replace(".", "/")

    if version != "latest":
      return self.base_url + "/".join(
        [group_id_with_slashes, artifact_id, version, artifact_id]) + "-" + version + "." + file_extension
    else:
      metadata_file = self.metadata_local_location(group_id, artifact_id)
      # TODO: If metadata file is present, don't fetch again
      metadata_url = self.base_url + "/".join([group_id_with_slashes, artifact_id]) + "/maven-metadata.xml"
      self.fetch(metadata_url, metadata_file)
      # TODO: Parse metadata file and return the latest version.
      namespaces = {'xmlns': ''}
      tree = ElementTree.parse(metadata_file)
      root = tree.getroot()
      latest_version = root.find(".//latest").text
      self.add_latest_version_to_cache(group_id, artifact_id, version, file_extension, latest_version)
      return self.base_url + "/".join(
        [group_id_with_slashes, artifact_id, latest_version, artifact_id]) + "-" + latest_version + "." + file_extension

  def add_latest_version_to_cache(self, group_id, artifact_id, version, file_extension, latest_version):
    self.latest_versions_cache["_".join([group_id, artifact_id, version, file_extension])] = latest_version

  def get_latest_version_from_cache(self, group_id, artifact_id, version, file_extension):
    key = "_".join([group_id, artifact_id, version, file_extension])
    if key in self.latest_versions_cache:
      return self.latest_versions_cache[key]
    else:
      return "latest"

  def metadata_local_location(self, group_id, artifact_id):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id]) + \
           "/" + "maven-metadata.xml"

  def local_location(self, group_id, artifact_id, version, file_extension):
    v = version
    if version == "latest":
      v = self.get_latest_version_from_cache(group_id, artifact_id, version, file_extension)

    return self.local_lib_directory(group_id, artifact_id, v) + \
           "/" + artifact_id + "-" + v + "." + file_extension

  def local_lib_directory(self, group_id, artifact_id, version):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id, version])

  def fetch(self, remote_loc, local_loc):
    urllib.request.urlretrieve(remote_loc, local_loc)

  def has_already_been_downloaded(self, group_id, artifact_id, version, file_extension):
    return os.path.exists(self.local_location(group_id, artifact_id, version, file_extension))

  def local_pom_exists(self, group_id, artifact_id, version):
    return os.path.exists(self.local_location(group_id, artifact_id, version, "pom"))


class MavenCentralArtifact:
  def __init__(self, group_id, artifact_id, version):
    self.group_id = group_id
    self.artifact_id = artifact_id
    self.specified_version = version
    self.latest_versions_cache = {}

  def version(self):
    if self.specified_version != "latest":
      return self.specified_version
    else:
      return self.latest_version_from_metadata()

  def latest_version_from_metadata(self):
    latest_version_from_cache = self.get_latest_version_from_cache()
    if latest_version_from_cache != "latest":
      return latest_version_from_cache
    else:
      tree = ElementTree.parse(self.metadata_file())
      root = tree.getroot()
      latest_version = root.find(".//latest").text
      self.add_latest_version_to_cache(latest_version)

      return latest_version

  def metadata_file(self):
    metadata_file = self.metadata_local_location(self.group_id, self.artifact_id)
    if os.path.exists(metadata_file):
      return metadata_file
    else:
      group_id_with_slashes = self.group_id.replace(".", "/")
      metadata_url = self.base_url + "/".join([group_id_with_slashes, self.artifact_id]) + "/maven-metadata.xml"
      self.fetch(metadata_url, metadata_file)
      return metadata_file

  def relative_remote_location(self):
    if not self.file_extension:
      common.print_error("File extension is not set for " + self.artifact_id)
      self.file_extension.length

    group_id_with_slashes = self.group_id.replace(".", "/")

    return "/".join(
      [group_id_with_slashes, self.artifact_id, self.version(), self.artifact_id]
    ) + "-" + self.version() + "." + self.file_extension

  def local_location(self):
    return self.local_lib_directory() + \
           "/" + self.artifact_id + "-" + self.version() + "." + self.file_extension

  def local_lib_directory(self):
    group_id_with_slashes = self.group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, self.artifact_id, self.version()])

  def add_latest_version_to_cache(self, latest_version):
    self.latest_versions_cache["_".join([self.group_id, self.artifact_id, self.specified_version, self.file_extension])] = latest_version

  def get_latest_version_from_cache(self):
    key = "_".join([self.group_id, self.artifact_id, self.specified_version, self.file_extension])
    if key in self.latest_versions_cache:
      return self.latest_versions_cache[key]
    else:
      return "latest"

class JarDependency:
  def __init__(self, group_id, artifact_id, version):
    self.group_id = group_id
    self.artifact_id = artifact_id
    self.version = version
    self.pom = Pom(group_id, artifact_id, version)
    self.jar = Jar(group_id, artifact_id, version)
    self.metadata = JarDependencyMetadata(group_id, artifact_id)


  def dependencies(self):
    jar_deps = []
    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
    tree = ElementTree.parse(self.pom.pom_file())
    root = tree.getroot()

    deps = root.findall("./xmlns:dependencies/xmlns:dependency", namespaces=namespaces)
    for d in deps:
      groupId = d.find("xmlns:groupId", namespaces=namespaces).text
      artifactId = d.find("xmlns:artifactId", namespaces=namespaces).text
      version = d.find("xmlns:version", namespaces=namespaces).text
      if version.startswith("${"):
        version = self.pom.resolve_property(version)
      dep = JarDependency(groupId, artifactId, version)
      jar_deps.append(dep)
    return jar_deps

  def __eq__(self, other):
    """Overrides the default implementation"""
    if isinstance(self, other.__class__):
      return self.group_id == other.group_id and self.artifact_id == other.artifact_id and self.version == other.version

    return NotImplemented

  def __hash__(self):
    """Overrides the default implementation"""
    return hash(tuple(sorted([self.group_id, self.artifact_id, self.version])))

  def __repr__(self):
    return "JarDependency[" + self.group_id + "," + self.artifact_id + "," + self.version + "]"


class JarDependencyMetadata:

  def __init__(self, group_id, artifact_id):
    self.group_id = group_id
    self.artifact_id = artifact_id
    self.latest_versions_cache = {}
    self.base_url="https://repo1.maven.org/maven2/"

  def latest_version(self):
    latest_version_from_cache = self.get_latest_version_from_cache()
    if latest_version_from_cache != "latest":
      return latest_version_from_cache
    else:
      tree = ElementTree.parse(self.metadata_file())
      root = tree.getroot()
      latest_version = root.find(".//latest").text
      self.add_latest_version_to_cache(latest_version)

      return latest_version

  def metadata_file(self):
    metadata_file = self.metadata_local_location(self.group_id, self.artifact_id)
    if os.path.exists(metadata_file):
      return metadata_file
    else:
      metadata_url = self.metadata_remote_location()
      self.fetch(metadata_url, metadata_file)
      return metadata_file

  def metadata_local_location(self):
    group_id_with_slashes = self.group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, self.artifact_id]) + \
           "/" + "maven-metadata.xml"

  def metadata_remote_location(self):
    group_id_with_slashes = self.group_id.replace(".", "/")
    return self.base_url + "/".join([group_id_with_slashes, self.artifact_id]) + "/maven-metadata.xml"

  def add_latest_version_to_cache(self, latest_version):
    self.latest_versions_cache["_".join([self.group_id, self.artifact_id, self.specified_version, self.file_extension])] = latest_version

  def get_latest_version_from_cache(self):
    key = "_".join([self.group_id, self.artifact_id, self.specified_version, self.file_extension])
    if key in self.latest_versions_cache:
      return self.latest_versions_cache[key]
    else:
      return "latest"


class Pom(MavenCentralArtifact):

  def __init__(self, group_id, artifact_id, version):
    super().__init__(group_id, artifact_id, version)
    self.file_extension = "pom"

  def pom_file(self):
    return self.local_location()

  def resolve_property(self, property_name):
    prop_name = property_name.strip("${}")

    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
    pom_xml = self.pom_file()
    tree = ElementTree.parse(pom_xml)
    root = tree.getroot()

    common.print_verbose("Looking for property " + prop_name)
    props = root.findall("./xmlns:properties", namespaces=namespaces)
    for el in props[0].iter():
      if el.tag == "{http://maven.apache.org/POM/4.0.0}" + prop_name:
        prop_value = el.text
        common.print_verbose("Found property " + prop_name + " = " + prop_value)
        return prop_value


class Jar(MavenCentralArtifact):

  def __init__(self, group_id, artifact_id, version):
    super().__init__(group_id, artifact_id, version)
    self.file_extension = "jar"

import os, common
import urllib.request
from xml.etree import ElementTree

class CommandLineInstaller:
  def __init__(self, command_base):
    self.command_base = command_base
    return

  def install(self, dep_name, dep_version, details):
    exit_code, output = common.run_command(self.command_base + [dep_name])
    common.stop_if_failed(exit_code, output)

class PipInstaller:
  def __init__(self):
    return

  def install(self, dep_name, dep_version="latest", details={}):
    package_name = dep_name
    if not dep_version == "latest":
      package_name = dep_name + "==" + str(dep_version)
    exit_code, output = common.run_command(['/usr/local/bin/pip3', '-q', 'install', package_name])
    common.stop_if_failed(exit_code, output)

class MavenCentralInstaller:
  # https://search.maven.org/remotecontent?filepath=
  def __init__(self, url_base="https://repo1.maven.org/maven2/", lib_dir="lib"):
    self.url_base = url_base
    self.lib_dir = lib_dir
    return

  def install(self, name, version, details):
    self.install_file(name, version, details, "jar")
    self.install_file(name, version, details, "pom")
    self.install_transitive_dependencies(name, version, details, "pom")

  def install_transitive_dependencies(self, name, version, details, extension):
    namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
    tree = ElementTree.parse(self.local_location(details["group_id"], name, version, extension))
    root = tree.getroot()
    deps = root.findall("./xmlns:dependencies/xmlns:dependency", namespaces=namespaces)
    for d in deps:
      version = "latest"
      groupId = d.find("xmlns:groupId", namespaces=namespaces).text
      artifactId = d.find("xmlns:artifactId", namespaces=namespaces).text
      version_elem = d.find("xmlns:version", namespaces=namespaces)
      if version_elem is not None:
        version = version_elem.text
      self.install(artifactId, version, {"group_id": groupId})

  def install_file(self, name, version, details, extension):
    remote_loc = self.remote_location(details["group_id"], name, version, extension)
    local_lib_dir = self.local_lib_directory(details["group_id"], name, version)
    local_loc = self.local_location(details["group_id"], name, version, extension)
    if not self.has_already_been_downloaded(details["group_id"], name, version, extension):
      common.print_raw("Downloading " + remote_loc + " to " + local_loc)
      common.run_command(["mkdir", "-p", local_lib_dir])
      self.fetch(remote_loc, local_loc)
    else:
      common.print_raw("Dependency found at " + local_loc)
    return 0, ""


  def remote_location(self, group_id, artifact_id, version, file_extension):
    group_id_with_slashes = group_id.replace(".", "/")

    if version != "latest":
      return self.url_base + "/".join([group_id_with_slashes, artifact_id, version, artifact_id]) + "-" + version + "." + file_extension
    else:
      metadata_file = self.metadata_local_location(group_id, artifact_id)
      #TODO: If metadata file is present, don't fetch again
      metadata_url = self.url_base + "/".join([group_id_with_slashes, artifact_id]) + "/maven-metadata.xml"
      self.fetch(metadata_url, metadata_file)
      #TODO: Parse metadata file and return the latest version.
      namespaces = {'xmlns' : ''}
      tree = ElementTree.parse(metadata_file)
      root = tree.getroot()
      latest_version = root.find(".//latest").text
      return self.url_base + "/".join([group_id_with_slashes, artifact_id, latest_version, artifact_id]) + "-" + latest_version + "." + file_extension

  def metadata_local_location(self, group_id, artifact_id):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id]) + \
           "/" + "maven-metadata.xml"

  def local_location(self, group_id, artifact_id, version, file_extension):
    return self.local_lib_directory(group_id, artifact_id, version) + \
           "/" + artifact_id + "-" + version + "." + file_extension

  def local_lib_directory(self, group_id, artifact_id, version):
    group_id_with_slashes = group_id.replace(".", "/")
    return "lib/java/" + "/".join([group_id_with_slashes, artifact_id, version])

  def fetch(self, remote_loc, local_loc):
    urllib.request.urlretrieve(remote_loc, local_loc)

  def has_already_been_downloaded(self, group_id, artifact_id, version, file_extension):
    return os.path.exists(self.local_location(group_id, artifact_id, version, file_extension))

import os, common
import urllib.request


class CommandLineInstaller:
  def __init__(self, command_base):
    self.command_base = command_base
    return

  def install(self, dep_name, dep_version, details):
    exit_code, output = common.run_command(self.command_base + [dep_name])
    common.stop_if_failed(exit_code, output)


class MavenCentralInstaller:
  def __init__(self, url_base="https://search.maven.org/remotecontent?filepath=", lib_dir="lib"):
    self.url_base = url_base
    self.lib_dir = lib_dir
    return

  def install(self, name, version, details):
    remote_loc = self.remote_location(details["group_id"], name, version, "jar")
    local_lib_dir = self.local_lib_directory(details["group_id"], name, version)
    local_loc = self.local_location(details["group_id"], name, version, "jar")
    common.run_command(["mkdir", "-p", local_lib_dir])
    if not self.has_already_been_downloaded(details["group_id"], name, version, "jar"):
      common.print_raw("Downloading " + remote_loc + " to " + local_loc)
      self.fetch(remote_loc, local_loc)
    else:
      common.print_raw("Dependency found at " + local_loc)
    return 0, ""

  def remote_location(self, group_id, artifact_id, version, file_extension):
    group_id_with_slashes = group_id.replace(".", "/")
    return self.url_base + "/".join([group_id_with_slashes, artifact_id, version, artifact_id]) + "-" + version + "." + file_extension

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

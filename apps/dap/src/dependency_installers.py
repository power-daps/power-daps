import common


class CommandLineInstaller:
  def __init__(self, command_base):
    self.command_base = command_base
    return

  def install(self, dep_name, dep_version, details):
    exit_code, output = common.run_command(self.command_base + [dep_name])
    common.stop_if_failed(exit_code, output)


class MavenCentralInstaller:
  def __init__(self, url_base="https://search.maven.org/remotecontent?filepath="):
    self.url_base = url_base
    return

  def install(self, name, version, details):
    return 0, ""
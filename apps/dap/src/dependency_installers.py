import common


class CommandLineInstaller:
  def __init__(self, command_base):
    self.command_base = command_base
    return

  def install(self, dep_name, dep_version):
    exit_code, output = common.run_command(self.command_base + [dep_name])
    common.stop_if_failed(exit_code, output)

import yaml
import common

class Dependencies():
  def __init__(self, dependencies_file_contents):
    self.dependencies_file_contents = dependencies_file_contents
    self.dependencies = dict()
    dependencies_yaml = yaml.load(self.dependencies_file_contents)
    if not dependencies_yaml:
      common.print_verbose("No dependencies found")
      return

    for stage in dependencies_yaml.items():
      stage_name_from_yaml = stage[0]

      # No stages defined
      if not stage_name_from_yaml in self.dependencies:
        self.dependencies[stage_name_from_yaml] = list()

      # Stage is defined but not dependencies listed for the stage
      stage_dependencies_from_yaml = stage[1] if stage[1] else dict()

      for dependency in stage_dependencies_from_yaml.items():
        self.dependencies[stage_name_from_yaml].append(Dependency(name=dependency[0], version=dependency[1]["version"], installer=dependency[1]["installer"]))

    return

  def dependencies_for(self, stage_name):
    return self.dependencies.get(stage_name, list())

class Dependency():
  def __init__(self, name, version, installer):
    self.name = name
    self.version = version
    self.installer = installer
    return

  def __eq__(self, other):
      """Overrides the default implementation"""
      if isinstance(self, other.__class__):
          return self.__dict__ == other.__dict__
      return NotImplemented

  def __ne__(self, other):
      """Overrides the default implementation (unnecessary in Python 3)"""
      x = self.__eq__(other)
      if x is not NotImplemented:
          return not x
      return NotImplemented

  def __hash__(self):
      """Overrides the default implementation"""
      return hash(tuple(sorted(self.__dict__.items())))

  def install_command(self):
    installers = dict()
    installers["pip3"] = ['/usr/local/bin/pip3', '-q']
    installers["brew_cask"] = [common.power_daps_dir() + "bin/brew", 'cask']

    return installers[self.installer] + ['install', self.name]

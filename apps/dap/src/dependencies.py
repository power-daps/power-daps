import yaml
import common
from dependency_installers import CommandLineInstaller, MavenCentralInstaller

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
        dep_name = dependency[0]
        dep_version = dependency[1]["version"]
        dep_installer = dependency[1]["installer"]
        dep_details = dict(dependency[1])
        del dep_details["version"]
        del dep_details["installer"]
        self.dependencies[stage_name_from_yaml].append(\
          Dependency(name=dependency[0], version=dep_version, installer=dep_installer, details=dep_details))

    return

  def dependencies_for(self, stage_name):
    return self.dependencies.get(stage_name, list())

class Dependency():

  def __init__(self, name, version, installer, details=dict()):
    self.name = name
    self.version = version
    self.installer_type = installer
    if len(details) > 0:
      self.details = details
    else:
      self.details = None
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

  def installer(self):
    installers = dict()
    installers["npm"] = CommandLineInstaller(['/usr/local/bin/npm', 'install', '--save-dev'])
    installers["pip3"] = CommandLineInstaller(['/usr/local/bin/pip3', '-q', 'install'])
    installers["brew_cask"] = CommandLineInstaller([common.app_dir() + "deps/bin/brew", 'cask', 'install'])
    installers["jar"] = MavenCentralInstaller()

    return installers[self.installer_type]

  def install(self):
    common.print_raw("Installing '" + self.name + "', " + self.version + " version via " + self.installer_type)
    self.installer().install(self.name, self.version, self.details)

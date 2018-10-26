import yaml
import common

class Dependencies():
  def __init__(self, dapfile_contents):
    self.dapfile_contents = dapfile_contents
    self.dependencies = dict()
    for stage in yaml.load(self.dapfile_contents).items():
      if not stage[0] in self.dependencies:
        self.dependencies[stage[0]] = list()

      for dependency in stage[1].items():
        self.dependencies[stage[0]].append(Dependency(name=dependency[0], version=dependency[1]["version"], installer=dependency[1]["installer"]))

    return

  def dependencies_for(self, stage_name):
    return self.dependencies[stage_name]

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

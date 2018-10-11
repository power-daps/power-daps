
class Dependencies():
  def __init__(self, dapfile_contents):
    return

  def dependencies_for(self, stage_name):
    dependencies = list()
    dependencies.append(Dependency(name="a", version="latest", installer="blah"))
    return dependencies

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

import os
import common
import glob
import dependencies

class DepsAction():
  name = "deps"
  default_dapfile_location = common.dapfile_location()

  def __init__(self, dapfile_location = ""):
    self.set_dapfile_location(dapfile_location)
    return
 
  def run(self):
    deps = dict()
    with open(self.dapfile_location) as f:
      dapfile_contents = f.read()
      deps = dependencies.Dependencies(dapfile_contents)
    f.closed

    for dep in deps.dependencies_for("default"):
      common.stop_if_failed(*common.run_command(self.install_command(dep)))

    return 0, ""

  def set_dapfile_location(self, dapfile_location):
    if dapfile_location:
      self.dapfile_location = dapfile_location
    else:
      self.dapfile_location = DepsAction.default_dapfile_location

  def install_command(self, dependency):
    installers = dict()
    installers["pip3"] = '/usr/local/bin/pip3'
    return [installers[dependency.installer], '-q', 'install', dependency.name]

def action():
   return DepsAction()

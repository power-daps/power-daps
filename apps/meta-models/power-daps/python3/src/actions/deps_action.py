import os
import common
import glob
import dependencies

class DepsAction():
  name = "deps"
  default_dependencies_file_location = common.dependencies_file_location()

  def __init__(self, dependencies_file_location = ""):
    self.set_dependencies_file_location(dependencies_file_location)
    return
 
  def run(self):
    with open(self.dependencies_file_location) as f:
      dependencies_file_contents = f.read()
      self.deps = dependencies.Dependencies(dependencies_file_contents)
    f.closed

    for dep in self.deps.dependencies_for("default"):
      common.stop_if_failed(*common.run_command(self.install_command(dep)))

    return 0, ""

  def set_dependencies_file_location(self, dependencies_file_location):
    if dependencies_file_location:
      self.dependencies_file_location = dependencies_file_location
    else:
      self.dependencies_file_location = DepsAction.default_dependencies_file_location

  def install_command(self, dependency):
    installers = dict()
    installers["pip3"] = '/usr/local/bin/pip3'
    return [installers[dependency.installer], '-q', 'install', dependency.name]

def action():
   return DepsAction()

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
    common.print_verbose("Running " + self.name + " action")

    self.deps = self.load_dependencies(self.dependencies_file_location)

    for dep in self.deps.dependencies_for("default"):
      dep.install()

    return 0, ""

  def load_dependencies(self, dependencies_file_location):
    dependencies_file_contents = ""
    try:
      with open(dependencies_file_location) as f:
        dependencies_file_contents = f.read()
      f.closed
    except (OSError, IOError) as e:
      common.print_warning("No dependencies file found at " + dependencies_file_location)

    return dependencies.Dependencies(dependencies_file_contents)

  def set_dependencies_file_location(self, dependencies_file_location):
    if dependencies_file_location:
      self.dependencies_file_location = dependencies_file_location
    else:
      self.dependencies_file_location = DepsAction.default_dependencies_file_location


def action():
   return DepsAction()

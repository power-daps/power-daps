import os
import common
import glob

class DepsAction():
  name = "deps"

  def __init__(self):
    return
 
  def run(self):
    common.stop_if_failed(*common.run_command(['/usr/local/bin/pip3', '-q', 'install', 'pyinstaller']))
    try:
        os.mkdir(common.app_dir() + "deps/bin")
        os.link('/Library/Frameworks/Python.framework/Versions/3.5/bin/pyinstaller', common.app_dir() + "deps/bin/pyinstaller")
    except FileExistsError:
        common.print_verbose("File already exists")
    return 0, ""

def action():
   return DepsAction()

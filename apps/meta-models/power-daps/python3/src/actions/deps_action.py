import os
import common
import glob

class DepsAction():
  name = "deps"

  def __init__(self):
    return
 
  def run(self):
    common.stop_if_failed(*common.run_command(['/usr/local/bin/pip3', '-q', 'install', 'pyinstaller']))
    common.stop_if_failed(*common.run_command(['/usr/local/bin/pip3', '-q', 'install', 'pyparsing']))
    return 0, ""

def action():
   return DepsAction()

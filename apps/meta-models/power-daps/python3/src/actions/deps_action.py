import common
import glob

def run():
    command = ['/usr/local/bin/pip3', 'install', 'pyinstaller']
    common.run_command(command)

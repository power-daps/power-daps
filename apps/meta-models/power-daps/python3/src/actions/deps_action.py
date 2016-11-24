import os
import common
import glob

def run():
    common.stop_if_failed(*common.run_command(['/usr/local/bin/pip3', 'install', 'pyinstaller']))
    try:
        os.mkdir(common.app_dir() + "deps/bin")
        os.link('/Library/Frameworks/Python.framework/Versions/3.5/bin/pyinstaller', common.app_dir() + "deps/bin/pyinstaller")
    except FileExistsError:
        common.print_verbose("File already exists")
    return 0, ""

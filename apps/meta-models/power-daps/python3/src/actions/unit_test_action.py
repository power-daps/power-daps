import common
import glob

def run():
    tests = []
    for filename in glob.iglob('**/test/**/*.py', recursive=True):
        tests.append(filename)
    command = ['/usr/local/bin/python3', '-m', 'unittest']
    command.extend(tests)
    return common.run_command(command)

import glob, os, sys
import common

class UnitTestAction():
  name = "unit_test"

  def __init__(self):
    return

  def run(self):
    exit_code = 0
    for test_dir in glob.iglob('**/test', recursive=True):
      original_working_directory = os.getcwd()
  
      run_directory = os.path.join(original_working_directory, str(test_dir))
      common.print_info("Running tests in " + str(run_directory))
      common.print_verbose("Changing directory to " + str(run_directory))
      os.chdir(run_directory)
  
      tests = []
      for filename in glob.iglob('**/*.py', recursive=True):
          tests.append(filename)
      command = ['/usr/local/bin/python3', '-m', 'unittest']
      command.extend(tests)
      subprocess_exit_code, output = common.run_command(command)
      if subprocess_exit_code != common.SUCCESS:
        exit_code = common.FAILED
      common.print_verbose(output)
      common.continue_if_failed(subprocess_exit_code, output)
  
      common.print_verbose("Changing directory to " + str(original_working_directory))
      os.chdir(original_working_directory) 
    
    return exit_code, ""

def action():
   return UnitTestAction()


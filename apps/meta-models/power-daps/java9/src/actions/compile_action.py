import common


class CompileAction:
  name = "compile"

  def __init__(self, source_dir="src", target_dir="target/production", classpath=""):
    self.source_dir = source_dir
    self.target_dir = target_dir
    self.classpath = classpath

  def run(self):
    common.print_verbose("Running " + self.name + " action")

    cp_string = ""
    if self.classpath != "":
      cp_string = " -cp " + self.classpath

    common.run_command_in_shell('rm -rf ' + self.target_dir)
    common.run_command_in_shell('mkdir -p ' + self.target_dir)
    common.run_command_in_shell('find ' + self.source_dir + \
                                ' -type f -name "*.java" -print | xargs javac ' + \
                                cp_string + " " + \
                                ' -d ' + self.target_dir + ' -sourcepath ' + self.source_dir)
    return 0, ""


def action():
  return CompileAction()

import common


class CompileTestAction:
  name = "compile_test"

  def __init__(self, source_dir="test", target_dir="target/test", classpath=".:target/production"):
    self.source_dir = source_dir
    self.target_dir = target_dir
    self.classpath = classpath

  def run(self):
    common.print_verbose("Running " + self.name + " action")
    cp_string = ""
    if self.classpath != "":
      cp_string = " -cp " + self.classpath + ":" + self.libs_classpath()
    else:
      cp_string = " -cp " + self.libs_classpath()

    common.run_command_in_shell('rm -rf ' + self.target_dir)
    common.run_command_in_shell('mkdir -p ' + self.target_dir)
    common.run_command_in_shell('find ' + self.source_dir + \
                                ' -type f -name "*.java" -print | xargs javac ' + \
                                cp_string + " " + \
                                ' -d ' + self.target_dir + ' -sourcepath ' + self.source_dir)
    return 0, ""

  def libs_classpath(self):
    libs = common.run_command_in_shell('find lib/java -type f -name "*.jar" -print')[1]
    return ":".join(libs.splitlines())

def action():
  return CompileTestAction()

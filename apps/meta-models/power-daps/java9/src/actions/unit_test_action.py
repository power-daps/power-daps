import common


class UnitTestAction:
  name = "unit_test"

  def __init__(self, source_dir="test", target_dir="target/test", classpath=".:target/production:target/test"):
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

    common.run_command_in_shell('mkdir -p ' + self.target_dir)
    exit_code, output = common.run_command_in_shell('java ' + \
                                cp_string + " " + \
                                'org.junit.runner.JUnitCore ' + \
                                " ".join(self.list_of_test_classes()))

    common.print_raw(output)
    return 0, ""

  def libs_classpath(self):
    libs = common.run_command_in_shell('find lib/java -type f -name "*.jar" -print')[1]
    return ":".join(libs.splitlines())

  def list_of_test_classes(self):
    test_classes = common.run_command_in_shell('find test -type f -name "*Test.java" -print')[1].splitlines()
    return [ test_class.replace("test/", "").replace(".java", "").replace("/", ".") for test_class in test_classes ]

def action():
  return UnitTestAction()

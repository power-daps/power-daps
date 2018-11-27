import os, sys, inspect
import unittest
from unittest.mock import MagicMock

dap_src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../../../../dap/src")))
src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src/actions")))


if dap_src_dir not in sys.path:
  sys.path.insert(0, dap_src_dir)

if src_dir not in sys.path:
  sys.path.insert(0, src_dir)

if actions_dir not in sys.path:
  sys.path.insert(0, actions_dir)

import common, init_action

from meta_model import MetaModel

class TestInitAction(unittest.TestCase):
  def test_copies_init_template(self):
    common.run_command = MagicMock()
    init_action.action().run()
    mm = MetaModel(common.meta_model())
    expected_command = ["/bin/cp", "-R", mm.template_for_action("init") + "/*", '.']
    common.run_command.assert_called_once()


if __name__ == '__main__':
  unittest.main()

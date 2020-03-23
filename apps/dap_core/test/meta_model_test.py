#  Copyright 2016-2020 Prasanna Pendse <prasanna.pendse@gmail.com>
# 
#  This file is part of power-daps.
# 
#  power-daps is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  power-daps is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with power-daps.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

from dap_core import common
from dap_core.meta_model import MetaModel

class TestMetaModel(unittest.TestCase):
  def test_self_awareness(self):
    meta_model = MetaModel("power_daps/python3")
    self.assertEqual("power_daps/python3", meta_model.name())

  def test_actions_loads_actions_from_actions_dir(self):
    meta_model = MetaModel("power_daps/python3")
    actions_dir = "dir"
    meta_model.actions_dir = MagicMock(return_value = actions_dir)
    meta_model.load_actions_from_dir = MagicMock(return_value = "some actions")
    actions = meta_model.actions()
    meta_model.load_actions_from_dir.assert_called_with(actions_dir)
    self.assertEqual("some actions", actions)

  def test_can_actually_load_actions(self):
    meta_model = MetaModel("power_daps/python3")
    actions = meta_model.actions()
    self.assertGreater(len(actions), 0)
    for action in actions:
      self.assertIs(type(action.run), type(self.test_can_actually_load_actions))


  def test_non_existent_metamodel_fails_gracefully(self):
    common.exit_with_error_message = self.assert_called_with_string_containing("Meta-model 'non-existent' not found")

    meta_model = MetaModel("non-existent")
    actions = meta_model.actions()

  def test_invalid_metamodel_fails_gracefully(self):
    common.exit_with_error_message = self.assert_called_with_string_containing("no actions found")

    meta_model = MetaModel("invalid")
    old_actions_dir = meta_model.actions_dir
    meta_model.actions_dir = MagicMock()
    meta_model.actions_dir.return_value = "."
    actions = meta_model.actions()
    meta_model.actions_dir = old_actions_dir

  def test_actions_found_in_returns_the_right_actions(self):
    meta_model = MetaModel("power_daps/python3")
    actions_found_in_meta_model = meta_model.actions_found_in(meta_model.actions_dir() + "/actions")
    assert "default" in actions_found_in_meta_model, \
      "'%s' does not contain '%s'" % (actions_found_in_meta_model, "default")
    self.assertEqual(8, len(actions_found_in_meta_model))

  def test_template_for_action(self):
    meta_model = MetaModel("power_daps/java9")
    template_for_init = meta_model.template_for_action("init")
    assert "templates/init" in template_for_init, "'%s' does not contain '%s'" % (template_for_init, "templates/init")



  def assert_called_with_string_containing(self, expected_substring):
    def wrapper(arg):
      assert str(expected_substring) in arg, "'%s' does not contain '%s'" % (arg, expected_substring)
    return wrapper


if __name__ == '__main__':
  unittest.main()

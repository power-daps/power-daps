import os, sys, inspect
import unittest
from unittest.mock import MagicMock

src_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))

if src_dir not in sys.path:
     sys.path.insert(0, src_dir)

import common
from meta_model import MetaModel

class TestMetaModel(unittest.TestCase):
  def test_self_awareness(self):
    meta_model = MetaModel("power-daps/python3")
    self.assertEqual("power-daps/python3", meta_model.name())

  def test_actions_loads_actions_from_actions_dir(self):
    meta_model = MetaModel("power-daps/python3")
    actions_dir = "dir"
    meta_model.actions_dir = MagicMock(return_value = actions_dir)
    meta_model.load_actions_from_dir = MagicMock(return_value = "some actions")
    actions = meta_model.actions()
    meta_model.load_actions_from_dir.assert_called_with(actions_dir)
    self.assertEqual("some actions", actions)

  def test_can_actually_load_actions(self):
    meta_model = MetaModel("power-daps/python3")
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




  def assert_called_with_string_containing(self, expected_substring):
    def wrapper(arg):
      assert str(expected_substring) in arg, "'%s' does not contain '%s'" % (arg, expected_substring)
    return wrapper

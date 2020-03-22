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

from dap_core import common
import yaml
from meta_model import MetaModel
from no_action_error import NoActionError


class DefaultAction:
  name = "default"
  default_actions_file_location = common.actions_file_location()

  def __init__(self, actions_file_location = ""):
    self.set_actions_file_location(actions_file_location)
    return

  def run(self):
    common.print_verbose("Running " + self.name + " action")

    with open(self.actions_file_location) as f:
      actions_file_contents = f.read()
      for stage in yaml.load(actions_file_contents, Loader=yaml.SafeLoader).items():
        for an_action in stage[1]:
          common.stop_if_failed(*self.action_for(an_action).run())
    f.closed
    return 0, ""

  def action_for(self, action_name):
    meta_model = MetaModel("power_daps/java9")
    the_actions = list(filter(lambda a: a.name==action_name, meta_model.actions()))
    the_actions
    if the_actions:
      return the_actions[0]
    else:
      return NoActionError(action_name)

  def set_actions_file_location(self, actions_file_location):
    if actions_file_location:
      self.actions_file_location = actions_file_location
    else:
      self.actions_file_location = DefaultAction.default_actions_file_location


def action():
  return DefaultAction("./actions.yml")


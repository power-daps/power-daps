#!/usr/bin/env python

import os, sys, inspect, importlib

import common
from meta_model import MetaModel

def main(log_level="info", meta_model_name="power-daps/python3", actions_to_run=["default"]):
    common.set_log_level(log_level)
    meta_model = MetaModel(meta_model_name)
    common.set_meta_model(meta_model_name)

    valid_actions = meta_model.actions()

    # actions_dir = common.actions_dir()
    # if actions_dir not in sys.path:
      # sys.path.insert(0, actions_dir)

    for action_to_run in actions_to_run:
      for valid_action in valid_actions:
        if valid_action.name == action_to_run:
          action_module = importlib.import_module("actions." + valid_action.name + "_action")
          common.stop_if_failed(*action_module.run())

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="dap")
    parser.add_argument("-q", "--quiet", dest="log_level",
                        default="info", action="store_const",
                        const="error")
    parser.add_argument("-m", "--meta-model", dest="meta_model",
                        default="power-daps/python3",
                        help="Use the specified meta-model. Defaults to 'power-daps/python3'")
    parser.add_argument("action",
        help="List of actions to run. Defaults to 'default' for the given meta-model",
        default=["default"], nargs="*")

    args = parser.parse_args()

    main(args.log_level, args.meta_model, args.action)
    sys.exit(common.exit_code())

#!/usr/bin/env python

import common
import os, sys, inspect, importlib

def main(meta_model=None, actions=["default"]):
    common.set_meta_model(meta_model)

    actions_dir = common.actions_dir()
    if actions_dir not in sys.path:
      sys.path.insert(0, actions_dir)

    for action in actions:
      action_module = importlib.import_module("actions." + action + "_action")
      common.stop_if_failed(*action_module.run())

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="dap")
    parser.add_argument("-m", "--meta-model", dest="meta_model",
                        default="power-daps/python3",
                        help="Use the specified meta-model. Defaults to 'power-daps/python3'")
    parser.add_argument("action",
        help="List of actions to run. Defaults to 'default' for the given meta-model",
        default=["default"], nargs="*")

    args = parser.parse_args()

    main(args.meta_model, args.action)
    sys.exit(common.exit_code())

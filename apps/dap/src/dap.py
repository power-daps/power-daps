#!/usr/bin/env python

import common
import os, sys, inspect

actions_dir = common.actions_dir()
if actions_dir not in sys.path:
     sys.path.insert(0, actions_dir)

import actions
from actions import deps_action, unit_test_action, package_action

def main(argv):
    deps_action.run()
    unit_test_action.run()
    package_action.run()


if __name__ == '__main__':
    main(sys.argv[1:])

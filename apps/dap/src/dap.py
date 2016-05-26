#!/usr/bin/env python

import common
import os, sys, inspect


actions_dir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../meta-models/" + common.meta_model() + "/src")))

if actions_dir not in sys.path:
     sys.path.insert(0, actions_dir)

import actions
from actions import run_test

def run_action(action):
    actions.run_test.run()

def main(argv):
    run_action("test")


if __name__ == '__main__':
    main(sys.argv[1:])

#!/usr/bin/env python

import common
import sys
import actions

from actions import run_test

def run_action(action):
    run_test.run()

def main(argv):
    run_action("test")


if __name__ == '__main__':
    main(sys.argv[1:])

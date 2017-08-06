import os, inspect, sys, importlib
import common

def run(name):
  action_module = importlib.import_module("actions." + name + "_action")
  common.stop_if_failed(*action_module.action().run())
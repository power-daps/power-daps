#!/usr/bin/env python

import os, sys, getopt, subprocess, inspect

log_level = "info"
FAILED = 1
SUCCESS = 0
saved_exit_code = SUCCESS
saved_meta_model = None

def run_command( command ):
    subprocess_exit_code = SUCCESS
    output = ""

    print_verbose("Running command " + str(command))
    try:
        output = subprocess.check_output(command).decode("utf-8")
        if output:
            print_info(output)
    except FileNotFoundError as e:
        subprocess_exit_code = e.errno
        output = e.strerror
        print_error("Exit code: " + str(subprocess_exit_code))
        print_error(output)
    except subprocess.CalledProcessError as e:
        subprocess_exit_code = e.returncode
        print_error("Exit code: " + str(subprocess_exit_code))
        if output:
          print_error(output)
    return subprocess_exit_code, output

def print_warning(warning):
    global log_level
    if(log_level == "verbose" or log_level == "info" or log_level == "warning"):
       print_raw("WARNING: " + warning)

def print_error(error):
    if(log_level == "verbose" or log_level == "info" or log_level == "warning" or log_level == "error"):
      print_raw("ERROR: " + error)

def print_info(info):
    if(log_level == "verbose" or log_level == "info"):
      print_raw("INFO: " + info)

def print_raw(s):
    print(s)

def print_info_no_eol(info):
    sys.stdout.write(info)

def print_verbose(verbose_info):
    if(log_level == "verbose"):
        print_raw("VERBOSE: " + verbose_info)

def print_verbose_no_eol(verbose_info):
    if(log_level == "verbose"):
        sys.stdout.write(verbose_info)

def stop_if_failed(subprocess_exit_code=SUCCESS, error_message=""):
    if(subprocess_exit_code != SUCCESS):
        sys.exit(FAILED)

def continue_if_failed(subprocess_exit_code=SUCCESS, error_message=""):
    global saved_exit_code
    if(subprocess_exit_code != SUCCESS):
        saved_exit_code = FAILED

def exit_code():
    return saved_exit_code

def set_log_level(log_level_to_set):
    global log_level
    log_level = log_level_to_set

def set_meta_model(meta_model):
    global saved_meta_model
    saved_meta_model = meta_model

def meta_model():
    global saved_meta_model
    if(saved_meta_model == None):
      saved_meta_model = os.getenv("POWER_DAPS_META_MODEL", "power-daps/python3")
    return saved_meta_model

def power_daps_dir():
    return os.path.dirname(os.path.abspath(__file__)) + "/../../../"

def app_dir():
    return power_daps_dir() + "apps/dap/"

def actions_dir():
    ret_val = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../meta-models/" + meta_model() + "/src")))
    return ret_val

if __name__ == '__main__':
    print_error("This module " + __file__ + " cannot be run as a stand alone command")
    sys.exit(1)


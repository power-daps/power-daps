#!/usr/bin/env python

import os, sys, getopt, subprocess, inspect

verbose = False
FAILED = 1
SUCCESS = 0
saved_exit_code = SUCCESS

def run_command( command ):
    subprocess_exit_code = SUCCESS
    output = ""
    print_info("Running command " + str(command))
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
    print_raw("WARNING: " + warning)


def print_error(error):
    print_raw("ERROR: " + error)

def print_info(info):
    print_raw("INFO: " + info)

def print_raw(s):
    print(s)

def print_info_no_eol(info):
    sys.stdout.write(info)

def print_verbose(verbose_info):
    if verbose == True:
        print_info(verbose_info)

def print_verbose_no_eol(verbose_info):
    if verbose == True:
        print_info_no_eol(verbose_info)

def stop_if_failed(subprocess_exit_code=SUCCESS, error_message=""):
    if(subprocess_exit_code != SUCCESS):
        sys.exit(FAILED)

def continue_if_failed(subprocess_exit_code=SUCCESS, error_message=""):
    global saved_exit_code
    print_info("HELLO!!! " + str(subprocess_exit_code))
    if(subprocess_exit_code != SUCCESS):
        saved_exit_code = FAILED

def exit_code():
    return saved_exit_code

def meta_model():
    return os.getenv("POWER_DAPS_META_MODEL", "power-daps/python3")

def app_dir():
    return "/Users/ppendse/src/power-daps/apps/dap/"

def actions_dir():
    ret_val = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../meta-models/" + meta_model() + "/src")))
    return ret_val

if __name__ == '__main__':
    print_error("This module " + __file__ + " cannot be run as a stand alone command")
    sys.exit(1)


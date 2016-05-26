#!/usr/bin/env python

import os, sys, getopt, subprocess

verbose = False

def run_command( command ):
    exit_code = 0
    output = ""
    print_info("Running command " + str(command))
    try:
        output = str(subprocess.check_output(command))
        if not output:
            print_info(output)
    except subprocess.CalledProcessError as e:
        exit_code = e.returncode
        print_error("Exit code: " + str(e.returncode))
    return (exit_code, output)


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

def meta_model():
    return os.getenv("POWER_DAPS_META_MODEL", "power-daps/python3")

if __name__ == '__main__':
    print_error("This module " + __file__ + " cannot be run as a stand alone command")
    sys.exit(1)


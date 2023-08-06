#!/usr/bin/env python3
############################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019-2021 Lauro Sumoy Lab, IGTP, Spain   ##
############################################################

#######
def get_require_modules(given_file):
    """
    Get main python requirements modules
    """
    with open(given_file, 'r') as f:
        myModules = [line.strip().split(',')[0] for line in f]
    
    return myModules

#######
def get_version(version_file):
    """
    Original code: PhiSpy setup.py 
    https://github.com/linsalrob/PhiSpy/blob/master/setup.py
    """
    with open(version_file, 'r') as f:
        v = f.readline().strip()
    return v
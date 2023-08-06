#!/usr/bin/env python3
############################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019-2020 Lauro Sumoy Lab, IGTP, Spain   ##
############################################################
"""
Shared functions used along ``BacterialTyper`` & ``XICRA`` pipeline.
With different purposes:
    - Print time stamps
  
    - Create system calls

    - Manage/list/arrange files/folders

    - Aesthetics

    - Manage fasta files

    - Other miscellaneous functions
"""
## useful imports
import time
from datetime import datetime


## my modules
from HCGB.functions import aesthetics_functions

###########################
##      TIME            ###
###########################

###############   
def print_time ():
    """Prints time stamp in human readable format: month/day/year, hour:minute:seconds."""
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print ('\t' + date_time + '\n')

###############   
def gettime (start_time):
    """Obtains time stamp in human readable format: hour:minute:seconds from a time.time() format timestamp."""
    total_sec = time.time() - start_time
    m, s = divmod(int(total_sec), 60)
    h, m = divmod(m, 60)
    return h, m, s

###############    
def timestamp (start_time_partial):
    """Prints a stamp of the time spent for a process in human readable format: hour:minute:seconds.
    Returns time in format time.time().
    """
    h,m,s = gettime(start_time_partial)
    aesthetics_functions.print_sepLine("-", 25, False)
    print ('(Time spent: %i h %i min %i s)' %(int(h), int(m), int(s)))
    aesthetics_functions.print_sepLine("-", 25, False)
    return time.time()

###############    
def print_time_stamp (out):
    """Prints out timestamp in a file provided. Format: time.time()"""
    timefile = open(out, 'w')    
    string2write = str(time.time())
    timefile.write(string2write)
    return()

###############    
def read_time_stamp (out):
    """Reads timestamp from a file provided. Format: time.time()"""
    st_hd = open(out, 'r')
    st = st_hd.read()
    st_hd.close()
    stamp = datetime.fromtimestamp(float(st)).strftime('%Y-%m-%d %H:%M:%S')
    return(stamp)

###############    
def get_diff_time(stamp_file):
    """Obtains the time spent for a process in days given a stamp in time.time() format.
    Returns days passed since.
    """
    time_today = time.time()
    st_hd = open(stamp_file, 'r')
    stamp = st_hd.read()
    st_hd.close()
    elapsed = float(stamp) - time_today
    days_passed = abs(round((elapsed/3600)/24))
    
    return(days_passed)

###############    
def create_human_timestamp():
    """Generates human timestamp for the date of day in format (yearmonthday): e.g. 20191011"""
    now = datetime.now()
    timeprint = now.strftime("%Y%m%d")
    return timeprint
###############

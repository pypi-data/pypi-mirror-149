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
import subprocess
import wget
from termcolor import colored
##from filehash import FileHash ## FIXME: not conda supported
import os

#################################
##         system call        ###
#################################

###############
def system_call(cmd, returned=False, message=True):
    """Generates system call using subprocess.check_output"""
    ## call system
    ## send command
    if (message):
        print (colored("[** System: %s **]" % cmd, 'magenta'))

    try:
        out = subprocess.check_output(cmd, shell = True)
        if (returned):
            return (out)
        return ('OK')
    except subprocess.CalledProcessError as err:
        if (returned):
            return (err.output)
        if (message):
            print (colored("** ERROR **", 'red'))
            print (colored(err.output, 'red'))
            print (colored("** ERROR **", 'red'))
        
        return ('FAIL')

###############
def wget_download(url, path):
    """
    Downloads file in the given path.
    
    It uses python module wget to download given ``url`` in the ``path`` provided.
    
    :param url: File to download from http/ftp site.
    :param path: Absolute path to the folder where to save the downloaded file.
    :type url: string
    :type path: string  
    
    :returns: Print messages and generates download
    """
    
    print ('\t+ Downloading: ', url)
    wget.download(url, path)
    print ('\n')

###############
def check_md5sum(string, File):
    ## FIXME: Not conda supported
    return(True)

#    md5hasher = FileHash('md5')
#    md5_file = md5hasher.hash_file(File) 
#    
#    if (md5_file == string):
#        #print (md5_file + '==' + string)
#        return (True)
#    else:
#        return (False)

###############
def chmod_rights(file, access_rights):
    """Changes access permission of a file:
    
    Read additional information in:
    https://docs.python.org/3/library/os.html#os.chmod
    https://www.geeksforgeeks.org/python-os-chmod-method/
    """
    access = os.chmod(file, access_rights, follow_symlinks=True)
    return(access)

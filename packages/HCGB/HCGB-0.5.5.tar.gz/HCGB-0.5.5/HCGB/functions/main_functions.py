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
import sys
import os
import pandas as pd
import urllib.request
import json

from HCGB import functions

###################################
##     General main functions    ##
###################################

#################
def print_all_pandaDF(pd_df):
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    print (pd_df)

#################
def printList2file(fileGiven, listGiven):
    """Prints list given in the output file provided. One item per row."""
    file_hd = open(fileGiven, 'w')
    file_hd.write("\n".join(listGiven))
    file_hd.close()

#################
def printDict2file(fileGiven, dictGiven, split_char):
    """Prints dictionary given in the output file provided. One item per row."""
    with open(fileGiven, 'w') as file_hd:
        for key in dictGiven.keys():
            file_hd.write("%s%s%s\n"%(key, split_char, dictGiven[key]))
    file_hd.close()

#################
def readList_fromFile(fileGiven):
    """Reads list from the input file provided. One item per row."""
    # open file and read content into list
    lineList = [line.rstrip('\n') for line in open(fileGiven)]
    return (lineList)

###########
def retrieve_matching_files(folder, string, debug=False, starts=False):
    """Lists folder path provided and given a string to search, returns all files ending with the given string"""
    my_all_list = get_fullpath_list(folder)
    if starts:
        matching = [s for s in my_all_list if s.startswith(string)]
    else:
        matching = [s for s in my_all_list if s.endswith(string)]
        
        
    return (matching)

##########
def file2dictionary(file2read, split_char):
    """Read file and generate a dictionary"""
    d = {}
    with open(file2read) as f:
        for line in f:
            line = line.rstrip('\n')
            (key, val) = line.split(split_char)
            d[key] = val

    return(d)

###############
def file2dataframe(file2read, names):
    ## TODO: check if duplicated with get_data function
    """Read csv file into pandas dataframe"""
    d = pd.read_csv(file2read, comment="#", names=names)
    return(d)

#################
def get_fullpath_list(dir_given, debug=False):
    """Retrieve full absolute path for the files within a directory specified.

    :param dir_given: Directory to retrieve files
    :type dir_given: string

    :returns: List of absolute path files.
    """
    return_path = []
    for root, dirs, files in os.walk(dir_given):
        for f in files:
            return_path.append(os.path.join(root,f))

    ## returns list of files
    return return_path

###############
def get_data(ID_file, SEP, options):    
    if options == 'index_col=0':
        data = pd.read_csv(ID_file, sep=SEP, index_col=0)
        return(data)
    elif options == 'header=None':
        data = pd.read_csv(ID_file, sep=SEP, header=None)
        return(data)    
    else:
        data = pd.read_csv(ID_file, sep=SEP)
        return(data)
    ## fix for another example if any
    
###############
def get_number_lines(input_file):    
    with open(input_file) as foo:
        lines = len(foo.readlines())
    foo.close()
    return (lines)

###############
def get_info_file(input_file):    
    with open(input_file) as f:
        lines = f.read().splitlines() 
    f.close()
    return (lines)
          
#################
def optimize_threads(total, samples):
    cpu = int(int(total)/int(samples))
    
    if (cpu==0): ## 5 availabe cpus for 10 samples == 0 cpu
        cpu = 1
    
    return(cpu)

#################
def parse_sublist(lst, ind): 
    ## extract elemnts of the list
    ## Original Code: https://www.geeksforgeeks.org/python-get-first-element-of-each-sublist/
    return [item[ind] for item in lst]

##################
def decode(x):
    """
    Python decode string method

    It converts bytes to string.

    :param x: String of text to decode
    :type x: string
    :returns: Text decoded

    .. attention:: Be aware of Copyright

        The code implemented here was retrieved and modified from ARIBA (https://github.com/sanger-pathogens/ariba)

        Give them credit accordingly.
    """
    try:
        s = x.decode()
        return s
    except:
        return x

##################
def urllib_request(folder, url_string, file_name, debug):
    
    file_name_unzipped="n.a."
    zipped=False
    
    ## add more compression types if necessary
    if file_name.endswith('gz'):
        zipped=True
        file_name_unzipped = file_name.split('.gz')[0]
    else:
        file_name_unzipped = file_name    
    ### debugging messages
    if debug:
        print ("folder: ", folder)
        print ("url_string: ",url_string)
        print ("file_name:", file_name)
        print ("Zip: ", zipped)
        print ("file_name_unzipped: ", file_name_unzipped)
        
    ##
    url_string = url_string + file_name
        
    
    ## timestamp
    filename_stamp = folder + '/.success'
    file_path_name = os.path.join(folder, file_name)
    file_path_name_unzipped = os.path.join(folder, file_name_unzipped)
    
    ## check if previously exists
    if os.path.exists(file_path_name) or os.path.exists(file_path_name_unzipped):
        ## debug message
        if debug:
            print ("## Debug: File %s exists in folder" %file_name)
    
        ## check if previously timestamp generated
        if os.path.isfile(filename_stamp):
            stamp = functions.time_functions.read_time_stamp(filename_stamp)
            print ("\tFile (%s) Previously downloaded in: %s" %(file_name, stamp))
            return(file_path_name_unzipped)

    ## debug message
    if debug:
        print ("## Debug: Download file: ", file_name, ":: ", url_string)
    
    # downloads
    urllib.request.urlretrieve(url_string, file_path_name )
    
    ## check if correctly download
    if os.path.exists(file_path_name):
        functions.time_functions.print_time_stamp(filename_stamp)
    else:
        sys.exit('Could not download file %s (%s)' %(file_name, url_string))

    ## extract if zipped
    if (zipped):
        functions.files_functions.extract(file_path_name, out=folder)
        return (file_path_name_unzipped)
        
    else:
        return(file_path_name)

###################
def create_excel_file(file_name, dict_data, SEP=",", options="index_col=0", debug=False):
    '''
    :param file_name: Absolute file path name for the file to write in xlsx format.
    :param dict_data: Dictionary containing as key the name for the tab and as a value an absolute file path to dump in each tab.
    '''
    
    ## write to excel
    writer_Excel = pd.ExcelWriter(file_name, engine='xlsxwriter') ## open excel handle
    
    ## loop over dictionary and print dataframe
    for name, each_data in dict_data.items():
        if debug:
            print ("Name: ", name)
            print ("Data: ", each_data)
            
        each_df = get_data(each_data, SEP, options)
        each_df.to_excel(writer_Excel, sheet_name=name) ## write excel handle
            
    writer_Excel.save() ## close excel handle

######################################
def read_json_file(file, debug=False):
    """Read information in json format"""

    if debug:
        functions.aesthetics_functions.debug_message("Read JSON information:", 'yellow')
        functions.aesthetics_functions.debug_message("file: " + file, 'yellow')
    
    with open(file) as json_file:
        data=json.load(json_file)

    if debug:
        print(data)
    
    ## return json
    return (data)
    
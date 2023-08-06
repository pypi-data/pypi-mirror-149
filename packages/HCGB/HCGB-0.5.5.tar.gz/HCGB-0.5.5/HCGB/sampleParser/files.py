#!/usr/bin/ python3
##########################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019 Lauro Sumoy Lab, IGTP, Spain        ##
##########################################################
"""
Get information from files
"""

import os
import re
import pandas as pd
from termcolor import colored

from HCGB import functions
from HCGB import sampleParser
from HCGB.functions.aesthetics_functions import debug_message 

###############
def get_fields(file_name_list, pair, Debug, include_all):
    """
    Get information from files
    
    Creates and returns a dataframe containing information for each sample for:
    "sample", "dirname", "name", "new_name", "name_len", "lane", "read_pair","lane_file","ext","gz", "tag"
    
    :param file_name_list: List of files to parse
    :param pair: True/false for Paired-end files
    :param Debug: True/false for debugging messages
    
    :type file_name_list: list
    :type pair: bool
    :type Debug: bool
    
    :returns: Pandas dataframe.
    
    """
    ## init dataframe
    name_columns = ("sample", "dirname", "name", "new_name", "name_len", 
                "lane", "read_pair","lane_file","ext","gz", "tag", "file")
    name_frame = pd.DataFrame(columns=name_columns)
    
    ## loop through list
    for path_files in file_name_list:
        ## get file name
        file_name = os.path.basename(path_files)
        dirN = os.path.dirname(path_files)
        trim_search = re.search(r".*trim.*", file_name)
        lane_search = re.search(r".*\_L\d+\_.*", file_name)
        
        ### declare
        name= ""
        lane_id= ""
        read_pair= ""
        lane_file= ""
        ext= ""
        gz= ""
        
        ## get name
        if (include_all):
            if (pair):
                if (trim_search):
                    name_search = re.search(r"(.*)\_trim\_(R1|1|R2|2)\.(f.*q)(\..*){0,1}", file_name)
                else:
                    name_search = re.search(r"(.*)\_(R1|1|R2|2)\_{0,1}(.*)\.(f.*q)(\..*){0,1}", file_name)
            
                lane_id = ""
                read_pair = name_search.group(2)
                lane_file = name_search.group(3)
                ext = name_search.group(4)
                gz = name_search.group(5)
            
            else:
                if (trim_search):
                    name_search = re.search(r"(.*)\_trim(.*)\.(f.*q)(\..*){0,1}", file_name) ## trim.fastq or trim_joined.fastq
                else:
                    name_search = re.search(r"(.*)\.(f.*q)(\..*){0,1}", file_name)
                
                ext = name_search.group(2)
                gz = name_search.group(3)
                
        else:    
            if (pair):
                ## pair could be: R1|R2 or 1|2
                if (trim_search):
                    name_search = re.search(r"(.*)\_trim\_(R1|1|R2|2)\.(f.*q)(\..*){0,1}", file_name)
                    
                    read_pair = name_search.group(2)
                    ext = name_search.group(3)
                    gz = name_search.group(4)
                    
                else:
                    ## Lane files: need to merge by file_name: 33i_S5_L004_R1_001.fastq.gz
                    ## lane should contain L00x            
                    if (lane_search):
                        name_search = re.search(r"(.*)\_(L\d+)\_(R1|1|R2|2)\_{0,1}(.*)\.(f.*q)(\..*){0,1}", file_name)

                        lane_id = name_search.group(2)
                        read_pair = name_search.group(3)
                        lane_file = name_search.group(4)
                        ext = name_search.group(5)
                        gz = name_search.group(6)
                        
                    else:
                        name_search = re.search(r"(.*)\_(R1|1|R2|2)\.(f.*q)(\..*){0,1}", file_name)
                        
                        read_pair = name_search.group(2)
                        ext = name_search.group(3)
                        gz = name_search.group(4)
            else:
                if (trim_search):
                    if (lane_search):
                        name_search = re.search(r"(.*)\_(L\d+)\_{0,1}(.*)\.(f.*q)(\..*){0,1}", file_name)

                        lane_id = name_search.group(2)
                        lane_file = name_search.group(3)
                        ext = name_search.group(4)
                        gz = name_search.group(5)

                    else:
                        name_search = re.search(r"(.*)\_trim(.*)\.(f.*q)(\..*){0,1}", file_name) ## trim.fastq or trim_joined.fastq
                    
                        ext = name_search.group(2)
                        gz = name_search.group(3)
                else:
                    name_search = re.search(r"(.*)\.(f.*q)(\..*){0,1}", file_name)
                    
                    ext = name_search.group(2)
                    gz = name_search.group(3)
        
        if name_search:
            name = name_search.group(1)
            name_len = len(name)
            
            if (Debug):
                debug_message("Search for sample names: ")
                debug_message("File: " + path_files)
                debug_message("Name: " + name_search.group(1))
                debug_message("Lane: " + lane_id)
                debug_message("Pair: " + read_pair)
                debug_message("Lane file: " + lane_file)
                debug_message("Ext: " + ext)
                debug_message(gz)
    
            # if (pair):
            #     if (include_all):
            #         lane_id = ""
            #         read_pair = name_search.group(2)
            #         lane_file = name_search.group(3)
            #         ext = name_search.group(4)
            #         gz = name_search.group(5)
            #
            #     ## Lane files: need to merge by file_name: 33i_S5_L004_R1_001.fastq.gz
            #     elif (lane_search):
            #         lane_id = name_search.group(2)
            #         read_pair = name_search.group(3)
            #         lane_file = name_search.group(4)
            #         ext = name_search.group(5)
            #         gz = name_search.group(6)
            #     else:
            #         ## could exist or not
            #         read_pair = name_search.group(2)
            #         ext = name_search.group(3)
            #         gz = name_search.group(4)
            # else:
            #     ext = name_search.group(2)
            #     gz = name_search.group(3)
    
            ## populate dataframe
            name_frame.loc [len(name_frame)] = (path_files, dirN, name, name, name_len, 
                                            lane_id, read_pair, lane_file, ext, gz, "reads", os.path.basename(path_files))
    
        else:
            ## debug message
            if (Debug):
                print (colored("**DEBUG: sampleParser.get_fields **", 'yellow'))
                print (colored("*** ATTENTION: Sample did not match the possible parsing options...", 'yellow'))
                print (file_name)
            
            print (colored("*** ATTENTION: Sample (%s) did not match the possible parsing options..." %path_files, 'yellow'))

    return (name_frame)

###############

################################
def get_files(options, input_dir, mode, extension, debug, bam=False):
    """
    Parser function to get files
    
    Given an input dir and a mode in retrieves
    matching files with the extension desired.
    
    :param options: Contains several options as parser.parse_args options.
    :param input_dir: Absolute path to input dir containing samples.
    :param mode: Options are: fastq, trim, annot, assembly, etc...
    :param extension: List of possible extension to retrieve.
    :param debug
    
    :type options: parser.parse_args
    :type input_dir: string 
    :type mode: string 
    :type extension: list
    
    :returns: Pandas dataframe with sample and file information.
    
    options contains:
        + options.debug bool
        + options.project bool
        + options.batch bool
        + options.pair bool
        + options.include_all bool
        + options.include_lane bool
        + options.in_sample file or string
        + options.ex_sample file or string    
    
    """
    ## get list of input files
    files = []
    if (options.project):
        
        ## input folder is not a dir, is it a batch input file?
        if (options.batch):
            if os.path.isfile(input_dir):
                if (options.debug):
                    print (colored("\n**DEBUG: sampleParser.get_files input folder is a batch file, get full path **", 'yellow'))
                dir_list = [line.rstrip('\n') for line in open(input_dir)]
                for d in dir_list:
                    if os.path.exists(d):
                        print ('+ Folder (%s) exists' %d)
                        files = files + functions.main_functions.get_fullpath_list(d)
                    else:
                        ## input folder does not exist...
                        if (options.debug):
                            print (colored("\n**DEBUG: sampleParser.get_files batch option; input folder does not exists **", 'yellow'))
                            print (d)
                            print ("\n")
        else:        
            ### a folder containing a project is provided
            if os.path.exists(input_dir):
                print ('+ Input folder exists')
                ## get files in folder
                for ext in extension:
                    if mode == 'trim':
                        files_tmp = functions.main_functions.get_fullpath_list(input_dir)
                        files = [s for s in files_tmp if ext in s]
                    else:
                        files_tmp = functions.main_functions.retrieve_matching_files(input_dir, ext, debug)
                        files = files + files_tmp
    
                files = set(files)

            else:
                ## input folder does not exist...
                if (options.debug):
                    print (colored("\n**DEBUG: sampleParser.get_files input folder does not exists **", 'yellow'))
                    print (input_dir)
                    print ("\n")
    
                print (colored('***ERROR: input folder does not exist or it is not readable', 'red'))
                exit()                        
    else:
        ### provide a single folder or a file with multiple paths (option batch)
        if (options.batch):
            if os.path.isfile(input_dir):
                dir_list = [line.rstrip('\n') for line in open(input_dir)]
                for d in dir_list:
                    if os.path.exists(d):
                        print ('+ Folder (%s) exists' %d)
                        files_tmp = functions.main_functions.get_fullpath_list(d)
                        files = files + files_tmp
            
                    else:
                        ## input folder does not exist...
                        if (options.debug):
                            print (colored("\n**DEBUG: sampleParser.get_files batch option; input folder does not exists **", 'yellow'))
                            print (d)
                            print ("\n")
                        
        else:
            if os.path.exists(input_dir):
                print ('+ Input folder exists')
                ## get files in folder
                files = functions.main_functions.get_fullpath_list(input_dir)
            else:
                ## input folder does not exist...
                if (options.debug):
                    print (colored("\n**DEBUG: sampleParser.get_files input folder does not exists **", 'yellow'))
                    print (input_dir)
                    print ("\n")
    
                print (colored('***ERROR: input folder does not exist or it is not readable', 'red'))
                exit()

    if options.debug:
        print (colored("** DEBUG: sampleParser.get_files files", 'yellow'))
        print (files)

    ## get list of samples
    samples_names = []
    exclude=False

    if (options.in_sample):
        if os.path.isfile(os.path.abspath(options.in_sample)): ## a file
            in_file = os.path.abspath(options.in_sample)
            samples_names = [line.rstrip('\n') for line in open(in_file)]
            print ('+ Retrieve selected samples to obtain from the list files available.')
        else: ## a single ID
            samples_names = [options.in_sample]
        
        exclude=False

        ## in sample list...
        if (options.debug):
            print (colored("\n**DEBUG: sampleParser.get_files include sample list **", 'yellow'))
            print (samples_names, '\n')


    elif (options.ex_sample):
        if os.path.isfile(os.path.abspath(options.ex_sample)): ## a file
            ex_file = os.path.abspath(options.ex_sample)
            samples_names = [line.rstrip('\n') for line in open(ex_file)]
            print ('+ Retrieve selected samples to exclude from the list files available.')        
            exclude=True
        else: ## a single ID
            samples_names = [options.ex_sample]
        
        ## in sample list...
        if (options.debug):
            print (colored("\n**DEBUG: sampleParser.get_files exclude sample list **", 'yellow'))
            print (samples_names, '\n')

    else:
        samples_names = ['.*']

    ## discard empty sample_names
    samples_names = list(filter(None, samples_names)) ## empty space
    samples_names = set(samples_names)

    ## discard some files obtain
    files = [s for s in files if '.sam' not in s]
    files = [s for s in files if '.log' not in s]
    files = [s for s in files if '.annot' not in s]
    files = [s for s in files if '.abundances.txt' not in s]
    files = [s for s in files if '.gff3' not in s]
    files = [s for s in files if 'trimmed.fq' not in s]
    files = [s for s in files if 'trim.clpsd.fq' not in s]
    files = [s for s in files if 'failed.fq.gz' not in s]
    files = [s for s in files if 'unjoin' not in s]
    files = [s for s in files if '00.0_0.cor.' not in s]
    
    ## exceptions of the exceptions
    if not bam:
        files = [s for s in files if '.bam' not in s]
    
    ## skip using trim if fastq mode provided
    if (mode == 'fastq'):
        files = [s for s in files if 'trim' not in s]
    
    ## skip using join if trimm mode provided    
    if (mode == 'trim'):
        files = [s for s in files if 'joined' not in s]
    
    ##
    files = list(filter(None, files)) ## empty space
    files = set(files) ## unique results
    
        
    ## files list...
    if (options.debug):
        print (colored("\n**DEBUG: sampleParser.get_files files list to check **", 'yellow'))
        print ('DO NOT PRINT THIS LIST: It could be very large...')
        print (files, '\n')

    ## get information
    if mode in ['fastq', 'trim', 'join']:
        pd_samples_retrieved = sampleParser.samples.select_samples(files, samples_names, options.pair, exclude, options.debug, options.include_lane, options.include_all)
    else:
        pd_samples_retrieved = sampleParser.samples.select_other_samples(options.project, files, samples_names, mode, extension, exclude, options.debug)        
    
    ## remove duplicates & return
    pd_samples_retrieved = pd_samples_retrieved.drop_duplicates()
    
    return(pd_samples_retrieved)

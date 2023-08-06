#!/usr/bin/ python3
##########################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019 Lauro Sumoy Lab, IGTP, Spain        ##
##########################################################
"""
Prepares samples for further analysis.
"""

import os
import re
import pandas as pd
from termcolor import colored

from HCGB import sampleParser
from HCGB import functions

###########################################################################
def select_samples (list_samples, samples_prefix, pair=True, exclude=False, Debug=False, lane=False, include_all=False):
    """
    Select samples
    
    Given a sample prefix (any or a given list), this function retrieves
    sample files from a list given. If exclude option provided, excludes 
    the files retrieved from the total.
    
    :param list_samples: List of absolute path for fastq files
    :param samples_prefix: List of prefix to search 
    :param pair: True/false for paired-end files
    :param exclude: True/false for exclude found files from the total
    :param Debug: True/false for debugging messages
    :param lane: Include lane tag within name id
    
    :type list_samples: list
    :type samples_prefix: list
    :type pair: bool
    :type exclude: bool
    :type Debug: bool
    :type lane: bool
    
    :returns: Dataframe
    """
    #Get all files in the folder "path_to_samples"
    sample_list = pd.DataFrame(columns=('sample', 'file'))
    
    for names in samples_prefix:
        for path_fastq in list_samples:    
            fastq = os.path.basename(path_fastq)
            samplename_search = re.search(r"(%s)\_{0,1}(R1|1|R2|2){0,1}(.*){0,1}\.f.*q.*" % names, fastq)
            enter = ""
            if samplename_search:
                if (exclude): ## exclude==True
                    enter = False
                else: ## exclude==True
                    enter = True
            else:
                if (exclude): ## exclude==True
                    enter = True
                else: ## exclude==True
                    enter = False
                    
            if enter:
                if fastq.endswith('.gz') or fastq.endswith('fastq') or fastq.endswith('fq'):
                    sample_list.loc[len(sample_list)] = (names, path_fastq) 
                else:
                    ## debug message
                    if (Debug):
                        print (colored("**DEBUG: sampleParser.select_samples **", 'yellow'))
                        print (colored("** ERROR: %s is a file that is neither in fastq.gz or .fastq format, so it is not included" %path_fastq, 'yellow'))
                            
    ## discard duplicates if any
    non_duplicate_names = sample_list['sample'].to_list() #
    non_duplicate_names = list(set(non_duplicate_names))
    
    ## it might be a bug in exclude list.
    ## if sample X1 is provided to be excluded, we might be also excluding
    ## sample X12, sample X13, etc.
    ## TODO: check this

    ## debugging messages
    if Debug:
        print (colored("** DEBUG: select_samples",'yellow'))
        print ("non_duplicate_names:")
        print (non_duplicate_names)
    
    ## check they match with given input
    if (exclude): ## exclude==True
        if bool(set(samples_prefix).intersection(non_duplicate_names)):
            print(colored("** ERROR: Some non desired samples are included", 'red'))
    else: ## exclude==True
        non_duplicate_names = set(samples_prefix).intersection(non_duplicate_names)

    ## get fields
    
    tmp = sample_list[ sample_list['sample'].isin(non_duplicate_names) ]
    non_duplicate_samples = tmp['file'].to_list()
    
    ## debugging messages
    if Debug:
        print (colored("** DEBUG: select_samples",'yellow'))
        print ("non_duplicate_names:")
        print (non_duplicate_names)
        print ("samples_prefix")
        print (samples_prefix)
        print ("non_duplicate_samples")
        print (non_duplicate_samples)
        print ("tmp dataframe")
        functions.main_functions.print_all_pandaDF(tmp)
        print(tmp)
                
    ## get info
    name_frame_samples = sampleParser.files.get_fields(non_duplicate_samples, pair, Debug, include_all)    
    number_files = name_frame_samples.index.size
    total_samples = set(name_frame_samples['name'].to_list())
    
    ##
    if (lane):
        ## include lane tag within name
        name_frame_samples['name'] = name_frame_samples['name'] + '_' + name_frame_samples['lane']
        name_frame_samples['new_name'] = name_frame_samples['name']
            
    ## debugging messages
    if Debug:
        print (colored("** DEBUG: select_samples",'yellow'))
        print ("name_frame_samples:")
        print (name_frame_samples)
        print ("number_files:")
        print (number_files)
        print ("total_samples:")
        print (total_samples)
    
    ### get some stats
    if (number_files == 0):
        print (colored("\n**ERROR: No samples were retrieved. Check the input provided\n",'red'))
        exit()
    print (colored("\t" + str(number_files) + " files selected...", 'yellow'))
    print (colored("\t" + str(len(total_samples)) + " samples selected...", 'yellow'))
    if (pair):
        print (colored("\tPaired-end mode selected...", 'yellow'))
    else:
        print (colored("\tSingle end mode selected...", 'yellow'))
    
    ## return info
    return (name_frame_samples)

###########################################################################
def select_other_samples (project, list_samples, samples_prefix, mode, extensions, exclude=False, Debug=False):

    ## init dataframe
    name_columns = ("sample", "dirname", "name", "ext", "tag")

    ## initiate dataframe
    df_samples = pd.DataFrame(columns=name_columns)

    ## debug message
    if (Debug):
        print (colored("**DEBUG: samples_prefix **", 'yellow'))
        print (samples_prefix)
        print (colored("**DEBUG: mode **", 'yellow'))
        print (mode)
        print (colored("**DEBUG: extensions **", 'yellow'))
        print (extensions)

    #Get all files in the folder "path_to_samples"    
    for names in samples_prefix:
        for path_file in list_samples:
            f = os.path.basename(path_file)
            dirN = os.path.dirname(path_file)
            #samplename_search = re.search(r"(%s).*" % names, f)
            samplename_search = re.search(r"(%s).*" % names, path_file)
            
            enter = ""
            if samplename_search:
                if (exclude): ## exclude==True
                    enter = False
                else: ## exclude==True
                    enter = True
            else:
                if (exclude): ## exclude==True
                    enter = True
                else: ## exclude==True
                    enter = False
                    
            if enter:
                
                ## project mode:
                if project:
                    if mode == 'annot':
                        #### /path/to/folder/annot/name.faa
                        for ext in extensions:
                            f_search = re.search(r".*\/%s\/(.*)\.%s$" %(mode, ext), path_file)
                            if f_search:
                                file_name = f_search.group(1) 
                                df_samples.loc[len(df_samples)] = [path_file, dirN, file_name, ext, mode]    

                    elif mode== 'assembly':
                        #### name_assembly.faa
                        for ext in extensions:
                            f_search = re.search(r"(.*)\_%s\.%s$" %(mode, ext), f)
                            if f_search:
                                file_name = f_search.group(1) 
                                df_samples.loc[len(df_samples)] = [path_file, dirN, file_name, ext, mode]    

                    elif mode== 'mash':
                        #### name.sig
                        for ext in extensions:
                            f_search = re.search(r".*\/%s\/(.*)\.%s$" %(mode, ext), path_file)
                            if f_search:
                                file_name = f_search.group(1) 
                                df_samples.loc[len(df_samples)] = [path_file, dirN, file_name, ext, mode]    

                    elif mode== 'miRNA':
                        #### counts/mirtop.tsv
                        for ext in extensions:
                            f_search = re.search(r".*\/data\/(.*)\/%s\/(.*)\/counts\/%s$" %(mode, ext), path_file)

                            if f_search:
                                sample_name = f_search.group(1)
                                soft_name = f_search.group(2).split("_")[0] ## miraligner_miRTop
                                df_samples.loc[len(df_samples)] = [path_file, dirN, sample_name, soft_name, mode]    
                    
                    elif mode== 'piRNA':
                        #### sample_name/piRNA/soft_name/*_clusters.bed
                        for ext in extensions:
                            f_search = re.search(r".*\/data\/(.*)\/%s\/(.*)\/.*%s$" %(mode, ext), path_file)
                            
                            if f_search:
                                sample_name = f_search.group(1)
                                soft_name = f_search.group(2).split("_")[0] ## pilfer/other
                                df_samples.loc[len(df_samples)] = [path_file, dirN, sample_name, soft_name, mode]    

                    else:
                        for ext in extensions:
                            f_search = re.search(r".*\/(.*)\/%s\/(.*)\_summary\.%s$" %(mode, ext), path_file)
                            if f_search:
                                ### get information
                                if mode == 'profile':
                                    name = f_search.group(1)
                                    db_name = f_search.group(2).split('_')[-1]
                                    if not name.startswith('report'):
                                        df_samples.loc[len(df_samples)] = [path_file, dirN, name, db_name, mode]    
    
                                elif mode == 'ident':
                                    name = f_search.group(1)
                                    df_samples.loc[len(df_samples)] = [path_file, dirN, name, 'csv', mode]
                                    
                            else:
                                #### common: path/sample_name/job/info.csv
                                for ext in extensions:
                                    f_search = re.search(r"(.*)\/%s\/(.*)\.%s$" %(mode, ext), path_file)
                                    if f_search:
                                        file_name = os.path.basename(f_search.group(1))
                                        df_samples.loc[len(df_samples)] = [path_file, dirN, file_name, ext, mode]
                                    else:
                                        f_search2 = re.search(r"(.*)\/%s\/%s$" %(mode, ext), path_file)
                                        if f_search2:
                                            file_name = os.path.basename(f_search2.group(1))
                                            df_samples.loc[len(df_samples)] = [path_file, dirN, file_name, ext, mode]    
                                            
                                    
                ## detached mode
                else:
                    for ext in extensions:
                        if f.endswith(ext):
                            file_name, ext1 = os.path.splitext(f)
                            ##columns = ("sample", "dirname", "name", "ext", "tag")
                            file_name= os.path.basename(dirN)
                            df_samples.loc[len(df_samples)] = [path_file, dirN, file_name, ext, mode]    

    ## debug message
    if (Debug):
        print (colored("**DEBUG: df_samples **", 'yellow'))
        print (df_samples)
        print ("test OK")
    
    ## print stats
    number_samples = df_samples.index.size
    if (number_samples == 0):
        print (colored("\n**ERROR: No samples were retrieved for this option. Continue processing...\n",'red'))
        return (df_samples)
    print (colored("\t" + str(number_samples) + " samples selected from the input provided...", 'yellow'))

    df_samples['new_name'] = df_samples['name']
    return (df_samples)

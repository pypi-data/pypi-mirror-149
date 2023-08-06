#!/usr/bin/ python3
##########################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019 Lauro Sumoy Lab, IGTP, Spain        ##
##########################################################
"""
Merge files from different sequencing lanes
"""

import pandas as pd
from termcolor import colored
import shutil
import concurrent.futures

from HCGB import functions

###############
def gunzip_merge(outfile, list_files):
    """
    Merge gunzip files into final file
    
    :param outfile: String for output file
    :param list_files: List of files to merge
    
    :type outfile: string
    :type list_files: list
        
    """
    list_files = list(list_files)
    list_files.sort()
    print ("\tMerging files into: ", outfile)
    #print ("\tFiles: ", list_files)

    with open(outfile, 'wb') as wfp:
        for fn in list_files:
            with open(fn, 'rb') as rfp:
                shutil.copyfileobj(rfp, wfp)

    return()
    
###############    
def one_file_per_sample(dataFrame, outdir_dict, threads, outdir, Debug=False):
    """
    Merge fastq files from different lanes positions for each sample
    
    """
    ## merge sequencing files for sample, no matter of sector or lane generated.    
    list_samples = set(dataFrame['new_name'].tolist())
    print (colored("\t" + str(len(list_samples)) + " samples to be merged from the input provided...", 'yellow'))
    print ("+ Merging sequencing files for samples")

    ##
    sample_frame = dataFrame.groupby(["new_name", "read_pair"])
    
    ### get extension for files
    ext_list = dataFrame.ext.unique()
    gz_list = dataFrame.gz.unique()
    ## might generate a bug if several extension or some zip/unzip files provided
    if gz_list:
        ext = ext_list[0] + gz_list[0]
    else:
        ext = ext_list[0]

    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor: ## need to do 1 by one as there is a problem with the working directory
        commandsSent = { executor.submit(gunzip_merge, 
                                        outdir_dict[name[0]] + '/' + name[0] + '_' + name[1] + '.' + ext, 
                                        sorted(set(cluster["sample"].tolist()))): name for name, cluster in sample_frame }
        for cmd2 in concurrent.futures.as_completed(commandsSent):
            details = commandsSent[cmd2]
            try:
                data = cmd2.result()
            except Exception as exc:
                print ('***ERROR:')
                print (cmd2)
                print('%r generated an exception: %s' % (details, exc))                
                            
    ## return output name merged generated in dataframe
    name_columns = ("new_name", "dirname", "read_pair", "new_file", "ext", "gz")
    name_frame = pd.DataFrame(columns=name_columns)

    ## print to a file
    timestamp = functions.time_functions.create_human_timestamp()
    merge_details = outdir + '/' + timestamp + '_prep_mergeDetails.txt'
    merge_details_hd = open(merge_details, 'w')

    for name, cluster in sample_frame: ## loop over samples
        outfile = outdir_dict[name[0]] + '/' + name[0] + '_' + name[1] + ext
        
        merge_details_hd.write("####################\n")        
        merge_details_hd.write("Sample: " + name[0] + '\n')
        merge_details_hd.write("New name: " + name[0] + '\n')
        
        merge_details_hd.write("Read: " + name[1] + '\n')
        merge_details_hd.write("Files:\n")
        merge_details_hd.write(",".join(sorted(cluster["sample"].tolist())))
        merge_details_hd.write('\n')
        merge_details_hd.write("####################\n")        
        
        name_frame.loc[len(name_frame)] = (name[0], outdir_dict[name[0]], name[1], outfile, ext_list[0], gz_list[0])

    merge_details_hd.close()
    return(name_frame)

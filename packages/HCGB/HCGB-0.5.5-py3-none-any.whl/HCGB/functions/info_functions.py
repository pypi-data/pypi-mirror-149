#!/usr/bin/env python3
############################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019-2021 Lauro Sumoy Lab, IGTP, Spain   ##
############################################################

import json
import os
from HCGB import functions

######################################
def dump_info_run(out_folder, module, userinput, runInfo, debug):
    """
    Prints information of the job run in json format
    
    :param out_folder: Absolute path to folder to dump results
    :param module: Module or script name executed
    :param runInfo: Contains configuration detail information to dump
    
    :type out_folder: string 
    :type module: string 
    :type runInfo: dict
    
    :returns: Prints information in json format in the output folder provided.
    
    Example of information to include:
    
    userinput = {"filename":infiles, 
                "database":path_to_database,
                "file_format":file_format}
                
    runInfo = { "module":module, 
                "analysis":example,
                "date":date, 
                "time":time}
    
    Original idea extracted from https://bitbucket.org/genomicepidemiology/kmerfinder/src/master/kmerfinder.py
    
    """
    
    # Collect all data of run-analysis
    
    ## convert to dictionary
    userinput_dict = vars(userinput)
    del userinput_dict['func']
    
    ## merge dictionaries:: data = {**runInfo, **userinput_dict}
    
    ## add sub dictionary
    data = runInfo.copy()
    data['input_options'] = userinput_dict
    
    ## debug messages
    if debug:
        functions.aesthetics_functions.debug_message("Dump information:", 'yellow')
        print()
        functions.aesthetics_functions.debug_message("runInfo:", 'yellow')
        print(runInfo)
        print(type(runInfo))
        print()
        
        functions.aesthetics_functions.debug_message("userinput_dict:", 'yellow')
        print(userinput_dict)
        print(type(userinput_dict))
        print()
        
        functions.aesthetics_functions.debug_message("data:", 'yellow')
        print(data)
        print(type(data))
        print()
    
    # Save json output
    result_json_file = os.path.join(out_folder, module + ".json") 
    with open(result_json_file, "w") as outfile:  
        json.dump(data, outfile, indent=3)

######################################
def compare_info_dict(dict1, dict2, listItems, debug):
    """Given a pair of dictionaries and a list of items, compare values."""
    print()
    
    
    
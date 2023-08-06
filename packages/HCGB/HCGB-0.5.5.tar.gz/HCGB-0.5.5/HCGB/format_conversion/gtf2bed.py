#!/usr/bin/env python3
#############################################################
## Jose F. Sanchez, Marta Lopez & Lauro Sumoy              ##
## Copyright (C):2012 Davud Li Wei - https://weililab.org/ ##
##               2019-2021 Lauro Sumoy Lab, IGTP, Spain    ##
#############################################################
"""
gtf2bed.py converts GTF file to BED file.
Usage: gtf2bed.py {OPTIONS} [.GTF file]
History
    Nov.5th 2012:
        1. Allow conversion from general GTF files (instead of only Cufflinks supports).
        2. If multiple identical transcript_id exist, transcript_id will be appended a string like "_DUP#" to separate.

    Nov.9th 2021: Modified by JFSanchezherrero
        1. Reformat code to use as a function
        2. Add additional details
        3. Simplify

Copyrigth: http://alumni.cs.ucr.edu/~liw/scripts.html
BED Format details: https://genome.ucsc.edu/FAQ/FAQformat.html#format1
"""

import sys
import os
import re
from termcolor import colored

import HCGB.functions.aesthetics_functions as HCGB_aes
import HCGB.functions.files_functions as HCGB_files
import HCGB.functions.time_functions as HCGB_time

allids = {}

############################################################
def parse_GTF_call(gtf_file, out_file, debug=False):

    ## debug messaging    
    if debug:
        print()
        HCGB_aes.debug_message("********************** parse_GTF_call ********************** ")
        HCGB_aes.debug_message("Checking if GTF has been previously converted to BED", "yellow")
    
    path_given=os.path.dirname(out_file)
    name = HCGB_files.get_file_name(out_file)
    gtf_file = os.path.abspath(gtf_file)
        
    ## get absolute path and name
    name_file = HCGB_files.get_path_name(gtf_file, path_given, 
                              name, debug=debug) + ".bed"
                              
    if debug:
        HCGB_aes.debug_message("gtf_file: " + gtf_file, "yellow")
        HCGB_aes.debug_message("name: " + name, "yellow")
        HCGB_aes.debug_message("out_file: " + out_file, "yellow")
        HCGB_aes.debug_message("name_file: " + name_file, "yellow")
                              

    filename_stamp = os.path.join(path_given, '.' + name + "_GTF_convertion_success")
    if HCGB_files.is_non_zero_file(filename_stamp):
        if HCGB_files.is_non_zero_file(out_file):
            ## bed files exists
            if debug:
                HCGB_aes.debug_message("Timestamp exists: .split_GTF_success ", "yellow")
                print()
    
            print (colored("\tA previous command generated results on: %s [%s]" %(HCGB_time.read_time_stamp(filename_stamp)
                                                                                  , 'convert GTF -> BED'), 'yellow'))
            
            return(out_file)
    
    ## File is not processed or not finished
    parse_GTF(gtf_file, out_file, debug=debug)
    
    ## print time stamp
    HCGB_time.print_time_stamp(filename_stamp)
            
    if debug:
        HCGB_aes.debug_message("********************** parse_GTF_call ********************** ")
    
    return (out_file)


############################################################
def savebedline(estart, eend, field, nline, debug):
    """
    
    est=int(field[3])
    eed=int(field[4])
    estart +=[est]
    eend +=[eed]
    
    :param estart: Contains feature coordinates for each exon start (+) or end (-).
    :param eend: Contains feature coordinates for each exon start (-) or end (+).
    :param field: GTF line splitted. Contains 9 fields.
    :param nline: Number of line in the GTF file
    :param debug: True/False for debugging messages
    
    :type estart: list
    :type eend: list
    :type field: list
    :type nline: int
    :type debug: bool
    
    :returns: String to write in BED format.
    """
    
    ## debug messages    
    if debug:
        HCGB_aes.debug_message("GTF line: ", "yellow")
        print(field)
        
    ## ---------------------------------
    # use regular expression to get transcript_id, gene_id and expression level
    ## ---------------------------------
    #geneid=re.findall(r'gene_id +\"([\w\.]+)\";',field[8])
    #transid=re.findall(r'transcript_id +\"([\w\.]+)\";',field[8])
    #fpkmval=re.findall(r'FPKM +\"([\d\.]+)\";',field[8])
    #biotype=re.findall(r'transcript_biotype +\"([\w\.]+)\";',field[8])
    
    geneid=re.findall(r'gene_id +\"(.+)[\";]+.*',field[8])
    transid=re.findall(r'transcript_id +\"(.+)[\";]+.*',field[8])
    fpkmval=re.findall(r'FPKM +\"(.+)[\";]+.*',field[8])
    biotype=re.findall(r'transcript_biotype +\"(.+)[\";]+.*',field[8])
    ## add others if required: e.g. transcript_biotype
    
    ## ---------------------------------
    ## Get Gene ID
    ## ---------------------------------
    if len(geneid)==0:
        print('Warning: no gene_id field in line ' + str(nline))
        gene_id="none"
    else:
        gene_id=geneid[0].split('\"')[0]
    
    ## ---------------------------------
    ## Get transcript biotype
    ## ---------------------------------
    if len(biotype)==0:
        print('Warning: no transcript_biotype field in line ' + str(nline))
        transcript_biotype="none"
    else:
        transcript_biotype=biotype[0].split('\"')[0]

    ## ---------------------------------
    ## FPKM field
    ## ---------------------------------
    fpkmint=100
    if len(fpkmval)>0: # Warning: no FPKM field
        fpkmval=fpkmval[0].split('\"')[0]
        fpkmint=round(float(fpkmval))

    ## ---------------------------------
    ## Get transcript ID
    ## ---------------------------------
    if len(transid)==0: # Warning: no transcript_id field
        transid='Trans_'+str(nline) ## set a new name for transcript if missing
        print('Warning: no transcript_id field in line ' + str(nline))
        print('Warning: Generate new: ' + transid)
    else:
        transid=transid[0].split('\"')[0]
    
    ## Previous transcript ID
    if transid in allids.keys():
        transid2=transid+'_DUP'+str(allids[transid])
        allids[transid]=allids[transid]+1
        transid=transid2;
    ## New transcript ID
    else:
        allids[transid]=1
    
    ## ---------------------------------
    ## Get exon start and lengths
    ## ---------------------------------
    if (field[6]=="+"):
    
        seglen=[eend[i]-estart[i]+1 for i in range(len(estart))]
        estp=estart[0]-1
        eedp=eend[-1]
        segstart=[estart[i]-estart[0] for i in range(len(estart))]
    
    elif (field[6]=="-"):
        seglen=[eend[i]-estart[i]+1 for i in range(len(estart))]
        estp=estart[0]-1
        eedp=eend[-1]
    
        segstart=[estart[0]-estart[i] for i in range(len(estart))]
        if len(estart)!=1: ## if a single exon by gene, it is correct. Otherwise, we need to "transpose". 
            estp=eend[-1]
            eedp=estart[0]-1

    strl=str(seglen[0])
    for i in range(1,len(seglen)):
        strl+=','+str(seglen[i])

    strs=str(segstart[0])
    for i in range(1,len(segstart)):
        strs+=','+str(segstart[i])

    ## debug messages    
    if debug:
        HCGB_aes.debug_message("estart: " + str(estart), "yellow")
        HCGB_aes.debug_message("seglen: " + str(seglen), "yellow")
        HCGB_aes.debug_message("segstart: " + str(segstart), "yellow")
        HCGB_aes.debug_message("strl: " + str(strl), "yellow")
        HCGB_aes.debug_message("strs: " + str(strs), "yellow")
    
    ## ---------------------------------
    ## Save data information
    ## ---------------------------------
    ###            #"chr"            "start"            "end"         "transcript_id"            "fpkm"             "strand"      "thickstart"        "thickend"             "RGB"             "estart"               "strs"        "strl"     "gene_id"         "transcript_biotype"
    string2write = field[0] + '\t' + str(estp) + '\t' + str(eedp) + '\t' + transid + '\t' +  str(fpkmint)+ '\t' +  field[6]+ '\t' +  str(estp) + '\t' + str(eedp) + '\t' + "255,0,0"+ '\t' + str(len(estart)) + '\t' + strs+ '\t' + strl+ '\t' + gene_id+ '\t' + transcript_biotype

    ## debug messages    
    if debug:        
        HCGB_aes.debug_message("data BED format: " + transid, "yellow")
        print(string2write)

    return (string2write)
    
############################################################
def parse_GTF(gtf_file, out_file, debug):
    
    original_stdout = sys.stdout # Save a reference to the original standard output

    ## Start the parsing of GTF
    ## Init variables 
    estart=[]
    eend=[]
    nline=0 # read lines one to one
    prevfield=[]
    prevtransid=''

    if debug:
        print("")
        HCGB_aes.debug_message("*************")
        
    with open(out_file, 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        ## Loop through big GTF file
        for lines in open(gtf_file):
            field=lines.strip().split('\t')
            ## count lines
            nline=nline+1
            
            ## debug messages
            if debug:
                HCGB_aes.debug_message("nline: " + str(nline), "yellow")
                print(lines)
                

                
            ## skip comment lines
            if field[0].startswith("#"): ## Comment line: skipping
                continue
                    
            if len(field)<9:
                print('Error: the GTF should has at least 9 fields at line ')
                continue
    
            if field[1]!='Cufflinks':
                pass
                #print('Warning: the second field is expected to be \'Cufflinks\' at line '+str(nline),file=sys.stderr)
            
            if field[2]!='exon' and field[2] !='transcript':
                if debug:        
                    HCGB_aes.debug_message("Line: ", "yellow")
                    print(lines, file=sys.stderr)
                    HCGB_aes.debug_message("nline: " + str(nline), "yellow")
                    print('Error: the third filed is expected to be exon or transcript')
                    
                continue
            
            ## ---------------------------------
            # use regular expression to get transcript_id
            #transid=re.findall(r'transcript_id +\"([\w\.]+)\";',field[8])
            transid=re.findall(r'transcript_id +\"(.+)[\";]+.*',field[8])
            if len(transid)>0:
                transid=transid[0].split('\"')[0]
            else:
                transid=''
            
            ## debug messages
            if debug:
                HCGB_aes.debug_message("prevtransid: " + str(prevtransid))
                HCGB_aes.debug_message("transid: " + transid)
            
            ## when changes, save previous field information                
            if field[2]=='transcript' or (prevtransid != '' and transid!='' and transid != prevtransid):
                #print('prev:'+prevtransid+', current:'+transid)
                # A new transcript record, write
                if len(estart)!=0:
                    ## debug messages    
                    if debug:        
                        HCGB_aes.debug_message("savebedline call")
                        HCGB_aes.debug_message("estart: " + str(estart))
                        HCGB_aes.debug_message("eend: " + str(eend))
                        HCGB_aes.debug_message("prevfield: " + str(prevfield))
                    
                    ## save record in bed format
                    strin2print = savebedline(estart, eend, prevfield, nline, debug)
                    print(strin2print)
                    
                    ## debug messages
                    if debug:        
                        HCGB_aes.debug_message("*************")
                        print("")
                    
                # Reset
                estart=[]
                eend=[]
                        
            ## ---------------------------------
            prevfield=field
            prevtransid=transid
            if field[2]=='exon':
                try:  
                    est=int(field[3])
                    eed=int(field[4])
                    estart +=[est]
                    eend +=[eed]
                except ValueError:
                    print('Error: non-number fields at line '+str(nline))
      
        #############################        
        # the last record
        #############################
        if len(estart)!=0:
            ## debug messages    
            if debug:        
                HCGB_aes.debug_message("savebedline call")
                HCGB_aes.debug_message("transid: " + transid)
                HCGB_aes.debug_message("estart: " + str(estart))
                HCGB_aes.debug_message("eend: " + str(eend))
                HCGB_aes.debug_message("prevfield: " + str(prevfield))
                HCGB_aes.debug_message("prevtransid: " + str(prevtransid))

            ## save record in bed format
            strin2print = savebedline(estart, eend, field, nline, debug)
            print(strin2print)
    
    # Reset the standard output to its original
    sys.stdout = original_stdout  

    ## ---------------------------------
    ## return when finished
    return()

############################################################
def main():
    ## this code runs when call as a single script
    if len(sys.argv)<2:
        print('This script converts .GTF into .BED annotations.\n')
        print('Usage: gtf2bed [.GTF file] [OUT bed]\n')
        print('\nNote:')
        print('1\tOnly "exon" and "transcript" are recognized in the feature field (3rd field).')
        print('2\tIn the attribute list of .GTF file, the script tries to find "gene_id", "transcript_id" and "FPKM" attribute, and convert them as name and score field in .BED file.') 
        
        print('Author: Wei Li (li.david.wei AT gmail.com)')
        sys.exit()

    ## get output file
    out_file=""
    if len(sys.argv)>=3:
        out_file = sys.argv[2]
    else:
        out_file = "example.bed"
    
    out_file = os.path.abspath(out_file)
    
    print("+ Converting GTF to bed...")
    
    ## parse 
    parse_GTF_call(sys.argv[1], out_file, False)

    ## final

############################################################
if __name__== "__main__":
    main()

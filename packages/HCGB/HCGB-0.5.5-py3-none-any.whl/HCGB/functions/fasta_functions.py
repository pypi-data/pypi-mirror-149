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
import re
from Bio import SeqIO
from termcolor import colored
from collections import defaultdict
##
from HCGB.functions import system_call_functions

#################################
###         FASTA files        ##
#################################

##########################################################
def get_fasta_dict(fasta_file, Debug):
    """
    
    """
    fasta_count = defaultdict(int)
    with open(fasta_file, 'r') as fh:
        lines = []
        for line in fh:
            lines.append(line.rstrip())
            if len(lines) == 2:
                record = process_fasta(lines)
                #sys.stderr.write("Record: %s\n" % (str(record)))
                lines = []
                fasta_count[record['sequence']] = record['name'].split(">")[1]
                
    return fasta_count        

###############
def ReverseComplement(seq):
    seq_dict = {'A':'T','T':'A','G':'C','C':'G','N':'N'}
    return "".join([seq_dict[base] for base in reversed(seq)])

###############
def concat_fasta(dirFasta, Fasta):
    print ("+ Concatenating all information into one file...")    
    cmd = 'cat ' + dirFasta + '/*fna > ' + Fasta
    return(system_call_functions.system_call(cmd))

###############
def subset_fasta(ident, fasta, out):
    output_FASTA = open(out, 'w')    
    for record in SeqIO.parse(fasta, "fasta"):
        all_id = record.description
        species_search = re.search(r"%s" % ident, all_id)
        if species_search:
            head = ">" + all_id + "\n"
            output_FASTA.write(head)
            output_FASTA.write(str(record.seq))
            output_FASTA.write("\n")
    
    output_FASTA.close()

###############
def rename_fasta_seqs(fasta_file, name, new_fasta):
    """Rename fasta sequences provided in file :file:`fasta_file` using id :file:`name`. Save results in file :file:`new_fasta` provided.
    
    Check for id character lenght do not exceed 37 characters as it might be a limitiation in further annotation and subsequent analysis. Read Prokka_ issue for further details: https://github.com/tseemann/prokka/issues/337.
    
    :param fasta_file: Absolute path to fasta file.
    :type fasta_file: string
    :param name: String to add every fasta sequence header.
    :type name: string
    :param new_fasta: Name for the new fasta file (Absolute path).
    :type new_fasta: string
    :return: Path to tabular delimited file containing conversion from all to new id for each sequence.
    :warnings: Returns FAIL if name is >37 characters.
    
    .. include:: ../../links.inc         
    """

    output_FASTA = open(new_fasta, 'w')
    id_conversion = open(new_fasta + "_conversionID.txt", 'w')
    
    if len(name) > 37:
        print (colored("** ERROR **", 'red'))
        print (colored("rename_fasta_seqs():: name id is > 37 characters.", 'red'))
        print (colored("** ERROR **", 'red'))
        return ('FAIL')
    
    counter_seqs = 0
    for record in SeqIO.parse(fasta_file, "fasta"):
        old_id = record.description
        counter_seqs += 1
        new_id = name + "_" + str(counter_seqs)
        head = ">" + new_id + "\n"
        output_FASTA.write(head)
        output_FASTA.write(str(record.seq))
        output_FASTA.write("\n")
        
        id_conversion.write(old_id + "\t" + new_id)
        id_conversion.write("\n")
    
    output_FASTA.close()
    id_conversion.close()
        
    return (new_fasta + "_conversionID.txt")

### 
def process_fasta(lines):
    ks = ['name', 'sequence']
    return {k: v for k, v in zip(ks, lines)}

### 
def process_fastq(lines):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

#####
def reads2tabular(fastq_file, out):
    
    ## dictionary
    freq_fasta = defaultdict(int)
    
    ## read fastq    
    n = 4
    with open(fastq_file, 'r') as fh:
        lines = []
        for line in fh:
            lines.append(line.rstrip())
            if len(lines) == n:
                record = process_fastq(lines)
                #sys.stderr.write("Record: %s\n" % (str(record)))
                lines = []
                
                ## add sequences & count
                freq_fasta[record['sequence']] += 1

    ## print in file
    with open(out,'w') as file:
        for k in sorted (freq_fasta.keys()):
            file.write("%s\t%s\n" % (k, freq_fasta[k]))
    
    return(freq_fasta)





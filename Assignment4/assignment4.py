import os
import sys
from Bio import SeqIO
import csv

def contig_parser(input_file):
    #appends the length of each sequence to a list
    seq_lengths_list = []
    
    record_dict = SeqIO.to_dict(SeqIO.parse(input_file, "fasta"))
    for key in record_dict.items():
        seq_lengths_list.append(len(key[1].seq))
    seq_lengths_list.append(5)

    return seq_lengths_list

def calculate_N50(seq_lengths_list):
    """Calculate N50 for a sequence of numbers.
    Args:list_of_lengths (list): List of numbers.
    Returns:float: N50 value.
 
    """
    tmp = []
    for tmp_number in set(seq_lengths_list):
            tmp += [tmp_number] * seq_lengths_list.count(tmp_number) * tmp_number
    tmp.sort()
 
    if (len(tmp) % 2) == 0:
        median = (tmp[int(len(tmp) / 2) - 1] + tmp[int(len(tmp) / 2)]) / 2
    else:
        median = tmp[int(len(tmp) / 2)]
 
    return median

if __name__ == "__main__":
  input = sys.stdin
  output = sys.stdout #as a simple number
  N50 = str(calculate_N50(contig_parser(input)))
  output.write(f"{N50}, ")

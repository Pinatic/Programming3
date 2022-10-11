from Bio import SeqIO
import os
import sys

def contig_parser(input):
    #appends the length of each sequence to a list
    seq_lengths = []
    seq_list_unfiltered = SeqIO.to_dict(SeqIO.parse(input, "fasta"))

    for seq in seq_list_unfiltered.items():
        seq_lengths.append(len(seq[1].seq))
    
    seq_lengths.sort(key=len)

    return seq_lengths

def calculate_N50(seq_lengths):
    """Calculate N50 for a sequence of numbers.
    Args:list_of_lengths (list): List of numbers.
    Returns:float: N50 value.
 
    """
    tmp = []
    for tmp_number in set(seq_lengths):
            tmp += [tmp_number] * seq_lengths.count(tmp_number) * tmp_number
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

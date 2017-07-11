from Bio import AlignIO

"""
Functions:
    file_converter(input_file, input_type, output_type, output_file)
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

def file_converter(input_file, input_type, output_type, output_file):
    input_handle = open(input_file, "rU")
    output_handle = open(output_file, "w")

    alignments = AlignIO.parse(input_handle, input_type)
    AlignIO.write(alignments, output_handle, output_type)

    output_handle.close()
    input_handle.close()

if __name__ == '__main__':
    file_converter('../testFiles/phylip.txt', 'phylip-relaxed', 'fasta', '../henlo')
    # file_converter("seqfileWF1200m4Formatted2", "fasta", "phylip-sequential", "ChillLeo.phylip")

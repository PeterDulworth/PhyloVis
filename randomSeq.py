## random sequence generation
import random

# PHYLIP Format
def phylip(len, num, output_name):
    """
    Creates random DNA 
    sequence in PHYLIP format.
    
    Input: 
    len -- length of sequence
    num -- number of sequences
    
    Returns:
    Random DNA sequences in a file.
    """
    bases = ["A", "T", "C", "G"]
    file = open(output_name, "w")
    file.write(" " + str(num) + " " + str(len)+ "\n")
    for i in range(num):
        file.write("seq" + str(i) + " ")
        for j in range(len):
            file.write(random.choice(bases))
        file.write("\n")
    file.close()

if __name__ == '__main__':
    phylip(100, 10, "phylip.txt")
    # phylip(1000000, 10, "phylipBig.txt")
    # phylip(25, 5, "test.txt")
    # phylip(1000, 10, "bitch.txt")


# FASTA Format
def fasta(len, num, output_name):
    """
        Creates random DNA 
        sequence in FASTA format.

        *** VERY LARGE FILES ***
        
        Input: 
        len -- length of sequence
        num -- number of sequences

        Returns:
        Random DNA sequences in a file.
        """
    bases = ["A", "T", "C", "G"]
    file = open(output_name, "w")
    file.write(str(num) + "\n")
    file.write(str(len) + "\n")
    for i in range(num):
        file.write(">seq" + str(i) + "\n")
        for j in range(1, len + 1):     # keeps actual length
            file.write(random.choice(bases))
            if j % 70 == 0:     # 70-80 lines max
                file.write("\n")
        file.write("\n")
    file.close()

if __name__ == '__main__':
    fasta(100000, 10, "fasta.txt")

from Bio import AlignIO

def file_converter(input_file, input_type,output_type, output_file):
    input_handle = open(input_file, "rU")
    output_handle = open(output_file, "w")

    alignments = AlignIO.parse(input_handle, input_type)
    AlignIO.write(alignments, output_handle, output_type)

    output_handle.close()
    input_handle.close()

    return

if __name__ == '__main__':
    file_converter("seqfileWF1200m4Formatted2", "fasta", "phylip-sequential", "ChillLeo.phylip")


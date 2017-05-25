## random sequence generation
import random

# PHYLIP Format
def phylip(len, num):
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
    file = open("phylip.txt", "w")
    file.write(str(num) + "\n")
    file.write(str(len) + "\n")
    for i in range(num):
        file.write("seq" + str(i) + " ")
        for j in range(len):
            file.write(random.choice(bases))
        file.write("\n")
    file.close()

# phylip(1000000, 10)

# FASTA Format
def fasta(len, num):
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
    file = open("fasta.txt", "w")
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

# fasta(100000, 10)


## random sequence
import random

def seq(len, num):
    """
    Creates random DNA 
    sequence.
    
    Input: 
    len -- length of sequence
    num -- number of sequences
    
    Returns:
    Random DNA sequences in a file.
    """
    file = open("phylip.txt", "w")
    bases = ["A", "T", "C", "G"]
    for i in range(num):
        file.write("seq" + str(i) + " ")
        for j in range(len):
            file.write(random.choice(bases))
        file.write("\n")
    file.close()


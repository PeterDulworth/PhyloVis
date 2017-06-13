
from Bio import SeqIO

# record = SeqIO.read("NC_005816.gb", "genbank")
# print record
from Bio import SeqIO

with open("testPhylip.txt", "rU") as input_handle:
    with open("cor6_6.fasta", "w") as output_handle:
        sequences = SeqIO.parse(input_handle, "phylip")
        count = SeqIO.write(sequences, output_handle, "fasta")

# record = SeqIO.read("fasta.txt", "fasta")
from Bio import SeqIO

count = SeqIO.convert("testconvert.fasta", "fasta", "testconvert.phylip", "phylip")
print("Converted %i records" % count)
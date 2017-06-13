from Bio import AlignIO

# input_handle = open("testPhylip.txt", "rU")
# output_handle = open("example.phylip", "w")
#
# alignments = AlignIO.parse(input_handle, "phylip")
# AlignIO.write(alignments, output_handle, "phylip-sequential")

input_handle = open("phylip.txt", "rU")
output_handle = open("bgPhylip.txt", "w")

alignments = AlignIO.parse(input_handle, "phylip-relaxed")
AlignIO.write(alignments, output_handle, "phylip")

output_handle.close()
input_handle.close()
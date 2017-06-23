from Bio import Phylo
from matplotlib import pyplot as plt

###################Stuff to show trees
# tree = Phylo.parse('RAxML_Files\\RAxML_bipartitions.0', 'newick')
tree = Phylo.read('RAxML_Files\\RAxML_bipartitions.0', "newick")
# tree.rooted = True

# Create the figure
fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)

# Create the tree image
Phylo.draw(tree, "Test Tree", axes=axes, do_show=False)

# # Rotate the image and save it
# im = Image.open(output_file)
# im.rotate(-90).save(output_file)
plt.show()

# plt.clf()


####################Stuff for regular expression
import re


# Below pattern works perfectly on https://regex101.com/r/h1ISM8/1/
# It removes the characters inside the desire parentheses but doesn't touch character after the close parenthese
pattern = "(?<=\()[^()]+(?=((\))([+-]?([0-9]*)(\.([0-9]+))?)(:)(?=.)([+-]?([0-9]*)(\.([0-9]+))?)))"


txt="start(gnsiun)1.235:1.234,finish"
# txt = "(seq5:1.0,((((((seq3:7.8,seq8:0.6)0:0.9,seq1:0.9)50:3.1,seq6:0.9)50:7.5,seq4:0.9)0:3.6,seq2:0.9)0:0.9,(seq0:3.5,seq7:0.9)50:3.9)50:5.1,seq9:14.5);"
# txt = "(seq3:7.8,seq8:0.6)0:0.9,"
txt = "(((seq3:7.8,seq8:0.6)0:0.9,seq1:0.9)50:3.1,seq6:0.9)"


m = re.sub(pattern,"",txt)

print m
print txt

# Original
# (seq5:0.00000100000050002909,((((((seq3:17.85432306915368627642,seq8:0.06720234450647442903)0:0.99847599272177456342,seq1:0.00000100000050002909)50:34.53877639491068407551,seq6:0.00000100000050002909)50:17.56137571998827340281,seq4:0.00000100000050002909)0:3.68205663473320221613,seq2:0.00000100000050002909)0:0.00000100000050002909,(seq0:3.59573165919989401473,seq7:0.00000100000050002909)50:3.98204256501537390278)50:5.13876914332701062449,seq9:14.59065439946260944737);
# Shortened
# (seq5:1.0,((((((seq3:7.8,seq8:0.6)0:0.9,seq1:0.9)50:3.1,seq6:0.9)50:7.5,seq4:0.9)0:3.6,seq2:0.9)0:0.9,(seq0:3.5,seq7:0.9)50:3.9)50:5.1,seq9:14.5);
# Contraction threshold >50
# (seq5:1.0,((seq0:3.5,seq7:0.9)50:3.9)50:5.1,seq9:14.5);


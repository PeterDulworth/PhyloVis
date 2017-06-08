from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO

# record = SeqIO.read("NC_005816.gb", "genbank")
record = SeqIO.read("fasta.txt", "fasta")

# We're using a top down approach, so after loading in our sequence we next create an empty diagram, then add an (empty) track, and to that add an (empty) feature set:

gd_diagram = GenomeDiagram.Diagram("Yersinia pestis biovar Microtus plasmid pPCP1")
gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
gd_feature_set = gd_track_for_features.new_set()

# Now the fun part - we take each gene SeqFeature object in our SeqRecord, and use it to generate a feature on the diagram. We're going to color them blue, alternating between a dark blue and a light blue.

for feature in record.features:
    if feature.type != "gene":
        #Exclude this feature
        continue
    if len(gd_feature_set) % 2 == 0:
        color = colors.blue
    else:
        color = colors.lightblue
    gd_feature_set.add_feature(feature, color=color, label=True)

# Now we come to actually making the output file. This happens in two steps, first we call the draw method, which creates all the shapes using ReportLab objects. Then we call the write method which renders these to the requested file format. Note you can output in multiple file formats:

gd_diagram.draw(format="linear", orientation="landscape", pagesize='A4',
                fragments=4, start=0, end=len(record))
gd_diagram.write("plasmid_linear.pdf", "PDF")
gd_diagram.write("plasmid_linear.eps", "EPS")
gd_diagram.write("plasmid_linear.svg", "SVG")
# Also, provided you have the dependencies installed, you can also do bitmaps, for example:

gd_diagram.write("plasmid_linear.png", "PNG")


# Notice that the fragments argument which we set to four controls how many pieces the genome gets broken up into.

# If you want to do a circular figure, then try this:

gd_diagram.draw(format="circular", circular=True, pagesize=(20*cm,20*cm),
                start=0, end=len(record), circle_core=0.7)
gd_diagram.write("plasmid_circular.pdf", "PDF")



























# Original

# record = SeqIO.read("NC_005816.gb", "genbank")
#
# # We're using a top down approach, so after loading in our sequence we next create an empty diagram, then add an (empty) track, and to that add an (empty) feature set:
#
# gd_diagram = GenomeDiagram.Diagram("Yersinia pestis biovar Microtus plasmid pPCP1")
# gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
# gd_feature_set = gd_track_for_features.new_set()
#
# # Now the fun part - we take each gene SeqFeature object in our SeqRecord, and use it to generate a feature on the diagram. We're going to color them blue, alternating between a dark blue and a light blue.
#
# for feature in record.features:
#     if feature.type != "gene":
#         #Exclude this feature
#         continue
#     if len(gd_feature_set) % 2 == 0:
#         color = colors.blue
#     else:
#         color = colors.lightblue
#     gd_feature_set.add_feature(feature, color=color, label=True)
#
# # Now we come to actually making the output file. This happens in two steps, first we call the draw method, which creates all the shapes using ReportLab objects. Then we call the write method which renders these to the requested file format. Note you can output in multiple file formats:
#
# gd_diagram.draw(format="linear", orientation="landscape", pagesize='A4',
#                 fragments=4, start=0, end=len(record))
# gd_diagram.write("plasmid_linear.pdf", "PDF")
# gd_diagram.write("plasmid_linear.eps", "EPS")
# gd_diagram.write("plasmid_linear.svg", "SVG")
# # Also, provided you have the dependencies installed, you can also do bitmaps, for example:
#
# gd_diagram.write("plasmid_linear.png", "PNG")
#
#
# # Notice that the fragments argument which we set to four controls how many pieces the genome gets broken up into.
# #
# # If you want to do a circular figure, then try this:
#
# gd_diagram.draw(format="circular", circular=True, pagesize=(20*cm,20*cm),
#                 start=0, end=len(record), circle_core=0.7)
# gd_diagram.write("plasmid_circular.pdf", "PDF")
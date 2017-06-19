from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib.colors import red, grey, orange, green, brown, blue, lightblue, purple
from Bio.SeqUtils import GC, GC_skew, GC123
import os

A_rec = SeqIO.read("NC_002703.gbk", "gb")
B_rec = SeqIO.read("AF323668.gbk", "gb")

A_colors = [red]*5 + [grey]*7 + [orange]*2 + [grey]*2 + [orange] + [grey]*11 + [green]*4 \
         + [grey] + [green]*2 + [grey, green] + [brown]*5 + [blue]*4 + [lightblue]*5 \
         + [grey, lightblue] + [purple]*2 + [grey]
B_colors = [red]*6 + [grey]*8 + [orange]*2 + [grey] + [orange] + [grey]*21 + [green]*5 \
         + [grey] + [brown]*4 + [blue]*3 + [lightblue]*3 + [grey]*5 + [purple]*2

name = "Proux Fig 6"
gd_diagram = GenomeDiagram.Diagram(name)

# max_len = 0
# for record, gene_colors in zip([A_rec, B_rec], [A_colors, B_colors]):
#     max_len = max(max_len, len(record))
#     gd_track_for_features = gd_diagram.new_track(1, name=record.name, greytrack=True, start=0, end=len(record), scale=1)
#     gd_feature_set = gd_track_for_features.new_set()
#     gd_graph_set = gd_track_for_features.new_set('graph')
#
#     graphData = GC_skew(record.seq, 20)
#     graphData = [(i*20, graphData[i]) for i in range(len(graphData))]
#     print graphData
#
#     gd_graph_set.new_graph(graphData,style="line")
#
#     i = 0
#     for feature in record.features:
#         print feature
#         if feature.type != "gene":
#             #Exclude this feature
#             continue
#         gd_feature_set.add_feature(feature, color=gene_colors[i], label=True, name = str(i+1), label_position="start", label_size = 6, label_angle=0, style="line")
#
#         i+=1

#################### TRACK 1 ##############################

gd_track_for_features = gd_diagram.new_track(1, name=A_rec.name, greytrack=True, start = 0, end=len(A_rec), scale=1)
gd_feature_set = gd_track_for_features.new_set()
gd_graph_set = gd_track_for_features.new_set('graph')

graphData = GC_skew(A_rec.seq, 23)
graphData = [(i*23, graphData[i]) for i in range(len(graphData))]
print graphData

gd_graph_set.new_graph(graphData,style="line")

i = 0
for feature in A_rec.features:
    if feature.type != "gene":
        # Exclude this feature
        continue
    gd_feature_set.add_feature(feature, color=A_colors[i], label=True, name = str(i+1), label_position="start", label_size = 6, label_angle=0, style="line")

    i+=1

##################### TRACK 2 ##########################

gd_track_for_features = gd_diagram.new_track(2, name=B_rec.name, greytrack=True, start = 0, end=len(B_rec), scale=1)
gd_feature_set = gd_track_for_features.new_set()
gd_graph_set = gd_track_for_features.new_set('graph')

graphData = GC_skew(B_rec.seq, 20)
graphData = [(i*20, graphData[i]) for i in range(len(graphData))]
print graphData

gd_graph_set.new_graph(graphData,style="line")

i = 0
for feature in B_rec.features:
    if feature.type != "gene":
        #Exclude this feature
        continue
    gd_feature_set.add_feature(feature, color=B_colors[i], label=True, name = str(i+1), label_position="start", label_size = 6, label_angle=0, style="line")

    i+=1

max_len = max(len(A_rec), len(B_rec))
print max_len
gd_diagram.draw(format="circular", pagesize='A4', fragments=100, start=0, end=max_len, fragment_size=2)

gd_diagram.write(name + ".pdf", "PDF")

# gd_diagram.write(name + ".eps", "EPS")
# gd_diagram.write(name + ".svg", "SVG")

os.system("open " + "Proux\ Fig\ 6" + ".pdf")
from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib.colors import red, grey, orange, green, brown, blue, lightblue, purple
from reportlab.lib import colors
from Bio.SeqUtils import GC, GC_skew, GC123



# the data
record = SeqIO.read("NC_002703.gbk", "gb")



# list of all data
records = [record]



############################ features/graphs < featureSets/graphSets < tracks < diagram ############################

# name of the figure
name = "IDK"



# create the diagram -- highest level container for everything
# the diagram directly contains tracks
# the diagram has levels -- for circular the innermost level is the lowest -- for linear the top level is the lowest
# after you are done building the diagram you call the .draw method to display it and the .write method to save it
diagram = GenomeDiagram.Diagram(name)



# create tracks -- and add them to the diagram
inner_track = diagram.new_track(1, greytrack=1, name="Inner Track", height=1.0, hide=0, greytrack_labels=2, greytrack_font_size=8,grey_track_font_color=colors.Color(0.6,0.6,0.6), scale=1, scale_color=colors.black, scale_font='Helvetica', scale_fontsize=6, scale_fontangle=45, scale_ticks=1, scale_largeticks=0.5, scale_smallticks=0.3, scale_largetick_interval=1000000, scale_small_tick_interval=10000, scale_largetick_labels=1, scale_smalltick_labels=0)
outer_track = diagram.new_track(2, greytrack=1, name="Outer Track", height=1.0, hide=0, greytrack_labels=2, greytrack_font_size=8,grey_track_font_color=colors.Color(0.6,0.6,0.6), scale=1, scale_color=colors.black, scale_font='Helvetica', scale_fontsize=6, scale_fontangle=45, scale_ticks=1, scale_largeticks=0.5, scale_smallticks=0.3, scale_largetick_interval=1000000, scale_small_tick_interval=10000, scale_largetick_labels=1, scale_smalltick_labels=0)



#create graph sets and feature sets -- and add them to tracks
graphSet = inner_track.new_set('graph')
featureSet = outer_track.new_set('feature')



#create a graph and add it to a graph set
graphData = GC_skew(record.seq, 23)
graphData = [(i * 23, graphData[i]) for i in range(len(graphData))]

graphSet.new_graph(graphData, style="line")



#add features to a feature set
i = 0
for feature in record.features:
    if feature.type != "gene":
        #Exclude this feature
        continue
    featureSet.add_feature(feature, color='red', label=False, name=str(i+1), label_position="start", label_size=6, label_angle=0)
    i+=1



#build the diagram
# if there is more than one record take the max of all the records
max_len = max([len(r) for r in records])
# in the case of 1 record the following would be equivalent
# max_len = max(len(record))
diagram.draw(format="circular", pagesize='A4', fragments=100, start=0, end=max_len, fragment_size=2)



# save the file(s)
diagram.write(name + ".pdf", "PDF")
# diagram.write(name + ".eps", "EPS")
# diagram.write(name + ".svg", "SVG")
# diagram.write(name + ".png", "PNG")

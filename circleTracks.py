from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib.colors import red, grey, orange, green, brown, blue, lightblue, purple
from reportlab.lib import colors
from Bio.SeqUtils import GC, GC_skew, GC123



# the data
record = SeqIO.read("NC_002703.gbk", "gb")
print record


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


# def new_graph(self, data, name=None, style='bar', color=colors.lightgreen,
#  87                    altcolor=colors.darkseagreen, linewidth=1, center=None,
#  88                    colour=None, altcolour=None, centre=None):
#  89          """ new_graph(self, data, name=None, style='bar', color=colors.lightgreen,
#  90                    altcolor=colors.darkseagreen)
#  91
#  92              o data      List of (position, value) int tuples
#  93
#  94              o name      String, description of the graph
#  95
#  96              o style     String ('bar', 'heat', 'line') describing how the graph
#  97                          will be drawn
#  98
#  99              o color    colors.Color describing the color to draw all or 'high'
# 100                         (some styles) data (overridden by backwards compatible
# 101                         argument with UK spelling, colour).
# 102
# 103              o altcolor  colors.Color describing the color to draw 'low' (some
# 104                          styles) data (overridden by backwards compatible argument
# 105                          with UK spelling, colour).
# 106
# 107              o linewidth     Float describing linewidth for graph
# 108
# 109              o center        Float setting the value at which the x-axis
# 110                              crosses the y-axis (overridden by backwards
# 111                              compatible argument with UK spelling, centre)
# 112
# 113              Add a GraphData object to the diagram (will be stored
# 114              internally
#
# #create graph sets and feature sets -- and add them to tracks
# graphSet = inner_track.new_set('graph')
# featureSet = outer_track.new_set('feature')



#create a graph and add it to a graph set
graphData = GC_skew(record.seq, 23)
graphData = [(i * 23, graphData[i]) for i in range(len(graphData))]

graphSet.new_graph(graphData, style="line", colour=colors.lightgreen, altcolour=colors.darkseagreen)



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
diagram.draw(format="circular", pagesize='A4', orientation='landscape', x=0.05, y=0.05, track_size=0.75, tracklines=0, fragments=100, start=0, end=max_len, fragment_size=2, circular=0)



# save the file(s)
diagram.write(name + ".pdf", "PDF")
# diagram.write(name + ".eps", "EPS")
# diagram.write(name + ".svg", "SVG")
# diagram.write(name + ".png", "PNG")

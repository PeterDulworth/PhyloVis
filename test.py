import networkx as nx

# plain graph

G = nx.complete_graph(5)   # start with K5 in networkx
A = nx.nx_agraph.to_agraph(G)        # convert to a graphviz graph
A.layout()            # neato layout
A.draw("k5.ps")
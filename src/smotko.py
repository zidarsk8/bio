import re
import networkx as nx
import pylab
from collections import defaultdict, Counter
from math import log
import sys
import random
from IPython.core.display import Math
import math
if __name__ == '__main__':
    database = open('data/morbidmap').readlines()[:200]
    
    # 1.Create the network
    
    G = nx.Graph()
    genes = defaultdict(set)
    ngenes = defaultdict(int)
    nclusters = defaultdict(int)
    draw_labels = defaultdict(int)
    for d in database:
        fields = d.strip().split('|')
        start = re.search('[A-Za-z]', fields[0]).start()
        end = re.search('[A-Za-z \-]*', fields[0][start:]).end() # TODO: ending dash?
        name = fields[0][start:start+end].strip()
        
        genes[name] = genes[name].union(set(fields[1].split(', ')))
        ngenes[name] += len(genes[name])
        
        if name not in G:
            G.add_node(name, new_name=name)

        for n in genes:
            if n == name: continue
            if len(genes[name].intersection(genes[n])) > 0:
                G.add_edge(name, n)
        
                
        nclusters[name] = 0
        
    # 2. Analyze the network [TODO]
        
    conn_comp = [len(c) for c in nx.connected_component_subgraphs(G)]
    
#    pylab.bar(range(len(conn_comp)), conn_comp)
#    pylab.figure(1)
#    pylab.yscale('log')
#    pylab.xlabel("Distribution of sizes of connected components")
#    pylab.ylabel("TODO")
#    pylab.title("TODO")
    #pylab.show()
        
#    hist = nx.degree_histogram(G)
#    pylab.figure(2)
#    pylab.subplot(121)
#    pylab.bar(range(len(hist)), hist, lw=1)
#    pylab.xlabel("Degree distribution of the network ")
#    pylab.ylabel("TODO")
#    pylab.title("TODO")
#    
#    pylab.subplot(122)
#    pylab.bar(range(len(hist)), [log(h+1) for h in hist])
#
#    pylab.xlabel("Degree distribution of the network (log)")
#    pylab.ylabel("TODO")
#    pylab.title("TODO")
    #pylab.show()
    
    
    # 3. Clustering [TODO]
    
    G=nx.connected_component_subgraphs(G)[0]
    cluster_labels = {g:g for g in G.nodes()}
    for i in range(100):
        newG = nx.Graph()
        nodes = G.nodes()
        random.shuffle(nodes)
        for n in nodes:
            neighbors = G.neighbors(n)
            c  = Counter(cluster_labels[nei] for nei in neighbors)
            if len(c.most_common(1)) > 0: 
                new_label = c.most_common(1)[0][0] 
                cluster_labels[n] = new_label
                
    # 4. Extract clusters [TODO]
    
    pos = nx.spring_layout(G, iterations=500)
    
    for l in cluster_labels:
        nclusters[l] = sum(ord(i) for i in cluster_labels[l]) % 255 #len(cluster_labels[l])
        draw_labels[cluster_labels[l]] += 1
        
    
    onlyclusters = {}
    for p in pos:
        if draw_labels[p] > 15:
            onlyclusters[p] = pos[p]
        else:
            onlyclusters[p] = [-100, -100]

    nodes = G.nodes() #fix node positions
    nx.draw_networkx_nodes(G, pos, nodes,
        node_size = [ (ngenes[a])*0.8 for a in nodes],
        node_color = [ nclusters[a] for a in nodes ],
        linewidths = 1,
        alpha=0.4) #just because the colors are dark
    #print [n for n in nclusters if n > 1]
    #print pos
    #print {p:pos[p] for p in pos if nclusters[p] > 1}
    
    
    nx.draw_networkx_labels(G, onlyclusters)
    nx.draw_networkx_edges(G, pos, alpha=0.2, width = 0.3)
    #pylab.figure(1)
    pylab.axis("off")
    pylab.show()
    #pylab.savefig("nicer.pdf")

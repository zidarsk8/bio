import networkx as nx
import collections
import random
import pylab
import re
import lev

def getReverseIndex(joined):
    ri = collections.defaultdict(list) 

    [[ri[gene].append(name) for gene in genes] 
            for name, genes in joined.items()]

    return ri

def getData(size = 100000):
    
    l = [i.strip().split("|")[:2] 
            for i in open("data/morbidmap").readlines()[:size]]

    l = map(lambda x: (
        re.search('\W*([A-Za-z -]*[A-Za-z]).*', x[0]).group(1), 
        set([i.strip() for i in x[1].split(",")]) )
        ,l)

    joined = collections.defaultdict(set)
    for (i,j) in l:
        joined[i] = joined[i].union(j) 

    return joined


def getNxGraph(joined, connectedOnly = True):
    ri = getReverseIndex(joined)
    G = nx.Graph()
    if not connectedOnly:
        [G.add_node(name) for name in joined.keys()]

    [G.add_edge(name,othername) 
            for name, genes in joined.items() 
            for gene in genes 
            for othername in ri[gene] if name != othername]
    
    return G

def getClusters(g, iterLimit=100):

    clusters = {j:i for i,j in enumerate(g.nodes())}

    def labelCounter(nei):
        return collections.Counter(clusters[n] for n in nei)

    for i in xrange(iterLimit):
        nodes = g.nodes()
        random.shuffle(nodes)
        for node in nodes:
            count = labelCounter(g.neighbors(node))
            if len(count) == 0:
                continue

            m = max(count.itervalues())
            candidates = [i for i,j in count.iteritems() if j == m]
            random.shuffle(candidates)
            clusters[node] = candidates[0]

    return clusters


def plotG(G, ngenes, iterations = 50):

    nclusters = getClusters(G)

    pos = nx.spring_layout(G, iterations=iterations)
    nx.draw(G, pos)
    #pylab.savefig("dsull.pdf")

    pylab.clf() #prepare a new figure

    nodes = G.nodes() #fix node positions
    nx.draw_networkx_nodes(G, pos, nodes,
        node_size = [ 50*ngenes[a] for a in nodes],
        node_color = [ nclusters[a] for a in nodes ],
        linewidths = 0.1,
        alpha=0.4) #just because the colors are dark

    # turn this on when cluster
    #nx.draw_networkx_labels(G, pos)

    nx.draw_networkx_edges(G, pos, alpha=0.2)

    pylab.axis("off")
    pylab.show()
    #pylab.savefig("nicer.pdf")

joined = getData(3000)

G = getNxGraph(joined)

size = lambda x: len(x)**(8/10.)
ngenes = {name:size(genes) for name, genes in joined.items()}

plotG(nx.connected_component_subgraphs(G)[0], ngenes)

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

def getClusters(g, iterLimit=1000):

    clusters = {j:i for i,j in enumerate(g.nodes())}

    def labelCounter(nei):
        return collections.Counter(clusters[n] for n in nei)

    def getCandidate(count):
        m = max(count.itervalues())
        c = [i for i,j in count.iteritems() if j == m]
        random.shuffle(c)
        return c[0]

    for ii in xrange(iterLimit):
        change = False
        nodes = g.nodes()
        random.shuffle(nodes)
        for node in nodes:
            count = labelCounter(g.neighbors(node))
            if len(count) == 0:
                continue

            candidate = getCandidate(count)

            change |= clusters[node] != candidate

            clusters[node] = candidate

        if not change :
            break
            

    ind = set(clusters.values())
    mainNodes = [j for i,j in enumerate(g.nodes()) if i in ind]
    return clusters


def plotG(G, ngenes, iterations = 100):

    nclusters = getClusters(G)

    pos = nx.spring_layout(G, iterations=iterations)
    nx.draw(G, pos)
    #pylab.savefig("dsull.pdf")

    pylab.clf() #prepare a new figure

    nodes = G.nodes() #fix node positions
    nx.draw_networkx_nodes(G, pos, nodes,
        node_size = [ ngenes[a] for a in nodes],
        node_color = [ nclusters[a] for a in nodes ],
        linewidths = 0.1,
        alpha=0.4) #just because the colors are dark

    nx.draw_networkx_edges(G, pos, alpha=0.2)


    #nx.draw_networkx_labels(G, pos)

    pylab.axis("off")
    pylab.show()
    #pylab.savefig("nicer.pdf")

joined = getData(3000)

G = getNxGraph(joined)

size = lambda x: len(x)**(8/10.) * 50
ngenes = {name:size(genes) for name, genes in joined.items()}

plotG(nx.connected_component_subgraphs(G)[0], ngenes)


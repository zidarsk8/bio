import matplotlib.pyplot as plt
import networkx as nx
import collections
import cPickle
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
    print "cluster iterations: %4d" % ii

    ind = set(clusters.values())
    mainNodes = [j for i,j in enumerate(g.nodes()) if i in ind]
    return clusters


def plotG(G, pos, ngenes, nclusters, joined, allLabels = False, fontSize = 10):


    print "number of nodes:    %4d" % len(G.nodes())
    print "number of edges:    %4d" % len(G.edges())
    print "number of clusters: %4d" % len(set(nclusters.values()))


    nx.draw(G, pos) #somehow makes bg white
    pylab.clf() #prepare a new figure

    nodes = G.nodes() #fix node positions
    nx.draw_networkx_nodes(G, pos, nodes,
        node_size = [ ngenes[a] for a in nodes],
        node_color = [ nclusters[a] for a in nodes ],
        linewidths = 0.1,
        alpha=0.4) #just because the colors are dark

    nx.draw_networkx_edges(G, pos, alpha=0.2, width = 0.4)

    ri = getReverseIndex({i:[j] for i,j in nclusters.items()})
    ri = [i[1] for i in ri.items()]
    
    cCount = {i:len(j) for i,j in joined.items()}

    cLabels = set([sorted([(cCount[j],j) for j in i])[-1][1] for i in ri])
    
    cpos = {p: (pos[p] if (p in cLabels) or allLabels else [100,100])  
            for i,p in enumerate(pos)}

    nx.draw_networkx_labels(G, cpos, font_size=fontSize)


    pylab.axis("off")
    pylab.show()
    #pylab.savefig("nicer.pdf")

    

def plotDegreeDistribution(G, log=False):
    deg = nx.degree_histogram(G)
    if log:
        deg = [i+1 for i in deg]
        plt.yscale('log')
        plt.xscale('log')
    l = plt.plot(range(len(deg)), deg)
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.title('Degree distribution of the network')
    plt.show()


def plotSizesOfConnected(G):
    deg = sorted(map(len,G))[:-1]

    n, bins, patches = plt.hist(deg, 20, facecolor='blue', log=True)
    plt.xlabel('Degree')
    plt.ylabel('Count')
    plt.title('Distribution of sizes of connected components')
    plt.show()


def extractCluster(joined,clusters,name):
    cl = clusters[name]
    elements = set([i for i,j in clusters.items() if j == cl])
    joined = {i:j for i,j in joined.items() if i in elements}

    G = getNxGraph(joined, False)
    subgraphs = nx.connected_component_subgraphs(G)
    pos = nx.spring_layout(subgraphs[0], iterations=500 )

    size2 = lambda x: (len(x) * 50 )**(8/10.)
    ngenes = {name:size2(genes) for name, genes in joined.items()}
    nclusters = {i:1 for i in elements}

    plotG(G, pos, ngenes, nclusters, joined, True, 8)



#joined = getData()
#
#G = getNxGraph(joined, False)
#subgraphs = nx.connected_component_subgraphs(G)
#pos = nx.spring_layout(subgraphs[0], iterations=500 )
#nclusters = getClusters(subgraphs[0],5000)
#
#size1 = lambda x: len(x)**(8/10.) * 50
#size2 = lambda x: (len(x) * 50 )**(8/10.)
#ngenes = {name:size2(genes) for name, genes in joined.items()}
#
#cPickle.dump((joined,G,subgraphs,pos,nclusters,ngenes), open("data/dump.pkl","w"))

joined,G,subgraphs,pos,nclusters,ngenes = cPickle.load(open("data/dump.pkl"))



plotG(subgraphs[0], pos, ngenes, nclusters, joined)
plotDegreeDistribution(G)
plotDegreeDistribution(G,True)
plotSizesOfConnected(subgraphs)

print "largest diameter:   %4d" % nx.diameter(subgraphs[0])

for name in ["Breast cancer", "Deafness", "Diabetes mellitus"]:
    extractCluster(joined, nclusters, name)


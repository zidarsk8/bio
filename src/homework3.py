import NeedlemanWunsch
import mitochondrion

def showDendrogram(a):
    distance = n.dictToMatrix(a)
    for i in range(len(distance)):
        for j in range(i,len(distance[i])):
            distance[i][j] = distance[j][i]

    names = [i['english']+"\n("+i['latin']+")" for i in m]

    import pylab
    from scipy.cluster.hierarchy import dendrogram, linkage


    dendrogram(linkage(distance, 'average'), 30, labels = names, 
            orientation = "left", color_threshold=300) 
    pylab.xlabel("Alignment score")
    pylab.ylabel("Species")
    pylab.show()


n = NeedlemanWunsch.NW()
n.gapPenalty = -11

m = mitochondrion.getDict()

a = {(i,j):n.similarityScore(m[i]['COX3'],m[j]['COX3']) 
        for i in range(len(m)) for j in range(i+1)}
        
n.printMatrix(a)
for i,j in enumerate(m):
    print "%3d & %13s & %26s & %30s " % (i,j['id'],j['english'],j['latin'])

showDendrogram(a)


import NeedlemanWunsch
import mitochondrion
reload(NeedlemanWunsch)



n = NeedlemanWunsch.NW()
m = mitochondrion.getDict()

a = {(i,j):n.similarityScore(m[i]['COX3'],m[j]['COX3']) for i in range(len(m)) for j in range(i+1)}
        
n.printMatrix(a)

for i,j in enumerate(m):
    print i,j['english']

distance = n.dictToMatrix(a)
for i in range(len(distance)):
    for j in range(i,len(distance[i])):
        distance[i][j] = distance[j][i]



import pylab
dendrogram(linkage(dist, 'average'), 30, labels = [a['name'] for a in animals], orientation = "left", color_threshold=300) 
pylab.xlabel("Alignment score")
pylab.ylabel("Species")
pylab.title("Evolutionary Tree")
pylab.show()

#
#
#
##n.printMatrix(a)
#
#

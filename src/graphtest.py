from apgl.graph import DenseGraph
import numpy

numVertices = 10

graph = DenseGraph(numVertices)
graph[1, 5] = 1
graph[1, 3] = 1
graph[1, 2] = 1
graph[2, 3] = 1
graph[3, 4] = 1
graph[4, 6] = 1
graph[4, 7] = 1
graph[8, 9] = 1

print graph.degreeDistribution() 
print graph.diameter(False)


from collections import defaultdict
import numpy as np

class NW:

    blosum = None
    gapPenalty = -5
    s = ""
    t = ""

    def __init__(self):

        self.blosum = self.setBlosum(filename)

    def setBlosum(self,b):
        blosum = {}
        for i,j in b:
            x,y = i
            blosum[x,y] = j
            blosum[y,x] = j

    def setBlosum62(self):
        from Bio.SubsMat.MatrixInfo import blosum62
        self.setBlosum(blosum62)

    def setBlosum50(self):
        from Bio.SubsMat.MatrixInfo import blosum62
        self.setBlosum(blosum62)

    def setBlosumFromFile(self,filename):
        l = [[j for j in i.strip().split(" ")] for i in open(filename).readlines()]
        j = l[0]
        i = [a[0] for a in l[1:]]
        b = {}
        for ii in range(len(i)):
            for jj in range(len(j)):
                b[i[ii],j[jj]] = int(l[ii+1][jj+1])
        self.blosum = b

    def cost(self,M,i,j):
        iGap = (M[i-1,j][0]+self.gapPenalty, (i-1,j) )
        jGap = (M[i,j-1][0]+self.gapPenalty, (j,i-1))
        noGap = (M[i-1,j-1][0]+self.blosum[self.s[i],self.t[j]], (i-1,j-1))
        
        M[i,j] = max(iGap,jGap,noGap)


    def similarityMatrix(self,s,t):
        self.s = s
        self.t = t

        # dict of (score, list of tuples from the best score, has gap)
        M = defaultdict(lambda: (0,[]))

        for i in range(len(s)):
            M[i,-1] = (M[i-1,-1][0] + self.gapPenalty, (i-1, 0))
        for j in range(len(t)):
            M[-1,j] = (M[-1,j-1][0] + self.gapPenalty, (0,j-1))

        [self.cost(M,i,j) for i in range(len(s)) for j in range(len(t))]

        return M

    def dictToFullMatrix(self, M):
        mi = max([i[0] for i in M.keys()])
        mj = max([i[1] for i in M.keys()])
        
        a = [[0 for j in range(mj+2)] for i in range(mi+2)]

        for i,j in M.items():
            a[i[0]+1][i[1]+1] = j[0]
        return a

    def printMatrix(self, M, space=5):
        m = self.dictToFullMatrix(M)
        for i in m:
            print "".join([("%%%dd" % space) % j for j in i])



f = open('data/rosalind_glob_test.txt')
f = open('data/rosalind_glob.txt')
s = f.readline().strip()
t = f.readline().strip()

n = NW()

a = n.similarityMatrix(s,t)

print max(i[0] for i in a.values())

#n.printMatrix(a)



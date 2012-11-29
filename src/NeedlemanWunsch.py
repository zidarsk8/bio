from collections import defaultdict

class NW:

    blosum = None
    gapPenalty = -5
    s = ""
    t = ""

    def __init__(self):
        self.setBlosum50()

    def setBlosum(self,b):
        self.blosum = {}
        for i,j in b.items():
            x,y = i
            self.blosum[x,y] = j
            self.blosum[y,x] = j

    def setBlosum62(self):
        from Bio.SubsMat.MatrixInfo import blosum62
        self.setBlosum(blosum62)

    def setBlosum50(self):
        from Bio.SubsMat.MatrixInfo import blosum50
        self.setBlosum(blosum50)

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

    def similarityScore(self, s, t):
        a = self.similarityMatrix(s,t)
        return a[len(s)-1, len(t)-1][0]

    def costDictToMatrix(self, M):
        return self.dictToMatrix({i:j[0] for i,j in M.items()})

    def dictToMatrix(self, M, fromZero=False):
        xkeys = [i[0] for i in M.keys()]
        ykeys = [i[1] for i in M.keys()]

        dx0 = min(xkeys, 0) if fromZero else min(xkeys) 
        dy0 = min(ykeys, 0) if fromZero else min(ykeys)
        lenx = max(xkeys) - dx0
        leny = max(ykeys) - dy0
        
        a = [[0 for j in range(leny+1)] for i in range(lenx+1)]

        for i,j in M.items():
            a[i[0]-dx0][i[1]-dy0] = j
        return a

    def printCostMatrix(self, M, space=5):
        m = self.costDictToMatrix(M)
        for i in m:
            print "".join([("%%%dd" % space) % j for j in i])

    def printMatrix(self, M, space=5):
        m = self.dictToMatrix(M)
        for i in m:
            print "".join([("%%%dd" % space) % j for j in i])



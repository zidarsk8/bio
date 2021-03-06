from bisect import bisect_left
from random import shuffle
from math import log
import numpy as np

# returns the number of bits set to 1 in a number
def countOnes(n):
    return bin(n).count("1")

# calculates information gain between two bitmaps (integers)
# x,y must be {n: number, c: numberOfOnes, s: sizeRepresented}
# I should get rid of the size since it's in x and y but too lazy
def ggain(x,y):
    size = max(x["s"],y["s"])
    x1 = x["c"]
    y1 = y["c"]
    x1y1 = countOnes(x["n"]&y["n"])
    x1y0 = x1 - x1y1
    x0y1 = y1 - x1y1
    x0y0 = size - x1y1 - x1y0 - x0y1
    px1 = x1 / float(size)
    py1 = y1 / float(size)
    px0 = 1 - px1
    py0 = 1 - py1
    px1y1 = x1y1 / float(size)
    px1y0 = x1y0 / float(size)
    px0y1 = x0y1 / float(size)
    px0y0 = x0y0 / float(size)
    return  (0 if x1y1==0 else x1y1 * log((px1y1)/(px1*py1),2)) + \
        (0 if x0y1==0 else px0y1 * log((px0y1)/(px0*py1),2)) + \
        (0 if x1y0==0 else px1y0 * log((px1y0)/(px1*py0),2)) + \
        (0 if x0y0==0 else px0y0 * log((px0y0)/(px0*py0),2)) 

def gain(x,y):
    xn = int(''.join(x),2)
    yn = int(''.join(y),2)
    
    xx = {'n':xn, 'c':x.count('1'), 's': len(x)}
    yy = {'n':yn, 'c':y.count('1'), 's': len(y)}
    
    print xx
    print yy

    return ggain(xx,yy)
# calculates and returns Info gain values for each pair of values from
# attributeArray and classArray
# the information is then pickled and if a pickle file exists it gets
# used insted of calculating again
def getOriginalGains(attribArr,classArr,clean=False):
    orig = {}
    for ci, clas in enumerate(classArr):
        orig[ci] = {} 
        for ai, attr in enumerate(attribArr):
            orig[ci][ai] = gain(clas,attr)
    return orig

# calculates info gain between the attrributeArray and random permutations of 
# classArray. 
# function returns a sorted list of all random gains for each pair of numbers
def getRandomGains(attribArr,clas,permutations):
    # najlazi je na zacetku hitr inicializirat randomGains tabelo
    rg = {}
    for a in range(len(attribArr)): rg[a] = []
    
    rArr = list(bin(clas["n"])[2:])
    for i in xrange(permutations): #for testing 
        shuffle(rArr)
        rc = {"n":int("".join(rArr),2), "s":clas["s"], "c":clas["c"]}
        [rg[ai].append(gain(rc,attr)) for ai, attr in enumerate(attribArr)]
    [a.sort() for a in rg.values()]
    return rg

def getGainValues(td, tl, orig, clas = 0, iterations = 100):
    #global orig, td, tl, trainD, y, m, n, maxLabel
    res = []
    rand = getRandomGains(td,tl[clas],iterations)
    # uzame random info gaine, in shrani tuple, lokacija (1 je najbolsa 0 najslabsa), stevilo nenicelnih, in index.
    # hkrati pa tudi filtrira da je stevilo nenicelnih vecje od filtra
    res.append(sorted([(bisect_left(rand[j],orig[clas][j])/float(iterations),td[j]["c"],j)\
            for j in xrange(len(orig[clas]))],reverse = True))
    return res

def getMeje(x,maxUnique = 100):
    un = np.unique(x)
    if un.size > maxUnique:
        ind = [int(float(i)/un.size*maxUnique) for i in range(un.size)]+[maxUnique]
        ind[0] = -1
        un = np.array([j for i,j in enumerate(un) if ind[i] != ind[i+1]])
    return (un[1:]+un[:-1])/2
    

def binarizeXmean(x,num = True):
    if not num:
        return x.mean();
    xbin = int("".join(["1" if i>x.mean() else "0" for i in x]),2)
    return {"c": countOnes(xbin), "n":xbin,"s":len(x)}

def binarizeX(x,y,num = True,maxUnique=50):
    oldg = 0
    best = {"c": 0, "n":0,"s":len(x)} if num else 0.5
    meje = getMeje(x,maxUnique) #dobi meje po katerih bo probal razdeliti x
    for s in meje:
        xbin = int("".join(["1" if i>s else "0" for i in x]),2)
        xbin = {"c": countOnes(xbin), "n":xbin,"s":len(x)}
        g = gain(xbin, y)
        if g>oldg:
            best = xbin if num else s
            oldg = g
    return best
    #td = [int("".join(["1" if i>minval else "0" for i in x]),2) for x in trainD.T]
    #td = [{"c": countOnes(i), "n":i,"s":m} for i in td]
    
def getGains(X,y,permutations = 1000, nonzero=50):
    m = X.shape[0] 
    yy = int("".join([str(int(a)) for a in y]),2);
    tl = [{"c": countOnes(yy), "n":yy,"s":m}]
    binVal = [binarizeX(x, tl[0], False) for x in X.T]
    td = [int("".join(["1" if j>binVal[i] else "0" for j in x]),2) for i,x in enumerate(X.T)]
    td = [{"c": countOnes(x), "n":x ,"s":m} for x in td]
    orig = getOriginalGains(td,tl)
    gains = getGainValues(td,tl, orig, clas = 0, iterations = 1000)
    #td[:,[x[2] for x in gains if x[1]>nonzero]] 
    return (binVal,gains)


#koda sposojena od majcna samo za testiranje ali moja dela pravilno
#def mpi_entropy(y, base=2):
#    """Calculate entropy of a discrete distribution/histogram
#    (C) 2009 Christoph Lampert <chl@tuebingen.mpg.de>
#    """
#    invtotal = 1./float(len(y))
#    p = np.array([invtotal*sum(y==l) for l in np.unique(y)])
#    S = -1.0*sum(p*np.log(p))/np.log(base)
#    return S
#
#def condentropy(truelabels, labels):
#    """Calculate conditional entropy of one label distribution given another label distribution
#    (C) 2009 Christoph Lampert <chl@tuebingen.mpg.de>
#    """
#    labels=np.array(labels)
#    truelabels=np.array(truelabels)
#    condent=0.
#    for l in xrange(min(labels),max(labels)+1):
#        sublabels = truelabels[ labels==l ]
#        condent += len(sublabels)*mpi_entropy( sublabels )
#    return condent/float(len(labels))
#
#def IG(x,y):
#    return mpi_entropy(x) - condentropy(x,y)

if __name__ == "__main__":
    
    c = ['1']*10+['0']*10
    
    shuffle(c)
    
    a1 = list(c)
    
    shuffle(a1)
    
    print c
    print a1
    print gain(a1, c)
    print gain(c, a1)
    
    
    
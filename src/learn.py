from collections import Counter
import Orange
import random
import cPickle
import math




def listToOrangeSingleClass(X,y):
    data, domain, features, class_var = cPickle.load(open('data/orage_tbl.pkl'))
    features += [Orange.feature.Continuous("generated_%d" % i) 
            for i in range(len(X[0])-len(features))]
    domain = Orange.data.Domain(features + [class_var])
    [data.append(Orange.data.Instance(domain, list(X[i])+[y[i]] )) for i in range(len(X))]
    return data




def getProb(trainD, trainC, testD , lrn):
    orangeData = listToOrangeSingleClass(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)

    cl = lrn(orangeTrainD)
    return [cl(i, Orange.classification.Classifier.GetProbabilities)
            for i in orangeTestD]


def nbHist(trainD, trainC, testD):
    prob = nb(trainD, trainC, testD)
    c = predToClass(trainC,prob)
    hist = 50
    trainExtra = [[trainC[max(0,i-hist):i].count("1"), 
        trainC[max(0,i-hist):i].count("2"),
        trainC[max(0,i-hist):i].count("3")] for i in range(len(trainC))]
    
    testExtra = [[y[max(0,i-hist):i].count("1"), 
        c[max(0,i-hist):i].count("2"),
        c[max(0,i-hist):i].count("3")] for i in range(len(c))]

    trainD = [trainD[i]+trainExtra[i] for i in range(len(trainD))]
    testD = [testD[i]+testExtra[i] for i in range(len(testD))]

    return nb(trainD, trainC, testD)

def nb(trainD, trainC, testD):
    learner = Orange.classification.bayes.NaiveLearner(name="naiveBayes")
    return getProb(trainD, trainC, testD, learner)

def knn(trainD, trainC, testD):
    knnLearner = Orange.classification.knn.kNNLearner(name="knn")
    return getProb(trainD, trainC, testD, knnLearner)

def randInt(f,t,n):
    start = f + int(random.random() * (t - f - n))
    return (start, start + n)

def selectBest(p):
    p = map(list,p)
    return [str(i.index(max(i))+1) for i in p]

def predToClass(y,p,av=10):
    c = Counter(y)
    p = zip(*[[sum(b[max(0,i-av):i+av])/len(b[max(0,i-av):i+av]) 
        for i,j in enumerate(b) ] 
        for b in zip(*p)])
    b = map(lambda x: 1.*sum(x)/len(x), zip(*p))
    return [ "2" if i[1] > b[1] else 
            ("3" if i[2] > b[2] else (
                "1" if i[0] > b[0] else "2")) for i in p  ]

def score(y,p):
    return 1.*len([i for i in xrange(len(y)) if y[i] == p[i]])/len(y)

def crossval(x,y,f,n=6):
    l = len(x)
    segment = int(math.ceil(1.*l/n))
    res = []
    for i in range(0, l, segment):
        trainx = x[i : i+segment]
        trainy = y[i : i+segment]
        interval = max( 
                ( i , randInt(0,i,segment) ) , 
                ( l-(i+segment) , randInt(i+segment,l,segment)))[1]
        #print i , i+segment , interval
        testx = x[interval[0]: interval[1]]
        testy = y[interval[0]: interval[1]]
        predy = f(trainx, trainy, testx)
        c = selectBest(predy)
        print score(trainy, c)

        res += c

    return res


def makeSubmission(fn ,lrn, sel, x,y,d):
    a = open("data/%s" % fn,'w')
    a.write("\n".join(selectBest(nbHist(x,y,d))))
    a.flush()
    a.close()


x,y,d = cPickle.load(open('data/pack_small.pkl'))
x,y,d = cPickle.load(open('data/pack.pkl'))

#r = crossval(x, y, nbHist, 6)
#print score(y,r)
#prob = knn(X[100:],y[100:],X[:100])

makeSubmission("nb_sel_best.csv",nbHist,selectBest,x,y,d)




import Orange
import random
import cPickle
import math




def listToOrangeSingleClass(X,y):
    data, domain, features, class_var = cPickle.load(open('data/orage_tbl.pkl'))
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



def nb(trainD, trainC, testD):
    learner = Orange.classification.bayes.NaiveLearner(name="naiveBayes")
    return getProb(trainD, trainC, testD, learner)

def knn(trainD, trainC, testD):
    knnLearner = Orange.classification.knn.kNNLearner(name="knn")
    return getProb(trainD, trainC, testD, knnLearner)

def randInt(f,t,n):
    start = f + int(random.random() * (t - f - n))
    return (start, start + n)

def score(y,p):
    return 1.*len([i for i in xrange(len(y)) if y[i] == p[i]])/len(y)

def crossval(x,y,f):
    n = 6
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
        print score(trainy, predy)
        res += predy

    return res




x,y,d = cPickle.load(open('data/pack_small.pkl'))

r = crossval(x, y, nb)

#prob = knn(X[100:],y[100:],X[:100])





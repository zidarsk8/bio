import Orange
lines = [i.strip().split(',') for i in open('data/train.csv').readlines()[1:]]

X = []
y = []

for line in lines:
    X.append(line[1:])
    y.append(line[0])


def listToOrangeSingleClass(X,y):
    features = [Orange.feature.Continuous("%d" % i) for i in range(len(X[0]))]
    class_var = Orange.feature.Discrete("class", values=["0","1","2","3","4"])
    domain = Orange.data.Domain(features + [class_var])
    data = Orange.data.Table(domain)
    [data.append(Orange.data.Instance(domain, list(X[i])+[str(y[i])])) 
            for i in range(len(X))]
    return data




def getProb(trainD, trainC, testD , lrn):
    orangeData = listToOrangeSingleClass(trainD+testD, trainC+[0]*len(testD))
    ind = [1]*len(trainD)+[0]*len(testD)
    orangeTrainD = orangeData.select_ref(ind,1)
    orangeTestD = orangeData.select_ref(ind,0)

    cl = lrn(orangeTrainD)
    return [cl(i, Orange.classification.Classifier.GetProbabilities)
            for i in orangeTestD]


def knn(trainD, trainC, testD):
    knnLearner = Orange.classification.knn.kNNLearner(name="knn")
    return getProb(trainD, trainC, testD, knnLearner)



prob = knn(X[100:],y[100:],X[:100])

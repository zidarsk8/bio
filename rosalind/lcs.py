from collections import defaultdict
from random import shuffle

f = open("data/rosalind_lcs.txt")



def long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and is_substr(data[0][i:i+j], data):
                    substr = data[0][i:i+j]
    return substr

def is_substr(find, data):
    if len(data) < 1 and len(find) < 1:
        return False
    for i in range(len(data)):
        if find not in data[i]:
            return False
    return True




lines = [i.strip() for i in f.readlines()]
    
result = long_substr(lines)



#def substrind(s,t):
#    m = defaultdict(int)
#    for i, ci in enumerate(s):
#        for j, cj in enumerate(t):
#            if ci == cj:
#                m[i,j] = m[i-1,j-1]+1
#    r = set([(i[0]-j+1,i[0]+1) for i,j in m.items()])
#    return m
#f = sorted([(len(lines[i]),i) for i in range(len(lines))])[0][1]
#short = lines.pop(f)
#
#
#
#m = substrind(short,lines[0])
#r = [(i[0]-j+1,i[0]+1) for i,j in m.items()]
#
#for i,item in enumerate(m.items()):
#    print item,r[i],short[r[i][0]:r[i][1]]
#

f = open("data/result_lcs.txt" ,"w")
f.write(result)
f.close()


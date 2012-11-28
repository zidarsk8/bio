from collections import defaultdict

f = open("data/rosalind_lcsq.txt")

    
def substrind(s,t):
    m = defaultdict(lambda: (0,(-1,-1)))
    for i, ci in enumerate(s):
        for j, cj in enumerate(t):
            m[i,j] = max(
                    (m[i-1,j-1][0]+int(ci==cj), (i-1,j-1) ), 
                    (m[i-1,j][0], (i-1,j) ), 
                    (m[i,j-1][0], (i,j-1) ))
    return m

def dictToFullMatrix(M):
    mi = max([i[0] for i in M.keys()])
    mj = max([i[1] for i in M.keys()])
    
    a = [[0 for j in range(mj+2)] for i in range(mi+2)]

    for i,j in M.items():
        a[i[0]+1][i[1]+1] = j[0]
    return a

lines = [i.strip() for i in f.readlines()]

s = lines[0]
t = lines[1]
m = substrind(s,t)

last = (len(s)-1,len(t)-1)
result = []

while m[last][1] > (-1,-1):
    if m[last][0] > m[m[last][1]][0] and s[last[0]] == t[last[1]]:
        result.insert(0,s[last[0]])
    last = m[last][1]
if m[last][0] > m[m[last][1]][0] and s[last[0]] == t[last[1]]:
    result.insert(0,s[last[0]])

result = "".join(result)
    



f = open("data/result_lcsq.txt" ,"w")
f.write(result)
f.close()


from collections import defaultdict

def matrix(s,t):

    def cost(M, i, j):
        iGap = (M[i-1,j][0]+1, (i-1,j,s[i],"-") )
        jGap = (M[i,j-1][0]+1, (i,j-1,"-",t[j]))
        noGap = (M[i-1,j-1][0] + int(s[i]!=t[j]), (i-1,j-1,s[i],t[j]))
        
        M[i,j] = min(iGap,jGap,noGap)

    M = {(i,j): ( j+i+2 , (max(i-1,-1),max(j-1,-1),"","")) for i in range(-1,len(s)) for j in range(-1,len(t))}

    [cost(M,i,j) for i in range(len(s)) for j in range(len(t))]

    return M

def walk(M,s,t):
    last = M[len(s)-1,len(t)-1]
    maxCost = last[0]
    ss = [last[1][2]]
    tt = [last[1][3]]
    while (last[1][0],last[1][1]) != (-1,-1):
        last = M[last[1][0],last[1][1]]
        ss.append(last[1][2])
        tt.append(last[1][3])
    return (maxCost, "".join(ss[::-1]), "".join(tt[::-1]))

    

f = open("data/rosalind_edta_test.txt")
s,t = [i.strip() for i in f.readlines()]

M = matrix(s,t)

m, ss, tt = walk(M,s,t)
result = "%d\n%s\n%s" % (m,ss,tt)
print result

f = open("data/result_edta.txt" ,"w")
f.write(result)
f.close()


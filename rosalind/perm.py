

n = 6
ss = set([str(i) for i in range(1,n+1)])
s = range(10**(n-1),10**n-1)

al = [" ".join(list(str(i))) for i in s if set(str(i)) == ss]

f = open("data/result_perm_%d.txt" % n ,"w")

f.write("%d\n" % len(al))
f.write("\n".join(al))
f.close()

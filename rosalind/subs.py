f = open('data/rosalind_subs.txt')

s = f.readline().strip()
t = f.readline().strip()
lt = len(t)

ind = [str(i+1) for i in xrange(len(s)) if s[i:i+lt] == t]


r = open('data/result_subs.txt', 'w')
r.write(" ".join(ind))
r.close()


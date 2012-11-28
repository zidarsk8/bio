f = open("data/rosalind_sseq.txt")
lines = [i.strip() for i in f.readlines()]

s = lines[0]
t = lines[1]

prev = 0
res = []
for i in t:
    prev = s.find(i,prev)+1
    res.append(prev)

aa = " ".join(map(str,res))


f = open("data/result_sseq.txt" ,"w")
f.write(aa)
f.close()

from collections import Counter
f = open("data/rosalind_cons.txt")

lines = [i.strip() for i in f.readlines()]

l = [Counter(i) for i in zip(*lines)]

order = ['A','C','G','T']

c = [[i[o] for i in l] for o in order]

result = "".join([order[i.index(max(i))] for i in zip(*c)])

result += "\n"+"\n".join([o+": "+(" ".join(map(str,c[i]))) for i,o in enumerate(order)])

print result

f = open("data/result_cons.txt" ,"w")
f.write(result)
f.close()


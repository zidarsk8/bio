f = open("data/rosalind_gc.txt")

lines = ("".join([i.strip() for i in f.readlines()])).split('>')[1:]

def sg(l):
    name = l[:13]
    l = l[13:]
    c = 100.0 * (l.count("G")+l.count("C"))/len(l)
    return (c,name)

c = sorted([sg(i) for i in lines])

f = open("data/result_cg.txt" ,"w")
f.write("%s\n%.6f%%" % (c[-1][1],c[-1][0]))
f.close()


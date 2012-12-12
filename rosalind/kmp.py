
f = open("data/rosalind_kmp_test.txt")

line = f.readline().strip()

p = [0]
start = 1
count = 0
for i in xrange(1,len(line)):
    if line[i-start] == line[i]:
        count += 1
    else:
        start = i+1
        count = 0
    p.append(count)
       

result = " ".join(map(str,p))
print result


f = open("data/result_kmp.txt" ,"w")
f.write(result)
f.close()


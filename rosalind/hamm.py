f = open('data/rosalind_hamm.txt')

l1 = f.readline().strip()
l2 = f.readline().strip()

print sum([ l1[i]!=l2[i] for i in range(min(len(l1),len(l2)))])+max(len(l1),len(l2))-min(len(l1),len(l2))


from collections import Counter

l = open("data/rosalind_dna.txt").readline().strip()

c = Counter(l)

print c['A'], c['C'], c['G'], c['T']

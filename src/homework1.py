"""Sample script that shows the difference between permutation test probabilities and exact calculations."""

from Bio import SeqIO
import collections
import random
from math import log
from matplotlib import pyplot as plt
from math import factorial as f
import functions as fun

log2 = lambda x: log(x, 2)

def count_kmers(s, k):
    """Count k-mers in string s and return a dictionary with counts."""
    d = collections.defaultdict(int)
    for i in xrange(len(s)-(k-1)):
        d[s[i:i+k]] += 1
    return d

def permutation_test(s, kmer,  n=100):
    """Assess odds ratio on permuted string and return a list with scores."""
    res = []
    for _ in range(n):
        random.shuffle(s)
        c = count_kmers("".join(s), len(kmer))
        res.append(c[kmer])
    return res

def kmer_prob_permut(s, kmer, n=100):
    r = permutation_test(list(s), kmer, n)
    return 1.*r.count(kmer)/len(r)

def bp_prob(s, a, b, k):
    n = len(s)
    N = count_kmers(s, 1)
    nn = [(i[1], i[0] in [a,b]) for i in N.items()]
    
    if k > min(N[a],N[b]) or k < 0: 
        return 0 
    
    ns = sum([( f(n-j) / ( reduce(lambda x,y: x*( f(y[0] - (j if y[1] else 0) ) ) , nn, 1) * f(j-k) * f(k) ) ) * (-1)**(j-k)\
              for j in range(k,min(N[a],N[b])+1)])
    
    return (ns / ( f(n) / ( reduce(lambda x,y: x*f(y[0]) , nn, 1) ) / 10**100   )   )*(10.0**(-100))


files = [ "NC_001807.2.fasta", "NC_012920.fasta", "NC_001807.3.fasta", "NC_001807.1.fasta", "NC_012920.1.fasta"]

#res1 = []
#for i in range(5):
#    res1.append([])
#    for j in range(5):
#        if i == j : 
#            res1[-1].append(0)
#            continue
#        s1 = SeqIO.read("data/%s" % files[i], "fasta").seq.tostring().upper()
#        s2 = SeqIO.read("data/%s" % files[j], "fasta").seq.tostring().upper()
#        res1[-1].append(fun.levenshtein1(s1,s2))
#        
#print res1
res1 = [[0, 1, 1, 3, 1], [1, 0, 2, 4, 0], [1, 2, 0, 4, 2], [3, 4, 4, 0, 4], [1, 0, 2, 4, 0]]


#res3 = []
#for i in range(5):
#    res3.append([])
#    for j in range(5):
#        if i == j : 
#            res3[-1].append(0)
#            continue
#        s1 = SeqIO.read("data/%s" % files[i], "fasta").seq.tostring().upper()
#        s2 = SeqIO.read("data/%s" % files[j], "fasta").seq.tostring().upper()
#        res3[-1].append(fun.levenshtein3(s1,s2))
#        
#print res3
res3 = [[0, 2, 1, 3, 2], [2, 0, 2, 5, 0], [1, 2, 0, 4, 2], [3, 5, 4, 0, 5], [2, 0, 2, 5, 0]]








#fname = "HomoSapiensMitochondrion"
#all_data = SeqIO.read("data/%s.fasta" % fname, "fasta").seq.tostring().upper()
#
#data = all_data[:500]
#
#p = 1000
#
##print cpg_prob_permut(data, 20, p)
##print cpg_prob(data, 20)
#
#f2 = count_kmers(data, 2)
#f1 = count_kmers(data, 1)
#
#a = "A"; b = "T"
#
#permut_res = permutation_test(list(data), a+b, p)
#
#exact_res = [bp_prob(data, a, b, i)*p for i in range(min(f1[a],f1[b])+1)]
#exact_ind = [i for i in range(min(f1[a],f1[b])+1)]
#
#plt.close()
#plt.hist(permut_res, bins=max(permut_res)-min(permut_res))
#plt.plot(exact_ind,exact_res,color="red")
#plt.title("Distribution of CpG base pairs with permutation test (blue) \n" +
#          "and exact calculated values (in red), for %d permutations" % p) 
#plt.show()


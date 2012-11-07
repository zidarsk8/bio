from Bio import Entrez
from Bio import SeqIO
import os
import cPickle

def memoize(f):
    cache= {}
    def memf(*x):
        if x not in cache:
            cache[x] = f(*x)
        return cache[x]
    return memf


def get_sequence(seq_id,fetch = False):
    pickleFile = "data/%s.pickle" % seq_id
    if fetch or not os.path.isfile(pickleFile):
        handle = Entrez.efetch(db="nucleotide", rettype="gb", id=seq_id, email="zidarsk8@gmail.com")
        rec = SeqIO.read(handle, "gb")
        handle.close()
        cPickle.dump(rec,file(pickleFile,"w"))
        return rec
    else:
        return cPickle.load(open(pickleFile))
        
    

@memoize
def equ(a,b):
    if a == b : return True
    maps = {"N":list("ACTG KMBVSWDYRH"),
            "K":list("TG"),
            "M":list("AC"),
            "B":list("CTG KSY"),
            "V":list("ACG MSYR"),
            "W":list("AT"),
            "S":list("CG"),
            "D":list("ATG KWR"),
            "Y":list("CT"),
            "R":list("AG"),
            "H":list("ACT MWYR")}
    return sum([1 if i in [a,b] and (a in j or b in j) else 0 for i,j in maps.items()]) > 0



@memoize
def levenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        oneago, thisrow = thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]
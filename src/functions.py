def memoize(f):
    cache= {}
    def memf(*x):
        if x not in cache:
            cache[x] = f(*x)
        return cache[x]
    return memf



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
def levenshtein1(s1, s2):
    if len(s1) < len(s2):
        return levenshtein1(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (not equ(c1,  c2))
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]



@memoize
def levenshtein2(a, b):
    
    if not a: return len(b)
    if not b: return len(a)
    return min(levenshtein2(a[1:], b[1:])+(not equ(a[0], b[0])), levenshtein2(a[1:], b)+1, levenshtein2(a, b[1:])+1)



@memoize
def levenshtein3(seq1, seq2):
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
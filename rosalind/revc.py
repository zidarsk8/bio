l = open('data/rosalind_revc.txt').readline().strip()

s = {'A':'T','T':'A','C':'G','G':'C'}
print "".join([s[i] for i in l][::-1])

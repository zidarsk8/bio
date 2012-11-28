f = open("data/rosalind_splc.txt")

t = {"UUU":"F","CUU":"L","AUU":"I","GUU":"V","UUC":"F","CUC":"L","AUC":"I","GUC":"V","UUA":"L","CUA":"L","AUA":"I","GUA":"V","UUG":"L","CUG":"L","AUG":"M","GUG":"V","UCU":"S","CCU":"P","ACU":"T","GCU":"A","UCC":"S","CCC":"P","ACC":"T","GCC":"A","UCA":"S","CCA":"P","ACA":"T","GCA":"A","UCG":"S","CCG":"P","ACG":"T","GCG":"A","UAU":"Y","CAU":"H","AAU":"N","GAU":"D","UAC":"Y","CAC":"H","AAC":"N","GAC":"D","UAA":"","CAA":"Q","AAA":"K","GAA":"E","UAG":"","CAG":"Q","AAG":"K","GAG":"E","UGU":"C","CGU":"R","AGU":"S","GGU":"G","UGC":"C","CGC":"R","AGC":"S","GGC":"G","UGA":"","CGA":"R","AGA":"R","GGA":"G","UGG":"W","CGG":"R","AGG":"R","GGG":"G"}

lines = [i.strip() for i in f.readlines()]

a = lines[0]

for i in lines[1:]:
    a = a.replace(i,"") 

rna = a.replace("T","U")

aa = "".join([ t[rna[i:i+3]] for i in range(0,len(rna),3)])


f = open("data/result_splc.txt" ,"w")
f.write(aa)
f.close()

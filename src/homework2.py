from bisect import bisect_left

import functions
reload(functions)

def get_reading_frames(rec, start_codons, stop_codons):
    rf = []
    
    for seq, rev in [(str(rec.seq), False), (str(rec.seq.reverse_complement()), True)]:
        
        b, e = {0:[], 1:[], 2:[]}, {0:[-1], 1:[-1], 2:[-1]} #begining and end
        
        [b[i % 3].append(i) for i in xrange(len(seq) - 2) if seq[i:i + 3] in start_codons]
        [e[i % 3].append(i + 3) for i in xrange(len(seq) - 2) if seq[i:i + 3] in stop_codons]
        
        for i in range(3):
            for j in xrange(1, len(e[i])):
                loc = bisect_left(b[i], e[i][j - 1])
                if loc < len(b[i]) and b[i][loc] < e[i][j] :
                    rf.append({'start': len(seq) - e[i][j]  if rev else b[i][loc], 
                               'end': len(seq) - b[i][loc]if rev else e[i][j],
                               'strand':-1 if rev else 1})
    return rf
    

seq_id = 'NC_006058'

rec = functions.get_sequence(seq_id)

rf = get_reading_frames(rec, ["ATG"], ["TGA"]);




#for i in range(min(len(b),len(e))):
#    print i

for f in rec.features:
    if f.type == "CDS":
        print "start", f.location.start.position
        print "end", f.location.end.position
        print "strand", ["-", "+" ][(f.strand + 1) / 2]
        print f.strand
        print 
#        
#        

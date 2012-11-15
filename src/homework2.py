from bisect import bisect_left

from matplotlib import pyplot as plt

import functions



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
                               'length': ((len(seq) - b[i][loc]if rev else e[i][j])-(len(seq) - e[i][j]  if rev else b[i][loc]))/3,
                               'strand':-1 if rev else 1})
    
    return rf
    

def match(orig,pred,cutoff_len = 60):
    """
    takes in two lists of tupples (len, start).
    removes tuples with len smallar than cutoff_len from the second list
    return intesection of start positions of the two lists, 
    """
    pred = [i[1] for i in pred[bisect_left(pred, (cutoff_len, -1 )):]]
    return set([i[1] for i in orig]).intersection(set(pred))

def cut(tab, cutoff = 60):
    return [i[1] for i in tab[bisect_left(tab, (cutoff, -1 )):]]

def precision(orig,pred):
    orig, pred = set(orig), set(pred)
    tp = float(len(orig.intersection(pred)))
    return tp / len(pred)

def recall(orig,pred):
    orig, pred = set(orig), set(pred)
    tp = float(len(orig.intersection(pred)))
    fp = float(len(orig.difference(pred)))
    return tp / (tp+fp)

def get_precisions(orig, pred, cutoffs):
    stp = sorted([(i['length'],i['start']) for i in pred])
    sto = [i['start'] for i in orig]
    return [precision(sto, cut(stp,i)) for i in cutoffs]
    
def get_recalls(orig, pred, cutoffs):
    stp = sorted([(i['length'],i['start']) for i in pred])
    sto = [i['start'] for i in orig]
    return [recall(sto, cut(stp,i)) for i in cutoffs]
    

if __name__ == "__main__":
        
    seq_id = 'NC_007346'
    
    start_c = {'NC_006058' : set(["ATG"]), 
               'NC_007346' : set(["ATG", "TTG", "CTG"]) }
    stop_c = {'NC_006058' : set(["TGA"]), 
              'NC_007346' : set(["TAA", "TAG", "TGA"]) }
    
    
    rec = functions.get_sequence(seq_id)
    
    rf_pred = get_reading_frames(rec, start_c[seq_id], stop_c[seq_id]);
    
    rf_orig = [{'start': f.location.start.position,
                'end': f.location.end.position,
                'length': (f.location.end.position - f.location.start.position)/3,
                'strand':-f.strand}  
               for f in rec.features if f.type == "CDS"]
    
    
    cutoffs = range(0,500,1)
    pre = get_precisions(rf_orig, rf_pred, cutoffs);
    rec = get_recalls(rf_orig, rf_pred, cutoffs);
    
    
    p1, = plt.plot(cutoffs, pre, lw=1)
    p2, = plt.plot(cutoffs, rec, lw=1)
    

    l2 = plt.legend([p2,p1], ["precision","recall"]) # this removes l1 from the axes.

    plt.xlabel("Minimum ORF length")
    plt.ylabel("Score")
    plt.title("Precision and recall as a function of minimum ORF length")
    
    plt.show()

    


import functions
reload(functions)


seq_id = 'NC_006058'

rec = functions.get_sequence(seq_id)



for f in rec.features:
    if f.type == "CDS":
        print "start", f.location.start.position
        print "end", f.location.end.position
        print "strand", ["-", "+" ][(f.strand+1)/2]
        print f.strand
        print 
        
        
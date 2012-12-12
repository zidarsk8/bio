import functions 

def getDict(fname = 'data/mitochondrion.txt'):
    ids =   ['NC_000845.1',
             'NC_004299.1',
             'AC_000022.2',
             'NC_002083.1',
             'NC_001643.1',
             'NC_011137.1',
             'NC_012920.1',
             'NC_001645.1',
             'NC_002008.4',
             'NC_006580.1',
             'NC_012420.1',
             'NC_011391.1',
             'NC_012061.1',
             'NC_001640.1']
    a = []
    for i in ids:
        r = functions.get_sequence(i)
        d = {   'seq' : r,
                'id' : i,
                'latin' : r.annotations['source'].split('(')[0].replace('mitochondrion','').strip(),
                'english' : r.annotations['source'].split('(')[1].replace(')','').strip(),
                'COX3' : [f.qualifiers['translation'][0] for f in r.features if f.type == 'CDS' and f.qualifiers['gene'][0] == "COX3"][0]
                }

        a.append(d)
    return a

import sys,collections
def load(f):
    v=collections.OrderedDict()
    for l in open(f,encoding='utf-8'):
        p=l.split()
        if not p: continue
        ref=f'{int(p[0][2:4])}:{int(p[0][4:6])}'
        if p[1] in ('RA','C-','P-','X-','RP','RR','RD','RI') : continue
        if p[6] in ('εἰμί','οὐ','μή','ὑμεῖς','ἐγώ','αὐτός','πᾶς','ἑαυτοῦ','ἡμεῖς','εἰς'): continue
        v.setdefault(ref,set()).add(p[6])
    return v
J=load(sys.argv[1]); P=load(sys.argv[2])
for jr,jl in J.items():
    best=sorted(((len(jl&pl),pr,sorted(jl&pl)) for pr,pl in P.items()),reverse=True)[:2]
    print('Jude',jr,'->',' | '.join(f'2Pe {b[1]} ({b[0]}): {" ".join(b[2])}' for b in best if b[0]>=2))

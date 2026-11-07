import sys,re,os
sys.path.insert(0,os.path.dirname(__file__))
from usfm2txt import book
Z=os.path.join(os.path.dirname(__file__),'..','.cache','englsv_usfm.zip')
cache={}
for ref in sys.argv[1:]:
    m=re.match(r'([1-3]?[A-Z]{2,3})\s*(\d+):(\d+)(?:-(\d+))?',ref)
    code,c,v1,v2=m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4) or m.group(3))
    if code not in cache: cache[code]=book(Z,code)
    b=cache[code]
    out=[f'{v} '+b[(c,str(v))] for v in range(v1,v2+1) if (c,str(v)) in b]
    print(f'[{ref}]',' '.join(out))

import sys,re,unicodedata
t=open(sys.argv[1],encoding='utf-8').read()
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').lower()
entries=re.findall(r'<entry n="([^"|]*)\|?[^"]*">(.*?)</entry>',t,flags=re.S)
idx={}
for n,body in entries: idx.setdefault(strip(n),[]).append((n,body))
for w in sys.argv[2:]:
    for n,body in idx.get(strip(w),[('NOT FOUND','')]):
        b=re.sub(r'<[^>]+>','',body); b=re.sub(r'\s+',' ',b).strip()
        print(f'## {w} -> {n}: {b[:900]}\n')

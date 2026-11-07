import zipfile,sys,re
def clean(s):
    s=re.sub(r'\\f .*?\\f\*','',s)
    s=re.sub(r'\\x .*?\\x\*','',s)
    s=re.sub(r'\\\+?w ([^|\\]*?)(\|[^\\]*?)?\\\+?w\*',r'\1',s)
    s=re.sub(r'\\\+?(add|nd|wj|qs|tl|sc|bk|k|it|bd|em|pn|qt)\*','',s)
    s=re.sub(r'\\\+?(add|nd|wj|qs|tl|sc|bk|k|it|bd|em|pn|qt) ','',s)
    return s
def book(zpath, code):
    z=zipfile.ZipFile(zpath)
    names=[n for n in z.namelist() if code in n and n.endswith('.usfm')]
    if not names: return None
    t=z.read(names[0]).decode('utf-8-sig')
    out={}; ch=0
    for line in t.split('\n'):
        m=re.match(r'\\c (\d+)',line)
        if m: ch=int(m.group(1)); continue
        for vm in re.finditer(r'\\v (\d+[a-z]?) (.*?)(?=\\v \d|$)',line):
            out[(ch,vm.group(1))]=clean(vm.group(2)).strip()
        if not re.search(r'\\v \d',line) and ch and out and not line.startswith('\\c') and line.strip() and not re.match(r'\\(s|ms|mr|d|r|h|toc|mt|id|ide|rem|cl)\d?\b',line):
            last=list(out.keys())[-1]
            extra=re.sub(r'^\\(p|q\d?|m|pi\d?|li\d?|nb|b|pmo|mi)\b','',line).strip()
            extra=clean(extra)
            if extra: out[last]+=' '+extra
    return out
if __name__=='__main__':
    zpath,code=sys.argv[1],sys.argv[2]
    chs=sys.argv[3] if len(sys.argv)>3 else None
    b=book(zpath,code)
    if b is None: print('NOT FOUND'); sys.exit()
    for (c,v),txt in b.items():
        if chs and str(c)!=chs: continue
        print(f'{c}:{v} {re.sub(r"\s+"," ",txt)}')

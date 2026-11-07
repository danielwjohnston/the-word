#!/usr/bin/env python3
"""Download the INTF NTVMR transcriptions of Jude (CC BY 4.0) for the ten manuscripts used in
section A, and save them as .cache/ntvmr/jude_ms.json (manuscript -> verse -> plain text).

Usage: python3 -I tools/fetch_ntvmr.py [--force]
"""
import os, re, sys, json, html, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), '.cache', 'ntvmr', 'jude_ms.json')
DOCS = {'P72': 10072, 'P78': 10078, '01': 20001, '02': 20002, '03': 20003, '04': 20004,
        '044': 20044, '1739': 31739, '018': 20018, '020': 20020}
API = 'https://ntvmr.uni-muenster.de/community/vmr/api/transcript/get/?docID={d}&indexContent=Jude.1.{v}&format=xhtml'

def fetch(d, v):
    req = urllib.request.Request(API.format(d=d, v=v), headers={'User-Agent': 'jude-unfolded-research-script'})
    t = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')
    t = re.sub(r'(?is)<(script|style|head).*?</\1>', '', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'\s+', ' ', t)
    return t.split('(C) ')[0].strip()

def main():
    if os.path.exists(OUT) and '--force' not in sys.argv:
        print('exists:', OUT); return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    res = {}
    for sig, d in DOCS.items():
        res[sig] = {}
        for v in range(1, 26):
            try:
                res[sig][str(v)] = fetch(d, v)
            except Exception as e:
                res[sig][str(v)] = f'ERROR {e}'
            time.sleep(0.2)
        print(sig, flush=True)
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Check every Greek word form quoted in the book against real Greek texts:
the SBLGNT New Testament (MorphGNT), the Jude texts of Robinson-Pierpont and the TR,
Brenton's Greek LXX, and Abbott-Smith headwords. Unmatched forms are listed for manual review."""
import os, re, glob, sys, zipfile, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from usfm2txt import book
C = os.path.join(ROOT, '.cache')
def norm(w):
    w = unicodedata.normalize('NFD', w)
    w = ''.join(ch for ch in w if unicodedata.category(ch) != 'Mn')
    return w.lower().replace('ς', 'σ').strip("’'ʼ᾽")
known = set()
for f in glob.glob(os.path.join(C, 'morphgnt', '*.txt')):
    for l in open(f, encoding='utf-8'):
        p = l.split()
        if len(p) >= 7:
            known.update(norm(x) for x in (p[4], p[5], p[6]))
for zf, codes in ((os.path.join(C, 'grcmt_usfm.zip'), ['JUD']), (os.path.join(C, 'grctr_usfm.zip'), ['JUD','2PE'])):
    for code in codes:
        for v in (book(zf, code) or {}).values():
            known.update(norm(w) for w in re.findall(r'[Ͱ-Ͽἀ-῿]+', v))
z = zipfile.ZipFile(os.path.join(C, 'grcbrent_usfm.zip'))
for n in z.namelist():
    if n.endswith('.usfm'):
        known.update(norm(w) for w in re.findall(r'[Ͱ-Ͽἀ-῿]+', z.read(n).decode('utf-8', 'ignore')))
known.update(norm(h) for h in re.findall(r'<entry n="([^"|]+)', open(os.path.join(C, 'abbott-smith.tei.xml'), encoding='utf-8').read()))
files = sorted(glob.glob(os.path.join(ROOT, 'chapters', '*.md'))) + sorted(glob.glob(os.path.join(ROOT, 'appendices', '*.md')))
unk = {}
total = 0
for f in files:
    t = open(f, encoding='utf-8').read()
    for w in re.findall(r'[Ͱ-Ͽἀ-῿]+', t):
        total += 1
        if norm(w) not in known:
            unk.setdefault(w, set()).add(os.path.basename(f))
print(f'Greek tokens checked: {total}; distinct forms not found in reference texts: {len(unk)}')
for w, fs in sorted(unk.items()):
    print(f'  {w}: {", ".join(sorted(fs))}')

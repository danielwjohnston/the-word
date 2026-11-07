#!/usr/bin/env python3
"""Shared loaders for the openly licensed source texts cached in .cache/.

All texts used here are public domain, CC0, CC BY, or CC BY-SA (see research/source-ledger.md).
Refs are tuples (CODE, chapter, v1, v2) using USFM book codes (GEN, JUD, ...).
"""
import os, re, sys, json, glob, unicodedata, functools

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
C = os.path.join(ROOT, '.cache')
sys.path.insert(0, HERE)
from usfm2txt import book as usfm_book  # noqa: E402

# Free English translations, in order of first publication (not order of preference).
# Dates: eBible.org copyright pages (T4T 2008-2017, ULB 2017, FBV 2018, LSV 2020, TCENT 2022, WEB "2020 stable
# text edition"); Wikipedia (Geneva Bible 1560; Darby complete Bible 1890; WEB 2000; OEB first release
# August 2010; BSB and MSB 2022). eBible's Geneva text is the 1599 edition; its Douay-Rheims is the 1899
# American edition of the Rheims New Testament (1582) as revised by Challoner.
TRANSLATIONS = [
    # abbr, eBible id, display name, date label, license
    ('TNT',  'engtnt',      'Tyndale New Testament',               '1534',          'Public domain'),
    ('GNV',  'enggnv',      'Geneva Bible',                        '1560; 1599 ed.', 'Public domain'),
    ('DRA',  'engDRA',      'Douay-Rheims',                        '1582; 1899 ed.', 'Public domain'),
    ('WBS',  'engwebster',  'Webster Bible',                       '1833',          'Public domain'),
    ('NOY',  'engnoy',      'Noyes Bible',                         '1869',          'Public domain'),
    ('RV',   'eng-rv',      'Revised Version',                     '1881',          'Public domain'),
    ('DBY',  'engDBY',      'Darby Translation',                   '1890',          'Public domain'),
    ('YLT',  'engylt',      "Young's Literal Translation",         '1898',          'Public domain'),
    ('ASV',  'eng-asv',     'American Standard Version',           '1901',          'Public domain'),
    ('WEB',  'engwebp',     'World English Bible',                 '2000; 2020 ed.', 'Public domain'),
    ('T4T',  'eng-t4t',     'Translation for Translators',         '2008–2017',     'CC BY-SA 4.0'),
    ('OEB',  'engoebus',    'Open English Bible',                  '2010',          'Public domain'),
    ('ULB',  'engULB',      'Unlocked Literal Bible',              '2017',          'CC BY-SA 4.0'),
    ('FBV',  'engfbv',      'Free Bible Version',                  '2018',          'CC BY-SA 4.0'),
    ('LSV',  'englsv',      'Literal Standard Version',            '2020',          'CC BY-SA 4.0'),
    ('BSB',  'engbsb',      'Berean Standard Bible',               '2022',          'Public domain'),
    ('MSB',  'engmsb',      'Majority Standard Bible',             '2022',          'Public domain'),
    ('TCENT','engtcent',    'Text-Critical English New Testament', '2022',          'CC BY 4.0'),
]
ABBR = {t[0]: t for t in TRANSLATIONS}
EXTRA = {'BRENTON': 'eng-Brenton', 'LXX': 'grcbrent', 'RP': 'grcmt', 'TR': 'grctr'}
EXCLUDED = ['ESV', 'NASB', 'NLT', 'NIV', 'NET', 'NKJV', 'CSB', 'HCSB', 'NRSV', 'RSV', 'KJV', 'AMP', 'MSG',
            'Message', 'Amplified', 'NIrV', 'GW', 'EMTV', 'BBE', 'TLB', 'NCV', 'CEV', 'GNT', 'NAB', 'NJB']

def _zip(eid):
    return os.path.join(C, f'{eid}_usfm.zip')

@functools.lru_cache(maxsize=None)
def _usfm(eid, code):
    return usfm_book(_zip(eid), code) or {}

def _clean_eng(s):
    s = s.replace('||', ' / ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def english(abbr, ref):
    """Text of a reference in a free English translation (or BRENTON), with verse numbers."""
    eid = ABBR[abbr][1] if abbr in ABBR else EXTRA[abbr]
    code, ch, v1, v2 = ref
    b = _usfm(eid, code)
    parts = []
    for v in range(v1, v2 + 1):
        t = b.get((ch, str(v)))
        if t:
            parts.append((v, _clean_eng(t)))
    return parts

# ---------- Greek New Testament (SBLGNT via MorphGNT) ----------
NT_FILES = {'MAT':'61-Mt','MRK':'62-Mk','LUK':'63-Lk','JHN':'64-Jn','ACT':'65-Ac','ROM':'66-Ro','1CO':'67-1Co','2CO':'68-2Co',
            'GAL':'69-Ga','EPH':'70-Eph','PHP':'71-Php','COL':'72-Col','1TH':'73-1Th','2TH':'74-2Th','1TI':'75-1Ti','2TI':'76-2Ti',
            'TIT':'77-Tit','PHM':'78-Phm','HEB':'79-Heb','JAS':'80-Jas','1PE':'81-1Pe','2PE':'82-2Pe','1JN':'83-1Jn','2JN':'84-2Jn',
            '3JN':'85-3Jn','JUD':'86-Jud','REV':'87-Re'}

@functools.lru_cache(maxsize=None)
def _sblgnt(code):
    out = {}
    for l in open(os.path.join(C, 'morphgnt', NT_FILES[code] + '.txt'), encoding='utf-8'):
        p = l.split()
        if len(p) < 4: continue
        ch, v = int(p[0][2:4]), int(p[0][4:6])
        w = re.sub('[⸀⸁⸂⸃⸄⸅]', '', p[3])
        out.setdefault((ch, v), []).append(w)
    return {k: ' '.join(x) for k, x in out.items()}

def greek_nt(ref):
    code, ch, v1, v2 = ref
    g = _sblgnt(code)
    return [(v, g[(ch, v)]) for v in range(v1, v2 + 1) if (ch, v) in g]

def is_nt(code):
    return code in NT_FILES

# ---------- Hebrew Bible (Westminster Leningrad Codex, PD, via OSHB) ----------
WLC = {'GEN':'Gen','EXO':'Exod','LEV':'Lev','NUM':'Num','DEU':'Deut','JOS':'Josh','JDG':'Judg','1SA':'1Sam','2SA':'2Sam',
       '1KI':'1Kgs','2KI':'2Kgs','1CH':'1Chr','2CH':'2Chr','NEH':'Neh','JOB':'Job','PSA':'Ps','PRO':'Prov','ISA':'Isa',
       'JER':'Jer','LAM':'Lam','EZK':'Ezek','DAN':'Dan','HOS':'Hos','JOL':'Joel','AMO':'Amos','MIC':'Mic','HAB':'Hab',
       'ZEC':'Zech','MAL':'Mal'}
# English -> Hebrew versification differences for the passages cited in this book.
def heb_ref(code, ch, v):
    if code == 'DEU' and ch in (13, 23): return ch, v + 1
    if code == 'DEU' and ch == 29: return ch, v - 1
    if code == 'JOL' and ch == 2 and v >= 28: return 3, v - 27
    if code == 'NUM' and ch == 16 and v >= 36: return 17, v - 35
    if code == 'NUM' and ch == 17: return 17, v + 15
    if code == 'PSA':
        off = {12: 1, 19: 1, 41: 1, 52: 2, 56: 1, 80: 1, 89: 1}.get(ch, 0)
        return ch, v + off
    if code == 'ISA' and ch == 9 and v >= 2: return 9, v - 1
    if code == 'DAN' and ch == 4 and v <= 3: return 3, v + 30
    if code == 'DAN' and ch == 4: return 4, v - 3
    if code == 'DAN' and ch == 6: return 6, v + 1
    return ch, v

CANT = re.compile('[֑-ֽ֯׀׃]')
@functools.lru_cache(maxsize=None)
def _wlc(code):
    t = open(os.path.join(C, 'wlc', WLC[code] + '.xml'), encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'<verse osisID="[^.]+\.(\d+)\.(\d+)">(.*?)</verse>', t, re.S):
        body = m.group(3)
        body = re.sub(r'<note.*?</note>', '', body, flags=re.S)
        body = body.replace('<seg type="x-maqqef">־</seg>', '־')
        body = re.sub(r'<seg type="x-sof-pasuq">׃</seg>', '׃', body)
        body = re.sub(r'<seg[^>]*>.*?</seg>', '', body)
        words = re.sub(r'<[^>]+>', ' ', body).replace('/', '')
        words = re.sub(r'\s*־\s*', '־', words)
        words = re.sub(r'\s+׃', '׃', words)
        words = CANT.sub('', re.sub(r'\s+', ' ', words).strip())
        out[(int(m.group(1)), int(m.group(2)))] = words
    return out

def hebrew(ref):
    code, ch, v1, v2 = ref
    if code not in WLC: return []
    w = _wlc(code)
    res = []
    for v in range(v1, v2 + 1):
        hc, hv = heb_ref(code, ch, v)
        if (hc, hv) in w: res.append((v, w[(hc, hv)], f'{hc}:{hv}'))
    return res

# ---------- Septuagint / Apocrypha (Brenton, PD) ----------
def lxx(ref):
    code, ch, v1, v2 = ref
    b = _usfm(EXTRA['LXX'], code)
    return [(v, re.sub(r'\s+', ' ', b[(ch, str(v))])) for v in range(v1, v2 + 1) if (ch, str(v)) in b]

# ---------- 1 Enoch (R. H. Charles 1917, PD; Wikisource transcription) ----------
@functools.lru_cache(maxsize=None)
def _enoch(ch):
    f = os.path.join(C, 'enoch', f'ch{ch:02d}.txt')
    if not os.path.exists(f): return {}
    t = open(f, encoding='utf-8').read()
    t = t.split('}}', 1)[-1]
    t = re.sub(r'\{\|.*?\|\}', ' ', t, flags=re.S)       # drop parallel-column tables
    t = re.sub(r'===.*?===', ' ', t)
    t = re.sub(r'CHAPTER [IVXLC]+\.', ' ', t)
    t = re.sub(r'[⌈⌉〈〉†]', '', t)
    t = re.sub(r'\s+', ' ', t)
    out = {}
    for m in re.finditer(r'(?<![\w.])(\d{1,2})[a-g]?\.\s(.*?)(?=(?<![\w.])\d{1,2}[a-g]?\.\s|$)', t):
        v = int(m.group(1))
        out.setdefault(v, '')
        out[v] = (out[v] + ' ' + m.group(2)).strip()
    return out

def enoch(ch, v1, v2):
    e = _enoch(ch)
    return [(v, e[v]) for v in range(v1, v2 + 1) if v in e]

if __name__ == '__main__':
    print(greek_nt(('JUD', 1, 5, 5)))
    print(hebrew(('ZEC', 3, 2, 2)))
    print(hebrew(('DEU', 13, 1, 1)))
    print(english('BSB', ('JUD', 1, 12, 12)))
    print(english('T4T', ('JUD', 1, 12, 12)))
    print(lxx(('SIR', 16, 7, 8)))
    print(enoch(1, 9, 9))

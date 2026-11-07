#!/usr/bin/env python3
"""Audit the Jude, Unfolded manuscript.

Checks
  1. LSV quotation fidelity: every quotation attributed to the LSV, whether an
     inline "..." (v. N) / "..." (Book C:V, LSV) or a block quote ending with
     "— Ref, LSV", must match the LSV text of the cited verses exactly
     (ellipses allowed, case- and punctuation-at-edges-insensitive).
  2. Coverage: every unit in research/coverage-matrix.md has its Greek key term
     in the named chapter file; every Jude verse is printed in some chapter's
     "A. The Text" section.
  3. Structure: each main chapter has sections A-K.
  4. Footnotes: every reference has a definition and vice versa; IDs unique.
  5. Word counts.
Usage: python3 tools/audit.py [--update-matrix] [files...]
"""
import os, re, sys, glob, unicodedata, zipfile, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from usfm2txt import book as usfm_book  # noqa: E402

LSV_ZIP = os.path.join(ROOT, '.cache', 'englsv_usfm.zip')

BOOKS = {
 'Gen':'GEN','Genesis':'GEN','Exod':'EXO','Exodus':'EXO','Lev':'LEV','Leviticus':'LEV','Num':'NUM','Numbers':'NUM',
 'Deut':'DEU','Deuteronomy':'DEU','Josh':'JOS','Joshua':'JOS','Judg':'JDG','Ruth':'RUT','1 Sam':'1SA','2 Sam':'2SA',
 '1 Kgs':'1KI','2 Kgs':'2KI','1 Chr':'1CH','2 Chr':'2CH','Ezra':'EZR','Neh':'NEH','Esth':'EST','Job':'JOB',
 'Ps':'PSA','Pss':'PSA','Psalm':'PSA','Prov':'PRO','Proverbs':'PRO','Eccl':'ECC','Song':'SNG','Isa':'ISA','Isaiah':'ISA',
 'Jer':'JER','Jeremiah':'JER','Lam':'LAM','Ezek':'EZK','Ezekiel':'EZK','Dan':'DAN','Daniel':'DAN','Hos':'HOS','Joel':'JOL',
 'Amos':'AMO','Obad':'OBA','Jonah':'JON','Mic':'MIC','Micah':'MIC','Nah':'NAM','Hab':'HAB','Zeph':'ZEP','Hag':'HAG',
 'Zech':'ZEC','Zechariah':'ZEC','Mal':'MAL','Matt':'MAT','Matthew':'MAT','Mark':'MRK','Luke':'LUK','John':'JHN','Acts':'ACT',
 'Rom':'ROM','Romans':'ROM','1 Cor':'1CO','2 Cor':'2CO','Gal':'GAL','Galatians':'GAL','Eph':'EPH','Phil':'PHP','Col':'COL',
 '1 Thess':'1TH','2 Thess':'2TH','1 Tim':'1TI','2 Tim':'2TI','Titus':'TIT','Tit':'TIT','Phlm':'PHM','Heb':'HEB','Hebrews':'HEB',
 'Jas':'JAS','James':'JAS','1 Pet':'1PE','2 Pet':'2PE','1 John':'1JN','2 John':'2JN','3 John':'3JN','Jude':'JUD','Rev':'REV',
 'Revelation':'REV',
}
BOOK_RE = '|'.join(sorted((re.escape(k) for k in BOOKS), key=len, reverse=True))

_cache = {}
def lsv_book(code):
    if code not in _cache:
        _cache[code] = usfm_book(LSV_ZIP, code) or {}
    return _cache[code]

def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub('[’‘“”"\']', '', s)
    s = s.replace('||', ' ').replace(' / ', ' ').replace('—', '—')
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()

def edge(s):
    return s.strip().strip(' ,.;:!?"\'').strip()

def verses_text(code, ch, v1, v2):
    b = lsv_book(code)
    parts = [b.get((ch, str(v)), '') for v in range(v1, v2 + 1)]
    return norm(' '.join(parts))

def matches(quote, text):
    frags = [edge(norm(f)) for f in re.split(r'…|\.\.\.', quote)]
    frags = [f for f in frags if f]
    pos = 0
    for f in frags:
        i = text.find(f, pos)
        if i < 0:
            return False, f
        pos = i + len(f)
    return True, None

def parse_ref(ref, default_book=None):
    """Return list of (code, ch, v1, v2) from strings like 'Jude 12', 'vv. 3-4', 'Zech 3:2-4', 'Gen 4:3, 8', '2 Pet 2:13; 2 Pet 2:17'."""
    ref = ref.replace('–', '-').replace('—', '-')
    out = []
    code, ch = None, None
    m = re.match(r'\s*v{1,2}\.\s*(.*)', ref)
    if m:
        code, ch, ref = 'JUD', 1, m.group(1)
    for piece in re.split(r'[;,]', ref):
        piece = piece.strip()
        if not piece:
            continue
        mb = re.match(r'(' + BOOK_RE + r')\s+(.*)', piece)
        if mb:
            code = BOOKS[mb.group(1)]
            piece = mb.group(2).strip()
            ch = 1 if code == 'JUD' else None
        if code is None:
            continue
        mm = re.match(r'(\d+)(?::(\d+))?(?:-(\d+)(?::(\d+))?)?', piece)
        if not mm:
            continue
        a, b, c, d = mm.groups()
        if code == 'JUD':
            if b:  # Jude 1:12 style
                v1 = int(b); v2 = int(d or c or b)
            else:
                v1 = int(a); v2 = int(c or a)
            out.append(('JUD', 1, v1, v2))
            continue
        if b:      # ch:v[-v2]
            ch = int(a); v1 = int(b); v2 = int(c) if (c and not d) else v1
        else:      # bare verse in current chapter
            if ch is None:
                continue
            v1 = int(a); v2 = int(c or a)
        out.append((code, ch, v1, v2))
    return out

QUOTE_INLINE = re.compile(r'[“"]([^“”"\n]{3,}?)[”"]\s*\(([^()\n]{1,60}?)\)')
QUOTE_PAREN = re.compile(r'\([“"]([^“”"\n]{3,}?)[,.]?[”"],\s*([A-Z0-9][^()\n]{0,40}?)\)')
try:
    from sources import TRANSLATIONS, english as _english, EXCLUDED
    KNOWN = [t[0] for t in TRANSLATIONS]
except Exception:  # sources cache missing
    TRANSLATIONS, KNOWN, EXCLUDED = [], [], []
SKIP_SRC = r'\b(my rendering|literally|lit\.|Charles|Brenton|LXX|Theodotion|critical text|NA28|SBLGNT|Greek)\b'

def trans_text(abbr, refs):
    if abbr == 'LSV':
        return ' '.join(verses_text(*r) for r in refs)
    out = []
    for r in refs:
        out += [x[1] for x in _english(abbr, r)]
    return norm(' '.join(out))

def check_one(path, q, ref, report):
    if re.search(SKIP_SRC, ref):
        return 0
    abbrs = [a for a in KNOWN if re.search(r'(?<![A-Za-z])' + re.escape(a) + r'(?![A-Za-z])', ref)]
    for ex in EXCLUDED:
        if re.search(r'(?<![A-Za-z])' + re.escape(ex) + r'(?![A-Za-z])', ref):
            report.append(f'{os.path.basename(path)}: EXCLUDED TRANSLATION cited ({ref.strip()}): “{q}”')
            return 0
    refs = parse_ref(re.sub(r'(?<![A-Za-z])(' + '|'.join(KNOWN + ['LSV']) + r')(?![A-Za-z])', '', ref).strip(' ,;'))
    if abbrs == ['LSV'] and not refs:
        return 0   # LSV quote whose reference is given elsewhere in the sentence
    if abbrs:
        if not refs:
            refs = [('JUD', 1, 1, 25)]
        ok_all = True
        for a in abbrs:
            ok, frag = matches(q, trans_text(a, refs))
            if not ok:
                ok_all = False
                report.append(f'{os.path.basename(path)}: QUOTE MISMATCH ({a}; {ref.strip()}): “{q}” — fragment not found: “{frag}”')
        return 1 if ok_all else 0
    is_lsv = 'LSV' in ref or re.match(r'\s*v{1,2}\.\s*\d', ref) or re.match(r'\s*(' + BOOK_RE + r')\s+\d', ref)
    if not is_lsv or not refs:
        return 0
    ok, frag = matches(q, trans_text('LSV', refs))
    if not ok:
        report.append(f'{os.path.basename(path)}: QUOTE MISMATCH ({ref.strip()}): “{q}” — fragment not found: “{frag}”')
        return 0
    return 1

def check_quotes(path, text, report):
    n_ok = 0
    for m in QUOTE_INLINE.finditer(text):
        n_ok += check_one(path, m.group(1), m.group(2), report)
    for m in QUOTE_PAREN.finditer(text):
        n_ok += check_one(path, m.group(1), m.group(2), report)
    # block quotes
    lines = text.split('\n')
    block = []
    for line in lines + ['']:
        if line.startswith('>'):
            block.append(line[1:].strip())
            continue
        if block:
            src = None
            for b in block:
                mm = re.match(r'[—-]{1,2}\s*(.+?),\s*LSV\s*$', b)
                if mm: src = mm.group(1)
            if src:
                body = ' '.join(b for b in block if b and not re.match(r'[—-]{1,2}\s', b))
                body = re.sub(r'\*\*\d+(?::\d+)?\*\*', ' ', body)      # verse numbers in bold
                body = re.sub(r'\[\^[^\]]+\]', '', body)
                refs = parse_ref(src)
                if refs:
                    hay = ' '.join(verses_text(*r) for r in refs)
                    ok, frag = matches(body, hay)
                    if ok: n_ok += 1
                    else: report.append(f'{os.path.basename(path)}: BLOCK MISMATCH ({src}): fragment not found: “{frag}”')
            block = []
    return n_ok

def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    update = '--update-matrix' in sys.argv
    files = args or sorted(glob.glob(os.path.join(ROOT, 'chapters', '*.md'))) + sorted(glob.glob(os.path.join(ROOT, 'appendices', '*.md')))
    report = []
    total_words = 0
    quotes_ok = 0
    fn_defs = collections.Counter(); fn_refs = collections.Counter(); fn_where = {}
    chapter_text = {}
    for f in files:
        t = open(f, encoding='utf-8').read()
        chapter_text[os.path.basename(f)] = t
        words = len(re.findall(r"[\w’'-]+", re.sub(r'\[\^[^\]]+\]:.*', '', t)))
        total_words += words
        quotes_ok += check_quotes(f, t, report)
        for d in re.findall(r'^\[\^([^\]]+)\]:', t, flags=re.M):
            fn_defs[d] += 1; fn_where[d] = os.path.basename(f)
        for r in re.findall(r'\[\^([^\]]+)\](?!:)', t):
            fn_refs[r] += 1
        base = os.path.basename(f)
        if re.match(r'\d\d-jude', base):
            for sec in 'ABCDEFGHIJK':
                if not re.search(r'^##\s+' + sec + r'\.\s', t, flags=re.M):
                    report.append(f'{base}: missing section {sec}.')
    for d, c in fn_defs.items():
        if c > 1: report.append(f'FOOTNOTE ID defined {c} times: {d}')
        if d not in fn_refs: report.append(f'FOOTNOTE defined but never referenced: {d} ({fn_where[d]})')
    for r in fn_refs:
        if r not in fn_defs: report.append(f'FOOTNOTE referenced but not defined: {r}')
    # coverage of verses in section A
    printed = set()
    for base, t in chapter_text.items():
        if not re.match(r'\d\d-jude', base): continue
        m = re.search(r'^##\s+A\..*?$(.*?)^##\s+B\.', t, flags=re.M | re.S)
        if m:
            for v in re.findall(r'\*\*(\d+)\*\*', m.group(1)):
                printed.add(int(v))
    if not args:
        missing = [v for v in range(1, 26) if v not in printed]
        if missing: report.append(f'Verses not printed in any section A: {missing}')
    # coverage matrix
    mpath = os.path.join(ROOT, 'research', 'coverage-matrix.md')
    rows = open(mpath, encoding='utf-8').read().split('\n')
    cov_ok = cov_missing = cov_pending = 0
    new_rows = []
    for row in rows:
        cells = [c.strip() for c in row.split('|')]
        if len(cells) >= 8 and cells[1].isdigit():
            term, chap = cells[3], cells[4]
            t = chapter_text.get(chap)
            if t is None:
                status = 'pending'; cov_pending += 1
            elif strip_acc(term) in strip_acc(t):
                status = '✓'; cov_ok += 1
            else:
                status = 'MISSING'; cov_missing += 1
                report.append(f'COVERAGE: v.{cells[1]} “{cells[2]}” ({term}) not found in {chap}')
            cells[6] = status
            row = '| ' + ' | '.join(cells[1:7]) + ' |'
        new_rows.append(row)
    if update and not args:
        open(mpath, 'w', encoding='utf-8').write('\n'.join(new_rows))
    print(f'Files audited: {len(files)}')
    print(f'Words (excluding footnote definitions): {total_words:,}')
    print(f'LSV quotations verified: {quotes_ok}')
    print(f'Coverage units: {cov_ok} ✓, {cov_missing} missing, {cov_pending} pending (chapter not yet written)')
    print(f'Footnotes: {sum(fn_defs.values())} defined, {len(fn_refs)} distinct referenced')
    print(f'Issues: {len(report)}')
    for r in report: print('  -', r)
    return 1 if report else 0

if __name__ == '__main__':
    sys.exit(main())

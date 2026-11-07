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
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
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
    """Return list of (code, ch, v1, v2) from strings like 'Jude 12', 'vv. 3-4', 'Zech 3:2-4', 'Gen 4:3, 8'."""
    ref = ref.replace('–', '-').replace('—', '-')
    out = []
    m = re.match(r'\s*v{1,2}\.\s*([\d\-,\s]+)', ref)
    if m:
        for part in m.group(1).split(','):
            part = part.strip()
            if not part: continue
            a, _, b = part.partition('-')
            out.append(('JUD', 1, int(a), int(b or a)))
        return out
    m = re.match(r'\s*(' + BOOK_RE + r')\s+([\d:\-,\s]+)', ref)
    if not m:
        return out
    code = BOOKS[m.group(1)]
    nums = m.group(2)
    if code == 'JUD':
        for part in nums.split(','):
            part = part.strip().replace('1:', '')
            if not part: continue
            a, _, b = part.partition('-')
            try: out.append(('JUD', 1, int(a), int(b or a)))
            except ValueError: pass
        return out
    ch = None
    for part in nums.split(','):
        part = part.strip()
        if not part: continue
        if ':' in part:
            c, _, vs = part.partition(':')
            ch = int(c)
        else:
            vs = part
        if ch is None: continue
        a, _, b = vs.partition('-')
        if ':' in b:  # cross-chapter range: take first chapter only
            b = ''
        try: out.append((code, ch, int(a), int(b or a)))
        except ValueError: pass
    return out

QUOTE_INLINE = re.compile(r'[“"]([^“”"\n]{3,}?)[”"]\s*\(([^()\n]{1,60}?)\)')

def check_quotes(path, text, report):
    n_ok = 0
    # inline quotes followed by a reference
    for m in QUOTE_INLINE.finditer(text):
        q, ref = m.group(1), m.group(2)
        is_lsv = 'LSV' in ref or re.match(r'\s*v{1,2}\.\s*\d', ref)
        if not is_lsv: continue
        if re.search(r'\b(WEB|ASV|BSB|KJV|NIV|ESV|NRSV|my rendering|literally|lit\.|Charles|Brenton|LXX)\b', ref):
            continue
        refs = parse_ref(ref.replace('LSV', '').strip(' ,;'))
        if not refs: continue
        hay = ' '.join(verses_text(*r) for r in refs)
        ok, frag = matches(q, hay)
        if ok: n_ok += 1
        else:
            # allow a match anywhere in Jude for Jude refs (verse numbering slip) but report it
            report.append(f'{os.path.basename(path)}: QUOTE MISMATCH ({ref.strip()}): “{q}” — fragment not found: “{frag}”')
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
                body = re.sub(r'\*\*\d+\*\*', ' ', body)      # verse numbers in bold
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

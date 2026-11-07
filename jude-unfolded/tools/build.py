#!/usr/bin/env python3
"""Assemble manuscript.md from the chapter and appendix files, regenerate the
generated appendices, and export EPUB, DOCX, and PDF.

Usage: python3 tools/build.py [--no-export]
Requires pandoc. PDF export uses the Chromium bundled with Playwright (node).
"""
import os, re, sys, glob, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CH = os.path.join(ROOT, 'chapters')
AP = os.path.join(ROOT, 'appendices')
EX = os.path.join(ROOT, 'exports')

ORDER = (
    ['00a-title-copyright.md', '00b-readers-introduction.md', '00c-method.md',
     '00d-historical-introduction.md', '00e-overview.md'] +
    [os.path.basename(p) for p in sorted(glob.glob(os.path.join(CH, '[01][0-9]-jude-*.md')))] +
    ['14-afterword.md']
)
APPX = ['A-textual-variants.md', 'B-disputed-interpretations.md', 'C-jude-and-2-peter.md',
        'D-glossary.md', 'E-scripture-index.md', 'F-subject-index.md']

META = """---
title: "Jude, Unfolded"
subtitle: "An Exploration of Every Verse, Word, Image, and Meaning"
author: "[Author Name]"
date: "First edition, 2026"
lang: en-US
rights: "Commentary © 2026 [Author Name], licensed CC BY-SA 4.0. Every source text is in the public domain or under a free license (CC0, CC BY, or CC BY-SA); see the Copyright and Licensing page and the acknowledgments."
description: "A book-length expository commentary on the Epistle of Jude, working from the Greek text and its earliest manuscripts and quoting eighteen free English translations without preference."
---
"""

CSS = """
body { font-family: 'DejaVu Serif', 'FreeSerif', Georgia, serif; line-height: 1.5; max-width: 42em; margin: auto; padding: 0 1em; color: #1a1a1a; }
h1 { font-size: 1.7em; margin-top: 2.2em; page-break-before: always; break-before: page; }
h1.title { page-break-before: avoid; text-align: center; font-size: 2.4em; }
p.subtitle { text-align: center; font-style: italic; font-size: 1.2em; }
h2 { font-size: 1.3em; margin-top: 1.6em; border-bottom: 1px solid #ccc; }
h3 { font-size: 1.1em; margin-top: 1.3em; }
blockquote { margin: 1em 1.5em; padding-left: 1em; border-left: 3px solid #b8a27a; color: #333; }
table { border-collapse: collapse; width: 100%; font-size: 0.85em; margin: 1em 0; }
th, td { border: 1px solid #bbb; padding: 0.3em 0.45em; vertical-align: top; }
th { background: #f3efe6; }
.footnotes { font-size: 0.85em; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 0.9em; }
nav#TOC ul { list-style: none; padding-left: 1em; }
div[lang=he] { font-family: 'FreeSerif', 'Ezra SIL', 'SBL Hebrew', serif; font-size: 1.15em; direction: rtl; text-align: right; }
div[lang=grc] { font-family: 'FreeSerif', 'DejaVu Serif', serif; }
@page { size: 6in 9in; margin: 0.7in 0.65in 0.8in 0.65in; }
"""

def read(path):
    return open(path, encoding='utf-8').read().strip() + '\n'

def toc(parts):
    lines = ['# Table of Contents {.unnumbered}', '']
    for p in parts:
        for m in re.finditer(r'^# (.+?)(?:\s*\{[^}]*\})?\s*$', p, flags=re.M):
            title = m.group(1).strip()
            if title in ('Title Page', 'Table of Contents'):
                continue
            lines.append(f'- {title}')
    return '\n'.join(lines) + '\n'

def assemble():
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 'make_parallels.py')], check=True)
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 'make_texts.py')], check=True)
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 'make_indexes.py')], check=True)
    sys.path.insert(0, HERE)
    import make_texts
    amap = make_texts.anchor_map()
    def load(d, f):
        # link Scripture references to the chapter's own "Texts Highlighted" section
        return make_texts.link_refs(read(os.path.join(d, f)), amap.get(f, {}))
    front = [load(CH, f) for f in ORDER[:5]]
    body = [load(CH, f) for f in ORDER[5:]]
    appx = [load(AP, f) for f in APPX]
    back = [read(os.path.join(ROOT, 'bibliography.md')), read(os.path.join(AP, 'G-acknowledgments-licensing.md'))]
    # demote "Part" structure: insert part dividers as level-1 unnumbered headings
    parts = [front[0]] + [toc(front[1:] + body + appx + back)] + front[1:] + \
            ['# Part One: The Commentary {.unnumbered .part}\n'] + body + \
            ['# Part Two: Reference {.unnumbered .part}\n'] + appx + back
    text = META + '\n' + '\n\n'.join(parts)
    # the title-page heading duplicates the pandoc title block in exports; keep it in Markdown for readers
    out = os.path.join(ROOT, 'manuscript.md')
    open(out, 'w', encoding='utf-8').write(text)
    words = len(re.findall(r"[\w’'-]+", re.sub(r'^\[\^[^\]]+\]:.*$', '', text, flags=re.M)))
    print(f'manuscript.md written ({words:,} words incl. headings/tables; footnote definitions excluded)')
    return out

def export(md):
    os.makedirs(EX, exist_ok=True)
    css = os.path.join(EX, 'book.css'); open(css, 'w').write(CSS)
    # Exports get pandoc's own title block and table of contents, so drop the
    # Markdown-only "Title Page" and "Table of Contents" sections.
    text = open(md, encoding='utf-8').read()
    text = re.sub(r'^# Title Page \{[^}]*\}\n.*?(?=^# )', '', text, flags=re.M | re.S)
    text = re.sub(r'^# Table of Contents \{[^}]*\}\n.*?(?=^# )', '', text, flags=re.M | re.S)
    src = os.path.join(EX, '.export-source.md'); open(src, 'w', encoding='utf-8').write(text)
    md = src
    common = ['pandoc', md, '--from', 'markdown+footnotes+pipe_tables+header_attributes', '--toc', '--toc-depth=1',
              '--reference-location=section']
    subprocess.run(common + ['--css', css, '-o', os.path.join(EX, 'jude-unfolded.epub'),
                             '--epub-title-page=true', '--split-level=1'], check=True)
    subprocess.run(common + ['-o', os.path.join(EX, 'jude-unfolded.docx')], check=True)
    html = os.path.join(EX, 'jude-unfolded.html')
    subprocess.run(common + ['--standalone', '--embed-resources', '--css', css, '-o', html], check=True)
    pdf = os.path.join(EX, 'jude-unfolded.pdf')
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://{html}', {{ waitUntil: 'load' }});
  await p.pdf({{ path: '{pdf}', width: '6in', height: '9in', printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#666"><span class="pageNumber"></span></div>',
    margin: {{ top: '0.6in', bottom: '0.7in', left: '0.6in', right: '0.6in' }} }});
  await b.close();
}})();
"""
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True)
    if r.returncode != 0:
        print('PDF export failed:', r.stderr[-800:])
    os.remove(src)
    for f in ('jude-unfolded.epub', 'jude-unfolded.docx', 'jude-unfolded.pdf', 'jude-unfolded.html'):
        p = os.path.join(EX, f)
        if os.path.exists(p):
            print(f'  exports/{f}: {os.path.getsize(p):,} bytes')

if __name__ == '__main__':
    md = assemble()
    if '--no-export' not in sys.argv:
        export(md)

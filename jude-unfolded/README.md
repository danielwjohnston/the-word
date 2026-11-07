# Jude, Unfolded

*An Exploration of Every Verse, Word, Image, and Meaning*

A book-length expository commentary on the Epistle of Jude for thoughtful readers without academic training. It is built on the **Literal Standard Version (LSV)** as its primary English text and on the **SBL Greek New Testament** as its primary Greek text.

## Read the book

- **`manuscript.md`**: the assembled book. This Markdown file is the editable master.
- **`exports/`**: EPUB, DOCX, and PDF generated from `manuscript.md`.
- **`chapters/`**: front matter and the 13 main chapters as separate files (the working sources of the manuscript).
- **`appendices/`**: textual variants, disputed interpretations, the Jude–2 Peter parallels, glossary, indexes, and licensing acknowledgments.
- **`bibliography.md`**: all works cited, grouped by how they were verified.

## Research and quality files

| File | Purpose |
|---|---|
| `research/source-ledger.md` | Every source, how it was obtained, what was verified, and what remains uncertain |
| `research/coverage-matrix.md` | Verse-and-phrase map checked automatically against the chapters |
| `research/interpretive-decisions.md` | Positions the book takes and the alternatives it presents |
| `research/data-notes.md` | Computed facts (word counts, hapax legomena, repeated words, Jude–2 Peter overlap) |
| `research/texts/` | Verified copies of Jude in the LSV, SBLGNT (with apparatus), Robinson–Pierpont, TR, WEB, ASV, BSB, and KJV |
| `outline.md` | Detailed manuscript outline |
| `quality-review.md` | Audit results: coverage, quotation fidelity, citations, consistency |
| `progress.md` | Checkpoint log, unresolved questions, and next work |

## Tools

```bash
tools/fetch_sources.sh                 # download openly licensed source texts into .cache/
python3 tools/audit.py                 # coverage, LSV-quotation, footnote, and structure audits
python3 tools/greek_audit.py           # every Greek form checked against SBLGNT, LXX, RP/TR, and Abbott-Smith
python3 tools/build.py                 # regenerate Appendix C and indexes, assemble manuscript.md, export EPUB/DOCX/PDF/HTML
python3 tools/lsv.py JUD1:1-2 ZEC3:2   # print LSV verses exactly (for quoting)
```

`tools/build.py` needs `pandoc`. The PDF export uses the Chromium installed with Playwright.

## Licensing

- **LSV** quotations: The Literal Standard Version of the Holy Bible is a registered copyright of Covenant Press and the Covenant Christian Coalition (© 2020). It is used under Creative Commons Attribution-ShareAlike 4.0 (<https://creativecommons.org/licenses/by-sa/4.0/>). The text is quoted unaltered, per the publisher's request.
- **SBLGNT** Greek: Copyright 2010 Society of Biblical Literature and Logos Bible Software. CC BY 4.0 (<https://creativecommons.org/licenses/by/4.0/>).
- WEB, ASV, BSB, KJV, Robinson–Pierpont, TR, and Brenton LXX: public domain.
- The commentary text is the author's. Because it is interleaved with CC BY-SA material, the book is offered under **CC BY-SA 4.0** unless the author decides otherwise; see the copyright page and `progress.md` → "Decisions for the author."

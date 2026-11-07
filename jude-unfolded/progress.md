# Progress Log: *Jude, Unfolded*

## Status (7 November 2026)

**Manuscript complete and audited.** `manuscript.md` is assembled, and it passes the coverage, LSV-quotation, footnote, structure, and Greek-spelling audits. See `quality-review.md`. EPUB, DOCX, PDF, and HTML exports are in `exports/`.

## Completed

| Phase | Item | Checkpoint |
|---|---|---|
| 1 | LSV text and license verified (eBible.org; lsvbible.com); SBLGNT text, license, and apparatus (2010 and NA28-updated); RP 2018, TR, WEB, ASV, BSB, KJV, Brenton LXX | `research/source-ledger.md`, `research/texts/` |
| 1 | Primary sources read: 1 Enoch (Charles), Targums (Etheridge), Josephus, Philo, T. Naphtali, Sirach/Wisdom/3 Macc, Eusebius, Clement, Origen, Tertullian, Ignatius, Didache, Pliny, Muratorian Fragment, Athanasius, Jerome, Augustine, Calvin, Luther, Theophrastus; Abbott-Smith lexicon | source ledger |
| 2 | Data analysis (hapaxes, counts, Jude–2 Peter overlap); interpretive decisions; outline; coverage matrix | `research/` |
| 3 | Front matter: copyright, reader's introduction, method, historical introduction, overview | `chapters/00a–00e` |
| 3 | Chapters 1–13 and afterword | `chapters/01–14` |
| 4 | Automated audits plus manual review; corrections applied | `quality-review.md` |
| 5 | Appendices A–C, glossary, indexes, bibliography, acknowledgments; assembly; exports | `appendices/`, `bibliography.md`, `manuscript.md`, `exports/` |

## Decisions for the author (open)

1. **Author name and license.** Replace "[Author Name]" (copyright page, `tools/build.py` metadata, acknowledgments). The commentary is set to CC BY-SA 4.0 by default because it interleaves CC BY-SA LSV text. Change it only after advice on ShareAlike obligations.
2. **LSV commercial terms.** Before commercial printing, confirm with Covenant Press. The publisher's site and eBible.org say CC BY-SA 4.0, but some listings mention non-commercial terms.
3. **Length.** The main text is about 64,000 words, slightly above the 60,000 target. Trimming candidates are listed in `quality-review.md` §8.

## Unresolved research questions (for pre-publication checking)

- Verify the "prior knowledge" (V3) attributions against the printed commentaries, chiefly Bauckham (WBC 50), Metzger (Textual Commentary), and Watson, and add page numbers.
- Verify manuscript witness lists for Jude 5 and 22–23 against NA28/ECM, especially P72's readings.
- Verify Milik's judgment on Jude 14–15 and the 4Q204 identification against Milik (1976) or Nickelsburg (2001).
- Optionally add the Greek text of 1 Enoch 1:9 from a verified edition (Black, *Apocalypsis Henochi Graece*, 1970).

## Next work (if continued)

1. Author decisions above, then rebuild with `python3 tools/build.py`.
2. Pre-publication verification of V3 citations, with page numbers added.
3. Optional: page-numbered indexes in a typeset edition; cover design; ISBN.

## How to resume

```bash
cd jude-unfolded
tools/fetch_sources.sh          # restores .cache/ (LSV, Greek texts, MorphGNT, Abbott-Smith)
python3 tools/audit.py          # must report Issues: 0
python3 tools/greek_audit.py    # review any new unmatched forms
python3 tools/build.py          # regenerates appendices C/E/F, manuscript.md, exports/
```

Edit chapters in `chapters/` and appendices A, B, D, and G in `appendices/`. Appendices C, E, and F are generated, so do not edit them by hand.

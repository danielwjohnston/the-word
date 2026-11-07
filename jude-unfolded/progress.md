# Progress Log: *Jude, Unfolded*

## Status (7 November 2026, second edition)

**Second edition complete and audited.** The book was rebuilt under the author's governing instructions (see `project-brief.md`): only free sources; the original manuscripts first; no translation preferred; every cited text printed; no length limit. `tools/audit.py` reports 0 issues; every manuscript claim is checked by `tools/make_texts.py`; see `quality-review.md` §10.

### Second-edition changes

| Item | Where |
|---|---|
| Free-sources rule applied; KJV, *Luther's Works*, and all copyrighted or unverified modern scholarship scrubbed; claims re-established from public-domain commentaries and ancient texts | all chapters; `bibliography.md`; `research/source-ledger.md` §§9–10 |
| Section A rebuilt: SBLGNT Greek, a verified table of ten manuscripts, and each verse in 18 free translations in order of first publication | `chapters/01`–`13`; `tools/make_texts.py` |
| Section C headings now Greek-first (phrase, transliteration, gloss) | `chapters/01`–`13`; `tools/greek_headings.py` |
| New section L: every cited passage printed in the original language plus BSB and WEB; references linked at build | all chapters and introductions; `tools/build.py` |
| Overview prints the whole letter in Greek, BSB, and WEB; keeping-thread table in Greek | `chapters/00e-overview.md` |
| Copyright page, Reader's Introduction, Method, acknowledgments, bibliography rewritten | `chapters/00a`–`00c`; `appendices/G`; `bibliography.md` |
| Appendix A rebuilt on the manuscript evidence, with a generated table of how all 18 translations read the major variants; Appendix C now Greek-first with BSB and WEB | `appendices/A`, `appendices/C`; `tools/make_parallels.py` |
| Corrections found while re-verifying: K also adds θεόν in v. 4; L has the full doxology; ἀγάπαις/ἀπάταις differ by two letters; translation dates | see source ledger §10 |

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

1. **Author name.** Replace "[Author Name]" (copyright page, `tools/build.py` metadata, acknowledgments). The license is settled as CC BY-SA 4.0 (copyleft), as the free-sources rule requires.
2. **Inline quotations.** Inline cross-reference quotations still most often use the LSV, for its word-for-word clarity; every such passage is also printed in the original and in BSB and WEB in section L. If wider variety in inline quotations is wanted, the quotation audit will verify any free translation substituted.

## Unresolved research questions (for pre-publication checking)

- Dates of some modern free translations rest on Wikipedia (WEB 2000, OEB 2010, BSB and MSB 2022); refine if publishers give more precise dates.
- The text basis of the BSB is described from project documentation as an eclectic critical text; confirm wording if the publisher states it formally.
- Optionally add the Greek text of 1 Enoch 1:9 from a public-domain edition.

## Next work (if continued)

1. Author decisions above, then rebuild with `python3 tools/build.py`.
2. Optional: vary the translations used for inline quotations (the audit verifies any free translation).
3. Optional: page-numbered indexes in a typeset edition; cover design; ISBN.

## How to resume

```bash
cd jude-unfolded
tools/fetch_sources.sh          # restores .cache/ (translations, Greek and Hebrew texts, manuscripts, MorphGNT, Abbott-Smith)
python3 -I tools/audit.py       # must report Issues: 0
python3 -I tools/greek_audit.py # review any new unmatched forms
python3 -I tools/build.py       # regenerates sections A and L, appendices A.2/C/E/F, manuscript.md, exports/
```

Edit chapters in `chapters/` and appendices A, B, D, and G in `appendices/`, outside the `<!-- BEGIN/END GENERATED -->` markers. Sections A and L, the overview text, Appendix A.2, and Appendices C, E, and F are generated, so do not edit them by hand.

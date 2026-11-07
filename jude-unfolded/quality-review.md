# Quality Review: Phase 4 Comprehensive Audit

Audit date: 7 November 2026. Each check below lists the method, the result, and any corrections made. Automated checks are reproducible with `python3 tools/audit.py` and `python3 tools/greek_audit.py`. Run `tools/fetch_sources.sh` first.

## Summary

| Check | Method | Result |
|---|---|---|
| Coverage of all 25 verses | Script: every verse printed in a chapter's "A. The Text" | **25/25** |
| Coverage of significant phrases and words | Script: 133 units in `research/coverage-matrix.md`, each Greek key term found in its assigned chapter | **133/133 ✓** |
| LSV quotation fidelity | Script: every quotation tagged LSV, or attributed to a verse/Bible reference without another version named, checked word for word against the LSV source text (ellipses allowed) | **414 quotations verified; 0 mismatches** |
| Greek spelling | Script: 1,533 Greek tokens checked against SBLGNT (MorphGNT), RP/TR Jude, Brenton LXX, Abbott-Smith headwords | **15 forms not in those texts, all intentional** (see §3) |
| Footnotes | Script: every reference defined, every definition referenced, IDs unique | **171/171** |
| Chapter structure A–K | Script: sections A–K present in all 13 main chapters | **13/13** |
| Citation authenticity | Manual: every footnote checked against `research/source-ledger.md`; unverifiable claims labeled "cited from prior knowledge" | Done (see §4) |
| Historical uncertainty | Manual review of every reconstruction | Done (see §5) |
| Consistency across chapters | Manual review of key decisions | Done (see §6) |
| Separation of exposition and application | Manual: all "I. Contemporary Understanding" sections carry an explicit label and use conditional language | Done |
| Licensing and attribution | Manual: copyright page, acknowledgments, README, and export metadata | Done (one open item, §7) |

## 1. Corrections made during the audit

The automated audit caught the following errors during drafting. All were corrected in the chapter files:

- Bible quotations written from memory instead of from the LSV (Heb 9:26; 1 Pet 3:18; 1 Cor 9:16; Dan 7:18; Gen 1:2; 2 Cor 5:2; Ps 95:11; Heb 1:3; Jas 3:2; 2 Thess 3:15; Ezek 34:4; Acts 2:42; Acts 20:11). All were replaced with exact LSV wording.
- An editorial insertion inside an LSV quotation ("kept in [or 'for'] Jesus Christ") was removed, in line with decision L1 (no alteration of LSV text).
- Glosses and translations of non-LSV texts (LXX, Theodotion, the critical-text readings of v. 25, Maranatha) had been formatted like LSV quotations. They are now marked with single quotes or tagged by source.
- Coverage gaps where a chapter discussed a lemma but not the inflected form in Jude (κοινῆς, μετατιθέντες, δεσπότην, μιαίνουσιν, κυριότητα, σώματος, Σόδομα) were closed by adding the Greek phrase in context.
- An overclaim in Chapter 8 ("the only place in the NT where a writing outside the Hebrew Bible is quoted and called prophecy") was corrected, since Titus 1:12 calls a pagan poet "a prophet."
- An unverified date for Calvin's commentary was removed, and an unverified page range for Ellis (1978) was removed from the bibliography.
- The Isaiah 42:6 reference was corrected from "his servant Israel" to "his servant," because the identity of the servant there is debated.

## 2. Coverage

- All 25 verses appear in full, in the LSV, in the "A. The Text" section of their chapter. The whole letter also appears in the Overview, and the parallel passages appear in Appendix C.
- All 16 New Testament hapax legomena in Jude are discussed. The three words shared only with 2 Peter are discussed in Chapters 6, 9, and 10 and in Appendix C.
- Every image named in the brief has a deep dive or extended treatment: love feast (Ch. 6), faith delivered (Ch. 2), angels and judgment traditions (Ch. 3), Sodom and Gomorrah (Ch. 3), Michael and Moses' body (Ch. 4), Cain/Balaam/Korah (Ch. 5), shepherding (Ch. 6), reefs vs. stains (Ch. 6), clouds without water (Ch. 6), trees twice dead (Ch. 6), wandering stars (Ch. 7), Enoch and canon (Ch. 8), praying in the Spirit (Ch. 11), keeping oneself in God's love (Ch. 11), mercy to doubters (Ch. 12), kept from stumbling (Ch. 13). Additional deep dives: Jesus' brothers (Intro), the text of Jude 5 (Ch. 3), the text of Jude 22–23 (Ch. 12).

## 3. Greek accuracy

- Lexical claims are tied to entries in Abbott-Smith (1922) that were actually read. Each footnote quotes the entry.
- Counts and frequency claims are computed from MorphGNT: 459 words, 226 lemmas, 16 hapaxes, 68 NT optatives, τηρέω ×5, the single NT superlative of ἅγιος, and οὐαί by book.
- The 15 Greek forms not found in the reference texts are intentional: dictionary/lemma forms (διακρίνομαι, ἁγιώτατος, ἀγάπαι), nomina sacra (ΙΣ, ΚΣ), quoted variant forms (παρεισεδύησαν, ἀσπίλους), etymological bases quoted from the lexicon (φθινόπωρον, μοῖρα, ἄθετον), abbreviations quoted from the lexicon (παράδ-, ὑπόδ-), a root (ἀσεβ-), Theophrastus's title (Μεμψιμοιρία), and μαραναθά (*Didache*).
- Etymological claims are flagged as such, and the method chapter and several "caution" notes warn against the etymological fallacy (ἐπαγωνίζομαι, ἀγάπη, ψυχικός, πλανήτης).

## 4. Citation authenticity

The bibliography is divided into three tiers, matching the source ledger:

1. **Consulted directly (V1):** all biblical texts, Greek editions and apparatus, 1 Enoch (Charles), Targums (Etheridge), Josephus, Philo, the Testament of Naphtali, the church fathers cited, Pliny (Latin), Theophrastus, Calvin, Luther's preface, and Abbott-Smith.
2. **Secondary reports (V2):** Wikipedia summaries of 1 Enoch and the Testament of Moses, Mayor and Moulton–Milligan through Abbott-Smith, Flink (2007), and Milik's judgment on Jude 14–15.
3. **Prior knowledge (V3):** Bauckham, Davids, Green, Schreiner, Neyrey, Kelly, Moo, Reese, Frey, Bigg, Watson, Ellis, Metzger, Wasserman, Nickelsburg, Bartholomä. The book attributes to these works only widely documented positions, without page numbers, and every such footnote says "cited from prior knowledge."

**No citation in the book was invented.** Specific claims whose evidence could not be retrieved, such as the full witness lists for Jude 5 and 22–23 and Gelasius of Cyzicus, are stated cautiously and flagged in footnotes.

## 5. Treatment of historical uncertainty

Reconstructions are labeled as such wherever they appear: the profile of the opponents (Intro §5; Ch. 2), the lost ending of the *Testament of Moses* (Ch. 4), the relationship of the love feast to the Lord's Supper (Ch. 6, with "documented / probable / later / speculative" categories), authorship and date (Intro §§1, 3), the relation of Jude to 2 Peter (Intro §8; App. C), Jude's source text for 1 Enoch 1:9 (Ch. 8), and the dating of the Targum traditions (Ch. 5).

## 6. Consistency across chapters

The following decisions were checked across all files and agree with `research/interpretive-decisions.md`:

- v. 1 "loved" (critical text) and "kept for/by/in" (Chs. 1, 11, 13).
- v. 5 "Jesus" (Chs. 2, 3, 8, 13; App. A, B).
- v. 6 Watcher tradition (Chs. 3, 7, 8).
- v. 7 "other flesh" = primarily angelic (Ch. 3; App. B).
- v. 12 σπιλάδες: "reefs" preferred, "stains" possible (Chs. 6, 12, 13; App. B).
- vv. 22–23: three-clause text followed, alternatives explained (Ch. 12; App. A, B).
- v. 25: LSV follows the Byzantine text, and the critical text is explained (Ch. 13; App. A).
- Authorship: "responsible conclusion, not proven" (Intro; Ch. 1; Ch. 10).

## 7. Licensing and attribution

- The LSV attribution text matches the publisher's statement and is placed on the copyright page, in the acknowledgments, in the README, and in the export metadata.
- LSV wording is unaltered throughout (verified by script).
- SBLGNT: CC BY 4.0 attribution is given, and the one change made (critical signs omitted in body quotations) is stated.
- **Open item for the author:** confirm the LSV's commercial-print terms with Covenant Press. Some third-party listings mention non-commercial terms. The publisher's site and eBible.org state CC BY-SA 4.0.
- **Open item for the author:** replace "[Author Name]" and confirm the license for the commentary text (CC BY-SA 4.0 is used by default; see the copyright page note).

## 8. Length

| Part | Words (raw count, including quotations, tables, Greek, and headings) |
|---|---|
| Front matter (reader's introduction, method, historical introduction, overview) | ≈ 7,600 |
| Main commentary, Chapters 1–13 | ≈ 56,000 |
| Afterword | ≈ 460 |
| **Main text total** | **≈ 64,100** |
| Appendices, glossary, indexes, bibliography, acknowledgments | ≈ 9,700 |

The main text is about 7% above the 60,000-word upper target. The raw count includes each chapter's LSV passage, the full letter in the Overview, about 30 Greek tables, and 65 reflection questions. Prose alone is close to the target. No filler was identified in review. If a shorter edition is wanted, the best candidates for trimming are the "F. Connections Across Scripture" sections, which sometimes restate cross-references already discussed in section C, and the length of Chapter 3, which contains three deep dives.

## 9. Known limitations

- Witness lists for individual manuscripts (P72, ℵ, A, B, C) are given only where widely reported and are flagged. A pre-publication check against NA28 or ECM is recommended.
- The Greek of 1 Enoch 1:9 is not quoted, because no verifiable transcription could be retrieved.
- Markdown has no page numbers, so the indexes point to chapters. A typeset edition should regenerate page-based indexes.
- The PDF is a clean reading copy produced from HTML via Chromium. It is not print-shop typesetting.

## 10. Second-edition audit (7 November 2026)

The second edition was rebuilt under `project-brief.md`. Audit results after the final build:

| Check | Tool | Result |
|---|---|---|
| Inline and block quotations match the translation they name (any of the 18; excluded translations blocked) | `tools/audit.py` | 395 verified, 0 mismatches |
| Coverage of every verse-and-phrase unit | `tools/audit.py` | 133/133 |
| Footnotes defined and referenced | `tools/audit.py` | 178/178, no duplicates or orphans |
| Sections A–L present in every chapter | `tools/audit.py` | 0 missing |
| Manuscript readings (ten witnesses, 25 verses) | `tools/make_texts.py` | every listed manuscript checked against its INTF transcription; build stops on any failure |
| Translation variants table (Appendix A.2) | `tools/make_texts.py` | every cell derived from, or asserted against, the translation's own text |
| Greek forms | `tools/greek_audit.py` | 16,295 tokens; 34 forms not in the reference texts, all reviewed: manuscript readings verified against INTF (e.g., ὑπερέχουσαι, τηρήσωμεν, ἀνοικοδομεῖσθε, Βαλαάκ), lexicon citation forms and fragments (Abbott-Smith), the catena fragment (Ch. 4), nomina sacra (ΙΣ, ΚΣ), and μαραναθά |
| Reference links to section L | `tools/build.py` + check of `manuscript.md` | 437 anchors, 680 links, 0 broken |
| Exports | `tools/build.py` | EPUB, DOCX, HTML, PDF (596 pages at 6 × 9 in.); Hebrew renders right-to-left (spot-checked) |

**Length.** About 77,800 words of commentary (excluding footnote definitions) and about 194,000 words of generated source texts: the Greek, manuscript tables, eighteen translations of every verse, and the full text of about 437 highlighted passages. The author asked for no length trimming, so the earlier length targets in §8 no longer apply.

**Scrubbing.** No quotation from a translation that requires permission remains; the KJV is replaced by Webster (WBS). The bibliography lists only free works, all consulted directly; the removed works are listed in `research/source-ledger.md` §10.

**Judgment calls to note.** (1) Inline cross-reference quotations still most often use the LSV, for its word-for-word clarity; every such passage is also printed in the original language and in BSB and WEB in section L. (2) Passages of more than five verses already printed in full earlier in the book are linked rather than repeated. (3) References to whole sections of 1 Enoch (chs. 1–36, 6–16, 72–82) are noted rather than printed.

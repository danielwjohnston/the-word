# Source Ledger — *Jude, Unfolded*

This ledger records every source the manuscript relies on, how it was obtained, what was actually verified in the working session of 7 November 2026, and what remains uncertain. It is the control document for the citation audit (see `quality-review.md`).

**Verification levels used below**

| Level | Meaning |
|---|---|
| **V1 — Retrieved and checked** | The text was downloaded or fetched during the session and the specific passages used in the book were read directly. |
| **V2 — Retrieved, secondary report** | The claim was confirmed only through a reliable secondary report (for example, a lexicon entry or reference work quoting the source), not from the primary text itself. |
| **V3 — Prior scholarly knowledge, not re-verified** | A standard published work cited for a well-known position. It could not be consulted in this session. Page numbers are deliberately omitted, and the manuscript attributes only widely documented positions to these works. **Check each against the printed work before publication.** |

---

## 1. Primary biblical texts

### 1.1 Literal Standard Version (LSV): primary English text — V1

- **Edition used:** eBible.org USFM edition, `englsv_usfm.zip`, source files dated 30 Oct 2026, retrieved 2026-11-07 from <https://ebible.org/Scriptures/englsv_usfm.zip>. Jude was cross-checked against the HTML rendering at <https://ebible.org/englsv/JUD01.htm>; the two agree word for word.
- **Copyright and license (verified at <https://ebible.org/englsv/copyright.htm> and <https://www.lsvbible.com/p/get-lsv.html>):** "The Literal Standard Version of the Holy Bible is a registered copyright of Covenant Press and the Covenant Christian Coalition (© 2020)." eBible.org distributes it under the **Creative Commons Attribution-ShareAlike 4.0** license (<https://creativecommons.org/licenses/by-sa/4.0/>). The lsvbible.com footer reads "a CC BY-SA translation by Covenant Press."
- **Publisher's requests (verified):** Covenant Press "requests that the text remain unaltered in the English language." For whole books or commercial use, attribution must include both "Literal Standard Version (LSV)" and the publisher's name.
- **Unresolved licensing note:** A third-party listing (find.bible) and freely-given.org report that some places describe English use in non-commercial (CC BY-NC-ND-like) terms. The publisher's own site and eBible.org both state CC BY-SA 4.0. The manuscript follows the publisher's stated CC BY-SA terms, attributes fully, and does not alter LSV wording. **Decision for the author:** before any commercial printing, confirm the current terms with Covenant Press. See `research/interpretive-decisions.md` §L1.
- **Textual basis (verified from the LSV preface, <https://www.lsvbible.com/p/the-preface-to-literal-standard-version.html>):** the Masoretic Text for the Old Testament and "the Textus Receptus (TR) and Majority Text (M) for the New," with other readings used "in certain, specific instances … where the evidence seems incontrovertible." The LSV prints the divine name in the Old Testament as "YHWH" and uses "LORD" in capitals in the New Testament "when a reference to YHWH is likely."
- **Observed in Jude (verified by comparing the texts):** the LSV follows critical-text readings in vv. 1 ("loved"), 3 ("our common salvation"), 4 (no "God"), and 5 ("Jesus"). It follows Byzantine/TR readings in v. 15 ("all their impious ones") and v. 25 ("only wise God," with no "through Jesus Christ our Lord" and no "before all the age"). In vv. 22–23 it has a three-clause text.
- **Formatting conventions:** square brackets are the LSV's own marks for supplied words. Double brackets `[[or …]]` mark the LSV's alternative renderings. `||` in the USFM marks poetic line divisions, and the manuscript shows these as line breaks or " / ". Strong's-number tags in the USFM were stripped. No words were changed.
- Saved copies: `research/texts/jude-lsv.md`, `research/texts/2peter-lsv.md`.

### 1.2 Greek New Testament: SBL Edition (SBLGNT), primary Greek text — V1

- Michael W. Holmes, ed., *The Greek New Testament: SBL Edition* (Atlanta: Society of Biblical Literature; Bellingham, WA: Logos Bible Software, 2010). Data version 1.2 (2023-07-10), <https://github.com/Faithlife/SBLGNT>.
- **License (verified in the repository README and LICENSE and at <https://www.sblgnt.com/license/>):** Creative Commons Attribution 4.0 International. "Copyright 2010 by the Society of Biblical Literature and Logos Bible Software."
- **Apparatus (verified):** the original SBLGNT apparatus for Jude at <https://www.sblgnt.com/download/86-Jud-APP.txt>, plus the updated apparatus citing NA28 in the eBible.org edition `grcsbl_usfm.zip` (files dated 30 Oct 2026). These establish the readings of WH, Tregelles, the NIV Greek text, Robinson–Pierpont, NA27, and NA28 at every variation unit in Jude.
- **Key verified facts:** NA28 reads Ἰησοῦς in v. 5 where NA27 read ὁ κύριος ἅπαξ. NA28 reads πᾶσαν ψυχήν in v. 15 where SBLGNT reads πάντας τοὺς ἀσεβεῖς. NA28 and SBLGNT both print the three-clause text of vv. 22–23.
- **Morphology and lemma data:** J. K. Tauber, ed., *MorphGNT: SBLGNT Edition*, v. 6.12, <https://github.com/morphgnt/sblgnt> (parsing CC BY-SA 3.0), DOI 10.5281/zenodo.376200. Used for word counts, hapax legomena, and parsing (see `research/data-notes.md`).
- Saved copy: `research/texts/jude-sblgnt.md`.

### 1.3 Comparison texts — all V1, all public domain

| Text | Source file | License verified |
|---|---|---|
| Robinson–Pierpont, *The New Testament in the Original Greek: Byzantine Textform 2018* | eBible.org `grcmt_usfm.zip` | Public domain (release statement verified) |
| Text-Critical Greek NT notes (Robinson text, notes by Robert Adam Boyd), with manuscript percentages | eBible.org `grctcgnt_usfm.zip` | Public domain |
| Greek Textus Receptus, with Adam Boyd's comparison notes | eBible.org `grctr_usfm.zip` | Public domain |
| 1904 Patriarchal Greek NT | eBible.org `grcbyz_usfm.zip` | Public domain |
| World English Bible (WEB) | eBible.org `engwebp_usfm.zip` | Public domain (trademark note respected: text unaltered) |
| American Standard Version (1901) | eBible.org `eng-asv_usfm.zip` | Public domain |
| Berean Standard Bible (BSB) | eBible.org `engbsb_usfm.zip` | Public domain |
| King James Version (1769 text) | eBible.org `eng-kjv2006_usfm.zip` | Public domain outside the UK (Crown patent noted) |
| Brenton, Greek Septuagint with Apocrypha | eBible.org `grcbrent_usfm.zip` | Public domain |
| Brenton, English Septuagint | eBible.org `eng-Brenton_usfm.zip` | Public domain |

Saved Jude copies: `research/texts/jude-*.txt`.

**Note on percentages:** the manuscript-percentage figures in the Text-Critical Greek NT notes (for example, "ἡγιασμένοις 90.2%") come from that edition's notes. They count manuscripts and do not weigh them. The book cites them only to illustrate how common a reading is, never as an argument for originality.

---

## 2. Jewish texts of the Second Temple and rabbinic periods

| Source | Edition and location | Passages checked | Level |
|---|---|---|---|
| **1 Enoch** | R. H. Charles, *The Book of Enoch* (London: SPCK, 1917; public domain), Wikisource transcription <https://en.wikisource.org/wiki/The_Book_of_Enoch_(Charles)> | 1:1–9; 2:1–3; 5:1–9; 10:1–19; 18:1–16; 21:1–10; 60:1–8; 80:1–8; 93:1–10 | V1 |
| 1 Enoch textual history | Wikipedia, "Book of Enoch" (Qumran Aramaic fragments 4Q201–4Q212; Akhmim/Panopolitanus Greek of chs. 1–32, published 1892; complete text only in Ge'ez; canonical in the Ethiopian and Eritrean Orthodox Tewahedo churches; Book of the Watchers usually dated 4th–3rd c. BC) | — | V2 |
| 1 Enoch 1:9 at Qumran (4Q204 = 4QEnᶜ ar, col. I) and Milik's judgment that Jude is closer to the Aramaic than the Greek or Ethiopic | Reported in secondary discussions found by search (b-hebrew list archive; Enoch scholarship blog) | — | V2 (attribute cautiously) |
| **Testament (Assumption) of Moses** | Wikipedia, "Testament of Moses": a single incomplete 6th-century Latin manuscript found by A. Ceriani in the Biblioteca Ambrosiana, Milan, published 1861. The Michael–devil dispute is not in the surviving text. Gelasius of Cyzicus and Origen cite the dispute. | — | V2 |
| **Testament of Naphtali** 3:3–5 | *Testaments of the Twelve Patriarchs*, trans. R. Sinker, ANF 8, New Advent <https://www.newadvent.org/fathers/0801.htm> | Sodom "changed the order of its nature, in like manner also the Watchers…" | V1 |
| **Sirach** 16:7–8; **Wisdom** 10:6–7; **3 Maccabees** 2:4–5; 6:39 | Brenton (English and Greek) | Giants and Sodom as examples; smoking waste land; ἀπταίστους in 3 Macc 6:39 | V1 |
| **Josephus**, *Antiquities* 1.2.1–2 (Cain); 4.6.6 (Balaam's counsel); 4.2 (Korah) | Trans. W. Whiston, Project Gutenberg #2848 | Cain "wholly intent upon getting," author of "measures and weights," etc.; Balaam advises using Midianite women | V1 (Whiston book.chapter.section numbering used) |
| **Targum Pseudo-Jonathan** and **Jerusalem (Fragment) Targum** on Gen 4:8 | J. W. Etheridge, *The Targums of Onkelos and Jonathan ben Uzziel on the Pentateuch* (1862; public domain), <https://www.targum.info/pj/pjgen1-6.htm> | Cain: "There is neither judgment nor Judge, nor another world…" | V1 |
| Septuagint idioms | Brenton Greek LXX | θαυμάζω πρόσωπον (Gen 19:21; Lev 19:15; Deut 10:17; Job 13:10; 22:8; 32:22; Prov 18:5; Isa 9:15 [Brenton 9:13]); ἐνυπνιαζόμενος of the false prophet (Deut 13:2–6 [Eng. 13:1–5]); λαλήσει ὑπέρογκα (Dan 11:36, Theodotion); ὕδωρ Ἀντιλογίας (Num 20:13); Zech 3:1–4 LXX (Ἐπιτιμήσαι Κύριος ἐν σοί, διάβολε; δαλὸς ἐξεσπασμένος ἐκ πυρός; ἱμάτια ῥυπαρά); Ezek 34:2, 8 (ποιμένες ἑαυτούς); Deut 33:2; Zech 14:5 | V1 |

---

## 3. Early Christian sources — all V1 (New Advent, ANF/NPNF public-domain translations, unless noted)

| Source | Passage | What it establishes |
|---|---|---|
| Eusebius, *Hist. eccl.* 2.23.25 | Jude among the seven "catholic epistles"; "not many of the ancients have mentioned it," yet "read publicly in very many churches" | Disputed but widely used |
| Eusebius, *Hist. eccl.* 3.19–20 | Hegesippus: grandsons of Jude before Domitian; owned land worth 9,000 denarii; calloused hands; later "ruled the churches"; lived until Trajan | Jude's family in tradition |
| Eusebius, *Hist. eccl.* 3.25.3 | Jude among the disputed writings "recognized by many" | Antilegomena status |
| Eusebius, *Hist. eccl.* 6.13.6; 6.14.1 | Clement of Alexandria used Jude and commented on it in the *Hypotyposes* | Late 2nd-century use |
| Clement of Alexandria, *Adumbrationes* on Jude (ANF 2, "Fragments," New Advent 0211) | Jude "did not say that he himself was His brother"; "Here he confirms the assumption of Moses" | Early identification of the Michael tradition |
| Clement of Alexandria, *Paedagogus* 2.1 | Criticizes calling lavish suppers "agape" | Love feast abuses c. 200 |
| Origen, *De principiis* 3.2.1 | "The Ascension of Moses (a little treatise, of which the Apostle Jude makes mention…)" | Source of Jude 9 |
| Origen, *Commentary on Matthew* 10.17 | Jude "wrote a letter of few lines… but filled with the healthful words of heavenly grace" | Early esteem |
| Tertullian, *De cultu feminarum* 1.3 | Defends Enoch's authority: "Enoch possesses a testimony in the Apostle Jude" | Jude used to defend Enoch |
| Tertullian, *Apology* 39 | Description of the agape: prayer, moderate eating, hymns, care for the needy | Love feast practice c. 197 |
| Ignatius, *To the Smyrnaeans* 8.2 | "It is not lawful without the bishop either to baptize or to celebrate a love-feast" | Earliest extra-NT use of "agape" for a meal |
| *Didache* 9–10 | Eucharistic prayers; "after you are filled, thus give thanks" | Meal setting of early Eucharist |
| Pliny the Younger, *Ep.* 10.96.7 (Latin, The Latin Library) | Christians met before dawn, sang "carmen Christo quasi deo," later reassembled "ad capiendum cibum, promiscuum tamen et innoxium," and stopped after the ban on *hetaeriae* | Non-Christian witness to a common meal, c. 110–112 |
| Muratorian Fragment (ANF 5, "Fragments of Caius," New Advent 0510) | "The Epistle of Jude, indeed, and two belonging to the above-named John… are reckoned among the Catholic epistles" | Acceptance in the West (date debated) |
| Athanasius, *Festal Letter* 39 (367) | Lists "one of Jude" among the seven catholic epistles | Canonical list |
| Jerome, *De viris illustribus* 4 | "Because in it he quotes from the apocryphal Book of Enoch it is rejected by many. Nevertheless by age and use it has gained authority" | Enoch as the reason for doubt |

**Reformation reception — V1**

- Martin Luther, "Preface to the Epistles of St. James and St. Jude" (1522), English as reproduced at <https://www.bible-researcher.com/antilegomena.html> (translation from *Luther's Works* vol. 35; page not verified). Luther calls Jude "an extract or copy of St. Peter's second epistle" and says Jude "speaks of the apostles like a disciple who comes long after them."
- John Calvin, *Commentaries on the Catholic Epistles*, trans. John Owen (Edinburgh: Calvin Translation Society, 1855; CCEL plain text <https://www.ccel.org/ccel/c/calvin/calcom45/cache/calcom45.txt>). On v. 9: Jude may refer to "what had already been handed down for many ages." On v. 14: "I rather think that this prophecy was unwritten, than that it was taken from an apocryphal book."

---

## 4. Lexical and grammatical sources

| Source | Status | Use |
|---|---|---|
| G. Abbott-Smith, *A Manual Greek Lexicon of the New Testament* (Edinburgh: T&T Clark, 1922; public domain). TEI edition <https://github.com/translatable-exegetical-tools/Abbott-Smith> | **V1.** Entries read for σπιλάς, σπίλος, σπιλόω, φθινοπωρινός, ἐπαφρίζω, ἄπταιστος, μεμψίμοιρος, παρεισδύω, ἐπαγωνίζομαι, ἀποδιορίζω, γογγυστής, ὑπέρογκος, πλανήτης, ζόφος, ἀΐδιος, οἰκητήριον, δεῖγμα, κυριότης, ἀσέλγεια, δεσπότης, ἐμπαίκτης, ψυχικός, ἀντιλογία, ἀγάπη, ἅπαξ, ἄμωμος, ἀγαλλίασις, μεγαλωσύνη, κατενώπιον, ἀθετέω, μιαίνω, φυσικῶς, πάλαι, προγράφω, μετατίθημι, ἐκπορνεύω, πρόκειμαι, δίκη, ὑπέχω, ἐκριζόω, ἄκαρπος, παραφέρω, ἄνυδρος, ὠφέλεια, κλητός, ἀφόβως, ἐκχέω | Primary lexical authority actually consulted |
| J. B. Mayor, *The Epistle of St. Jude and the Second Epistle of St. Peter* (London: Macmillan, 1907) | **V2** (cited through Abbott-Smith's references, e.g., Mayor's "elaborate note" on φθινοπωρινός, pp. 55–59, and his note on σπιλάς, p. 41) | Classic philological commentary |
| J. H. Moulton and G. Milligan, *The Vocabulary of the Greek Testament* (1930) | **V2** (cited through Abbott-Smith) | Papyri usage |
| W. Bauer, F. W. Danker et al., *A Greek-English Lexicon of the New Testament* (BDAG), 3rd ed. (2000) | **V3**: not consulted; no specific glosses attributed to it | Recommended for further study |
| H. G. Liddell, R. Scott, H. S. Jones, *A Greek-English Lexicon*, 9th ed. (1940) | **V3**: Perseus lookups failed in session; not quoted | Further study |
| D. B. Wallace, *Greek Grammar Beyond the Basics* (1996) | **V3**: general grammatical categories only | Further study |
| Data-derived counts (MorphGNT) | **V1**: computed by `tools/gnt_stats.py` | 459 words; 226 lemmas; 16 NT hapax; τηρέω ×5; optatives in the NT ×68 |

---

## 5. Modern scholarship cited — **V3 unless marked**

These works are standard in Jude scholarship. Because none could be opened in this session, the manuscript (a) attributes to them only positions that are widely reported and characteristic of the work, (b) cites them by passage of Jude discussed ("on v. 12") rather than by page, and (c) flags them for verification before publication.

| Work | Position(s) attributed in the manuscript |
|---|---|
| Richard Bauckham, *Jude, 2 Peter* (WBC 50; Waco: Word, 1983) | Authorship by Jude the brother of Jesus is plausible; Palestinian Jewish-Christian milieu; the "text + 'these'" interpretive pattern in vv. 5–19; the opponents were itinerant, antinomian charismatics rather than developed Gnostics; 2 Peter used Jude; the four nature images of vv. 12–13 echo 1 Enoch 2–5 and 80; the reading of κρίσιν βλασφημίας in v. 9 as "condemnation for slander" in a reconstructed Moses tradition; preference for a shorter two-clause text in vv. 22–23 |
| Richard Bauckham, *Jude and the Relatives of Jesus in the Early Church* (Edinburgh: T&T Clark, 1990) | Extended study of the family of Jesus and Jude's use of tradition |
| E. Earle Ellis, "Prophecy and Hermeneutic in Jude," in *Prophecy and Hermeneutic in Early Christianity* (Tübingen: Mohr Siebeck, 1978) | Midrashic structure of Jude |
| Duane F. Watson, *Invention, Arrangement, and Style: Rhetorical Criticism of Jude and 2 Peter* (SBLDS 104; Atlanta: Scholars Press, 1988) | Rhetorical outline: exordium (v. 3), narratio (v. 4), probatio (vv. 5–16), peroratio (vv. 17–23) |
| Bruce M. Metzger, *A Textual Commentary on the Greek New Testament*, 2nd ed. (Stuttgart: Deutsche Bibelgesellschaft / UBS, 1994) | Jude 5: the committee printed κύριος; Metzger and Allen Wikgren dissented in favor of Ἰησοῦς as "the best attested reading" (consistent with the Mounce report found by search, V2) |
| Tommy Wasserman, *The Epistle of Jude: Its Text and Transmission* (ConBNT 43; Stockholm: Almqvist & Wiksell, 2006) | The fullest study of Jude's manuscripts; cited as the standard resource (no specific conclusions attributed) |
| Peter H. Davids, *The Letters of 2 Peter and Jude* (PNTC; Grand Rapids: Eerdmans, 2006) | General commentary (further reading) |
| Gene L. Green, *Jude and 2 Peter* (BECNT; Grand Rapids: Baker Academic, 2008) | General commentary (further reading) |
| Thomas R. Schreiner, *1, 2 Peter, Jude* (NAC 37; Nashville: B&H, 2003) | General commentary (further reading) |
| Jerome H. Neyrey, *2 Peter, Jude* (AB 37C; New York: Doubleday, 1993) | Social-scientific reading (honor/shame, patronage); further reading |
| J. N. D. Kelly, *A Commentary on the Epistles of Peter and of Jude* (BNTC; London: A&C Black, 1969) | Further reading |
| Charles Bigg, *A Critical and Exegetical Commentary on the Epistles of St. Peter and St. Jude* (ICC; Edinburgh: T&T Clark, 1901) | Argued that 2 Peter was prior to Jude (minority view) |
| Jörg Frey, *The Letter of Jude and the Second Letter of Peter: A Theological Commentary* (Waco: Baylor University Press, 2018) | Further reading |
| Ruth Anne Reese, *2 Peter and Jude* (THNTC; Grand Rapids: Eerdmans, 2007) | Further reading |
| Douglas J. Moo, *2 Peter, Jude* (NIVAC; Grand Rapids: Zondervan, 1996) | Further reading |
| J. T. Milik, *The Books of Enoch: Aramaic Fragments of Qumrân Cave 4* (Oxford: Clarendon, 1976) | Publication of the Aramaic Enoch fragments; his judgment on Jude 14–15 (V2 via secondary report) |
| Timo Flink, "Reconsidering the Text of Jude 5, 13, 15 and 18," *Filologia Neotestamentaria* 20 (2007): 95–125 | Existence and topic verified by search result (V2); argues the reading Ἰησοῦς is hard to explain as a scribal invention |
| Philipp F. Bartholomä, "Did Jesus Save the People out of Egypt? A Re-examination of a Textual Problem in Jude 5," *Novum Testamentum* 50 (2008): 143–58 | Existence verified by search report (V2); title and pages from prior knowledge (V3) |

---

## 6. Searches that failed or were blocked (recorded so nothing is presented as verified when it was not)

- `lsv.scripturedirect.com`: DNS blocked in this environment. LSV verified through eBible.org and lsvbible.com instead.
- `sacred-texts.com`: HTTP 403. Charles's 1 Enoch obtained from Wikisource instead.
- Sefaria API: Cloudflare challenge. Targum obtained from targum.info (Etheridge) instead.
- Perseus LSJ: lookup errors. Abbott-Smith used instead. No LSJ glosses are quoted.
- The Greek text of 1 Enoch 1:9 (Akhmim) could not be retrieved in a verifiable transcription. **The manuscript does not quote it in Greek**; it compares Jude with Charles's English and describes the Greek only in general terms.
- Gelasius of Cyzicus, *Hist. eccl.* 2.21.7, and Didymus the Blind on Jude were not retrieved. They are mentioned only as reported (V2) and never quoted.

---

## 7. Open questions for pre-publication checking

1. Confirm the LSV license terms for commercial print with Covenant Press (CC BY-SA vs. reported NC language).
2. Verify the V3 attributions against the printed commentaries and add page numbers.
3. Verify the 4Q204 identification and Milik's assessment against Milik (1976) or Nickelsburg's Hermeneia commentary on 1 Enoch (2001).
4. Optionally consult NA28 and ECM directly for full witness lists (P72, ℵ, A, B, C, etc.). The manuscript names individual manuscripts only where the reading is verified or very widely reported, and marks those cases.

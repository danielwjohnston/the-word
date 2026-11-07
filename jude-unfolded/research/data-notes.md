# Data Notes: Computed Facts about the Text of Jude

Every figure below was computed in the 7 November 2026 session from the MorphGNT/SBLGNT data (`tools/gnt_stats.py`, `tools/parallels.py`) or read directly from the verified texts in `research/texts/`. The counts depend on the SBLGNT text and on MorphGNT's lemmatization. Another edition would give slightly different numbers. The book reports these figures as approximate ("about 460 words") whenever the edition could matter.

## Size

- **459** word tokens in the SBLGNT text of Jude. The book says "about 460 words."
- **226** distinct lemmas.
- Whole SBLGNT New Testament: 137,554 tokens. Jude is roughly 0.3% of the NT.

## Words found in Jude and nowhere else in the New Testament (SBLGNT lemmas)

| Lemma | Verse | Gloss (Abbott-Smith unless noted) |
|---|---|---|
| ἐπαγωνίζομαι | 3 | to contend for |
| παρεισδύω | 4 | to slip in secretly, steal in |
| ἐκπορνεύω | 7 | to give oneself up to fornication (strengthened form) |
| δεῖγμα | 7 | a thing shown; an example (a warning) |
| ὑπέχω | 7 | to undergo, suffer (δίκην, a penalty) |
| φυσικῶς | 10 | naturally, by nature |
| Κόρε | 11 | Korah (proper name) |
| σπιλάς | 12 | a rock or reef over which the sea dashes; in late writers = σπίλος, a spot, stain |
| φθινοπωρινός | 12 | autumnal (from φθινόπωρον, late autumn) |
| ἐπαφρίζω | 13 | to foam up |
| πλανήτης | 13 | a wanderer; ἀστέρες π., "wandering stars" (cl. planets) |
| ἀσεβέω | 15 | to act impiously |
| γογγυστής | 16 | a murmurer |
| μεμψίμοιρος | 16 | complaining of one's fate, querulous |
| ἀποδιορίζω | 19 | to mark off; to make separations |
| ἄπταιστος | 24 | without stumbling, sure-footed |

That is **16** NT hapax legomena in 25 verses. They make up about 7% of Jude's distinct lemmas, an unusually high share. The figure supports the common observation that Jude's vocabulary is rich and literary.

**Words shared only by Jude and 2 Peter** within the NT: συνευωχέομαι ("feast together," Jude 12 / 2 Pet 2:13), ὑπέρογκος ("swollen," Jude 16 / 2 Pet 2:18), and ἐμπαίκτης ("scoffer," Jude 18 / 2 Pet 3:3).

## Repeated words that carry the argument

| Lemma | Count in Jude | Verses | Observation |
|---|---|---|---|
| τηρέω (keep) | 5 | 1, 6 (×2), 13, 21 | Kept by God (1); angels who did not keep / are kept for judgment (6); darkness kept (13); "keep yourselves" (21). φυλάσσω ("guard") in v. 24 completes the theme. |
| οὗτος (this/these) | 9 | 4, 7, 8, 10, 12, 14, 16, 19 | "These are…" introduces the application after each example (vv. 8, 10, 12, 16, 19). |
| ἀσεβής / ἀσέβεια / ἀσεβέω (ungodly, ungodliness, act ungodly) | 6 total | 4, 15 (×4), 18 | Jude's chief label for the intruders, concentrated in the Enoch quotation. |
| ἀγαπητός (beloved) | 3 | 3, 17, 20 | Marks the three direct addresses to the readers. |
| ἀγάπη (love / love feast) | 3 | 2, 12, 21 | Greeting, the community meal, and "the love of God." |
| ἔλεος / ἐλεάω (mercy / show mercy) | 2 + 2 | 2, 21; 22, 23 | Mercy frames the letter's pastoral close. |
| κρίσις / κρίμα (judgment) | 3 + 1 | 6, 9, 15; 4 | |
| ἅπαξ (once, once for all) | 2 | 3, 5 | "Once for all delivered"; "once knowing all things." |
| Ἰησοῦς | 7 | 1, 4, 5, 17, 21, 25 | Counts SBLGNT's reading in v. 5. |
| ζόφος (deep gloom) | 2 | 6, 13 | |
| σάρξ (flesh) | 3 | 7, 8, 23 | |
| βλασφημέω (slander) | 2 | 8, 10 | Plus βλασφημία in v. 9. |
| πορεύομαι (go, walk) | 3 | 11, 16, 18 | "Went in the way of Cain"; "walking according to their lusts." |

## Grammar data

- **Optatives:** Jude has two, πληθυνθείη (v. 2) and ἐπιτιμήσαι (v. 9). The SBLGNT New Testament has only **68** optative verb forms in all.
- **Perfect participles of God's action on the readers** (v. 1): ἠγαπημένοις, τετηρημένοις.
- **Main imperatives addressed to readers:** μνήσθητε (v. 17), τηρήσατε (v. 21), and in vv. 22–23 the present imperatives ἐλεᾶτε, σῴζετε, ἐλεᾶτε.

## Jude and 2 Peter: lexical overlap by verse (computed)

The overlap below counts content-word lemmas shared between a verse of Jude and the best-matching verse of 2 Peter. It confirms the familiar list of parallels: Jude 4 ~ 2 Pet 2:1–3; 6 ~ 2:4; 7 ~ 2:6; 8 ~ 2:10; 9 ~ 2:11; 10 ~ 2:12; 11 ~ 2:15; 12–13 ~ 2:13, 17; 16 ~ 2:18; 17–18 ~ 3:2–3. The detailed table is in Appendix C.

| Jude | Best 2 Peter match | Shared lemmas |
|---|---|---|
| 6 | 2:4 | ἄγγελος, κρίσις, τηρέω, ζόφος |
| 7 | 2:6 | Σόδομα, Γόμορρα, πόλις |
| 8 | 2:10 | σάρξ, κυριότης, δόξα, βλασφημέω |
| 10 | 2:12 | βλασφημέω, ἄλογος, ζῷον, φθείρω |
| 11 | 2:15 | ὁδός, Βαλαάμ, μισθός |
| 13 | 2:17 | ζόφος, σκότος, τηρέω |
| 16 | 2:18 | ὑπέρογκος, ἐπιθυμία |
| 17 | 3:2 | μιμνῄσκομαι, ῥῆμα, προλέγω, ἀπόστολος, κύριος |
| 18 | 3:3 | ἔσχατος, ἐμπαίκτης, ἐπιθυμία, πορεύομαι |

Notable *absences* in 2 Peter: the Enoch quotation (Jude 14–15), the named dispute over Moses' body (2 Pet 2:11 speaks only generally of angels), Cain and Korah (only Balaam is kept), and the "wandering stars" and "wild waves."

# Interpretive and Editorial Decisions

This file records each decision that shapes the manuscript, the reason for it, and any alternative the book presents fairly. When a chapter takes a position, it should agree with this file. Where a question is genuinely open, the book says so and gives the options, and this file records how the book frames it.

## A. Text, translations, and sources (revised for the second edition, November 2026)

**L0. Only free sources.** Every text quoted or reproduced is in the public domain or under CC0, CC BY, or CC BY-SA. Anything requiring permission is excluded and scrubbed, including copyrighted translations (ESV, NASB, NLT, NIV, NET, NKJV, CSB, NRSV, Amplified, *The Message*), the KJV (Crown patent in the UK; Webster's 1833 revision is used instead), and modern commentaries, lexicons, and grammars that are under copyright or could not be consulted directly. The book is CC BY-SA 4.0 (copyleft). *Reason:* the author's instruction that God's word, and a book that opens it, be fully free and open. See `project-brief.md` §1.

**L1. The manuscripts have priority.** Each chapter's section A prints the SBLGNT Greek first and then a table of readings in ten manuscripts (P72, P78, ℵ, A, B, C, K, L, Ψ, 1739) from the INTF NTVMR transcriptions (CC BY 4.0). `tools/make_texts.py` checks every manuscript claim against the cached transcriptions and stops if one fails. Old Testament passages are given in the Hebrew of the WLC.

**L2. No translation is more important than another.** Every verse of Jude is printed in eighteen free translations in order of first publication. Inline quotations name their translation and are checked by `tools/audit.py`. The LSV is quoted most often inline because its word-for-word style shows the structure of the Greek under discussion. This is a choice of convenience, not of authority, and it is stated in the Reader's Introduction and the Method chapter. Long passages are given in two public-domain translations (BSB and WEB), which between them follow the critical and the Byzantine Majority texts.

**L3. Every cited text is highlighted.** Every passage of Scripture, the Apocrypha, or 1 Enoch that a chapter cites by reference is printed in that chapter's section L: original language (WLC Hebrew/Aramaic, SBLGNT Greek, or the LXX), then BSB and WEB (Brenton for the Apocrypha; Charles for 1 Enoch). A passage of more than five verses already printed in full earlier is linked, not repeated. References that name a whole section of 1 Enoch (chs. 1–36, 6–16, 72–82) are noted, not printed. At build time, references in the text are linked to their section L entries.

**L4. Greek-first headings.** Section C headings give the SBLGNT phrase, a transliteration, and this book's own gloss in single quotation marks.

**L5. Quotations unaltered.** Every translation is quoted exactly, including its own square brackets; the commentary never inserts words inside another translation's quotation marks. The LSV's publisher requests that its English remain unaltered, and the book honors that for every translation.

**L6. "Messengers" in the LSV.** The LSV renders ἄγγελος as "messenger" (vv. 6, 9). The commentary explains this as a literal rendering and uses "angel" in its own prose, since the context identifies heavenly beings.

**L7. Glosses vs. quotations.** Typographic convention: curly double quotes “…” mark direct quotations, which the audit checks against sources. Single quotes ‘…’ mark glosses and translation equivalents.

**L8. Older commentaries are quoted directly.** Public-domain commentaries (Mayor, Plummer, Plumptre, Huther, the *Pulpit Commentary*, Benson, Calvin, Luther in Gillett's translation) are quoted from the text consulted. Facts that postdate them are cited to named Wikipedia articles (CC BY-SA).

## B. Contested historical and critical questions

**H1. Authorship.** The book presents three views: (1) Jude, brother of James and of Jesus, wrote it; (2) a later writer used Jude's name; (3) a secretary or associate wrote under Jude's direction. *Framing:* the evidence is compatible with authorship by Jude the brother of Jesus. Several standard arguments against it, such as the quality of the Greek and "the faith" as a late concept, are weaker than often claimed. The book presents traditional authorship as a responsible view without asserting it as proven, and it explains the arguments of scholars who date the letter later.

**H2. Date.** No firm date can be established. The book gives the plausible range, from the 50s to the 80s or 90s, notes the arguments for each, and avoids building interpretation on a precise date.

**H3. Recipients.** These are unknown. Internal evidence (an assumed familiarity with Jewish traditions, love feasts, and the apostles' teaching) suggests a community or communities of Jewish Christians, or a mixed community at home with Jewish scriptural interpretation. The book does not invent a location.

**H4. Jude and 2 Peter.** The majority view is that 2 Peter used Jude. The book presents the evidence, which is the computed overlap plus the omission of Enoch and of the Moses dispute in 2 Peter, along with the minority alternatives (Jude used 2 Peter, as Luther and later Spitta held, reported via Gillett's Luther and Mayor; or both used a common source). It does not make the interpretation of Jude depend on the answer.

**H5. The opponents.** Identifying them as second-century Gnostics is anachronistic. The book describes them from Jude's own charges: they are inside the community, they claim revelatory dreams (v. 8), they reject authority, they are sexually permissive, they are self-serving at the love feasts, they cause division, and Jude says they lack the Spirit. Any fuller reconstruction of who they were is labeled as reconstruction.

## C. Exegetical decisions (verse by verse)

**E1 (v. 1): ἠγαπημένοις vs. ἡγιασμένοις.** The text is "loved." The book explains the Byzantine "sanctified" reading (K, L; WBS, WEB, MSB). The dative Ἰησοῦ Χριστῷ τετηρημένοις is presented with both senses, "kept *for* Jesus Christ" (for his coming) and "kept *by/in* Jesus Christ." The book prefers "kept for" as the more natural sense of the plain dative, while noting that the LSV's "in" is defensible.

**E2 (v. 3): τῇ … πίστει** = the content of faith ("the faith"), not the act of believing. ἅπαξ = "once for all." The book distinguishes "fixed" from "frozen": completeness of the apostolic message does not exclude growth in understanding.

**E3 (v. 4): "written beforehand."** προγεγραμμένοι refers primarily to judgment written in earlier texts and prophecies, the examples Jude goes on to cite. It does not mean a decree of individual reprobation. The book notes the predestinarian readings in the history of interpretation.

**E4 (v. 4): "our only Master and Lord Jesus Christ."** Both titles refer to Jesus (one article governs both nouns). The book explains the added θεόν (Ψ, K, L; TR) and the two-person rendering of older English Bibles (WBS).

**E5 (v. 5): Ἰησοῦς.** The book adopts "Jesus," following A, B, 1739, SBLGNT, and NA28 (with DRA, LSV, and BSB among the translations), and explains (a) the evidence, including P72's θεὸς Χριστός and the κύριος of ℵ, C*, Ψ, K, and L, (b) its theological implication (the pre-existent Christ acting in the exodus, cf. 1 Cor 10:4, 9), and (c) why many translations still print "the Lord." The placement of ἅπαξ ("once" with "knowing" vs. "once" with "saved") is explained.

**E6 (v. 6): the angels.** These are the angels of the Watcher tradition (Gen 6:1–4 as read in 1 Enoch 6–16). The book presents this as the meaning Jude most likely intended, shown by the verbal parallels with 1 Enoch 10. It notes the alternative "pre-mundane fall of Satan" reading and the "sons of God = Sethites" reading found in later interpretation, and explains why they fit Jude's wording less well.

**E7 (v. 7): "in like manner to these … other flesh."** τούτοις refers back to the angels. The parallel lies in crossing the boundary between heavenly and human beings: the angels with women, and the men of Sodom pursuing the angel-visitors. The book says plainly that this reading does not reduce Sodom's sin to one thing. Ezekiel 16:49–50 and other texts name pride, excess, and neglect of the poor, and the book also notes the sexual violence at the center of Genesis 19. It treats the passage's use in modern debates about sexuality carefully, separating what Jude's phrase most likely meant from what it is often used to prove.

**E8 (v. 8): "dreaming."** These are claimed visionary revelations (cf. Deut 13:1–5, where the LXX uses ἐνυπνιαζόμενος of the false prophet), not merely moral fantasy.

**E9 (v. 8): κυριότης and δόξαι.** κυριότης is most likely the Lord's authority (or the Lord himself). δόξαι are glorious angelic beings. Both are presented with alternatives (human church leaders; evil angels).

**E10 (v. 9): κρίσιν … βλασφημίας.** Two readings are presented. (1) Michael did not presume to pronounce a slanderous or abusive judgment on the devil. (2) In a reconstructed setting of the story, Michael did not presume to condemn the devil *for slander* against Moses, and left judgment to God; this is labeled as reconstruction. In either reading the point stands: even the archangel deferred to God's authority.

**E11 (v. 11): the three figures** are read both as types of sin (Cain: hatred, envy, murder, and in Jewish tradition cynicism about judgment; Balaam: greed and leading others into immorality; Korah: rebellion against God-given authority) and as the three stages of a progression marked by the three verbs.

**E12 (v. 12): σπιλάδες.** The primary sense is "hidden reefs," following classical usage, Abbott-Smith, and most modern versions (BSB). "Stains/spots" (the LSV, WBS, and the σπίλοι of 2 Pet 2:13) is a genuine possibility in later Greek. The book treats both, and explains why the reef image fits the shipwreck danger of the love feast.

**E13 (v. 12): ἀγάπαι = love feasts.** These were the community's shared meals, probably including or closely connected with the Lord's Supper in Jude's time. The book distinguishes first-century evidence (1 Cor 11; Jude; 2 Pet 2:13 v.l.) from later evidence (Ignatius, Pliny, Tertullian, Clement of Alexandria) and from later separation of Eucharist and agape.

**E14 (vv. 12–13): the four nature images.** Clouds, trees, sea, and stars correspond to the four regions of the natural world. The book presents the suggestion that they reflect 1 Enoch 2–5 and 80:2–8 (nature's obedience and its disorder in the days of sinners) as a probable background, verified from Charles's text; Mayor (EGT) already connects the wandering stars with 1 Enoch 80.

**E15 (v. 13): "wandering stars."** In ancient terms these are the planets and/or heavenly bodies that leave their courses. The background is 1 Enoch 18:13–16 and 21:1–6 (stars bound for transgressing). The book explicitly avoids importing modern astronomy and avoids "shooting stars/meteors" as *the* meaning while noting it as a proposal.

**E16 (vv. 14–15): Jude's use of 1 Enoch.** The book presents the range of views: (a) Jude regarded 1 Enoch as canonical Scripture (unlikely, since he uses no citation formula of Scripture, but possible); (b) Jude regarded this particular prophecy as genuinely from Enoch; (c) Jude used a respected text his readers valued without endorsing the whole book, as Paul quotes Aratus in Acts 17:28. The book shows how the early church argued about this (Tertullian, Jerome, Augustine) and leaves readers able to weigh the options. It states that quoting a book does not make that book canonical, and that inclusion in Jude does not imply that everything in 1 Enoch is endorsed.

**E17 (v. 19): ἀποδιορίζοντες** = "those who make divisions" or "make distinctions" (possibly spiritual ranking). ψυχικοί = "natural," and the book notes the possibility that Jude turns the opponents' own vocabulary against them (cf. 1 Cor 2:14–15).

**E18 (vv. 22–23): text and meaning.** The book follows the three-clause text (SBLGNT, NA28, LSV) and presents the two-clause forms (P72; B and WH; C; K, L and the Byzantine text) in Appendix A, from the verified manuscript transcriptions. "Doubting" (διακρινομένους) is read as "wavering," with "disputing" as the alternative. The fire imagery draws on Zech 3:2–4 (a brand snatched from the fire; filthy garments), verified in LXX and LSV.

**E19 (v. 25): verbless doxology.** In the Greek, "glory … be" or "glory … is" must be supplied. The LSV's "[is]" is one legitimate choice and "be" (wish) is another. The book notes that 1 Pet 4:11 supplies ἐστιν.

## D. Style and presentation

**S1.** Each chapter follows the A–L pattern (L added in the second edition). Within that pattern the prose flows as a guided discovery, and deep dives are set apart under "Deep dive" headings.

**S2.** Footnote IDs are chapter-prefixed (`[^c3-4]`) so that they stay unique in the assembled manuscript.

**S3.** Application sections are marked "Contemporary Understanding." They use conditional language ("may," "invites") and avoid claims about divine intention beyond what the text states.

**S4.** Numbers: verses are cited as "v. 12" within Jude and "Jude 12" across books. The book uses "Jude" for the letter and author, and the LSV's "Judas" only inside quotations.

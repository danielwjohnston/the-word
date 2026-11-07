#!/usr/bin/env python3
"""Generate Appendix C (Jude and 2 Peter parallels): the SBL Greek text of both letters first, then two
public-domain English translations (BSB and WEB), all drawn directly from the cached source files."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sources import greek_nt, english
def fmt(pairs, ch=None):
    return ' '.join(f'**{ch}:{v}** {t}' if ch else f'**{v}** {t}' for v, t in pairs)
def jt(a, b, src):
    return fmt(greek_nt(('JUD', 1, a, b)) if src == 'GRC' else english(src, ('JUD', 1, a, b)))
def pt(refs, src):
    out = []
    for ch, a, b in refs:
        out.append(fmt(greek_nt(('2PE', ch, a, b)) if src == 'GRC' else english(src, ('2PE', ch, a, b)), ch))
    return ' … '.join(out)
rows = [
 ((2,2), [(1,2,2)], 'Same wish formula, πληθυνθείη ("may it be multiplied"). Jude\'s triad (mercy, peace, love) differs from 2 Peter\'s pair (grace, peace).'),
 ((4,4), [(2,1,3)], 'Intruders: Jude\'s παρεισέδυσαν ("they slipped in") and 2 Peter\'s παρεισάξουσιν ("they will secretly bring in"). Both deny the Master (δεσπότης). Jude speaks of the past, 2 Peter of the future.'),
 ((5,5), [(1,12,12)], 'Both remind readers of what they already know.'),
 ((6,6), [(2,4,4)], 'Sinning angels kept (τετήρηκεν; τηρουμένους) in gloom (ζόφος) for judgment. 2 Peter adds ταρταρώσας, "casting into Tartarus."'),
 ((7,7), [(2,6,8)], 'Sodom and Gomorrah as example. 2 Peter adds the rescue of Lot and inserts the flood (2:5) to make a biblical sequence.'),
 ((8,8), [(2,10,10)], 'Defiling the flesh, despising lordship (κυριότης), slandering the "glorious ones" (δόξαι).'),
 ((9,9), [(2,11,11)], 'Angels do not bring a slanderous judgment. 2 Peter omits Michael, the Devil, and Moses.'),
 ((10,10), [(2,12,12)], 'Slandering what they do not know; irrational beasts; destruction.'),
 ((11,11), [(2,15,16)], 'Balaam and his reward. 2 Peter omits Cain and Korah and adds the donkey.'),
 ((12,12), [(2,13,13),(2,17,17)], 'Both use συνευωχούμενοι ("feasting together"), found in the NT only in these two passages. Jude\'s σπιλάδες ("reefs" or "stains") stands against 2 Peter\'s σπίλοι καὶ μῶμοι ("spots and blemishes"), and Jude\'s ἀγάπαις ("love feasts") against ἀπάταις ("deceptions") in the critical text of 2 Peter, words that differ by two letters. Jude\'s waterless clouds become in 2 Peter "springs without water and mists driven by a storm."'),
 ((13,13), [(2,17,17)], 'The phrase ὁ ζόφος τοῦ σκότους … τετήρηται ("the gloom of darkness has been kept") is applied in 2 Peter to the springs and mists.'),
 ((16,16), [(2,18,18)], 'ὑπέρογκα, "swollen" or "inflated" words, found in the NT only in these two passages.'),
 ((17,18), [(3,1,3)], 'Remembering the apostles\' words; scoffers in the last time/days following their own desires (ἐμπαῖκται; only here in the NT). 2 Peter adds the prophets and specifies mockery of the promise of Christ\'s coming.'),
 ((24,25), [(3,17,18)], 'Both close with a warning against falling and a doxology. 2 Peter\'s doxology is addressed to Christ.'),
]
L = []
L.append('# Appendix C. Jude and 2 Peter: The Parallel Passages {.unnumbered}\n')
L.append('This appendix sets the parallel passages side by side, first in the Greek of the SBL Greek New Testament and then in two public-domain English translations, the Berean Standard Bible (BSB) and the World English Bible (WEB). The texts are generated directly from the source files by `tools/make_parallels.py`, so they are exact. Each verse of Jude is also given in eighteen free translations in section A of its chapter. For discussion of the relationship between the two letters, see the Historical and Literary Introduction, §8.\n')
L.append('**Summary of the evidence.** The two letters share a sequence of themes, images, and rare words. Three Greek words occur in the New Testament only in these two letters: συνευωχέομαι ("feast together"), ὑπέρογκος ("swollen"), and ἐμπαίκτης ("scoffer").[^ac-1] Jude contains material not found in 2 Peter: the quotation of Enoch (vv. 14–15), the named dispute of Michael and the Devil over Moses\' body (v. 9), Cain and Korah (v. 11), the wild waves and wandering stars (v. 13), and the closing exhortations to mercy (vv. 20–23). 2 Peter adds the flood and Noah (2:5), Lot (2:7–8), Balaam\'s donkey (2:16), and the scoffers\' question about Christ\'s coming (3:4).\n')
for (a,b), prefs, note in rows:
    jref = f'Jude {a}' if a == b else f'Jude {a}–{b}'
    prefs_s = '; '.join(f'2 Pet {c}:{x}' + (f'–{y}' if y != x else '') for c,x,y in prefs)
    L.append(f'## {jref} ∥ {prefs_s}\n')
    L.append(f'> {jt(a,b,"GRC")}\n>\n> — {jref}, SBLGNT\n')
    L.append(f'> {pt(prefs,"GRC")}\n>\n> — {prefs_s}, SBLGNT\n')
    for tr in ('BSB', 'WEB'):
        L.append(f'*{tr}.* Jude: {jt(a,b,tr)}  \n2 Peter: {pt(prefs,tr)}\n')
    L.append(f'*Observation:* {note}\n')
L.append('## Material in Jude without a parallel in 2 Peter\n')
L.append('- The greeting\'s description of believers as called, loved, and kept (v. 1).\n- The exodus example, with the reading Ἰησοῦς, "Jesus," in the critical text (v. 5).\n- The story of Michael and the Devil over Moses\' body (v. 9).\n- Cain and Korah (v. 11).\n- Wild waves of the sea and wandering stars (v. 13).\n- The quotation from 1 Enoch (vv. 14–15).\n- "Grumblers" and flattery (v. 16).\n- Those who cause divisions, not having the Spirit (v. 19).\n- Building, praying in the Holy Spirit, keeping in God\'s love (vv. 20–21).\n- Mercy for the doubting and rescue from the fire (vv. 22–23).\n')
L.append('[^ac-1]: Computed from MorphGNT/SBLGNT lemmas; see `research/data-notes.md`.\n')
open(os.path.join(ROOT, 'appendices', 'C-jude-and-2-peter.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('written')

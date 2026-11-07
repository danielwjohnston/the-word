#!/usr/bin/env python3
"""Generate Appendix C (Jude and 2 Peter parallels) with exact LSV text drawn from the cached LSV USFM."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from usfm2txt import book
Z = os.path.join(ROOT, '.cache', 'englsv_usfm.zip')
J = book(Z, 'JUD'); P = book(Z, '2PE')
def jt(a, b): return ' '.join(f'**{v}** ' + J[(1, str(v))] for v in range(a, b + 1))
def pt(refs):
    out = []
    for ch, a, b in refs:
        out.append(' '.join(f'**{ch}:{v}** ' + P[(ch, str(v))] for v in range(a, b + 1)))
    return ' … '.join(out)
rows = [
 ((2,2), [(1,2,2)], 'Same wish formula ("be multiplied"); Jude\'s triad differs.'),
 ((4,4), [(2,1,3)], 'Intruders "came in … stealthily" / "will stealthily bring in"; both deny the Master (δεσπότης). Jude: past tense; 2 Peter: future.'),
 ((5,5), [(1,12,12)], 'Both remind readers of what they already know.'),
 ((6,6), [(2,4,4)], 'Sinning angels kept in gloom for judgment. 2 Peter adds "Tartarus."'),
 ((7,7), [(2,6,8)], 'Sodom and Gomorrah as example. 2 Peter adds the rescue of Lot and inserts the flood (2:5) to make a biblical sequence.'),
 ((8,8), [(2,10,10)], 'Defiling the flesh, despising lordship, slandering "glorious ones."'),
 ((9,9), [(2,11,11)], 'Angels do not bring a slanderous judgment. 2 Peter omits Michael, the Devil, and Moses.'),
 ((10,10), [(2,12,12)], 'Slandering what they do not know; irrational beasts; destruction.'),
 ((11,11), [(2,15,16)], 'Balaam and his reward. 2 Peter omits Cain and Korah and adds the donkey.'),
 ((12,12), [(2,13,13),(2,17,17)], '"Feasting together" (only here in the NT); "stains/reefs" vs. "spots and blemishes"; "love-feasts" vs. "deceits" (a one-letter difference in Greek); waterless clouds vs. "wells without water, and clouds driven by a storm."'),
 ((13,13), [(2,17,17)], '"The gloom of the darkness … has been kept" applied in 2 Peter to the wells and mists.'),
 ((16,16), [(2,18,18)], '"Swollen words" (ὑπέρογκα; only here in the NT).'),
 ((17,18), [(3,1,3)], 'Remembering the apostles\' words; scoffers in the last time/days following their own desires (ἐμπαῖκται; only here in the NT). 2 Peter adds the prophets and specifies mockery of the promise of Christ\'s coming.'),
 ((24,25), [(3,17,18)], 'Both close with a warning against falling and a doxology. 2 Peter\'s doxology is addressed to Christ.'),
]
L = []
L.append('# Appendix C. Jude and 2 Peter: The Parallel Passages {.unnumbered}\n')
L.append('This appendix sets the parallel passages side by side in the Literal Standard Version. The texts are generated directly from the LSV source files by `tools/make_parallels.py`, so they are exact. For discussion of the relationship between the two letters, see the Historical and Literary Introduction, §8.\n')
L.append('**Summary of the evidence.** The two letters share a sequence of themes, images, and rare words. Three Greek words occur in the New Testament only in these two letters: συνευωχέομαι ("feast together"), ὑπέρογκος ("swollen"), and ἐμπαίκτης ("scoffer").[^ac-1] Jude contains material not found in 2 Peter: the quotation of Enoch (vv. 14–15), the named dispute of Michael and the Devil over Moses\' body (v. 9), Cain and Korah (v. 11), the wild waves and wandering stars (v. 13), and the closing exhortations to mercy (vv. 20–23). 2 Peter adds the flood and Noah (2:5), Lot (2:7–8), Balaam\'s donkey (2:16), and the scoffers\' question about Christ\'s coming (3:4).\n')
for (a,b), prefs, note in rows:
    jref = f'Jude {a}' if a == b else f'Jude {a}–{b}'
    prefs_s = '; '.join(f'2 Pet {c}:{x}' + (f'–{y}' if y != x else '') for c,x,y in prefs)
    L.append(f'## {jref} ∥ {prefs_s}\n')
    L.append(f'> {jt(a,b)}\n>\n> — {jref}, LSV\n')
    L.append(f'> {pt(prefs)}\n>\n> — {prefs_s}, LSV\n')
    L.append(f'*Observation:* {note}\n')
L.append('## Material in Jude without a parallel in 2 Peter\n')
L.append('- The greeting\'s description of believers as called, loved, and kept (v. 1).\n- The exodus example, with the reading "Jesus" (v. 5).\n- The story of Michael and the Devil over Moses\' body (v. 9).\n- Cain and Korah (v. 11).\n- "Wild waves of a sea" and "stars going astray" (v. 13).\n- The quotation from 1 Enoch (vv. 14–15).\n- "Grumblers" and flattery (v. 16).\n- "Causing divisions … not having the Spirit" (v. 19).\n- Building, praying in the Holy Spirit, keeping in God\'s love (vv. 20–21).\n- Mercy for the doubting and rescue from the fire (vv. 22–23).\n')
L.append('[^ac-1]: Computed from MorphGNT/SBLGNT lemmas; see `research/data-notes.md`.\n')
open(os.path.join(ROOT, 'appendices', 'C-jude-and-2-peter.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('written')

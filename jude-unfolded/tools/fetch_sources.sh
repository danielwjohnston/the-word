#!/usr/bin/env bash
# Download the openly licensed source texts used by the generators and audits into
# jude-unfolded/.cache (git-ignored). Every source is public domain or CC-licensed.
# Re-run to fill in anything missing.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
cache="$here/.cache"; mkdir -p "$cache/morphgnt" "$cache/wlc" "$cache/enoch"
ua="jude-unfolded-research-script"

# eBible.org USFM: the 18 free English translations, Brenton (Greek and English), Greek NT editions
for id in engtnt enggnv engDRA engwebster engnoy eng-rv engDBY engylt eng-asv engwebp eng-t4t engoebus \
          engULB engfbv englsv engbsb engmsb engtcent eng-Brenton grcbrent grctr grcmt grcsbl grctcgnt; do
  [ -s "$cache/${id}_usfm.zip" ] || curl -sSfL -A "$ua" -o "$cache/${id}_usfm.zip" "https://ebible.org/Scriptures/${id}_usfm.zip"
done

# SBLGNT text and morphology (MorphGNT, CC BY-SA 3.0)
for f in 61-Mt 62-Mk 63-Lk 64-Jn 65-Ac 66-Ro 67-1Co 68-2Co 69-Ga 70-Eph 71-Php 72-Col 73-1Th 74-2Th 75-1Ti 76-2Ti 77-Tit 78-Phm 79-Heb 80-Jas 81-1Pe 82-2Pe 83-1Jn 84-2Jn 85-3Jn 86-Jud 87-Re; do
  [ -s "$cache/morphgnt/$f.txt" ] || curl -sSfL -A "$ua" -o "$cache/morphgnt/$f.txt" "https://raw.githubusercontent.com/morphgnt/sblgnt/master/$f-morphgnt.txt"
done

# Westminster Leningrad Codex (public domain) via the Open Scriptures Hebrew Bible
for b in Gen Exod Lev Num Deut Josh Judg 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Neh Job Ps Prov Isa Jer Lam Ezek Dan Hos Joel Amos Mic Hab Zech Mal; do
  [ -s "$cache/wlc/$b.xml" ] || curl -sSfL -A "$ua" -o "$cache/wlc/$b.xml" "https://raw.githubusercontent.com/openscriptures/morphhb/master/wlc/$b.xml"
done

# Abbott-Smith lexicon (public domain)
[ -s "$cache/abbott-smith.tei.xml" ] || curl -sSfL -A "$ua" -o "$cache/abbott-smith.tei.xml" "https://raw.githubusercontent.com/translatable-exegetical-tools/Abbott-Smith/master/abbott-smith.tei.xml"

# Manuscript transcriptions (INTF NTVMR, CC BY 4.0)
python3 -I "$here/tools/fetch_ntvmr.py"

# 1 Enoch (Charles 1917, public domain): tools/make_texts.py fetches any chapter it needs from
# Wikisource into .cache/enoch/ on first use.
echo "Sources cached in $cache"

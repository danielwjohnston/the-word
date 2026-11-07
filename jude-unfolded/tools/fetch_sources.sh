#!/usr/bin/env bash
# Download the openly licensed source texts used by the audit and analysis tools
# into jude-unfolded/.cache (git-ignored). Re-run to refresh.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
cache="$here/.cache"; mkdir -p "$cache/morphgnt"
for id in englsv engwebp eng-asv engbsb eng-kjv2006 grctr grcmt grcsbl grctcgnt grcbrent eng-Brenton; do
  [ -s "$cache/${id}_usfm.zip" ] || curl -sSfL -o "$cache/${id}_usfm.zip" "https://ebible.org/Scriptures/${id}_usfm.zip"
done
for f in 61-Mt 62-Mk 63-Lk 64-Jn 65-Ac 66-Ro 67-1Co 68-2Co 69-Ga 70-Eph 71-Php 72-Col 73-1Th 74-2Th 75-1Ti 76-2Ti 77-Tit 78-Phm 79-Heb 80-Jas 81-1Pe 82-2Pe 83-1Jn 84-2Jn 85-3Jn 86-Jud 87-Re; do
  [ -s "$cache/morphgnt/$f.txt" ] || curl -sSfL -o "$cache/morphgnt/$f.txt" "https://raw.githubusercontent.com/morphgnt/sblgnt/master/$f-morphgnt.txt"
done
[ -s "$cache/abbott-smith.tei.xml" ] || curl -sSfL -o "$cache/abbott-smith.tei.xml" "https://raw.githubusercontent.com/translatable-exegetical-tools/Abbott-Smith/master/abbott-smith.tei.xml"
echo "Sources cached in $cache"

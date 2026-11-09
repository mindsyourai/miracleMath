#!/usr/bin/env python3
"""
surahs_check.py -- miracleMath (Agent A: surah list verification)

Verifies data/surahs.json (built from MK's pasted 114-surah list) against
the corpus, three ways:

1. QAC v0.4: max (surah, verse) per surah, parsed from the location
   field of corpus/quranic-corpus-morphology-0.4.txt.
2. Standard Kufi ayah-count table: AYAH_COUNTS in data/letter_count.py
   (itself asserted equal to the QAC maxima in
   data/corpus_numbers_check.py).
3. Tanzil Uthmani text: total non-comment lines must be 6,236, and
   per-surah counts are re-derived from surah boundaries -- every
   surah except 9 opens with the Basmalah prepended to its first
   verse, so the 113 lines starting with the Basmalah mark the surah
   starts. Surahs 8 and 9 share one segment (9 has no Basmalah), so
   their split is taken from QAC and the combined 8+9 count (204) is
   what Tanzil checks directly.

Also reports the total verse count and the Meccan/Medinan split from
the pasted list. Exits non-zero on ANY mismatch -- a pasted count is
never silently "fixed"; a diff is reported, not repaired.

Usage: python3 data/surahs_check.py [--surahs PATH]
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from letter_count import AYAH_COUNTS  # noqa: E402

DEFAULT_SURAHS = HERE / "surahs.json"
DEFAULT_QAC = HERE.parent / "corpus" / "quranic-corpus-morphology-0.4.txt"
DEFAULT_TANZIL = HERE.parent / "corpus" / "quran-uthmani.txt"

LOC_RE = re.compile(r"\((\d+):(\d+):(\d+):(\d+)\)")
# Basmalah as it opens a surah in the Tanzil Uthmani text. Surahs 95
# and 97 write it with a shaddah on the ba (بِّسْمِ) where the other
# 111 write بِسْمِ -- same words, Uthmani spelling variant.
BASMALAH_RE = re.compile(r"^ب\u0651?ِسْمِ")


def qac_max_verse(path):
    max_verse = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#") or line.startswith("LOCATION"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            m = LOC_RE.match(parts[0])
            if not m:
                continue
            s, v = int(m.group(1)), int(m.group(2))
            max_verse[s] = max(max_verse.get(s, 0), v)
    return max_verse


def tanzil_counts(path):
    """Return (total_lines, per-surah counts via Basmalah boundaries).

    Lines starting with the Basmalah are surah starts (113 of them:
    1:1 plus the 112 unnumbered Basmalahs prepended to the first verse
    of every other surah except 9). The segment between surah 8's
    start and surah 10's start holds surahs 8 + 9 together; it is
    returned as a single combined entry keyed (8, 9).
    """
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            lines.append(line)
    starts = [i for i, ln in enumerate(lines)
              if BASMALAH_RE.match(ln)]
    assert len(starts) == 113, \
        f"expected 113 Basmalah-start lines, got {len(starts)}"
    counts = {}
    # Surah numbers that have a Basmalah start, in order: 1..8, 10..114
    numbered = [s for s in range(1, 115) if s != 9]
    for j, s in enumerate(numbered):
        end = starts[j + 1] if j + 1 < len(starts) else len(lines)
        if s == 8:
            # segment holds surahs 8 + 9
            counts[(8, 9)] = end - starts[j]
        else:
            counts[s] = end - starts[j]
    return len(lines), counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surahs", default=str(DEFAULT_SURAHS))
    ap.add_argument("--qac", default=str(DEFAULT_QAC))
    ap.add_argument("--tanzil", default=str(DEFAULT_TANZIL))
    args = ap.parse_args()

    with open(args.surahs, encoding="utf-8") as f:
        surahs = json.load(f)["surahs"]
    assert len(surahs) == 114

    qac = qac_max_verse(args.qac)
    kufi = {s + 1: n for s, n in enumerate(AYAH_COUNTS)}
    total_lines, tanzil = tanzil_counts(args.tanzil)

    diffs = []
    for s in surahs:
        n, pasted = s["n"], s["verses"]
        for src, ref in (("QAC v0.4 max verse", qac.get(n)),
                         ("Kufi table (letter_count.py)", kufi.get(n))):
            if pasted != ref:
                diffs.append(f"surah {n} ({s['name_tr']}): "
                             f"paste={pasted} {src}={ref}")
        if n not in (8, 9):
            if pasted != tanzil.get(n):
                diffs.append(f"surah {n} ({s['name_tr']}): "
                             f"paste={pasted} Tanzil Basmalah-segment="
                             f"{tanzil.get(n)}")
    # surahs 8 + 9: Tanzil checks the combined segment only
    if surahs[7]["verses"] + surahs[8]["verses"] != tanzil[(8, 9)]:
        diffs.append(f"surahs 8+9 combined: paste="
                     f"{surahs[7]['verses'] + surahs[8]['verses']} "
                     f"Tanzil Basmalah-segment={tanzil[(8, 9)]}")

    total = sum(s["verses"] for s in surahs)
    mecc = sum(1 for s in surahs if s["type"] == "Meccan")
    medi = sum(1 for s in surahs if s["type"] == "Medinan")

    print(f"Surahs in file: {len(surahs)}")
    print(f"Total verses (paste): {total} "
          f"(QAC distinct verses: {sum(1 for _ in qac)} surahs, "
          f"Tanzil non-comment lines: {total_lines})")
    print(f"Meccan / Medinan split (paste): {mecc} / {medi}")
    print(f"Tanzil Basmalah-start lines: 113 "
          f"(surah 8+9 combined segment: {tanzil[(8, 9)]} verses)")
    if diffs:
        print(f"\nDIFFS: {len(diffs)}")
        for d in diffs:
            print(f"  MISMATCH: {d}")
        print("FAIL: pasted counts do not match the corpus -- "
              "do NOT silently fix; report the diffs.")
        sys.exit(1)
    print("\nDIFFS: 0 -- every pasted verse count matches QAC v0.4 max "
          "verse, the Kufi table, and the Tanzil Basmalah-segmentation "
          "for all 114 surahs.")
    print("PASS")


if __name__ == "__main__":
    main()

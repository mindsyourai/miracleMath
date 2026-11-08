#!/usr/bin/env python3
"""Corrected alignment probes for Checker B (v2)."""
import re
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from methods_check_B import (parse_qac, load_tanzil, skeleton,
                             strip_prefixes, is_rahim, SURAH_VERSES,
                             QAC, TANZIL)

words, n_seg, seg_roots, seg_lems = parse_qac(QAC)
verses, bounds = load_tanzil(TANZIL)
# line index -> (surah, ayah); correct mapping
vmap = {}
idx = 0
for s, n in enumerate(SURAH_VERSES, start=1):
    for a in range(1, n + 1):
        vmap[idx] = (s, a)
        idx += 1
inv_vmap = {v: k for k, v in vmap.items()}


def tanzil_token(s, v, w):
    li = inv_vmap.get((s, v))
    toks = verses[li].split()
    ti = (w - 1 + 4) if (v == 1 and s > 1 and s != 9) else (w - 1)
    return toks[ti] if 0 <= ti < len(toks) else None


# --- 1. Rahim token-level diff (fixed alignment) ---
print("=== RAHIM TOKEN DIFF (fixed) ===")
bad = []
for loc in sorted(loc for loc, rec in words.items()
                  if "r~aHiym" in rec["lems"]):
    tok = tanzil_token(*loc)
    if not (tok and is_rahim(skeleton(tok))):
        bad.append((loc, tok, words[loc]["stem_forms"]))
print("QAC rahim words whose Tanzil token is NOT a rahim form:", len(bad))
for b in bad:
    print("  ", b)
# reverse: Tanzil rahim tokens (excl unnumbered basmalahs) with no QAC rahim
qac_rahim_locs = {(s, v, w) for (s, v, w), rec in words.items()
                  if "r~aHiym" in rec["lems"]}
missing = []
for (s, v), li in sorted(inv_vmap.items()):
    toks = verses[li].split()
    start = 4 if (v == 1 and s > 1 and s != 9) else 0
    for i, t in enumerate(toks[start:], start=start + 1):
        # QAC word number = token index adjusted for basmalah
        w = i - 4 if (v == 1 and s > 1 and s != 9) else i
        if is_rahim(skeleton(t)) and (s, v, w) not in qac_rahim_locs:
            missing.append(((s, v, w), t))
print("Tanzil rahim tokens (excl basmalahs) with no QAC rahim word:",
      len(missing), missing[:5])

# --- 2. min: Tanzil 3314 vs QAC min 3226. How many are QAC man? ---
print("\n=== MIN 88 (fixed) ===")
man_as_min = []
min_as_min = []
for loc, rec in sorted(words.items()):
    tok = tanzil_token(*loc)
    if tok and strip_prefixes(skeleton(tok)) == "من":
        if rec["stem_lem"] == "man":
            man_as_min.append((loc, tok))
        elif rec["stem_lem"] == "min":
            min_as_min.append((loc, tok))
        else:
            print("  other lemma for min-token:", loc, rec["stem_lem"], tok)
print("Tanzil min-tokens that are QAC LEM man (relative pronoun):",
      len(man_as_min), man_as_min[:5])
print("Tanzil min-tokens that are QAC LEM min:", len(min_as_min))
# what about QAC min words whose Tanzil token is NOT a bare min token?
min_other = []
for loc, rec in sorted(words.items()):
    if rec["stem_lem"] == "min":
        tok = tanzil_token(*loc)
        if not (tok and strip_prefixes(skeleton(tok)) == "من"):
            min_other.append((loc, tok))
print("QAC min words whose Tanzil token is not a bare min token:",
      len(min_other), min_other[:10])

# --- 3. Quran: QAC lemma quro'aAn = 70 vs Tanzil substring 71 ---
print("\n=== QURAN 70 vs 71 ===")
q_locs = sorted(loc for loc, rec in words.items()
                if rec["stem_lem"] == "quro'aAn")
print("QAC quro'aAn words:", len(q_locs))
for loc in q_locs:
    tok = tanzil_token(*loc)
    if not (tok and "قران" in skeleton(tok)):
        print("  quro'aAn word, odd Tanzil token:", loc, repr(tok))
# Tanzil quran-substring tokens with no QAC quro'aAn word
qset = set(q_locs)
for (s, v), li in sorted(inv_vmap.items()):
    toks = verses[li].split()
    start = 4 if (v == 1 and s > 1 and s != 9) else 0
    for i, t in enumerate(toks[start:], start=start + 1):
        w = i - 4 if (v == 1 and s > 1 and s != 9) else i
        if "قران" in skeleton(t) and (s, v, w) not in qset:
            print("  Tanzil quran token, not QAC quro'aAn:",
                  (s, v, w), repr(t),
                  "QAC stem lem:", words.get((s, v, w), {}).get("stem_lem"))
# verse lists for the enriched file
quran_verses = sorted({(s, v) for (s, v, _w) in q_locs})
print("quro'aAn verses:", len(quran_verses))
per = Counter(s for (s, _v) in quran_verses)
print("per-surah:", {str(s): per[s] for s in sorted(per)})
print("verse list:", [f"{s}:{v}" for (s, v) in quran_verses])

# --- 4. root wAd: the one root the abdulbaqi pipeline misses ---
print("\n=== ROOT wAd ===")
for loc, rec in sorted(words.items()):
    if "wAd" in rec["roots"]:
        print("  ", loc, rec["stem_forms"], sorted(rec["lems"]),
              "tanzil:", repr(tanzil_token(*loc)))
print("word-level root-bearing words:",
      sum(1 for rec in words.values() if rec["roots"]))

# --- 5. ism: QAC {som} = 39 breakdown by Tanzil token ---
print("\n=== ISM 39 ===")
br = Counter()
for loc, rec in sorted(words.items()):
    if rec["stem_lem"] == "{som":
        tok = tanzil_token(*loc)
        br[skeleton(tok) if tok else None] += 1
print(dict(br))

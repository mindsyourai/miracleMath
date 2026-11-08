#!/usr/bin/env python3
"""Follow-up probes for Checker B (run after methods_check_B.py)."""
import json, re
from collections import Counter
from pathlib import Path
import subprocess, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from methods_check_B import (parse_qac, load_tanzil, skeleton,
                             strip_prefixes, is_rahim, is_rahman,
                             SURAH_VERSES, QAC, TANZIL, BASE)

words, n_seg, seg_roots, seg_lems = parse_qac(QAC)
verses, bounds = load_tanzil(TANZIL)
inv = {}
for li, (n, a, b) in enumerate(bounds):
    for vi in range(1, SURAH_VERSES[n - 1] + 1):
        inv[(n, vi)] = li


def tanzil_token(s, v, w):
    li = inv.get((s, v))
    toks = verses[li].split()
    ti = (w - 1 + 4) if (v == 1 and s > 1 and s != 9) else (w - 1)
    return toks[ti] if 0 <= ti < len(toks) else None


# --- 1. Rahim: QAC 116 vs Tanzil 115. Find the differing word(s). ---
print("=== RAHIM DIFF ===")
for loc in sorted(loc for loc, rec in words.items()
                  if "r~aHiym" in rec["lems"]):
    tok = tanzil_token(*loc)
    sk = skeleton(tok) if tok else None
    if not (tok and is_rahim(sk)):
        print("QAC rahim word with non-matching Tanzil token:", loc,
              repr(tok), "stem_forms:", words[loc]["stem_forms"],
              "lems:", sorted(words[loc]["lems"]))
# reverse: Tanzil rahim tokens with no QAC rahim word at that spot
tanzil_rahim = Counter()
for n, a, b in bounds:
    for vi, ln in enumerate(verses[a:b], start=1):
        for t in skeleton(ln).split():
            if is_rahim(t):
                tanzil_rahim[(n, vi)] += 1
qac_rahim = Counter()
for loc, rec in words.items():
    if "r~aHiym" in rec["lems"]:
        qac_rahim[(loc[0], loc[1])] += 1
for ref in sorted(set(tanzil_rahim) | set(qac_rahim)):
    if tanzil_rahim[ref] != qac_rahim[ref]:
        print("verse mismatch:", ref, "tanzil:", tanzil_rahim[ref],
              "qac:", qac_rahim[ref])
print("tanzil rahim total (incl basmalahs):", sum(tanzil_rahim.values()))
print("qac rahim total:", sum(qac_rahim.values()))

# --- 2. min: which of the 3314 Tanzil 'min' tokens are QAC LEM man? ---
print("\n=== MIN 88 ===")
man_locs = {(loc) for loc, rec in words.items()
            if rec["stem_lem"] == "man"}
n_man_as_min_token = 0
examples = []
for loc in sorted(man_locs):
    tok = tanzil_token(*loc)
    if tok and strip_prefixes(skeleton(tok)) == "من":
        n_man_as_min_token += 1
        if len(examples) < 8:
            examples.append((loc, tok))
print("QAC LEM man words whose Tanzil token skeletons to a 'min' token:",
      n_man_as_min_token)
print("examples:", examples)
min_qac = sum(1 for rec in words.values() if rec["stem_lem"] == "min")
print("QAC stem-LEM min:", min_qac)

# --- 3. Quran LEM: what is the actual lemma? ---
print("\n=== QURAN LEM ===")
qr = Counter()
for rec in words.values():
    if "qrA" in rec["roots"]:
        qr[rec["stem_lem"]] += 1
print("root qrA stem-lemma breakdown:", dict(qr))
print("root qrA word count:",
      sum(1 for rec in words.values() if "qrA" in rec["roots"]))

# --- 4. Abdulbaqi pipeline, exactly as in his post ---
print("\n=== ABDULBAQI PIPELINE ===")
qac_text = open(QAC, encoding="utf-8").read().splitlines()
data_lines = [ln for ln in qac_text
              if ln and not ln.startswith("#")
              and not ln.startswith("LOCATION")]
print("data lines:", len(data_lines))
roots_pipe = []
for ln in data_lines:
    parts = ln.replace("\t", ",").split(",")
    if len(parts) >= 4:
        feats = parts[3]
        roots_pipe += re.findall(r"ROOT:[^|]*", feats)
vals = [r.split(":", 1)[1] for r in roots_pipe]
print("segment ROOT occurrences:", len(vals),
      "unique:", len(set(vals)))
print("top:", Counter(vals).most_common(5))
mine = {r for rec in words.values() for r in rec["roots"]}
print("roots in pipe but not in my word-level parse:",
      sorted(set(vals) - mine))
print("roots in my parse but not in pipe:", sorted(mine - set(vals)))

# --- 5. Hapax lemmas by POS class ---
print("\n=== HAPAX PROBES ===")
stem_counter = Counter(rec["stem_lem"] for rec in words.values()
                       if rec["stem_lem"])
hapax = {l for l, c in stem_counter.items() if c == 1}
print("hapax stem lemmas:", len(hapax))
# POS of the stem segment carrying each hapax lemma
pos_of = {}
for loc, rec in words.items():
    for form, feats in rec["segments"]:
        if feats.startswith("STEM|"):
            m = re.search(r"LEM:([^|]+)", feats)
            if m and m.group(1) in hapax:
                pos_of[m.group(1)] = feats.split("|")[1] if "|" in feats else feats
pos_counter = Counter(pos_of.values())
print("hapax lemmas by stem POS tag:", dict(pos_counter))
non_pn = sum(1 for l in hapax if not pos_of.get(l, "").startswith("PN"))
print("hapax lemmas excluding proper nouns (PN):", non_pn)
# content words only: nouns/adjectives/verbs
content = sum(1 for l in hapax
              if pos_of.get(l, "").split(":")[0] in ("N", "ADJ", "V"))
print("hapax lemmas that are N/ADJ/V stems:", content)

# --- 6. Quran verses with BOTH narrow and non-narrow forms ---
print("\n=== QURAN BOTH-FORMS ===")
narrow = {"القران", "والقران", "بالقران", "قرانا"}
for n, a, b in bounds:
    for vi, ln in enumerate(verses[a:b], start=1):
        toks = [t for t in skeleton(ln).split() if "قران" in t]
        if toks and any(t in narrow for t in toks) and \
                any(t not in narrow for t in toks):
            print(f"{n}:{vi}", toks)
print("(end both-forms list)")

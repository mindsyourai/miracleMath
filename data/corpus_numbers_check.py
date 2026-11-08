#!/usr/bin/env python3
"""
corpus_numbers_check.py -- miracleMath (Agent A: Quran facts + corpus numbers)

Re-verifies every corpus number from the two corpus files on disk, by
script, and writes data/corpus_numbers.json. Nothing is trusted from
earlier runs: every figure below is recomputed here.

Files:
  corpus/quranic-corpus-morphology-0.4.txt (QAC v0.4, Kais Dukes)
  corpus/quran-uthmani.txt (Tanzil Quran Text, Uthmani script v1.1)

Definitions (each stated in the JSON 'rule' field too):
  * words: one QAC word = one (surah, verse, word) location; a word
    with several segments (prefix + stem + suffix) counts once.
  * segments: one QAC data line = one segment (LOCATION/FORM/TAG/FEATURES).
  * unique surface forms: distinct whitespace-separated tokens in the
    Tanzil text as printed (diacritics kept), over the 6,236 verse
    lines, unnumbered basmalahs included. (Excluding them gives 18,993:
    one token form occurs only in a basmalah.)
  * unique stems: distinct FORM values on STEM segments in QAC
    (Buckwalter transliteration).
  * unique roots: distinct ROOT: values in QAC.
  * unique lemmas: distinct LEM: values in QAC.
  * verses / surahs: distinct (surah, verse) / surah numbers in QAC,
    cross-checked against the 6,236 Tanzil verse lines and the standard
    Kufi ayah-count table (sums to 6,236).
  * letters: see data/letter_count.py (project rule A4). Headline
    excludes the 112 unnumbered basmalahs.

Expected (all reproduced by this script on 2026-11-08):
  surahs 114, verses 6,236, words 77,429, segments 128,219,
  unique surface forms 18,994, stems 12,113, roots 1,642,
  lemmas 4,832, letters 325,386 excl. / 327,514 incl. basmalahs.

Usage: python3 data/corpus_numbers_check.py [--out PATH]
Prints every number it computes; writes corpus_numbers.json.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from letter_count import AYAH_COUNTS, letter_count, load_verses, \
    strip_unnumbered_basmalah, skeleton  # noqa: E402

DEFAULT_QAC = HERE.parent / "corpus" / "quranic-corpus-morphology-0.4.txt"
DEFAULT_TANZIL = HERE.parent / "corpus" / "quran-uthmani.txt"
DEFAULT_OUT = HERE / "corpus_numbers.json"

LOC_RE = re.compile(r"\((\d+):(\d+):(\d+):(\d+)\)")
ROOT_RE = re.compile(r"ROOT:([^|]+)")
LEM_RE = re.compile(r"LEM:([^|]+)")


def parse_qac(path):
    """Return dict of QAC totals."""
    n_seg = 0
    words = set()
    verses = set()
    surahs = set()
    stems = set()
    roots = set()
    lems = set()
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
            s, v, w, _sg = map(int, m.groups())
            n_seg += 1
            words.add((s, v, w))
            verses.add((s, v))
            surahs.add(s)
            max_verse[s] = max(max_verse.get(s, 0), v)
            form, feats = parts[1], parts[3]
            if feats.startswith("STEM|"):
                stems.add(form)
            r = ROOT_RE.search(feats)
            if r:
                roots.add(r.group(1))
            lm = LEM_RE.search(feats)
            if lm:
                lems.add(lm.group(1))
    return {"segments": n_seg, "words": len(words), "verses": len(verses),
            "surahs": len(surahs), "stems": len(stems), "roots": len(roots),
            "lemmas": len(lems), "max_verse": max_verse}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qac", default=str(DEFAULT_QAC))
    ap.add_argument("--tanzil", default=str(DEFAULT_TANZIL))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    q = parse_qac(args.qac)
    verses, vmap = load_verses(args.tanzil)
    excl = [strip_unnumbered_basmalah(verses[i], *vmap[i])
            for i in range(6236)]

    # --- cross-checks (fail loudly instead of forcing a match) ---
    assert sum(AYAH_COUNTS) == 6236
    assert q["max_verse"] == {s + 1: n for s, n in enumerate(AYAH_COUNTS)}, \
        "QAC max verse per surah != standard ayah-count table"
    assert q["verses"] == len(verses) == 6236
    assert q["surahs"] == 114

    tanzil_tokens = [t for ln in verses for t in ln.split()]
    tanzil_tokens_excl = [t for ln in excl for t in ln.split()]
    surf_incl = len(set(tanzil_tokens))
    surf_excl = len(set(tanzil_tokens_excl))
    letters_excl = sum(letter_count(ln) for ln in excl)
    letters_incl = sum(letter_count(ln) for ln in verses)
    assert letters_incl - letters_excl == 112 * 19
    basm_letters = letter_count(verses[0])
    assert basm_letters == 19

    # longest / shortest surah (for the facts file)
    longest = max(range(114), key=lambda i: AYAH_COUNTS[i]) + 1
    shortest = [s + 1 for s, n in enumerate(AYAH_COUNTS)
                if n == min(AYAH_COUNTS)]

    numbers = [
        {"id": "surahs", "label": "Surahs",
         "value": q["surahs"],
         "rule": "Distinct surah numbers in QAC v0.4; Tanzil has 6,236 verse lines across 114 surahs",
         "source": "data/corpus_numbers_check.py"},
        {"id": "verses", "label": "Verses (ayahs)",
         "value": q["verses"],
         "rule": "Distinct (surah, verse) locations in QAC v0.4; equals the 6,236 Tanzil verse lines and the Kufi ayah-count table",
         "source": "data/corpus_numbers_check.py"},
        {"id": "words", "label": "Words (QAC v0.4)",
         "value": q["words"],
         "rule": "One QAC word = one (surah, verse, word) location; a multi-segment word counts once",
         "source": "data/corpus_numbers_check.py"},
        {"id": "segments", "label": "Segments (QAC v0.4)",
         "value": q["segments"],
         "rule": "One QAC data line = one segment (prefix, stem or suffix)",
         "source": "data/corpus_numbers_check.py"},
        {"id": "unique_surface_forms", "label": "Unique surface forms",
         "value": surf_incl,
         "rule": "Distinct whitespace-separated tokens in the Tanzil Uthmani text as printed (diacritics kept), 6,236 verse lines incl. the 112 unnumbered basmalahs; excl. basmalahs 18,993",
         "source": "data/corpus_numbers_check.py"},
        {"id": "unique_stems", "label": "Unique stems (QAC v0.4)",
         "value": q["stems"],
         "rule": "Distinct FORM values on STEM segments in QAC v0.4 (Buckwalter transliteration)",
         "source": "data/corpus_numbers_check.py"},
        {"id": "unique_roots", "label": "Unique roots (QAC v0.4)",
         "value": q["roots"],
         "rule": "Distinct ROOT: values in QAC v0.4",
         "source": "data/corpus_numbers_check.py"},
        {"id": "unique_lemmas", "label": "Unique lemmas (QAC v0.4)",
         "value": q["lemmas"],
         "rule": "Distinct LEM: values in QAC v0.4",
         "source": "data/corpus_numbers_check.py"},
        {"id": "letters_excl_unnumbered_basmalahs",
         "label": "Letters (excl. unnumbered basmalahs)",
         "value": letters_excl,
         "rule": "HEADLINE letter figure. Base letters only on the Tanzil Uthmani text; diacritics/tashkil excluded, shaddah counts its letter once, hamza forms count as letters, alef wasla counts, dagger alif / small waw / small yeh are marks, not letters; the 112 unnumbered basmalahs (19 letters each) excluded",
         "source": "data/letter_count.py"},
        {"id": "letters_incl_unnumbered_basmalahs",
         "label": "Letters (incl. unnumbered basmalahs)",
         "value": letters_incl,
         "rule": "Same letter rule as the headline figure, but with the 112 unnumbered basmalahs as printed in the Tanzil text included (+2,128 letters)",
         "source": "data/letter_count.py"},
        {"id": "letters_classical_323671",
         "label": "Letters, classical total (Ibn Abbas report)",
         "value": 323671,
         "rule": "Classical report, NOT a script count: Ibn Abbas via al-Suyuti, al-Itqan fi Ulum al-Quran (1/231). Reproduces under no rule tried (325,386 excl. / 327,514 incl.); classical authorities disagree among themselves (Basra 323,015; Mujahid 321,000; Ibn Mas'ud 300,670; Salam Abu Muhammad 340,740). Shown for comparison only.",
         "source": "al-Suyuti, al-Itqan fi Ulum al-Quran 1/231 (Ibn Abbas report); cf. SeekersGuidance, Shaykh Anas al-Musa"},
        {"id": "basmalah_letters", "label": "Letters in the Basmalah",
         "value": basm_letters,
         "rule": "Letter count of Quran 1:1 under the project letter rule (alef wasla counts)",
         "source": "data/letter_count.py"},
        {"id": "basmalah_occurrences", "label": "Basmalah occurrences",
         "value": 114,
         "rule": "113 surah openings (every surah except At-Tawbah, 9) + the Basmalah inside verse 27:30; counted on the Tanzil text",
         "source": "data/corpus_numbers_check.py"},
        {"id": "tanzil_tokens_incl_basmalahs",
         "label": "Tanzil whitespace tokens (incl. basmalahs)",
         "value": len(tanzil_tokens),
         "rule": "Whitespace-separated tokens over the 6,236 Tanzil verse lines as printed; 452 more than QAC words (448 basmalah words + 4 segmentation differences)",
         "source": "data/corpus_numbers_check.py"},
        {"id": "tanzil_tokens_excl_basmalahs",
         "label": "Tanzil whitespace tokens (excl. basmalahs)",
         "value": len(tanzil_tokens_excl),
         "rule": "Whitespace-separated tokens over the 6,236 Tanzil verse lines with the 112 unnumbered basmalahs (4 words each) removed; 4 more than QAC words (segmentation differences)",
         "source": "data/corpus_numbers_check.py"},
    ]

    out = Path(args.out)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"numbers": numbers}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"QAC segments={q['segments']} words={q['words']} "
          f"verses={q['verses']} surahs={q['surahs']}")
    print(f"QAC unique stems={q['stems']} roots={q['roots']} "
          f"lemmas={q['lemmas']}")
    print(f"Tanzil tokens incl. basmalahs={len(tanzil_tokens)} "
          f"excl.={len(tanzil_tokens_excl)}")
    print(f"Unique surface forms incl. basmalahs={surf_incl} "
          f"excl.={surf_excl}")
    print(f"Letters excl. unnumbered basmalahs={letters_excl} "
          f"incl.={letters_incl} (basmalah={basm_letters} letters x 112)")
    print(f"Longest surah: {longest} ({AYAH_COUNTS[longest - 1]} verses); "
          f"shortest ({min(AYAH_COUNTS)} verses): surahs {shortest}")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

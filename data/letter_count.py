#!/usr/bin/env python3
"""
letter_count.py -- miracleMath (Agent A: Quran facts + corpus numbers)

Letter count of the Quran by script from the Tanzil Uthmani text.

Text: corpus/quran-uthmani.txt (Tanzil Quran Text, Uthmani script, v1.1).
The first 6,236 lines are the 6,236 numbered verses in order. Tanzil
prepends the Basmalah to the first verse line of every surah except
Surah 9 (At-Tawbah); only 1:1 is a numbered verse. So the file contains
113 surah-opening basmalahs, of which 112 are unnumbered (surahs 2-114
except 9) and 1 (1:1) is numbered. A 114th occurrence sits inside
verse 27:30 (Sulayman's letter).

LETTER RULE (project convention A4, same as data/assumption_recompute.py):
  * Count base letters only: each Arabic letter U+0621-U+064A counts once.
  * Diacritics / tashkil do NOT count: vowel marks, shaddah, sukun,
    maddah, tatweel (kashida) and the Quranic annotation marks
    (U+06D6-U+06ED, U+08D3-U+08FF) are stripped. A shaddah therefore
    counts its letter ONCE, not twice.
  * Hamza forms count as letters: standalone hamza (ء) counts once;
    hamza on a carrier (أ إ آ ؤ ئ) counts as the carrier letter, once.
  * Alef wasla (ٱ) counts as a letter (one alef).
  * Dagger alif (ٰ), small waw (ۥ) and small yeh (ۦ) are MARKS, not
    letters: they are dropped, not counted. (Counting the dagger alif
    as a letter would add ~9,700 and make the longest-word claim
    change; see the variants printed below.)
  * Basmalah treatment: reported BOTH ways. The headline figure
    EXCLUDES the 112 unnumbered basmalahs (19 letters each = 2,128),
    matching the QAC word-count convention, which also excludes them
    (QAC contains only 1:1 as words). The inclusive figure is given
    alongside so either convention can be checked.

HEADLINE: 325,386 letters (unnumbered basmalahs excluded);
          327,514 letters (all basmalahs as printed included).

COMPARISON WITH 323,671: the widely quoted classical total, reported
from Ibn Abbas via al-Suyuti, al-Itqan fi Ulum al-Quran (1/231).
It reproduces under NO rule tried here: our count is 1,715 higher
excluding the basmalahs and 3,843 higher including them. The classical
authorities disagree among themselves by far more than that (Basra
reciters 323,015; Mujahid 321,000; Ibn Mas'ud 300,670; Salam Abu
Muhammad 340,740 -- SeekersGuidance, Shaykh Anas al-Musa, citing
al-Suyuti / al-Zarkashi), and their counts were hand counts on early
manuscripts with a different rasm (omitted alifs, hamzat al-wasl
treatment) and no stated reproducible rule. The stated classical
explanation -- a doubled letter (shaddah) counted as two -- does not
reproduce it either: doubling shaddah on this text gives 348,064,
far above every classical figure. So 323,671 is a classical report
to cite, not a count this text reproduces.

Usage: python3 data/letter_count.py [--tanzil PATH]
Prints the headline counts plus the tested variants.
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_TANZIL = HERE.parent / "corpus" / "quran-uthmani.txt"

# Standard ayah counts per surah (Kufi count; sums to 6236, verified
# against the QAC file: max verse per surah matches this table).
AYAH_COUNTS = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52,
    99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34,
    30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18,
    45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30,
    52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22,
    17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4,
    7, 3, 6, 3, 5, 4, 5, 6]

DIACRITICS = re.compile(r"[\u064b-\u065f\u0640\u06d6-\u06ed\u08d3-\u08ff]")
HAMZA_MAP = str.maketrans({"\u0623": "\u0627", "\u0625": "\u0627",
                           "\u0622": "\u0627", "\u0671": "\u0627",
                           "\u0624": "\u0648", "\u0626": "\u064a"})
SMALL_MARKS = {"\u0670": "\u0627", "\u06e5": "\u0648", "\u06e6": "\u064a"}
SHADDAH = "\u0651"


def skeleton(text):
    """Diacritic-stripped, hamza-normalised text, for matching words
    (e.g. recognising the Basmalah) regardless of spelling marks."""
    t = text.translate(HAMZA_MAP)
    for k, v in SMALL_MARKS.items():
        t = t.replace(k, v)
    return DIACRITICS.sub("", t)


def letter_count(text, dagger_as_letter=False, count_wasla=True,
                 count_hamza=True, double_shaddah=False):
    """Count letters under the project rule (see module docstring).
    Variants are keyword flags, used only for the 323,671 comparison."""
    n_wasla = text.count("\u0671")          # alef wasla, before mapping
    n_shaddah = text.count(SHADDAH)
    t = text.translate(HAMZA_MAP)          # hamza carriers -> base letter
    if dagger_as_letter:
        for k, v in SMALL_MARKS.items():
            t = t.replace(k, v)
    else:
        for k in SMALL_MARKS:
            t = t.replace(k, "")
    t = DIACRITICS.sub("", t)              # strips shaddah, vowels, marks
    n = sum(1 for c in t if "\u0621" <= c <= "\u064a")
    if not count_wasla:
        n -= n_wasla
    if not count_hamza:
        n -= t.count("\u0621")             # standalone hamza only
    if double_shaddah:
        n += n_shaddah
    return n


def load_verses(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    verses = lines[:6236]
    assert len(verses) == 6236, f"expected 6236 verse lines, got {len(verses)}"
    assert sum(AYAH_COUNTS) == 6236
    vmap = {}
    idx = 0
    for s, n in enumerate(AYAH_COUNTS, start=1):
        for a in range(1, n + 1):
            vmap[idx] = (s, a)
            idx += 1
    return verses, vmap


def strip_unnumbered_basmalah(line, s, a):
    """Remove the 4-word basmalah prepended to verse 1 of every surah
    except 1 (where it IS verse 1:1) and 9 (which has none)."""
    if a == 1 and s > 1 and s != 9:
        return " ".join(line.split()[4:])
    return line


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tanzil", default=str(DEFAULT_TANZIL))
    args = ap.parse_args()

    verses, vmap = load_verses(args.tanzil)
    excl = [strip_unnumbered_basmalah(verses[i], *vmap[i])
            for i in range(6236)]

    # --- verify the basmalah structure before counting ---
    basm_words = skeleton("بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ").split()
    openings = 0
    for i in range(6236):
        s, a = vmap[i]
        if a == 1 and s > 1 and s != 9:
            toks = [skeleton(t) for t in verses[i].split()[:4]]
            assert toks == basm_words, (s, toks)
            openings += 1
    assert openings == 112, openings
    li_27_30 = [i for i in range(6236) if vmap[i] == (27, 30)][0]
    assert " ".join(basm_words) in " ".join(
        skeleton(t) for t in verses[li_27_30].split()), "27:30 basmalah"
    basm_letters = letter_count(verses[0])
    assert basm_letters == 19, basm_letters

    incl = sum(letter_count(ln) for ln in verses)
    excl_n = sum(letter_count(ln) for ln in excl)
    assert incl - excl_n == 112 * 19 == 2128, (incl, excl_n)

    print(f"Tanzil verse lines: {len(verses)}")
    print(f"Unnumbered basmalah lines (surahs 2-114 except 9): {openings}")
    print(f"Basmalah occurrences total (113 openings + 27:30): 114")
    print(f"Basmalah letters (Quran 1:1): {basm_letters}")
    print(f"HEADLINE letters, excl. unnumbered basmalahs: {excl_n}")
    print(f"Letters, incl. unnumbered basmalahs (as printed): {incl}")
    print("--- variants (excl. unnumbered basmalahs, for the 323,671 "
          "comparison) ---")
    print(f"  dagger alif / small waw / small yeh counted as letters: "
          f"{sum(letter_count(ln, dagger_as_letter=True) for ln in excl)}")
    print(f"  alef wasla NOT counted: "
          f"{sum(letter_count(ln, count_wasla=False) for ln in excl)}")
    print(f"  standalone hamza NOT counted: "
          f"{sum(letter_count(ln, count_hamza=False) for ln in excl)}")
    print(f"  shaddah doubled (letter counted twice): "
          f"{sum(letter_count(ln, double_shaddah=True) for ln in excl)}")
    print(f"Classical total 323671 (Ibn Abbas via al-Suyuti, al-Itqan "
          f"1/231): diff vs headline {excl_n - 323671}; "
          f"diff vs incl. {incl - 323671}")
    print("Conclusion: 323,671 reproduces under no rule tried; the "
          "classical authorities disagree among themselves by thousands, "
          "so it is cited as a classical report, not as the script count.")


if __name__ == "__main__":
    main()

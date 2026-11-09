#!/usr/bin/env python3
"""
more_names_check.py -- miracleMath (Agent A: more than 99 Names)

Verifies, by script on the corpus, the additional names/attributes of
Allah MK asked about -- phrases used of Allah in the Quran that are
NOT among the 99 cards in data/names.json. For each candidate:

  * Tanzil Uthmani text: skeleton search (diacritics stripped, alef
    variants and dagger alef normalised to plain alef) over the 6,236
    verse lines, reporting EVERY verse where the phrase occurs.
  * QAC v0.4: the same (surah, verse) locations must exist, and the
    QAC word forms at those verses must contain the phrase's key
    roots (Buckwalter ROOT: values).
  * data/names.json: the phrase must NOT already be one of the 99
    cards (checked by Arabic skeleton and by transliteration).

Findings on 2026-11-09 (this script reproduces them):
  * Dhul-Jalali wal-Ikram -- OCCURS (55:27 nominative, 55:78
    genitive) but is ALREADY card #85 of the 99 ("Dhu al-Jalal
    wa-l-Ikram", count 2). It is NOT an additional name; it is
    recorded here under checked_but_already_in_99 so the check is
    auditable, and it is NOT listed as an extra name.
  * Khayrul-Makirin -- VERIFIED additional: 3:54, 8:30 (and nowhere
    else in the Quran).
  * Ahsanul-Khaliqin -- VERIFIED additional: 23:14, 37:125 (and
    nowhere else). Distinct from card #11 Al-Khaliq (the single
    word); the full superlative phrase is not among the 99.
  * Rabbul-Arshil-Azim -- VERIFIED additional: 9:129, 23:86, 27:26.
    The brief listed only 9:129 and 27:26; the script found a third
    occurrence at 23:86, which is included. Distinct from card #33
    Al-Azim (the single word); the full phrase is not among the 99.

No total number of additional names is invented: the note states
"more than 99" with these verified examples and leaves it there.

The hadith citation (verified 2026-11-09 against sunnah.com):
  * Sahih al-Bukhari 7392 (Book 97, Hadith 21): "Allah has
    ninety-nine Names, one-hundred less one; and he who memorized
    them all by heart will enter Paradise."
  * Sahih Muslim 2677a (Book 48, Hadith 5) and 2677b (Book 48,
    Hadith 6): the same report from Abu Huraira.
  * Neither narration LISTS the names. The familiar enumerated list
    of 99 comes from a narration in Jami' at-Tirmidhi 3507; the
    Bukhari/Muslim narrations give the number and the reward, not
    the list.

Usage: python3 data/more_names_check.py [--out PATH]
Writes data/more_names.json; prints the verification table.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from letter_count import AYAH_COUNTS  # noqa: E402

DEFAULT_TANZIL = HERE.parent / "corpus" / "quran-uthmani.txt"
DEFAULT_QAC = HERE.parent / "corpus" / "quranic-corpus-morphology-0.4.txt"
DEFAULT_NAMES = HERE / "names.json"
DEFAULT_OUT = HERE / "more_names.json"

LOC_RE = re.compile(r"\((\d+):(\d+):(\d+):(\d+)\)")
ROOT_RE = re.compile(r"ROOT:([^|]+)")

# Skeleton normalisation for phrase search. Dagger alef (U+0670)
# stands in for a written alef in words like الجلال / الماكرين /
# الخالقين, so it normalises TO alef -- unlike the project's letter
# rule (letter_count.py), where it is a mark, not a letter. Alef
# maksura (U+0649) in ذى (55:78) normalises to yeh.
ALEF_NORM = {"\u0671": "ا", "\u0623": "ا", "\u0625": "ا",
             "\u0622": "ا", "\u0670": "ا", "\u0649": "ي"}
STRIP = (set(range(0x064B, 0x0660))
         | {0x06D6, 0x06D7, 0x06D8, 0x06D9, 0x06DA, 0x06DB, 0x06DC,
            0x06DF, 0x06E0, 0x06E1, 0x06E2, 0x06E3, 0x06E4, 0x06E7,
            0x06E8, 0x06EA, 0x06EB, 0x06EC, 0x06ED, 0x0640})


def skel(t):
    out = []
    for ch in t:
        if ord(ch) in STRIP:
            continue
        out.append(ALEF_NORM.get(ch, ch))
    return "".join(out)


# Candidates: (id, transliteration, meaning, skeleton phrase,
#              expected roots in QAC at those verses)
CANDIDATES = [
    {"id": "dhul_jalali_wal_ikram",
     "transliteration": "Dhul-Jalali wal-Ikram",
     "meaning_en": "Possessor of Majesty and Honour",
     "skeleton": "ذو الجلال والاكرام",
     "skeleton_genitive": "ذي الجلال والاكرام",
     "roots": ["jll", "krm"]},
    {"id": "khayrul_makirin",
     "transliteration": "Khayrul-Makirin",
     "meaning_en": "the Best of Planners",
     "skeleton": "خير الماكرين",
     "roots": ["xyr", "mkr"]},
    {"id": "ahsanul_khaliqin",
     "transliteration": "Ahsanul-Khaliqin",
     "meaning_en": "the Best of Creators",
     "skeleton": "احسن الخالقين",
     "roots": ["Hsn", "xlq"]},
    {"id": "rabbul_arshil_azim",
     "transliteration": "Rabbul-Arshil-Azim",
     "meaning_en": "Lord of the Mighty Throne",
     "skeleton": "رب العرش العظيم",
     "roots": ["rbb", "Er$", "EZm"]},
]


def load_verses(path):
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            lines.append(line)
    loc = []
    for s, n in enumerate(AYAH_COUNTS, start=1):
        for v in range(1, n + 1):
            loc.append((s, v))
    assert len(lines) == len(loc) == 6236
    return lines, loc


def parse_qac(path):
    """verse -> set of ROOT values present in that verse."""
    roots_by_verse = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#") \
                    or line.startswith("LOCATION"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            m = LOC_RE.match(parts[0])
            if not m:
                continue
            s, v = int(m.group(1)), int(m.group(2))
            r = ROOT_RE.search(parts[3])
            if r:
                roots_by_verse.setdefault((s, v), set()).add(r.group(1))
    return roots_by_verse


def extract_printed_phrase(line, skeleton_phrase):
    """Return the phrase as printed (with diacritics) in this verse.

    Walks the verse's skeleton and maps the skeleton span back to
    the original characters, keeping the diacritics that belong to
    the phrase's letters.
    """
    sk = skel(line)
    start = sk.index(skeleton_phrase)
    end = start + len(skeleton_phrase)
    # map skeleton index -> original index
    mapping = []
    for i, ch in enumerate(line):
        if ord(ch) in STRIP:
            continue
        mapping.append(i)
    o_start = mapping[start]
    o_end = mapping[end - 1]
    # extend over trailing diacritics of the last letter
    j = o_end + 1
    while j < len(line) and ord(line[j]) in STRIP:
        j += 1
    return line[o_start:j]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--tanzil", default=str(DEFAULT_TANZIL))
    ap.add_argument("--qac", default=str(DEFAULT_QAC))
    ap.add_argument("--names", default=str(DEFAULT_NAMES))
    args = ap.parse_args()

    lines, loc = load_verses(args.tanzil)
    qac_roots = parse_qac(args.qac)
    with open(args.names, encoding="utf-8") as f:
        cards = json.load(f)["names"]
    card_skeletons = {skel(c["arabic"]) for c in cards}
    card_trans = {c["transliteration"].lower() for c in cards}

    verified = []
    already = []
    dropped = []
    for cand in CANDIDATES:
        phrases = [cand["skeleton"]]
        if "skeleton_genitive" in cand:
            phrases.append(cand["skeleton_genitive"])
        hits = []
        for phrase in phrases:
            for i, ln in enumerate(lines):
                if phrase in skel(ln):
                    hits.append((loc[i], phrase))
        hits = sorted(set(hits))
        verses = sorted({h[0] for h in hits})

        # QAC cross-check: verse exists and carries the phrase's roots
        qac_ok = []
        for (s, v) in verses:
            roots = qac_roots.get((s, v), set())
            missing = [r for r in cand["roots"] if r not in roots]
            qac_ok.append({"verse": f"{s}:{v}",
                           "roots_present": sorted(roots & set(cand["roots"])),
                           "roots_missing": missing})
        qac_pass = all(not o["roots_missing"] for o in qac_ok)

        # already among the 99?
        in_99 = any(skel_p in card_skeletons for skel_p in phrases) \
            or cand["transliteration"].lower() in card_trans
        in_99_card = None
        if in_99:
            for c in cards:
                if skel(c["arabic"]) in phrases or \
                        c["transliteration"].lower() == \
                        cand["transliteration"].lower():
                    in_99_card = c["id"]
                    break

        # printed Arabic (first hit verse, nominative form)
        printed = None
        if hits:
            s, v = hits[0][0]
            printed = extract_printed_phrase(lines[loc.index((s, v))],
                                             hits[0][1])

        entry = {
            "id": cand["id"],
            "transliteration": cand["transliteration"],
            "meaning_en": cand["meaning_en"],
            # "arabic" is the field web/app.js renders; it is the phrase
            # exactly as printed in the Tanzil Uthmani text.
            "arabic": printed,
            "verses": [f"{s}:{v}" for (s, v) in verses],
            "verse_count": len(verses),
            "qac_cross_check": qac_ok,
            "qac_roots_pass": qac_pass,
            "already_in_99": in_99,
            "in_99_card_id": in_99_card,
        }
        if in_99:
            already.append(entry)
            print(f"{cand['transliteration']}: Tanzil {entry['verses']} "
                  f"-- ALREADY card #{in_99_card} of the 99, NOT additional")
        elif not verses:
            dropped.append(entry)
            print(f"{cand['transliteration']}: NOT FOUND in the Quran -- dropped")
        else:
            verified.append(entry)
            print(f"{cand['transliteration']}: Tanzil {entry['verses']} "
                  f"QAC roots pass={qac_pass} -- VERIFIED additional")

    out = {
        "note": "Allah has more than 99 names: the ninety-nine are the "
                "names whose memorisation the hadith promises Paradise "
                "for, not a count of all His names. These are verified "
                "additional names/attributes used of Allah in the Quran, "
                "each occurring in the Tanzil Uthmani text and "
                "cross-checked in QAC v0.4, and none of them is one of "
                "the 99 cards in data/names.json. No total number of "
                "additional names is claimed.",
        "hadith_99_names": {
            "text": "Allah has ninety-nine Names, one-hundred less one; "
                    "and he who memorized them all by heart will enter "
                    "Paradise.",
            "narrator": "Abu Huraira",
            "bukhari": "Sahih al-Bukhari 7392 (Book 97, Hadith 21)",
            "muslim": "Sahih Muslim 2677a (Book 48, Hadith 5) and "
                      "2677b (Book 48, Hadith 6)",
            "source_url": "https://sunnah.com/bukhari/97/21",
            "source_url_muslim": "https://sunnah.com/muslim/48/5",
            "caveat": "Neither narration lists the names. The familiar "
                      "enumerated list of 99 comes from a narration in "
                      "Jami' at-Tirmidhi 3507; the Bukhari/Muslim "
                      "narrations give the number and the reward, not "
                      "the list."
        },
        "verified_additional": verified,
        # "more_names" is the key build.py passes to the page
        # (web/app.js renders it); same list as verified_additional.
        "more_names": verified,
        "checked_but_already_in_99": already,
        "checked_but_not_found": dropped,
        "verification": "data/more_names_check.py -- Tanzil skeleton "
                        "search over all 6,236 verses + QAC v0.4 root "
                        "cross-check at each verse + names.json "
                        "membership check. Run it to reproduce.",
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"\nWrote {args.out}: {len(verified)} verified additional, "
          f"{len(already)} already in the 99, {len(dropped)} not found.")
    if any(not e["qac_roots_pass"] for e in verified + already):
        print("WARNING: a QAC root cross-check did not pass -- see JSON.")
        sys.exit(1)


if __name__ == "__main__":
    main()

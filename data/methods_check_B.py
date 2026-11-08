#!/usr/bin/env python3
"""
methods_check_B.py -- miracleMath methods + locations enrichment, Checker B.

Covers the 27 findings in categories code19 (11) + corpus_linguistics (16)
from data/scholar_findings.json. Recomputes every count from the local
corpus files by script (nothing hand-typed):

  corpus/quranic-corpus-morphology-0.4.txt  (QAC v0.4)
  corpus/quran-uthmani.txt                  (Tanzil Uthmani)

Counting conventions (taken from the project's existing scripts):
- QAC word = one (surah, verse, word) location; a word counts once even if
  several of its segments carry the root. QAC contains only the 1:1
  basmalah as words; the 112 unnumbered basmalahs prepended in Tanzil
  are NOT QAC words.
- Tanzil skeleton: diacritics/tatweel removed, hamza variants normalised,
  superscript letters KEPT as letters (dagger alif -> ا, small waw -> و,
  small yeh -> ي) for word matching.
- Letter counting (project convention): base letters count, incl. alef
  wasla (ٱ -> ا) and standalone hamza ء; dagger alif ٰ and small waw/yeh
  ۦ/ۥ do NOT count.
- Tanzil "lemma" counts strip leading clitics (و ف ب ل ك) before comparing.

Usage: python3 data/methods_check_B.py
Writes data/methods_check_B_results.json and prints a summary.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
QAC = BASE / "corpus" / "quranic-corpus-morphology-0.4.txt"
TANZIL = BASE / "corpus" / "quran-uthmani.txt"
OUT = HERE / "methods_check_B_results.json"

SURAH_VERSES = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109,
    123, 111, 43, 52, 99, 128, 111, 110, 98, 135,
    112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85,
    54, 53, 89, 59, 37, 35, 38, 29, 18, 45,
    60, 49, 62, 55, 78, 96, 29, 22, 24, 13,
    14, 11, 11, 18, 12, 12, 30, 52, 52, 44,
    28, 28, 20, 56, 40, 31, 50, 40, 46, 42,
    29, 19, 36, 25, 22, 17, 19, 26, 30, 20,
    15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3,
    5, 4, 5, 6,
]

DIACRITICS = re.compile(r"[\u064b-\u065f\u0640\u06d6-\u06ed\u08d3-\u08ff]")
SUPERSCRIPT = str.maketrans({"ٰ": "ا", "ۥ": "و", "ۦ": "ي"})
HAMZA_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ؤ": "و", "ئ": "ي"})
LETTER_MARKS = re.compile(r"[ٰۥۦ]")
ROOT_RE = re.compile(r"ROOT:([^|]+)")
LEM_RE = re.compile(r"LEM:([^|]+)")
LOC_RE = re.compile(r"\((\d+):(\d+):(\d+):(\d+)\)")


def strip_diacritics(text):
    return DIACRITICS.sub("", text.translate(SUPERSCRIPT))


def skeleton(text):
    return strip_diacritics(text).translate(HAMZA_MAP).replace("ء", "")


def letter_count(text):
    t = text.translate(HAMZA_MAP)
    t = LETTER_MARKS.sub("", t)
    t = DIACRITICS.sub("", t)
    return sum(1 for c in t if "\u0621" <= c <= "\u064a")


def strip_prefixes(tok):
    while len(tok) > 1 and tok[0] in "وفبلك":
        tok = tok[1:]
    return tok


def parse_qac(path):
    """words: (s,v,w) -> {roots, lems, stem_forms, stem_lem, segments}.
    Also segment-level counters."""
    words = {}
    seg_root_counter = Counter()
    seg_lem_counter = Counter()
    n_seg = 0
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
            form, feats = parts[1], parts[3]
            rec = words.setdefault((s, v, w), {
                "roots": set(), "lems": set(), "stem_forms": [],
                "stem_lem": None, "segments": []})
            rec["segments"].append((form, feats))
            n_seg += 1
            r = ROOT_RE.search(feats)
            if r:
                rec["roots"].add(r.group(1))
                seg_root_counter[r.group(1)] += 1
            l = LEM_RE.search(feats)
            if l:
                rec["lems"].add(l.group(1))
                seg_lem_counter[l.group(1)] += 1
            if feats.startswith("STEM|"):
                rec["stem_forms"].append(form)
                if l and rec["stem_lem"] is None:
                    rec["stem_lem"] = l.group(1)
    return words, n_seg, seg_root_counter, seg_lem_counter


def load_tanzil(path):
    raw = open(path, encoding="utf-8").read().splitlines()
    verses = [ln for ln in raw if ln.strip() and not ln.lstrip().startswith("#")]
    assert len(verses) == 6236, len(verses)
    bounds, i = [], 0
    for n, v in enumerate(SURAH_VERSES, start=1):
        bounds.append((n, i, i + v))
        i += v
    assert i == len(verses)
    return verses, bounds


def surah_lines(verses, bounds, n):
    _, a, b = bounds[n - 1]
    return verses[a:b]


def verses_of_word_locs(locs):
    """Deduplicated sorted surah:verse refs + per-surah verse counts."""
    vs = sorted({(s, v) for (s, v, _w) in locs})
    per = Counter(s for (s, _v) in vs)
    return [f"{s}:{v}" for (s, v) in vs], {str(s): per[s] for s in sorted(per)}


def is_allah(tok):
    if tok in {"تالله", "وتالله", "ابالله"}:
        return True
    t = tok
    while t and t[0] in "وف":
        t = t[1:]
    if t == "لله":
        return True
    return strip_prefixes(t) == "الله"


def is_rahman(tok):
    t = tok
    while t and t[0] in "وف":
        t = t[1:]
    if t == "للرحمان":
        return True
    return strip_prefixes(t) == "الرحمان"


def is_rahim(tok):
    return strip_prefixes(tok) in {"الرحيم", "رحيم", "رحيما"}


def main():
    words, n_seg, seg_roots, seg_lems = parse_qac(QAC)
    verses, bounds = load_tanzil(TANZIL)
    R = {}

    # ---- corpus totals -------------------------------------------------
    R["qac_words"] = len(words)
    R["qac_segments"] = n_seg
    R["qac_verses"] = len({(s, v) for (s, v, _w) in words})
    R["qac_surahs"] = len({s for (s, _v, _w) in words})
    tokens = [t for ln in verses for t in ln.split()]
    R["tanzil_tokens_incl_basmalahs"] = len(tokens)
    R["tanzil_tokens_excl_basmalahs"] = len(tokens) - 112 * 4
    R["tanzil_letters_incl_basmalahs"] = sum(letter_count(ln) for ln in verses)
    R["tanzil_letters_excl_basmalahs"] = (
        R["tanzil_letters_incl_basmalahs"] - 112 * 19)
    # per-surah QAC word counts and Tanzil letter counts (excl basmalahs)
    qac_per_surah = Counter(s for (s, _v, _w) in words)
    R["qac_words_per_surah"] = {str(s): qac_per_surah[s] for s in range(1, 115)}
    R["tanzil_letters_per_surah_excl_basmalahs"] = {}
    for n in range(1, 115):
        ls = surah_lines(verses, bounds, n)
        tot = sum(letter_count(ln) for ln in ls)
        if n not in (1, 9):
            tot -= 19  # unnumbered basmalah merged into verse 1
        R["tanzil_letters_per_surah_excl_basmalahs"][str(n)] = tot
    # letter-mark probes (for the RDS-Q 280-letter gap)
    full = "\n".join(verses)
    R["mark_counts_incl_basmalahs"] = {
        "dagger_alif_U0670": full.count("ٰ"),
        "small_waw_U06E5": full.count("ۥ"),
        "small_yeh_U06E6": full.count("ۦ"),
        "alef_wasla_U0671": full.count("ٱ"),
        "standalone_hamza_U0621": full.count("ء"),
        "shaddah_U0651": full.count("ّ"),
        "madda_U0653": full.count("ٓ"),
    }
    # letters under variant conventions (excl unnumbered basmalahs)
    def letters_variant(count_dagger=False, count_small=False,
                        count_shaddah_double=False):
        tot = 0
        for ln in verses:
            t = ln.translate(HAMZA_MAP)
            if not count_dagger:
                t = t.replace("ٰ", "")
            else:
                t = t.replace("ٰ", "ا")
            if not count_small:
                t = t.replace("ۥ", "").replace("ۦ", "")
            else:
                t = t.replace("ۥ", "و").replace("ۦ", "ي")
            n_shaddah = t.count("ّ")
            t = DIACRITICS.sub("", t)
            tot += sum(1 for c in t if "\u0621" <= c <= "\u064a")
            if count_shaddah_double:
                tot += n_shaddah
        return tot - 112 * 19
    R["letters_variant_excl_basmalahs"] = {
        "project_convention": letters_variant(),
        "plus_dagger_alif": letters_variant(count_dagger=True),
        "plus_dagger_and_small_letters":
            letters_variant(count_dagger=True, count_small=True),
        "plus_shaddah_doubled": letters_variant(count_shaddah_double=True),
    }
    # unique-form inventories
    skel_tokens = [skeleton(t) for t in tokens]
    R["unique_surface_raw"] = len(set(tokens))
    R["unique_surface_skeletonised"] = len(set(skel_tokens))
    R["hapax_surface_raw"] = sum(1 for c in Counter(tokens).values() if c == 1)
    R["hapax_surface_skeletonised"] = sum(
        1 for c in Counter(skel_tokens).values() if c == 1)
    stem_forms = [f for rec in words.values() for f in rec["stem_forms"]]
    R["unique_stem_forms_raw"] = len(set(stem_forms))
    R["unique_stem_forms_skeletonised"] = len({skeleton(f) for f in stem_forms})
    word_roots = Counter()
    for rec in words.values():
        for r in rec["roots"]:
            word_roots[r] += 1
    R["unique_roots_word_level"] = len(word_roots)
    R["unique_roots_segment_level"] = len(seg_roots)
    R["unique_lemmas_word_level_all_segments"] = len(
        {l for rec in words.values() for l in rec["lems"]})
    stem_lem_counter = Counter(
        rec["stem_lem"] for rec in words.values() if rec["stem_lem"])
    R["unique_lemmas_stem_level"] = len(stem_lem_counter)
    R["unique_lemmas_segment_level"] = len(seg_lems)
    R["top_roots_word_level"] = word_roots.most_common(10)
    R["top_roots_segment_level"] = seg_roots.most_common(10)
    R["roots_only_at_segment_level"] = sorted(
        set(seg_roots) - set(word_roots))
    R["roots_only_at_word_level"] = sorted(
        set(word_roots) - set(seg_roots))
    # roots whose segment-level count exceeds word-level count
    R["roots_segment_gt_word"] = sorted(
        (r, seg_roots[r], word_roots[r]) for r in seg_roots
        if seg_roots[r] > word_roots[r])
    R["root_Alh_word_level"] = word_roots.get("Alh", 0)
    R["root_Alh_segment_level"] = seg_roots.get("Alh", 0)
    R["root_Hsn_word_level"] = word_roots.get("Hsn", 0)
    R["root_Hsn_segment_level"] = seg_roots.get("Hsn", 0)
    R["root_qwl_word_level"] = word_roots.get("qwl", 0)
    R["root_kwn_word_level"] = word_roots.get("kwn", 0)
    R["root_rbb_word_level"] = word_roots.get("rbb", 0)
    # hapax lemmas (stem-lemma level)
    hapax_lems = {l for l, c in stem_lem_counter.items() if c == 1}
    R["hapax_stem_lemmas"] = len(hapax_lems)
    hapax_locs = sorted(loc for loc, rec in words.items()
                        if rec["stem_lem"] in hapax_lems)
    R["hapax_stem_lemma_verses"], R["hapax_stem_lemma_per_surah"] = \
        verses_of_word_locs(hapax_locs)
    hapax_roots = {r for r, c in word_roots.items() if c == 1}
    R["hapax_roots_word_level"] = len(hapax_roots)

    # ---- basmalah ------------------------------------------------------
    skel_text = skeleton("\n".join(verses))
    R["basmalah_occurrences"] = skel_text.count("بسم الله الرحمان الرحيم")
    R["basmalah_letters_1_1"] = letter_count(verses[0])
    basmalah_verses = []
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            if "بسم الله الرحمان الرحيم" in skeleton(ln):
                basmalah_verses.append(f"{n}:{vi}")
    R["basmalah_verses"] = basmalah_verses

    # ---- Allah / Rahman / Rahim (Tanzil lemma + QAC lemma) --------------
    def tanzil_lemma_count(pred):
        return sum(1 for t in skel_tokens if pred(t))

    R["allah_lemma_incl_basmalahs"] = tanzil_lemma_count(is_allah)
    R["allah_lemma_excl_basmalahs"] = R["allah_lemma_incl_basmalahs"] - 112
    R["rahman_lemma_incl_basmalahs"] = tanzil_lemma_count(is_rahman)
    R["rahman_lemma_excl_basmalahs"] = R["rahman_lemma_incl_basmalahs"] - 112
    R["rahim_lemma_incl_basmalahs"] = tanzil_lemma_count(is_rahim)
    R["rahim_lemma_excl_basmalahs"] = R["rahim_lemma_incl_basmalahs"] - 112
    # tokens in 9:128-129
    s9 = surah_lines(verses, bounds, 9)
    R["surah9_128_tokens_skeleton"] = skeleton(s9[127]).split()
    R["surah9_129_tokens_skeleton"] = skeleton(s9[128]).split()
    R["allah_in_9_128"] = sum(1 for t in skeleton(s9[127]).split()
                              if is_allah(t))
    R["allah_in_9_129"] = sum(1 for t in skeleton(s9[128]).split()
                              if is_allah(t))
    R["rahim_in_9_128"] = sum(1 for t in skeleton(s9[127]).split()
                              if is_rahim(t))
    R["rahim_in_9_129"] = sum(1 for t in skeleton(s9[128]).split()
                              if is_rahim(t))
    R["allah_lemma_excl_basmalahs_minus_9_129"] = (
        R["allah_lemma_excl_basmalahs"] - R["allah_in_9_129"])
    R["rahim_lemma_excl_basmalahs_minus_9_128"] = (
        R["rahim_lemma_excl_basmalahs"] - R["rahim_in_9_128"])
    # QAC lemma counts + verse lists
    def qac_lem_locs(*lems):
        return sorted(loc for loc, rec in words.items()
                      if rec["lems"] & set(lems))
    allah_q = qac_lem_locs("{ll~ah")
    R["allah_qac_lemma_count"] = len(allah_q)
    R["allah_qac_lemma_verses"], R["allah_qac_lemma_per_surah"] = \
        verses_of_word_locs(allah_q)
    R["allah_qac_lemma_verses_scholar_rule"] = [
        v for v in R["allah_qac_lemma_verses"] if v != "9:129"]
    rahman_q = qac_lem_locs("r~aHoma`n")
    R["rahman_qac_lemma_count"] = len(rahman_q)
    R["rahman_qac_lemma_verses"], R["rahman_qac_lemma_per_surah"] = \
        verses_of_word_locs(rahman_q)
    rahim_q = qac_lem_locs("r~aHiym")
    R["rahim_qac_lemma_count"] = len(rahim_q)
    R["rahim_qac_lemma_verses"], R["rahim_qac_lemma_per_surah"] = \
        verses_of_word_locs(rahim_q)
    R["rahim_qac_lemma_verses_scholar_rule"] = [
        v for v in R["rahim_qac_lemma_verses"] if v != "9:128"]
    # union locations for the rahman-57-rahim-115 finding
    union_q = sorted(set(rahman_q) | set(rahim_q))
    R["rahman_rahim_union_verses"], R["rahman_rahim_union_per_surah"] = \
        verses_of_word_locs(union_q)
    R["rahman_rahim_union_verses_scholar_rule"] = [
        v for v in R["rahman_rahim_union_verses"] if v != "9:128"]
    # Allah checksum sums
    def verse_text_excl_basmalah(n, vi, ln):
        if vi == 1 and n not in (1, 9):
            sk = skeleton(ln)
            if sk.startswith("بسم الله الرحمان الرحيم"):
                return sk[len("بسم الله الرحمان الرحيم"):].strip()
        return skeleton(ln)

    sums = {"incl_basmalahs": 0, "excl_basmalahs": 0,
            "excl_basmalahs_and_9_128_129": 0}
    n_verses_incl = n_verses_excl = 0
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            if any(is_allah(t) for t in skeleton(ln).split()):
                sums["incl_basmalahs"] += vi
                n_verses_incl += 1
            txt = verse_text_excl_basmalah(n, vi, ln)
            if any(is_allah(t) for t in txt.split()):
                sums["excl_basmalahs"] += vi
                n_verses_excl += 1
                if not (n == 9 and vi in (128, 129)):
                    sums["excl_basmalahs_and_9_128_129"] += vi
    R["allah_checksum_sums"] = sums
    R["allah_verses_incl_basmalahs"] = n_verses_incl
    R["allah_verses_excl_basmalahs"] = n_verses_excl
    # QAC-based checksum (QAC has no unnumbered basmalahs by construction)
    qac_sum = sum(v for (s, v) in {(s, v) for (s, v, _w) in allah_q})
    R["allah_checksum_qac_lemma_verses"] = qac_sum
    R["allah_checksum_qac_minus_9_129"] = qac_sum - 129

    # ---- ism -----------------------------------------------------------
    def ism_full(tok):
        u = strip_prefixes(tok)
        if u.startswith("ال"):
            u = u[2:]
        return u == "اسم"
    R["ism_full_spelling_count"] = sum(1 for t in skel_tokens if ism_full(t))
    ism_breakdown = Counter()
    for t in skel_tokens:
        if strip_prefixes(t) == "اسم":
            ism_breakdown["bare_ism"] += 1
        elif t == "الاسم":
            ism_breakdown["al_ism"] += 1
        elif strip_prefixes(t) == "اسما":
            ism_breakdown["plural_asma"] += 1
        elif t in {"بسم", "وبسم"}:
            ism_breakdown["contracted_bism"] += 1
    R["ism_breakdown"] = dict(ism_breakdown)
    ism_locs = []
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            if any(ism_full(t) for t in skeleton(ln).split()):
                ism_locs.append(f"{n}:{vi}")
    R["ism_full_spelling_verses"] = ism_locs
    R["ism_full_spelling_per_surah"] = {
        str(s): sum(1 for v in ism_locs if v.startswith(f"{s}:"))
        for s in sorted({int(v.split(":")[0]) for v in ism_locs})}
    ism_q = qac_lem_locs("{som")
    R["ism_qac_lemma_som_count"] = len(ism_q)
    R["ism_qac_lemma_som_verses"], _ = verses_of_word_locs(ism_q)
    # root smw lemma breakdown (what else shares the root)
    R["root_smw_lemma_breakdown"] = dict(Counter(
        rec["stem_lem"] for rec in words.values() if "smw" in rec["roots"]))
    R["root_smw_word_count"] = sum(
        1 for rec in words.values() if "smw" in rec["roots"])

    # ---- first revelation / surah 96 / surah 110 ------------------------
    s96 = surah_lines(verses, bounds, 96)
    R["surah96_verses"] = len(s96)
    R["surah96_first5_words_incl_basmalah"] = len(
        [t for ln in s96[:5] for t in ln.split()])
    R["surah96_first5_words_excl_basmalah"] = (
        R["surah96_first5_words_incl_basmalah"] - 4)
    R["surah96_first5_letters_incl_basmalah"] = sum(
        letter_count(ln) for ln in s96[:5])
    R["surah96_first5_letters_excl_basmalah"] = (
        R["surah96_first5_letters_incl_basmalah"] - 19)
    R["surah96_total_letters_incl_basmalah"] = sum(
        letter_count(ln) for ln in s96)
    R["surah96_total_letters_excl_basmalah"] = (
        R["surah96_total_letters_incl_basmalah"] - 19)
    R["surah96_first5_qac_words"] = sum(
        1 for (s, v, _w) in words if s == 96 and v <= 5)
    R["surah96_qac_words"] = sum(1 for (s, _v, _w) in words if s == 96)
    s110 = surah_lines(verses, bounds, 110)
    R["surah110_verses"] = len(s110)
    R["surah110_words_incl_basmalah"] = len(
        [t for ln in s110 for t in ln.split()])
    R["surah110_words_excl_basmalah"] = R["surah110_words_incl_basmalah"] - 4
    R["surah110_qac_words"] = sum(1 for (s, _v, _w) in words if s == 110)
    R["surah110_verse1_letters_incl_basmalah"] = letter_count(s110[0])
    R["surah110_verse1_letters_excl_basmalah"] = (
        R["surah110_verse1_letters_incl_basmalah"] - 19)

    # ---- min / ma (most frequent words) ---------------------------------
    R["min_tanzil_lemma_count"] = sum(
        1 for t in skel_tokens if strip_prefixes(t) == "من")
    min_breakdown = Counter()
    for t in skel_tokens:
        if strip_prefixes(t) == "من":
            min_breakdown[t] += 1
    R["min_tanzil_breakdown"] = dict(min_breakdown)
    min_q = qac_lem_locs("min")
    R["min_qac_lemma_count"] = len(min_q)
    R["min_qac_lemma_verses"], R["min_qac_lemma_per_surah"] = \
        verses_of_word_locs(min_q)
    R["man_qac_lemma_count"] = len(qac_lem_locs("man"))  # relative pronoun
    ma_q = qac_lem_locs("maA")
    R["ma_qac_lemma_count"] = len(ma_q)
    R["ma_tanzil_lemma_count"] = sum(
        1 for t in skel_tokens if strip_prefixes(t) == "ما")
    R["allahumma_qac_lemma_count"] = len(qac_lem_locs("{ll~ahum~a"))

    # ---- quran word ------------------------------------------------------
    quran_tokens = Counter()
    quran_verses_all = set()
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            for t in skeleton(ln).split():
                if "قران" in t:
                    quran_tokens[t] += 1
                    quran_verses_all.add(f"{n}:{vi}")
    R["quran_substring_token_count"] = sum(quran_tokens.values())
    R["quran_substring_token_breakdown"] = dict(quran_tokens)
    R["quran_substring_verses"] = sorted(
        quran_verses_all, key=lambda r: (int(r.split(":")[0]),
                                         int(r.split(":")[1])))
    narrow = {"القران", "والقران", "بالقران", "قرانا"}
    R["quran_narrow_selection_count"] = sum(
        quran_tokens[t] for t in narrow if t in quran_tokens)
    narrow_verses = set()
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            if any(t in narrow for t in skeleton(ln).split()):
                narrow_verses.add(f"{n}:{vi}")
    R["quran_narrow_selection_verses"] = sorted(
        narrow_verses, key=lambda r: (int(r.split(":")[0]),
                                      int(r.split(":")[1])))
    # Khalifa Table 21 as printed on submission.org/App1_p2.html (66 rows)
    table21 = ["2:185", "4:82", "5:101", "6:19", "7:204", "9:111", "10:37",
               "10:61", "12:2", "12:3", "15:1", "15:87", "15:91", "16:98",
               "17:9", "17:41", "17:45", "17:46", "17:60", "17:78", "17:82",
               "17:88", "17:89", "17:106", "18:54", "20:2", "20:113",
               "20:114", "25:30", "25:32", "27:1", "27:6", "27:76", "27:92",
               "28:85", "30:58", "34:31", "36:2", "36:69", "38:1", "39:27",
               "39:28", "41:3", "41:26", "42:7", "43:3", "43:31", "46:29",
               "47:24", "50:1", "50:45", "54:17", "54:22", "54:32", "54:40",
               "55:2", "56:77", "59:21", "72:1", "73:4", "73:20", "75:17",
               "75:18", "76:23", "84:21", "85:21"]
    R["table21_rows"] = len(table21)
    R["table21_rows_sorted"] = sorted(
        table21, key=lambda r: (int(r.split(":")[0]), int(r.split(":")[1])))
    R["quran_narrow_in_table21"] = sorted(
        set(R["quran_narrow_selection_verses"]) & set(table21),
        key=lambda r: (int(r.split(":")[0]), int(r.split(":")[1])))
    R["quran_narrow_NOT_in_table21"] = sorted(
        set(R["quran_narrow_selection_verses"]) - set(table21),
        key=lambda r: (int(r.split(":")[0]), int(r.split(":")[1])))
    R["table21_NOT_in_narrow"] = sorted(
        set(table21) - set(R["quran_narrow_selection_verses"]),
        key=lambda r: (int(r.split(":")[0]), int(r.split(":")[1])))
    R["quran_allform_NOT_in_table21"] = sorted(
        set(R["quran_substring_verses"]) - set(table21),
        key=lambda r: (int(r.split(":")[0]), int(r.split(":")[1])))
    quran_q = qac_lem_locs("quro'aAn")  # QAC lemma of the noun 'Quran'
    R["quran_qac_lemma_count"] = len(quran_q)
    R["quran_qac_lemma_verses"], R["quran_qac_lemma_per_surah"] = \
        verses_of_word_locs(quran_q)
    # which Table-21 verses contain a quran token of a form OUTSIDE the narrow set
    outside = {}
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            ref = f"{n}:{vi}"
            if ref in table21:
                toks = [t for t in skeleton(ln).split() if "قران" in t]
                if toks and not any(t in narrow for t in toks):
                    outside[ref] = toks
    R["table21_verses_with_only_non_narrow_quran_forms"] = outside
    # 10:15 / 13:31 / 41:44 tokens
    for ref in ("10:15", "13:31", "41:44"):
        s, v = map(int, ref.split(":"))
        ln = surah_lines(verses, bounds, s)[v - 1]
        R[f"tokens_{ref.replace(':', '_')}"] = [
            t for t in skeleton(ln).split() if "قران" in t]

    # ---- root Alh locations ----------------------------------------------
    alh_root_locs = sorted(loc for loc, rec in words.items()
                           if "Alh" in rec["roots"])
    R["root_Alh_verses"], R["root_Alh_per_surah"] = \
        verses_of_word_locs(alh_root_locs)

    # ---- RDS-Q odd/even (C+V parity) --------------------------------------
    # per-verse word counts on Tanzil excl. unnumbered basmalahs
    odd_w = even_w = odd_l = even_l = 0
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            toks = ln.split()
            if vi == 1 and n not in (1, 9):
                toks = toks[4:]
            w = len(toks)
            l = sum(letter_count(t) for t in toks)
            if (n + vi) % 2 == 1:
                odd_w += w
                odd_l += l
            else:
                even_w += w
                even_l += l
    R["rdsq_odd_even_CplusV_words"] = {"odd": odd_w, "even": even_w}
    R["rdsq_odd_even_CplusV_letters"] = {"odd": odd_l, "even": even_l}
    # same split on QAC words (Dukes data)
    qac_per_verse = Counter((s, v) for (s, v, _w) in words)
    odd_q = even_q = 0
    for (s, v), c in qac_per_verse.items():
        if (s + v) % 2 == 1:
            odd_q += c
        else:
            even_q += c
    R["rdsq_odd_even_CplusV_words_qac"] = {"odd": odd_q, "even": even_q}

    # ---- Botani cross-check ----------------------------------------------
    R["botani_verses_6236_plus_112"] = 6236 + 112
    R["botani_words_tanzil_incl_basmalahs"] = R["tanzil_tokens_incl_basmalahs"]
    R["botani_letters_tanzil_incl_basmalahs"] = \
        R["tanzil_letters_incl_basmalahs"]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ---- stdout summary ---------------------------------------------------
    for k in [
        "qac_words", "qac_segments", "tanzil_tokens_incl_basmalahs",
        "tanzil_tokens_excl_basmalahs", "tanzil_letters_incl_basmalahs",
        "tanzil_letters_excl_basmalahs", "unique_surface_raw",
        "unique_surface_skeletonised", "hapax_surface_raw",
        "hapax_surface_skeletonised", "unique_stem_forms_raw",
        "unique_stem_forms_skeletonised", "unique_roots_word_level",
        "unique_roots_segment_level", "unique_lemmas_stem_level",
        "unique_lemmas_word_level_all_segments",
        "unique_lemmas_segment_level", "hapax_stem_lemmas",
        "hapax_roots_word_level", "root_Alh_word_level",
        "root_Alh_segment_level", "root_Hsn_word_level",
        "basmalah_occurrences", "basmalah_letters_1_1",
        "allah_lemma_incl_basmalahs", "allah_lemma_excl_basmalahs",
        "allah_qac_lemma_count", "rahman_lemma_excl_basmalahs",
        "rahman_qac_lemma_count", "rahim_lemma_excl_basmalahs",
        "rahim_qac_lemma_count", "allah_in_9_128", "allah_in_9_129",
        "rahim_in_9_128", "rahim_in_9_129",
        "allah_lemma_excl_basmalahs_minus_9_129",
        "rahim_lemma_excl_basmalahs_minus_9_128",
        "ism_full_spelling_count", "ism_qac_lemma_som_count",
        "surah96_first5_words_excl_basmalah",
        "surah96_first5_words_incl_basmalah",
        "surah96_first5_letters_excl_basmalah",
        "surah96_total_letters_incl_basmalah",
        "surah96_total_letters_excl_basmalah",
        "surah96_first5_qac_words", "surah110_words_excl_basmalah",
        "surah110_qac_words", "surah110_verse1_letters_excl_basmalah",
        "min_tanzil_lemma_count", "min_qac_lemma_count",
        "man_qac_lemma_count", "ma_qac_lemma_count",
        "ma_tanzil_lemma_count", "quran_substring_token_count",
        "quran_narrow_selection_count", "table21_rows",
        "quran_qac_lemma_count",
    ]:
        print(f"{k} = {R[k]}")
    print("allah_checksum_sums =", R["allah_checksum_sums"])
    print("allah_verses_incl/excl =", R["allah_verses_incl_basmalahs"],
          R["allah_verses_excl_basmalahs"])
    print("allah_checksum_qac =", R["allah_checksum_qac_lemma_verses"],
          "minus 9:129 =", R["allah_checksum_qac_minus_9_129"])
    print("ism_breakdown =", R["ism_breakdown"])
    print("root_smw_lemma_breakdown =", R["root_smw_lemma_breakdown"])
    print("quran_substring_breakdown =", R["quran_substring_token_breakdown"])
    print("quran_narrow_NOT_in_table21 =", R["quran_narrow_NOT_in_table21"])
    print("table21_NOT_in_narrow =", R["table21_NOT_in_narrow"])
    print("table21_only_non_narrow =", R["table21_verses_with_only_non_narrow_quran_forms"])
    print("quran_allform_NOT_in_table21 =", R["quran_allform_NOT_in_table21"])
    print("10:15 tokens =", R["tokens_10_15"], "| 13:31 =",
          R["tokens_13_31"], "| 41:44 =", R["tokens_41_44"])
    print("letters_variant_excl_basmalahs =", R["letters_variant_excl_basmalahs"])
    print("mark_counts =", R["mark_counts_incl_basmalahs"])
    print("rdsq_odd_even_CplusV_words =", R["rdsq_odd_even_CplusV_words"])
    print("rdsq_odd_even_CplusV_letters =", R["rdsq_odd_even_CplusV_letters"])
    print("rdsq_odd_even_CplusV_words_qac =", R["rdsq_odd_even_CplusV_words_qac"])
    print("roots_only_at_segment_level =", R["roots_only_at_segment_level"])
    print("roots_segment_gt_word =", R["roots_segment_gt_word"])
    print("top_roots_word =", R["top_roots_word_level"])
    print("top_roots_segment =", R["top_roots_segment_level"])
    print("Wrote", OUT)


if __name__ == "__main__":
    main()

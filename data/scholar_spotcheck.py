#!/usr/bin/env python3
"""
Scholar spot-checks for project miracleMath (Agent 3 — literature/review layer).

Re-counts published Quranic word/letter-count claims against the project's own
Arabic corpus: Tanzil Quran Text, Uthmani script
  ~/workspace/projects/miracle-math/corpus/quran-uthmani.txt

Method notes (important — counts depend on them):
- The file is one verse per line, no surah/ayah numbers, no metadata columns.
  Comment lines starting with '#' and blank lines are dropped; the remaining
  lines are the 6236 verses in mushaf order.
- Surah boundaries are reconstructed from the standard Hafs verse-count table
  (sums to 6236; asserted below). The file itself carries no surah markers.
- Tokens = whitespace-separated words (includes the unnumbered basmalahs,
  which are merged into the first verse of each surah except 1 and 9).
- Matching is done on a "skeleton" form: diacritics/tatweel removed, hamza
  variants normalised (أ إ آ ٱ -> ا, ؤ -> و, ئ -> ي, ء dropped). Crucially,
  Uthmani superscript letters are KEPT as letters: dagger alif ٰ -> ا,
  small waw ۦ -> و, small yeh ۥ -> ي. (Deleting them merges distinct words,
  e.g. ملائكة -> مليكة, and undercounts letters.)
- "Lemma-style" counts strip leading clitics (و ف ب ل ك) before comparing a
  token to a target word, and also handle the elided-alif forms لله / ولله /
  فلله and للرحمن (the alif of الله / الرحمن is dropped after the لـ prefix).
- Nothing here uses any English translation. Arabic original text only.

Usage: python3 scholar_spotcheck.py
"""
import json
import re
from collections import Counter
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "corpus" / "quran-uthmani.txt"

# Standard Hafs verse counts per surah (1..114). Must sum to 6236.
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
# Uthmani superscript letters: dagger alif -> ا for WORD matching (it is the
# alif of e.g. ملائكة, السماوات, الصلوات), small waw U+06E5 -> و, small yeh
# U+06E6 -> ي. (An earlier draft had the two small letters swapped.)
SUPERSCRIPT = str.maketrans({"ٰ": "ا", "ۥ": "و", "ۦ": "ي"})
HAMZA_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ؤ": "و", "ئ": "ي"})
# Letters for COUNTING (Khalifa-consistent convention, validated by the
# 19-letter basmalah, 76 letters in 96:1-5, 19 in 110:1): base letters count,
# including alef wasla (ٱ -> ا); dagger alif and the small waw/yeh are marks
# and do NOT count; standalone hamza ء counts.
LETTER_MARKS = re.compile(r"[ٰۥۦ]")


def strip_diacritics(text: str) -> str:
    """Diacritics removed, but superscript letters kept as letters."""
    return DIACRITICS.sub("", text.translate(SUPERSCRIPT))


def letter_count(text: str) -> int:
    """Count base Arabic letters under the convention above."""
    t = text.translate(HAMZA_MAP)
    t = LETTER_MARKS.sub("", t)
    t = DIACRITICS.sub("", t)
    return sum(1 for c in t if "\u0621" <= c <= "\u064a")


def skeleton(text: str) -> str:
    """Diacritics removed, superscript letters kept, hamza normalised."""
    return strip_diacritics(text).translate(HAMZA_MAP).replace("ء", "")


def strip_prefixes(tok: str) -> str:
    while len(tok) > 1 and tok[0] in "وفبلك":
        tok = tok[1:]
    return tok


def main() -> dict:
    raw_lines = CORPUS.read_text(encoding="utf-8").splitlines()
    verses = [ln for ln in raw_lines if ln.strip() and not ln.lstrip().startswith("#")]
    assert len(SURAH_VERSES) == 114
    assert sum(SURAH_VERSES) == 6236, sum(SURAH_VERSES)

    out = {}
    out["corpus_file"] = str(CORPUS)
    out["raw_lines"] = len(raw_lines)
    out["verse_lines"] = len(verses)
    out["verses_match_6236"] = len(verses) == 6236

    bounds = []
    i = 0
    for n, v in enumerate(SURAH_VERSES, start=1):
        bounds.append((n, i, i + v))
        i += v
    assert i == len(verses)

    def surah_lines(n: int):
        _, a, b = bounds[n - 1]
        return verses[a:b]

    def surah_ref(n: int, vi: int) -> str:
        return f"{n}:{vi}"

    # ---- Whole-corpus totals -------------------------------------------
    tokens = [t for ln in verses for t in ln.split()]
    out["total_whitespace_tokens_incl_basmalahs"] = len(tokens)
    out["total_tokens_excl_unnumbered_basmalahs"] = len(tokens) - 112 * 4
    out["total_arabic_letters_incl_basmalahs"] = sum(
        letter_count(ln) for ln in verses)
    out["total_arabic_letters_excl_unnumbered_basmalahs"] = (
        out["total_arabic_letters_incl_basmalahs"] - 112 * 19)
    skel_tokens = [skeleton(t) for t in tokens]
    surf_raw = Counter(tokens)
    surf_skel = Counter(skel_tokens)
    out["unique_surface_forms_raw"] = len(surf_raw)
    out["unique_surface_forms_skeletonised"] = len(surf_skel)
    out["hapax_surface_forms_raw_occurring_once"] = sum(
        1 for c in surf_raw.values() if c == 1)
    out["top_15_tokens_raw"] = [[w, c] for w, c in surf_raw.most_common(15)]

    def count_exact(targets):
        return sum(1 for t in skel_tokens if t in targets)

    def count_lemma(targets):
        return sum(1 for t in skel_tokens if strip_prefixes(t) in targets)

    def count_substr(pat):
        return sum(1 for t in skel_tokens if pat in t)

    def count_lines_substr(*pats):
        return sum(1 for ln in verses if all(p in skeleton(ln) for p in pats))

    # ---- Basmalah -------------------------------------------------------
    skel_text = skeleton("\n".join(verses))
    out["basmalah_occurrences_whole_text"] = skel_text.count("بسم الله الرحمان الرحيم")
    out["basmalah_letters"] = letter_count(verses[0])
    out["lines_starting_with_basmalah"] = sum(
        1 for ln in verses if skeleton(ln).startswith("بسم الله"))
    out["lines_containing_basmalah_not_at_start"] = sum(
        1 for ln in verses
        if "بسم الله الرحمان الرحيم" in skeleton(ln)
        and not skeleton(ln).startswith("بسم الله"))

    # ---- Allah / basmalah words (Khalifa / Yuksel) ----------------------
    def is_allah(tok: str) -> bool:
        # All forms of the name, including the oath تالله / وتالله and the
        # interrogative أبالله (these are what reconciles the classical 2699
        # with the lemma count once unnumbered basmalahs are excluded).
        if tok in {"تالله", "وتالله", "ابالله"}:
            return True
        t = tok
        while t and t[0] in "وف":
            t = t[1:]
        if t == "لله":
            return True
        return strip_prefixes(t) == "الله"

    out["allah_lemma_count"] = sum(1 for t in skel_tokens if is_allah(t))
    out["allah_lemma_count_excl_unnumbered_basmalahs"] = (
        out["allah_lemma_count"] - 112)
    out["allah_strict_surface_count"] = count_exact({"الله"})
    out["allahumma_count"] = count_substr("اللهم")
    out["tallah_oath_count"] = count_exact({"تالله", "وتالله"})

    def is_rahman(tok: str) -> bool:
        t = tok
        while t and t[0] in "وف":
            t = t[1:]
        if t == "للرحمان":
            return True
        return strip_prefixes(t) == "الرحمان"

    out["rahman_lemma_count"] = sum(1 for t in skel_tokens if is_rahman(t))
    out["rahman_lemma_count_excl_unnumbered_basmalahs"] = (
        out["rahman_lemma_count"] - 112)
    out["rahim_lemma_count"] = count_lemma({"الرحيم", "رحيم", "رحيما"})
    out["rahim_lemma_count_excl_unnumbered_basmalahs"] = (
        out["rahim_lemma_count"] - 112)
    out["rahim_count_excl_surah9_128"] = out["rahim_lemma_count"] - sum(
        1 for t in [skeleton(t) for t in surah_lines(9)[127].split()]
        if strip_prefixes(t) in {"الرحيم", "رحيم", "رحيما"})
    out["ism_full_spelling_count"] = sum(
        1 for t in skel_tokens
        if (lambda u: u == "اسم")(
            strip_prefixes(t)[2:] if strip_prefixes(t).startswith("ال")
            else strip_prefixes(t)))
    out["ism_breakdown"] = {
        "bare_ism": sum(1 for t in skel_tokens if strip_prefixes(t) == "اسم"),
        "al_ism": count_exact({"الاسم"}),
        "plural_asma_skeletonised": sum(
            1 for t in skel_tokens if strip_prefixes(t) == "اسما"),
    }
    out["ism_contracted_bism_count"] = sum(
        1 for t in skel_tokens if t in {"بسم", "وبسم"})
    # Verses containing Allah (lemma), and Khalifa's verse-number checksum,
    # both unweighted (once per verse) and occurrence-weighted.
    allah_verses = []
    allah_occ_weighted_sum = 0
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            occ = sum(1 for t in ln.split() if is_allah(skeleton(t)))
            if occ:
                allah_verses.append((n, vi))
                allah_occ_weighted_sum += occ * vi
    out["verses_containing_allah_lemma"] = len(allah_verses)
    out["sum_of_verse_numbers_containing_allah"] = sum(v for _, v in allah_verses)
    out["occurrence_weighted_sum_of_verse_numbers_allah"] = allah_occ_weighted_sum
    # Same, but excluding the 112 unnumbered opening basmalahs (the QAC
    # convention behind the published "1,821 verses" figure): strip a leading
    # basmalah from verse 1 of every surah except 1 (where it IS verse 1)
    # and 9 (which has none).
    def verse_text_excl_basmalah(n, vi, ln):
        if vi == 1 and n not in (1, 9):
            sk = skeleton(ln)
            if sk.startswith("بسم الله الرحمان الرحيم"):
                return sk[len("بسم الله الرحمان الرحيم"):].strip()
        return skeleton(ln)

    allah_verses_excl = []
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            txt = verse_text_excl_basmalah(n, vi, ln)
            if any(is_allah(t) for t in txt.split()):
                allah_verses_excl.append((n, vi))
    out["verses_containing_allah_excl_unnumbered_basmalahs"] = len(allah_verses_excl)
    out["sum_of_verse_numbers_allah_excl_unnumbered_basmalahs"] = sum(
        v for _, v in allah_verses_excl)
    # Khalifa's checksum also drops his two rejected verses 9:128-129
    # (only 9:129 contains Allah, verse number 129).
    out["sum_of_verse_numbers_allah_excl_basmalahs_and_9_128_129"] = sum(
        v for (n, v) in allah_verses_excl if not (n == 9 and v in (128, 129)))

    # ---- First / last revelation (Khalifa "simple facts") ---------------
    def words_of(lines):
        return [t for ln in lines for t in ln.split()]

    def letters_of(lines):
        return sum(letter_count(ln) for ln in lines)

    basmalah_letters = letter_count(verses[0])

    s96 = surah_lines(96)
    out["surah96_verses"] = len(s96)
    out["surah96_first5_words_incl_basmalah"] = len(words_of(s96[:5]))
    out["surah96_first5_words_excl_basmalah"] = (
        out["surah96_first5_words_incl_basmalah"] - 4)
    out["surah96_first5_letters_incl_basmalah"] = letters_of(s96[:5])
    out["surah96_first5_letters_excl_basmalah"] = (
        out["surah96_first5_letters_incl_basmalah"] - basmalah_letters)
    out["surah96_total_letters"] = letters_of(s96)
    s110 = surah_lines(110)
    out["surah110_words_incl_basmalah"] = len(words_of(s110))
    out["surah110_words_excl_basmalah"] = out["surah110_words_incl_basmalah"] - 4
    out["surah110_verse1_letters_incl_basmalah"] = letters_of(s110[:1])
    out["surah110_verse1_letters_excl_basmalah"] = (
        out["surah110_verse1_letters_incl_basmalah"] - basmalah_letters)
    out["surah110_verses"] = len(s110)
    out["surah96_first5_tokens_excl_basmalah"] = words_of(s96[:5])[4:]

    # ---- Most frequent word: min (wordsofquran: 3226) -------------------
    out["min_lemma_count"] = count_lemma({"من"})
    out["min_strict_count"] = count_exact({"من"})

    # ---- Classic paired counts (Harun Yahya list and others) ------------
    # yawm: simple forms only, then + prefixed forms (the 365 reconstruction)
    out["yawm_simple_forms_exact"] = count_exact({"يوم", "اليوم", "يوما"})
    out["yawm_simple_plus_prefixed"] = count_exact({
        "يوم", "اليوم", "يوما", "ويوم", "واليوم", "ليوم", "فاليوم",
        "بيوم", "باليوم", "وباليوم"})
    out["yawm_all_tokens_containing_yawm_substr"] = count_substr("يوم")
    out["shahr_simple_forms_exact"] = count_exact({"شهر", "الشهر", "شهرا"})
    out["shahr_simple_plus_prefixed"] = count_exact({
        "شهر", "الشهر", "شهرا", "بالشهر", "والشهر"})
    out["shahr_all_tokens_containing_shahr"] = count_substr("شهر")
    out["dunya_substr"] = count_substr("دنيا")
    out["akhira_substr"] = count_substr("اخرة")
    out["jannah_strict"] = sum(
        1 for t in skel_tokens if strip_prefixes(t) in {"الجنة", "جنة"})
    out["jannah_substr_janna"] = count_substr("جنة")
    out["jahannam_substr"] = count_substr("جهنم")
    out["shaytan_substr"] = sum(
        1 for t in skel_tokens if ("شيط" in t or "شياط" in t))
    out["shaytan_singular_substr"] = count_substr("شيط")
    out["shaytan_plural_substr"] = count_substr("شياط")
    out["angel_malaika_substr"] = count_substr("ملايك")
    out["angel_singular_malak_exact"] = sum(
        1 for t in skel_tokens if strip_prefixes(t) in {"ملك", "الملك"})
    out["hayat_hayw_substr"] = count_substr("حيو")
    out["hayat_family_hayw_hayy_haya"] = sum(
        1 for t in skel_tokens
        if any(p in t for p in ("حيو", "حيي", "حيا")))
    out["hayat_noun_alhayat"] = count_exact({"الحيواة", "حيواة"})
    out["mawt_substr"] = count_substr("موت")
    out["mawt_family"] = sum(
        1 for t in skel_tokens
        if ("موت" in t or "ميت" in t
            or ("مات" in t and "ظلم" not in t and "كلم" not in t)))
    out["mawt_family_excl_darkness_false_positives"] = out["mawt_family"]
    out["mawt_noun_almawt"] = count_exact({"الموت", "موت"})
    out["mawt_tokens_breakdown"] = [
        [w, c] for w, c in Counter(
            t for t in skel_tokens
            if ("موت" in t or "ميت" in t
                or ("مات" in t and "ظلم" not in t and "كلم" not in t))).most_common(12)]
    out["rajul_substr_all"] = count_substr("رجل")
    out["rajul_man_singular"] = count_exact(
        {"رجل", "رجلا", "لرجل", "فرجل", "ورجلا"})
    out["rajul_man_all_singular_dual_plural"] = sum(
        1 for t in skel_tokens
        if strip_prefixes(t) in {"رجل", "رجلا", "رجلين", "رجلان"})
    out["rajul_foot_forms"] = sum(
        1 for t in skel_tokens if "رجل" in t and "ارجل" in t)
    out["imraa_substr_all"] = count_substr("امرا")
    out["imraa_man_word_count"] = count_exact({"امرا"})
    out["woman_singular"] = sum(
        1 for t in skel_tokens
        if strip_prefixes(t) in {"امراة", "امرات", "امراتهي", "امراتهو",
                                 "امراتك", "امراتى"})
    out["woman_all_singular_dual"] = out["woman_singular"] + count_exact(
        {"امراتان", "وامراتان", "امراتين"})
    out["shams_substr"] = count_substr("شمس")
    out["qamar_substr"] = count_substr("قمر")
    out["bahr_substr_all"] = count_substr("بحر")
    out["bahr_singular_definite"] = count_exact({"البحر", "والبحر"})
    out["barr_land_exact"] = sum(
        1 for t in skel_tokens if strip_prefixes(t) in {"بر", "البر"})
    out["salawat_substr_all"] = count_substr("صلوات")
    # Verses containing a صلوات token, with refs (to separate plural صلوات
    # from singular صلاة, which shares the Uthmani spelling).
    salawat_refs = []
    for n, a, b in bounds:
        for vi, ln in enumerate(verses[a:b], start=1):
            if any("صلوات" in skeleton(t) for t in ln.split()):
                salawat_refs.append(surah_ref(n, vi))
    out["salawat_token_verse_refs"] = salawat_refs
    out["quran_word_substr"] = count_substr("قران")
    out["quran_word_khalifa_selection"] = count_exact(
        {"القران", "والقران", "بالقران", "قرانا"})
    out["muhammad_substr"] = count_substr("محمد")
    out["seven_heavens_samawat_lines"] = count_lines_substr("سبع", "سماوات")
    out["seven_paths_lines"] = count_lines_substr("سبع", "طرايق")
    out["seven_strong_lines"] = count_lines_substr("سبع", "شداد")

    # ---- Per-surah letter counts (Khalifa's initials) -------------------
    def letter_count_in_surah(n, letter):
        return sum(strip_diacritics(ln).count(letter) for ln in surah_lines(n))

    out["qaf_count_surah50"] = letter_count_in_surah(50, "ق")
    out["qaf_count_surah42"] = letter_count_in_surah(42, "ق")
    out["nun_count_surah68"] = letter_count_in_surah(68, "ن")
    out["sad_count_surah38"] = letter_count_in_surah(38, "ص")
    out["sad_count_surah7"] = letter_count_in_surah(7, "ص")
    out["sad_count_surah19"] = letter_count_in_surah(19, "ص")
    out["sad_total_7_19_38"] = (out["sad_count_surah7"] + out["sad_count_surah19"]
                                + out["sad_count_surah38"])
    # 7:69 spelling check (Khalifa's Sad count depends on it)
    out["surah7_verse69_skeleton"] = skeleton(surah_lines(7)[68])

    # ---- Two verses said to contain all 28 letters ---------------------
    def distinct_letters(line):
        s = skeleton(line).replace("ة", "ه").replace("ى", "ي")
        return {c for c in s if "\u0621" <= c <= "\u064a"}

    ref28 = set("ابتثجحخدرزسشصضطظعغفقكلمنهوي")
    out["surah3_verse154_distinct_letters"] = len(distinct_letters(surah_lines(3)[153]))
    out["surah48_verse29_distinct_letters"] = len(distinct_letters(surah_lines(48)[28]))
    out["surah3_verse154_missing_letters"] = sorted(
        ref28 - distinct_letters(surah_lines(3)[153]))
    out["surah48_verse29_missing_letters"] = sorted(
        ref28 - distinct_letters(surah_lines(48)[28]))

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


if __name__ == "__main__":
    main()

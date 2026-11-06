#!/usr/bin/env python3
"""
root_counts_script.py -- miracleMath (Agent 1: root-word counts & paired relationships)

Counts occurrences of paired concepts in the Quranic Arabic Corpus (QAC),
morphology v0.4, matched by ROOT: (preferred) and cross-checked by LEM:.
Display Arabic is taken byte-for-byte from the Tanzil Uthmani text at the
same surah:verse (never retyped).

Primary source (QAC morphology v0.4):
  corpus/quranic-corpus-morphology-0.4.txt
  SHA-256 a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46
  6,309,503 bytes, 128,276 lines, 128,219 data lines = 77,429 words,
  6,236 verses, 114 surahs.
  HOW OBTAINED (honest record): corpus.quran.com's official download page
  serves v0.4 only behind an email form and publishes no direct file URL;
  the Java API (JQuranTree) is a Java library, not a REST API, so there is
  no live endpoint to query from here. This file was fetched from the
  textminingthequran.com mirror of the identical v0.4 file and verified
  against the corpus's own published figures (128,276 lines; 77,429 words;
  header copyright block verbatim). It was NOT downloaded directly from
  corpus.quran.com.

Cross-check source (display Arabic + totals):
  corpus/quran-uthmani.txt (Tanzil Quran Text, Uthmani script)
  SHA-256 ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af
  1,334,737 bytes; lines 0-6235 are the 6,236 verses in order.

Counting unit: one QAC *word* = one (surah, verse, word) location. A word
may have several segments (prefix + stem + suffix); a word is counted once
even if several of its segments carry the root. QAC's basmalah handling:
only Surah 1 verse 1 (the basmalah as a verse) is in the QAC word list;
the basmalahs prepended to the first verse of the other 112 surahs in the
Tanzil file are NOT QAC words, so QAC-based counts exclude them.

Usage:
  python3 root_counts_script.py [--qac PATH] [--tanzil PATH] [--out PATH]
Writes root_counts.json next to this script (or to --out) and prints a
summary plus a DIAGNOSTICS section (ambiguous cases, alignment audit).
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_QAC = HERE.parent / "corpus" / "quranic-corpus-morphology-0.4.txt"
DEFAULT_TANZIL = HERE.parent / "corpus" / "quran-uthmani.txt"
DEFAULT_OUT = HERE / "root_counts.json"

# Standard ayah counts per surah, in order (verified below to sum to 6236).
# CORRECTION (2026-11-06): the table supplied with the task had Surahs 5
# and 6 transposed (165, 120). The standard counts are 5:120, 6:165 --
# confirmed against the QAC file itself (max verse per surah: 5->120,
# 6->165). The sum is 6236 either way, so the swap only showed up in the
# verse-alignment audit (phantom 5:121-165, shifted Surah 6 refs).
AYAH_COUNTS = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52,
    99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34,
    30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18,
    45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30,
    52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19, 36, 25, 22,
    17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4,
    7, 3, 6, 3, 5, 4, 5, 6]

ROOT_RE = re.compile(r"ROOT:([^|]+)")
LEM_RE = re.compile(r"LEM:([^|]+)")
LOC_RE = re.compile(r"\((\d+):(\d+):(\d+):(\d+)\)")

# Verses where ROOT:Hyy LEM yasotaHoYi.^ means "to be shy" (excluded from
# the broad "life" family); the other occurrences mean "to spare alive".
SHY_VERSES = {(2, 26), (33, 53)}
# 29:20 "al-nash'a al-akhira" = "the latter creation", not the Hereafter.
# It is inside the 115 al-akhira forms; flagged, not removed from the
# primary count (see notes).
AKHIRA_LATTER_VERSE = (29, 20)


def parse_qac(path):
    """Return (words, n_segments). words: (s,v,w) -> dict with
    roots, lems, stem_forms (Buckwalter), segments."""
    words = {}
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
                "segments": []})
            rec["segments"].append((form, feats))
            n_seg += 1
            r = ROOT_RE.search(feats)
            if r:
                rec["roots"].add(r.group(1))
            l = LEM_RE.search(feats)
            if l:
                rec["lems"].add(l.group(1))
            if feats.startswith("STEM|"):
                rec["stem_forms"].append(form)
    return words, n_seg


def load_tanzil(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    verses = lines[:6236]
    # line index -> (surah, ayah)
    vmap = {}
    idx = 0
    for s, n in enumerate(AYAH_COUNTS, start=1):
        for a in range(1, n + 1):
            vmap[idx] = (s, a)
            idx += 1
    assert idx == 6236, f"ayah-count table sums to {idx}, expected 6236"
    assert len(verses) == 6236
    return verses, vmap


def tanzil_token_index(s, v, w):
    """0-based whitespace-token index of QAC word w in its Tanzil verse line.
    Tanzil prepends the 4-word basmalah to verse 1 of every surah except 9;
    QAC does not contain those basmalah words."""
    if v == 1 and s > 1 and s != 9:
        return w - 1 + 4
    return w - 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qac", default=str(DEFAULT_QAC))
    ap.add_argument("--tanzil", default=str(DEFAULT_TANZIL))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    words, n_seg = parse_qac(args.qac)
    verses, vmap = load_tanzil(args.tanzil)
    inv_vmap = {v: k for k, v in vmap.items()}

    n_words = len(words)
    n_verses = len({(s, v) for (s, v, _w) in words})
    n_surahs = len({s for (s, _v, _w) in words})
    tanzil_tokens = sum(len(v.split()) for v in verses)

    # ---- alignment audit: QAC words per verse vs Tanzil tokens (basmalah-adjusted)
    qac_per_verse = collections.Counter((s, v) for (s, v, _w) in words)
    mismatches = []
    for li, line in enumerate(verses):
        s, a = vmap[li]
        expect = len(line.split()) - (4 if (a == 1 and s > 1 and s != 9) else 0)
        got = qac_per_verse.get((s, a), 0)
        if got != expect:
            mismatches.append({"surah": s, "ayah": a, "qac_words": got,
                               "tanzil_tokens_adj": expect,
                               "diff_qac_minus_tanzil": got - expect})
    total_diff = sum(m["diff_qac_minus_tanzil"] for m in mismatches)

    # Basmalah lines in Tanzil: verse 1 of every surah except 9. Match
    # diacritic-insensitively: Surahs 95 and 97 spell it with a doubled ba.
    _bd = re.compile(r"[\u064B-\u065F\u0670\u0640\u06D6-\u06DC\u06DF-\u06E4"
                     r"\u06E5-\u06E8\u06EA-\u06ED]")
    n_basmalah_lines = 0
    for li, line in enumerate(verses):
        s, a = vmap[li]
        if a == 1 and s > 1 and s != 9 and _bd.sub("", line).startswith("بسم"):
            n_basmalah_lines += 1
    basmalah_tokens = 4 * n_basmalah_lines

    def tanzil_token(loc):
        """Arabic token (byte-for-byte from Tanzil) for a QAC word, or None."""
        s, v, w = loc
        li = inv_vmap.get((s, v))
        if li is None:
            return None, None
        toks = verses[li].split()
        ti = tanzil_token_index(s, v, w)
        if 0 <= ti < len(toks):
            return toks[ti], verses[li]
        return None, verses[li]

    # ---- concept matchers: each takes a word record + location, returns bool
    def has_root(rec, *roots):
        return bool(rec["roots"] & set(roots))

    def has_lem(rec, *lems):
        return bool(rec["lems"] & set(lems))

    def stem_match(rec, pred):
        return any(pred(f) for f in rec["stem_forms"])

    CONCEPTS = {
        # id: (matcher, qac roots cited, qac lems cited)
        "jannah": (
            lambda rec, loc: has_lem(rec, "jan~ap"),
            ["jnn"], ["jan~ap"]),
        "jahannam": (
            lambda rec, loc: has_lem(rec, "jahan~am"),
            [], ["jahan~am"]),  # proper noun: no ROOT in QAC, LEM only
        "nar": (
            lambda rec, loc: has_lem(rec, "naAr"),
            ["nwr"], ["naAr"]),
        "dunya": (
            lambda rec, loc: has_lem(rec, "d~unoyaA"),
            ["dnw"], ["d~unoyaA"]),
        "akhira": (
            lambda rec, loc: stem_match(
                rec, lambda f: f in ("'aAxirapi", "'aAxirapa", "'aAxirapu")),
            ["Axr"], ["A^xir"]),
        "life_noun": (
            lambda rec, loc: has_lem(rec, "Hayaw`p"),
            ["Hyy"], ["Hayaw`p"]),
        "life_broad": (
            lambda rec, loc: (
                has_lem(rec, "Hayaw`p", "Hay~", ">aHoyaA", "HaY~a",
                        "m~aHoyaA", "muHoY", "HayawaAn")
                or (has_lem(rec, "yasotaHoYi.^")
                    and (loc[0], loc[1]) not in SHY_VERSES)),
            ["Hyy"],
            ["Hayaw`p", "Hay~", ">aHoyaA", "HaY~a", "m~aHoyaA", "muHoY",
             "HayawaAn", "yasotaHoYi.^ (spare-alive senses only)"]),
        "death_noun": (
            lambda rec, loc: has_lem(rec, "mawot"),
            ["mwt"], ["mawot"]),
        "death_broad": (
            lambda rec, loc: has_root(rec, "mwt"),
            ["mwt"], ["mawot", "m~aAta", "m~ay~it", ">amaAta", "mayotap",
                      "m~ayot", "mamaAt", "mawotat"]),
        "angels": (
            lambda rec, loc: has_lem(rec, "malak") and stem_match(
                rec, lambda f: ("}ika" in f)
                or re.match(r"^m~?alak", f) is not None),
            ["mlk"], ["malak"]),
        "devils": (
            lambda rec, loc: has_root(rec, "$Tn"),
            ["$Tn"], ["$ayoTa`n"]),
        "belief": (
            lambda rec, loc: has_lem(rec, "'aAmana", "mu&omin", "<iyma`n",
                                     "m~u&omina`t", "m~u&ominap"),
            ["Amn"],
            ["'aAmana", "mu&omin", "<iyma`n", "m~u&omina`t", "m~u&ominap"]),
        "disbelief": (
            lambda rec, loc: has_root(rec, "kfr") and not has_lem(
                rec, "kaf~ara", "kaf~a`rap"),
            ["kfr"],
            ["kafara", "ka`firuwn", "kufor", "kaAfir", "kafuwr", "kaf~aAr",
             "kufuwr", "kaAfirap", "kuforaAn", "kawaAfir", "kaAfuwr",
             ">akofara"]),
        "reward": (
            lambda rec, loc: has_lem(rec, ">ajor"),
            ["Ajr"], [">ajor"]),
        "punishment": (
            lambda rec, loc: has_root(rec, "E*b"),
            ["E*b"], ["Ea*aAb", "Ea*~aba", "muEa*~ib", "Ea*ob",
                      "muEa*~abiyn"]),
        "punishment_noun": (
            lambda rec, loc: has_lem(rec, "Ea*aAb"),
            ["E*b"], ["Ea*aAb"]),
        "day": (
            lambda rec, loc: has_root(rec, "ywm")
            or has_lem(rec, "yawoma}i*"),
            ["ywm"], ["yawom", "yawoma}i*"]),
        "night": (
            lambda rec, loc: has_root(rec, "lyl"),
            ["lyl"], ["layol", "layolap"]),
        "sun": (
            lambda rec, loc: has_root(rec, "$ms"),
            ["$ms"], ["$amos"]),
        "moon": (
            lambda rec, loc: has_root(rec, "qmr"),
            ["qmr"], ["qamar"]),
        "man": (
            lambda rec, loc: has_lem(rec, "rajul", "rijaAl"),
            ["rjl"], ["rajul", "rijaAl"]),
        "woman": (
            lambda rec, loc: has_lem(rec, "{mora>at", "nisaA^'"),
            ["mrA", "nsw"], ["{mora>at", "nisaA^'"]),
        "love": (
            lambda rec, loc: has_root(rec, "Hbb") and not has_lem(
                rec, "Hab~", "Hab~ap"),
            ["Hbb"],
            [">aHobabo", "Hub~", "{sotaHab~u", ">aHab~", ">aHib~a`^&",
             "maHab~ap", "Hab~aba"]),
        "hate": (
            lambda rec, loc: has_lem(rec, "kariha", "ka`rihuwn",
                                     "makoruwh", "kar~aha")
            or (has_lem(rec, "kuroh") and loc == (2, 216, 5)),
            ["krh"], ["kariha", "ka`rihuwn", "makoruwh", "kar~aha",
                      "kuroh (only 2:216 'fighting is hateful to you')"]),
        "rich": (
            lambda rec, loc: has_lem(rec, "ganiY~"),
            ["gny"], ["ganiY~"]),
        "poor": (
            lambda rec, loc: has_root(rec, "fqr"),
            ["fqr"], ["faqiyr", "faqor", "faAqirap"]),
        "good": (
            lambda rec, loc: has_lem(rec, "xayor", "xayora`t"),
            ["xyr"], ["xayor", "xayora`t"]),
        "evil": (
            lambda rec, loc: has_lem(rec, "$ar~"),
            ["$rr"], ["$ar~"]),
        "allah": (
            lambda rec, loc: has_lem(rec, "{ll~ah"),
            ["Alh"], ["{ll~ah"]),
        "allahumma": (
            lambda rec, loc: has_lem(rec, "{ll~ahum~a"),
            ["Alh"], ["{ll~ahum~a"]),
        "ilah": (
            lambda rec, loc: has_lem(rec, "<ila`h"),
            ["Alh"], ["<ila`h"]),
        # extras
        "jinn": (
            lambda rec, loc: has_lem(rec, "jin~", "jin~ap", "jaA^n~"),
            ["jnn"], ["jin~", "jin~ap", "jaA^n~"]),
        "sky": (
            lambda rec, loc: has_lem(rec, "samaA^'"),
            ["smw"], ["samaA^'"]),
        "thawab_noun": (
            lambda rec, loc: has_lem(rec, "vawaAb"),
            ["vwb"], ["vawaAb"]),
        "miskin": (
            lambda rec, loc: has_lem(rec, "misokiyn"),
            ["skn"], ["misokiyn"]),
    }

    # ---- count every concept; collect matched locations + Tanzil surface forms
    results = {}
    diagnostics = {"root_lemma_breakdowns": {}, "alignment_mismatches": mismatches,
                   "alignment_total_diff_qac_minus_tanzil": total_diff}
    for cid, (matcher, _roots, _lems) in CONCEPTS.items():
        locs = sorted(loc for loc, rec in words.items() if matcher(rec, loc))
        surf = collections.Counter()
        unaligned = []
        for loc in locs:
            tok, _verse = tanzil_token(loc)
            if tok is None:
                unaligned.append(loc)
            else:
                surf[tok] += 1
        # lemma/root breakdown of the matched words
        lem_c = collections.Counter()
        root_c = collections.Counter()
        for loc in locs:
            rec = words[loc]
            for l in rec["lems"]:
                lem_c[l] += 1
            for r in rec["roots"]:
                root_c[r] += 1
        results[cid] = {"count": len(locs), "locations": locs,
                        "surface_forms": dict(surf), "unaligned": unaligned,
                        "lemma_breakdown": dict(lem_c),
                        "root_breakdown": dict(root_c)}
        diagnostics["root_lemma_breakdowns"][cid] = {
            "lemmas": dict(lem_c), "roots": dict(root_c)}

    def refs(cid, n=3):
        # First occurrence in each of the first n distinct verses, so the
        # examples are spread out instead of three words from one verse.
        out = []
        seen_verses = set()
        for loc in results[cid]["locations"]:
            if (loc[0], loc[1]) in seen_verses:
                continue
            seen_verses.add((loc[0], loc[1]))
            s, v, w = loc
            tok, verse = tanzil_token(loc)
            out.append({"surah": s, "ayah": v, "qac_location": f"{s}:{v}:{w}",
                        "arabic": tok, "verse_arabic": verse})
            if len(out) >= n:
                break
        return out

    def side(cid, term_en, term_ar, root_note, notes):
        r = results[cid]
        return {"term_en": term_en, "term_ar": term_ar,
                "qac_root": CONCEPTS[cid][1], "qac_lemmas": CONCEPTS[cid][2],
                "root_note": root_note, "count": r["count"],
                "refs": refs(cid),
                "surface_forms_tanzil": r["surface_forms"],
                "lemma_breakdown": r["lemma_breakdown"], "notes": notes}

    def ratio(a, b):
        return round(a / b, 2) if b else None

    pairs = [
        {"id": "heaven_hell", "label_en": "Heaven / Hell",
         "label_ar": "الجنة / جهنم",
         "a": side("jannah", "heaven (Garden)", "الجنة", "ROOT jnn, LEM jan~ap",
                   "Garden only. Same root jnn also gives jinn (39 words), "
                   "madness/possession (majnun, 11), shield (junnah, 2), "
                   "fetuses (ajinnah, 1) and the verb janna 'night covered' "
                   "(1) -- all excluded via LEM."),
         "b": side("jahannam", "Hell (Jahannam)", "جهنم",
                   "proper noun: no ROOT in QAC; LEM jahan~am",
                   "Unambiguous proper name of Hell."),
         "ratio": ratio(results["jannah"]["count"], results["jahannam"]["count"]),
         "ratio_str": f"{results['jannah']['count']}:{results['jahannam']['count']}",
         "notes": "Secondary hell-word: nar (fire), "
                  f"{results['nar']['count']} -- see extras. "
                  "Jannah 147 is the figure most often quoted; it reproduces "
                  "exactly here (singular + plural garden, LEM jan~ap)."},
        {"id": "heaven_hell_fire", "label_en": "Heaven / Hell-fire (nar)",
         "label_ar": "الجنة / النار",
         "a": side("jannah", "heaven (Garden)", "الجنة", "ROOT jnn, LEM jan~ap",
                   "As above."),
         "b": side("nar", "fire / Hell-fire", "النار", "ROOT nwr, LEM naAr",
                   "All nar words: Hell-fire AND literal fire (e.g. Moses' "
                   "fire, 20:10; the fire of this world). QAC's LEM naAr "
                   "does not separate the senses, so 145 is the combined "
                   "count; jahannam (77) is the unambiguous Hell count."),
         "ratio": ratio(results["jannah"]["count"], results["nar"]["count"]),
         "ratio_str": f"{results['jannah']['count']}:{results['nar']['count']}",
         "notes": "Tanzil surface check agrees exactly: 145 نار tokens "
                  "once the vocative يَٰنَارُ ('O Fire!', 21:69) is counted."},
        {"id": "world_hereafter", "label_en": "This world / Hereafter",
         "label_ar": "الدنيا / الآخرة",
         "a": side("dunya", "this world", "الدنيا", "ROOT dnw, LEM d~unoyaA",
                   "All 115 are al-dunya. Same root also gives adna "
                   "(nearest/lower, 12), daniyah (near, 3), dana (drew "
                   "near, 2) -- excluded via LEM."),
         "b": side("akhira", "the Hereafter", "الآخرة",
                   "ROOT Axr, LEM A^xir, feminine al-akhira forms only",
                   "115 al-akhira forms. One of them (29:20, al-nash'a "
                   "al-akhira, 'the latter creation') means 'latter', not "
                   "the Hereafter, so the strict hereafter-sense count is "
                   "114. Masculine al-akhir ('the Last / the other') and "
                   "plural akhirun/ukhar are excluded via FORM."),
         "ratio": ratio(results["dunya"]["count"], results["akhira"]["count"]),
         "ratio_str": f"{results['dunya']['count']}:{results['akhira']['count']}",
         "notes": "Exact 115 : 115 tie -- the famous pairing reproduces "
                  "exactly on QAC root/lemma matching."},
        {"id": "life_death", "label_en": "Life / Death",
         "label_ar": "الحياة / الموت",
         "a": side("life_noun", "life", "الحياة", "ROOT Hyy, LEM Hayaw`p",
                   "Noun al-hayah only. Broad Hyy family (life_broad) = "
                   f"{results['life_broad']['count']}: noun + hayy (living, "
                   "incl. the divine name al-Hayy) + ahya verbs (give life) "
                   "+ mahya (my living) + hayawan (the true life, 29:64) + "
                   "yastahyi 'spare alive' (6). Excluded: greeting (hayya, "
                   "tahiyyah), shyness (yastahyi 2:26, 33:53; istihya' 28:25) "
                   "and hayyah 'snake' (20:20)."),
         "b": side("death_noun", "death", "الموت", "ROOT mwt, LEM mawot",
                   "Noun al-mawt only. Broad mwt family (death_broad) = "
                   f"{results['death_broad']['count']}: noun + amata "
                   "(cause to die) + mayyit (dead) + maytah (carrion) + "
                   "mamat (death)."),
         "ratio": ratio(results["life_noun"]["count"], results["death_noun"]["count"]),
         "ratio_str": f"{results['life_noun']['count']}:{results['death_noun']['count']}",
         "notes": "Life-broad vs death-broad: "
                  f"{results['life_broad']['count']} : "
                  f"{results['death_broad']['count']}. The widely quoted "
                  "145 : 145 for life/death does NOT reproduce under any "
                  "clean QAC rule (noun 76 : 50; whole-root 184 : 165; "
                  "broad families as defined here "
                  f"{results['life_broad']['count']} : "
                  f"{results['death_broad']['count']}). See VERIFICATION.md."},
        {"id": "angels_devils", "label_en": "Angels / Devils",
         "label_ar": "الملائكة / الشياطين",
         "a": side("angels", "angels", "الملائكة", "ROOT mlk, LEM malak",
                   "73 plural mala'ikah + 15 singular malak (incl. dual "
                   "al-malakayn, the two angels, 2:102, and collective "
                   "singulars 69:17, 89:22). Same root mlk also gives mulk "
                   "(dominion, 48), malik (king, 15), malakut (kingdom, 4) "
                   "-- excluded by FORM (malik/mulk) and LEM (malakato is "
                   "the verb 'to own')."),
         "b": side("devils", "devils (shayatin)", "الشياطين",
                   "ROOT $Tn (QAC root for shaytan is sh-T-n, not sh-y-T), "
                   "LEM $ayoTa`n",
                   "Singular shaytan + plural shayatin, all senses (the "
                   "Devil and devils). QAC tags shaytan as a proper noun "
                   "with ROOT $Tn."),
         "ratio": ratio(results["angels"]["count"], results["devils"]["count"]),
         "ratio_str": f"{results['angels']['count']}:{results['devils']['count']}",
         "notes": "Angels 88 : devils "
                  f"{results['devils']['count']}."},
        {"id": "belief_disbelief", "label_en": "Belief / Disbelief",
         "label_ar": "الإيمان / الكفر",
         "a": side("belief", "belief / faith", "الإيمان", "ROOT Amn",
                   "Verb amana (believed, 537) + mu'min (believer, 202 + "
                   "22 feminine plural + 6 feminine singular) + iman "
                   "(faith, 45). QAC's LEM split cleanly separates belief "
                   "from the same root's safety/trust senses: amin "
                   "(trustworthy, 14), amn (security, 5), amanah (trust, 6), "
                   "ma'man (safe place, 1), aaminin (secure ones, 10) etc. "
                   "-- 67 words, excluded."),
         "b": side("disbelief", "disbelief", "الكفر", "ROOT kfr",
                   "Verb kafara (289) + kafirun (129) + kufr (37) + kafir "
                   "(27) + kafur (ungrateful, 12) + kaffar (5) etc. "
                   "Excluded: kaffara 'to expiate/atone' (14) and kaffarah "
                   "'expiation' (4) -- same root, different sense."),
         "ratio": ratio(results["belief"]["count"], results["disbelief"]["count"]),
         "ratio_str": f"{results['belief']['count']}:{results['disbelief']['count']}",
         "notes": "Whole ROOT:Amn = 879 words; belief-sense = 812. Whole "
                  "ROOT:kfr = 525; disbelief-sense = 507."},
        {"id": "reward_punishment", "label_en": "Reward / Punishment",
         "label_ar": "الأجر / العذاب",
         "a": side("reward", "reward (ajr)", "الأجر", "ROOT Ajr, LEM >ajor",
                   "Noun ajr (reward/wage, incl. plural ujur). Excluded: "
                   "ista'jara 'to hire' (28:26, 2) and ta'jurani 'you hire "
                   "me' (28:27, 1) -- same root, hiring sense. Secondary "
                   "reward-word: thawab (noun, 13; family 18) -- see extras."),
         "b": side("punishment", "punishment (adhab)", "العذاب",
                   "ROOT E*b (QAC writes dhal as '*': E-b = ayn-dhal-ba), "
                   "LEM Ea*aAb (noun) + verb forms",
                   f"Noun adhab alone = {results['punishment_noun']['count']}; "
                   "whole E*b family (noun + yu'adhdhibu 'He punishes' etc.) "
                   f"= {results['punishment']['count']}."),
         "ratio": ratio(results["reward"]["count"], results["punishment"]["count"]),
         "ratio_str": f"{results['reward']['count']}:{results['punishment']['count']}",
         "notes": "Noun-only comparison: ajr 105 : adhab "
                  f"{results['punishment_noun']['count']}."},
        {"id": "day_night", "label_en": "Day / Night",
         "label_ar": "اليوم / الليل",
         "a": side("day", "day", "اليوم", "ROOT ywm, LEM yawom",
                   "Singular yawm (378, incl. al-yawm 'today') + plural "
                   "ayyam (27) + yawma'idhin 'on that day' (70, LEM "
                   "yawoma}i* -- QAC gives it no ROOT, so it is matched by "
                   "LEM and listed separately in the breakdown). Dual "
                   "yawmayn (2 days) is inside the 378."),
         "b": side("night", "night", "الليل", "ROOT lyl, LEM layol/layolap",
                   "Layl (84) + laylah (night, 8) + layal (nights, plural, "
                   "inside layol count). Excluded: qalil 'little' and "
                   "khalil 'friend' -- look-alikes that a naive substring "
                   "search would catch."),
         "ratio": ratio(results["day"]["count"], results["night"]["count"]),
         "ratio_str": f"{results['day']['count']}:{results['night']['count']}",
         "notes": "The widely quoted 'day 365' does not reproduce under "
                  "any clean rule on this text: singular yawm = 378; "
                  "+ yawma'idhin = 448; + ayyam = 475. See VERIFICATION.md."},
        {"id": "sun_moon", "label_en": "Sun / Moon",
         "label_ar": "الشمس / القمر",
         "a": side("sun", "sun", "الشمس", "ROOT $ms, LEM $amos",
                   "All shams words; no look-alike collisions."),
         "b": side("moon", "moon", "القمر", "ROOT qmr, LEM qamar",
                   "All qamar words; no look-alike collisions."),
         "ratio": ratio(results["sun"]["count"], results["moon"]["count"]),
         "ratio_str": f"{results['sun']['count']}:{results['moon']['count']}",
         "notes": ""},
        {"id": "man_woman", "label_en": "Man / Woman",
         "label_ar": "الرجل / المرأة",
         "a": side("man", "man", "الرجل", "ROOT rjl, LEM rajul/rijaAl",
                   "Rajl (29, incl. dual rajulan) + rijal (28). Excluded: "
                   "rijl 'foot/leg' (15, LEM rijol) and rajil 'on foot' "
                   "(1, 2:239 fa-rijalan) -- same consonants, different "
                   "word. Related: imru'/mar' 'a man/person' (ROOT mrA, 9) "
                   "is NOT counted here; see notes."),
         "b": side("woman", "woman", "المرأة", "ROOT mrA + nsw",
                   "Imra'ah (26) + nisa' (women, 59). Nisa' is the plural "
                   "of imra'ah (which has no plural of its own), so the two "
                   "lemmas are counted together; both roots are cited."),
         "ratio": ratio(results["man"]["count"], results["woman"]["count"]),
         "ratio_str": f"{results['man']['count']}:{results['woman']['count']}",
         "notes": "Counting the generic 'man/person' words imru'/mar' "
                  "(ROOT mrA, 9) with man would give 66 : 85. Male/female "
                  "as adjectives (dhakar/untha) is a separate, harder pair: "
                  "untha (female) = 30, but dhakar is mostly dhikr "
                  "'remembrance' -- not counted here."},
        {"id": "love_hate", "label_en": "Love / Hate",
         "label_ar": "الحب / الكره",
         "a": side("love", "love", "الحب", "ROOT Hbb",
                   "Verb ahabba (64) + hubb (love, 9) + istahabba "
                   "(preferred/loved, 4) + ahibba' (beloved ones, 1) + "
                   "mahabbah (love, 1) + ahabb (dearest, 3) etc. Excluded: "
                   "habb 'grain/seed' (7) and habbah 'a grain' (5) -- same "
                   "root, different sense."),
         "b": side("hate", "hate / dislike", "الكره", "ROOT krh",
                   "Verb kariha (17) + karihun (haters, 7) + makruh "
                   "(hated thing, 1) + karraha (made hateful, 1) + kurh "
                   "at 2:216 only ('fighting is hateful to you'). Excluded "
                   "as compulsion/unwillingness or hardship, not hate: "
                   "karhan 'unwillingly' (5: 3:83, 4:19, 9:53, 13:15, "
                   "41:11), kurhan 'in hardship' (46:15, 2), ukriha 'was "
                   "compelled' (5), ikrah 'compulsion' (2)."),
         "ratio": ratio(results["love"]["count"], results["hate"]["count"]),
         "ratio_str": f"{results['love']['count']}:{results['hate']['count']}",
         "notes": "Whole ROOT:Hbb = 95 (incl. 12 grain words); whole "
                  "ROOT:krh = 41 (27 hate-sense + 14 compulsion/hardship)."},
        {"id": "rich_poor", "label_en": "Rich / Poor",
         "label_ar": "الغني / الفقير",
         "a": side("rich", "rich / self-sufficient", "الغني", "ROOT gny",
                   "Adjective ghani (24, incl. al-Ghani 'the "
                   "Self-Sufficient' as a divine name, and plural "
                   "aghniya' 'the rich'). Verb forms of the same root are "
                   "NOT in this count: aghna 'He enriched / it availed' "
                   "(form IV, 28), ghaniya/aghnā 'to be rich, thrive, "
                   "avail' (15), istaghna 'to be free of need' (4), "
                   "mughnun 'one who avails' (2) -- whole ROOT:gny = 73."),
         "b": side("poor", "poor", "الفقير", "ROOT fqr",
                   "Faqir (12) + faqr (poverty, 1) + faqirah (1). Related: "
                   "miskin 'needy' (ROOT skn) is a different word -- see "
                   "extras."),
         "ratio": ratio(results["rich"]["count"], results["poor"]["count"]),
         "ratio_str": f"{results['rich']['count']}:{results['poor']['count']}",
         "notes": "Whole ROOT:gny = 73 (adjective ghani 24 + enrich/avail/"
                  "thrive verbs 43 + istaghna 4 + mughnun 2) vs poor 14."},
        {"id": "good_evil", "label_en": "Good / Evil",
         "label_ar": "الخير / الشر",
         "a": side("good", "good / better", "الخير", "ROOT xyr",
                   "Khayr (178, incl. comparative 'better/best') + khayrat "
                   "(good things, 10). Excluded: ikhtara/yatakhayyar "
                   "'to choose' (6) and khiyarah 'choice' (2) -- same "
                   "root, different sense."),
         "b": side("evil", "evil", "الشر", "ROOT $rr, LEM $ar~",
                   "All sharr words (30). Excluded: sharar 'sparks' (1, "
                   "77:32) -- same root, different sense. A naive "
                   "substring search for 'shr' would also catch shirk "
                   "(association), bashar (human), 'ashr (ten), shariba "
                   "(drink) -- all excluded here by ROOT/LEM."),
         "ratio": ratio(results["good"]["count"], results["evil"]["count"]),
         "ratio_str": f"{results['good']['count']}:{results['evil']['count']}",
         "notes": ""},
    ]

    extras = [
        {"id": "allah", "label_en": "Allah (sanity anchor)",
         "label_ar": "الله",
         "count": results["allah"]["count"],
         "qac_root": ["Alh"], "qac_lemmas": ["{ll~ah"],
         "refs": refs("allah"),
         "notes": "The standard anchor figure is 2699 and it reproduces "
                  "exactly. Excludes allahumma 'O Allah' (5, counted "
                  "separately) and ilah 'god' (147, generic -- counted "
                  "separately). NOTE: QAC excludes the 112 basmalahs "
                  "prepended to surahs 2-114, each containing Allah once; "
                  "a raw Tanzil-surface count is therefore 112 higher (2811)." },
        {"id": "allahumma", "label_en": "O Allah (allahumma)",
         "label_ar": "اللهم", "count": results["allahumma"]["count"],
         "qac_root": ["Alh"], "qac_lemmas": ["{ll~ahum~a"],
         "refs": refs("allahumma"),
         "notes": "Vocative form; not part of the 2699."},
        {"id": "ilah", "label_en": "god (generic, ilah)",
         "label_ar": "إله", "count": results["ilah"]["count"],
         "qac_root": ["Alh"], "qac_lemmas": ["<ila`h"],
         "refs": refs("ilah"),
         "notes": "Generic 'god' (incl. 'there is no god but Allah'). "
                  "Same root Alh as Allah, different lemma -- kept separate."},
        {"id": "jinn", "label_en": "jinn (beings)",
         "label_ar": "الجن",
         "count": results["jinn"]["count"],
         "qac_root": ["jnn"], "qac_lemmas": ["jin~", "jin~ap", "jaA^n~"],
         "refs": refs("jinn"),
         "notes": "Jinn (22) + jinnah (10) + jann (7, incl. serpent "
                  "sense). Same root as jannah; separated by LEM."},
        {"id": "sky", "label_en": "heaven / sky (sama')",
         "label_ar": "السماء",
         "count": results["sky"]["count"],
         "qac_root": ["smw"], "qac_lemmas": ["samaA^'"],
         "refs": refs("sky"),
         "notes": "The other 'heaven' word (sky). Same root smw also "
                  "gives ism 'name' (39) -- excluded by LEM."},
        {"id": "thawab", "label_en": "reward (thawab, noun)",
         "label_ar": "الثواب",
         "count": results["thawab_noun"]["count"],
         "qac_root": ["vwb"], "qac_lemmas": ["vawaAb"],
         "refs": refs("thawab_noun"),
         "notes": "Secondary reward-word. Family (noun 13 + athaba "
                  "'rewarded' 3 + mathubah 'reward' 2) = 18. Excluded: "
                  "thiyab 'clothes' (8) and mathabah 'place of return' "
                  "(1) -- same root, different senses."},
        {"id": "miskin", "label_en": "needy (miskin)",
         "label_ar": "المسكين",
         "count": results["miskin"]["count"],
         "qac_root": ["skn"], "qac_lemmas": ["misokiyn"],
         "refs": refs("miskin"),
         "notes": "Related to 'poor' (faqir) but a different word; "
                  "listed as an extra, not added to the poor count."},
        {"id": "life_broad", "label_en": "Life (broad Hyy family)",
         "label_ar": "الحياة (broad)",
         "count": results["life_broad"]["count"],
         "qac_root": ["Hyy"],
         "qac_lemmas": ["Hayaw`p", "Hay~", ">aHoyaA", "HaY~a",
                        "m~aHoyaA", "muHoY", "HayawaAn",
                        "yasotaHoYi.^ (spare-alive only)"],
         "refs": refs("life_broad"),
         "notes": "See life/death pair notes for what is included and "
                  "excluded."},
        {"id": "death_broad", "label_en": "Death (broad mwt family)",
         "label_ar": "الموت (broad)",
         "count": results["death_broad"]["count"],
         "qac_root": ["mwt"],
         "qac_lemmas": ["mawot", "m~aAta", "m~ay~it", ">amaAta",
                        "mayotap", "m~ayot", "mamaAt", "mawotat"],
         "refs": refs("death_broad"),
         "notes": "Whole ROOT:mwt; every lemma is a death sense."},
        {"id": "punishment_noun", "label_en": "Punishment (adhab, noun only)",
         "label_ar": "العذاب",
         "count": results["punishment_noun"]["count"],
         "qac_root": ["E*b"], "qac_lemmas": ["Ea*aAb"],
         "refs": refs("punishment_noun"),
         "notes": "Noun-only subset of the punishment count in the pair."},
    ]

    data = {
        "project": "miracleMath",
        "agent": "Agent 1 (root-word counts & paired relationships)",
        "generated_by": "data/root_counts_script.py (run it to regenerate)",
        "methodology": {
            "primary_source": {
                "name": "Quranic Arabic Corpus, morphology version 0.4",
                "copyright": "Copyright (C) 2011 Kais Dukes, GNU GPL",
                "site": "https://corpus.quran.com",
                "file": "corpus/quranic-corpus-morphology-0.4.txt",
                "sha256": "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46",
                "bytes": 6309503, "lines_total": 128276,
                "data_lines_segments": 128219,
                "how_obtained": (
                    "corpus.quran.com's official download page "
                    "(https://corpus.quran.com/download/) serves v0.4 only "
                    "behind an email form (POST to /download/default.jsp) "
                    "and publishes no direct file URL; the Java API "
                    "(JQuranTree) is a Java library, not a REST API, so "
                    "there is no live endpoint to query. This file was "
                    "fetched from the textminingthequran.com mirror of the "
                    "identical v0.4 file and verified against the corpus's "
                    "own published figures (128,276 lines; 77,429 words; "
                    "header copyright block verbatim). It was NOT downloaded "
                    "directly from corpus.quran.com."),
            },
            "display_source": {
                "name": "Tanzil Quran Text, Uthmani script",
                "site": "https://tanzil.net",
                "file": "corpus/quran-uthmani.txt",
                "sha256": "ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af",
                "bytes": 1334737,
                "role": ("Arabic display text only (verse quotes and matched "
                         "tokens, copied byte-for-byte, never retyped); "
                         "also used for the totals cross-check."),
            },
            "counting_rules": [
                "Counting unit: one QAC word = one (surah, verse, word) "
                "location. A word with several segments (prefix + stem + "
                "suffix) is counted once even if several segments carry "
                "the root.",
                "Matching is by ROOT: first (e.g. jannah ROOT jnn, dunya "
                "ROOT dnw), then narrowed by LEM: to the intended sense. "
                "Where QAC assigns no ROOT (proper nouns: jahannam; the "
                "time-adverb yawma'idhin), matching is by LEM: (or FORM:) "
                "alone -- stated per concept in qac_root/qac_lemmas.",
                "Buckwalter transliteration is used ONLY for matching "
                "(ROOT:/LEM:/FORM: fields). All Arabic shown comes from "
                "the Tanzil file.",
                "Prefixes (wa-, fa-, bi-, li-, ka-, al-) and suffixes "
                "(pronouns, case endings, plural/dual markers) are already "
                "segmented in QAC, so they need no stripping: matching is "
                "on the stem segment's ROOT/LEM, which is prefix- and "
                "suffix-independent.",
                "Plurals and duals are included wherever the lemma covers "
                "them (e.g. jan~ap covers jannah + jannat; rijaAl covers "
                "rijal). Where a plural has its own lemma it is cited "
                "separately (nisa' for women).",
                "Basmalah: QAC contains only the basmalah of 1:1 as words. "
                "The basmalahs prepended to verse 1 of the other 112 surahs "
                "in the Tanzil file are NOT QAC words and are NOT counted. "
                "This affects the Allah anchor by exactly 112 (see extras).",
                "Diacritics: not stripped by us -- QAC's annotation already "
                "encodes vowels in FORM and sense in LEM, which is what "
                "resolves look-alikes (iman vs ayman 'oaths', malak 'angel' "
                "vs malik 'king', dhakar 'male' vs dhikr 'remembrance').",
                "Ambiguous roots are split by LEM and the excluded senses "
                "are listed per concept (grain for Hbb, expiation for kfr, "
                "safety/trust for Amn, compulsion for krh, hiring for Ajr, "
                "choosing for xyr, sparks for $rr, clothes for vwb).",
                "Ratios are a:b as a/b rounded to 2 decimals; ratio_str "
                "gives the raw counts.",
                "English (Clear Quran) translation was NOT used as a "
                "counting source anywhere.",
            ],
            "verse_mapping": ("Line index -> surah:ayah via the standard "
                              "ayah counts per surah; table verified to sum "
                              "to 6236 before use."),
            "reproduce": "python3 data/root_counts_script.py",
        },
        "totals": {
            "qac_segments": n_seg,
            "qac_words": n_words,
            "qac_verses": n_verses,
            "qac_surahs": n_surahs,
            "tanzil_whitespace_tokens_6236_verses": tanzil_tokens,
            "tanzil_vs_qac_token_difference": tanzil_tokens - n_words,
            "tanzil_vs_qac_explanation": (
                f"Tanzil has {tanzil_tokens - n_words} more whitespace "
                f"tokens than QAC has words: {basmalah_tokens} = "
                f"{n_basmalah_lines} basmalahs x 4 words (prepended in "
                "Tanzil, absent from QAC except 1:1; Surahs 95 and 97 spell "
                "the basmalah with a doubled ba, so a plain startswith "
                "count finds only 111 of the 113 basmalah lines) + "
                f"{(tanzil_tokens - n_words) - basmalah_tokens} tokens "
                "where the two texts segment words differently (per-verse "
                f"audit: {len(mismatches)} verses differ, net "
                f"{-total_diff} tokens; see alignment_audit). QAC words "
                "and Tanzil tokens are different units; the counts are not "
                "forced to match."),
            "allah_anchor_qac_lemma_llah": results["allah"]["count"],
            "alignment_audit": {
                "verses_with_word_count_mismatch": len(mismatches),
                "total_diff_qac_minus_tanzil": total_diff,
                "mismatches": mismatches,
            },
        },
        "pairs": pairs,
        "extras": extras,
    }

    out = Path(args.out)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ---- stdout summary + diagnostics
    print(f"QAC segments={n_seg} words={n_words} verses={n_verses} "
          f"surahs={n_surahs}")
    print(f"Tanzil whitespace tokens (6236 verses)={tanzil_tokens} "
          f"(diff vs QAC words: {tanzil_tokens - n_words})")
    print(f"Alignment mismatches: {len(mismatches)} verses, "
          f"total diff {total_diff}")
    print(f"Allah (LEM {{ll~ah) = {results['allah']['count']}")
    for p in pairs:
        print(f"{p['id']}: {p['a']['count']} : {p['b']['count']} "
              f"(ratio {p['ratio']})")
    print(f"Wrote {out}")
    print("\n=== DIAGNOSTICS ===")
    print("--- alignment mismatches ---")
    for m in mismatches:
        print(" ", m)
    print("--- karoh / kuroh / ikrah / ukriha words (hate vs compulsion) ---")
    for loc in sorted(loc for loc, rec in words.items()
                      if rec["lems"] & {"karoh", "kuroh", "<ikoraAh",
                                        ">ukoriha", "kar~aha", "makoruwh"}):
        tok, _v = tanzil_token(loc)
        print("  ", loc, sorted(words[loc]["lems"]), repr(tok))
    print("--- >agonaY` (elative?) vs >agonato (verb?) examples ---")
    for lem in (">agonaY`", ">agonato", "ganiY~", "m~ugonuwn"):
        ex = [loc for loc, rec in words.items() if lem in rec["lems"]][:4]
        print("  ", lem, [(loc, tanzil_token(loc)[0]) for loc in ex])
    print("--- bare 'aAxira FORM words (ROOT Axr, no al-) ---")
    for loc in sorted(words):
        if any(f == "'aAxira" for f in words[loc]["stem_forms"]) \
                and "Axr" in words[loc]["roots"]:
            print("  ", loc, sorted(words[loc]["lems"]),
                  repr(tanzil_token(loc)[0]))
    print("--- 29:20 check (al-nash'a al-akhira, 'latter creation') ---")
    for loc in sorted(words):
        if loc[0] == 29 and loc[1] == 20 and "Axr" in words[loc]["roots"]:
            print("  ", loc, sorted(words[loc]["lems"]),
                  words[loc]["stem_forms"], repr(tanzil_token(loc)[0]))
    print("--- QAC max verse per surah (spot check 5, 6) ---")
    _mx = {}
    for (s, v, _w) in words:
        _mx[s] = max(_mx.get(s, 0), v)
    print("  surah 5 max:", _mx[5], "surah 6 max:", _mx[6],
          "total verses:", sum(_mx.values()))
    print("--- devils ROOT $Tn lemma breakdown ---")
    print(" ", diagnostics["root_lemma_breakdowns"]["devils"])
    print("--- punishment ROOT E*b lemma breakdown ---")
    print(" ", diagnostics["root_lemma_breakdowns"]["punishment"])
    print("--- rich lemma breakdown (ganiY~ vs >agonaY` vs >agonato) ---")
    print(" ", diagnostics["root_lemma_breakdowns"]["rich"])
    print("--- hate lemma breakdown ---")
    print(" ", diagnostics["root_lemma_breakdowns"]["hate"])
    print("--- akhira locations (check 'aAxira bare forms + 29:20) ---")
    print(" ", [f"{s}:{v}:{w}" for (s, v, w) in results["akhira"]["locations"]][:5],
          "... total", results["akhira"]["count"])
    print("--- nar: QAC naAr words whose Tanzil token lacks nar (diacritic-stripped) ---")
    _diac = re.compile(r"[\u064B-\u065F\u0670\u0640\u06D6-\u06DC\u06DF-\u06E4"
                       r"\u06E5-\u06E8\u06EA-\u06ED]")
    def _strip(s):
        s = _diac.sub("", s)
        return (s.replace("\u0622", "\u0627").replace("\u0623", "\u0627")
                 .replace("\u0625", "\u0627").replace("\u0671", "\u0627")
                 .replace("\u0624", "\u0621").replace("\u0626", "\u0621")
                 .replace("\u0649", "\u064A"))
    for loc in results["nar"]["locations"]:
        tok, _v = tanzil_token(loc)
        if tok is not None and "نار" not in _strip(tok):
            print("  ", loc, repr(tok))
    print("--- miskin count / surface forms ---")
    print(" ", results["miskin"]["count"], results["miskin"]["surface_forms"])
    print("--- vwb (thawab) full ROOT breakdown ---")
    vwb = [loc for loc, rec in words.items() if "vwb" in rec["roots"]]
    print("  words:", len(vwb),
          collections.Counter(tuple(sorted(words[l]["lems"])) for l in vwb))
    print("--- unaligned words (should be none) ---")
    for cid, r in results.items():
        if r["unaligned"]:
            print(" ", cid, r["unaligned"])


if __name__ == "__main__":
    main()

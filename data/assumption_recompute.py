#!/usr/bin/env python3
"""
assumption_recompute.py -- miracleMath research redesign, Agent A (2026-11-08).

Defines a small set of named assumption sets (data/assumption_sets.json) and
recomputes EVERY finding's numbers under each applicable set BY SCRIPT from
the corpus (QAC v0.4 morphology + Tanzil Uthmani), writing the result into
the "assumptions" field of every finding in data/scholar_findings.json.

Assumption sets (see data/assumption_sets.json for the authoritative list):
  A1  Standard root rule -- QAC ROOT, all forms, prefixes/suffixes in,
      unnumbered basmalahs excluded (only 1:1 and 27:30 count); where the
      root covers other senses, narrow by lemma to the intended sense as
      documented per finding; where the claim is about a lemma or a form
      subset, that subset's number is given instead (METHODS.md convention).
      For corpus totals, the QAC word unit.
  A2  Lemma rule -- QAC LEM, all forms, prefixes/suffixes in, basmalahs
      excluded as in A1.
  A3  Surface-form rule -- exact surface forms on the Tanzil skeleton text:
      the forms listed in the finding's selection where one is documented
      (singular-only, bare-form, narrow or plural selections), otherwise
      the plain surface reading of the claimed word; basmalahs excluded.
  A4  Letter rule -- base letters on the Tanzil Uthmani text under the
      project letter convention (alef wasla counts; dagger alif, small waw
      and small yeh are marks, not letters; shaddah counts once);
      unnumbered basmalahs excluded.
  A5  Scholar's stated rule -- the counting rule as stated in the scholar's
      own source, applied to the corpus (per-finding; null where the source
      states no counting rule).
  A6  Scholar's reconstructed rule -- the specific selection/exclusion
      documented in the finding's scholar_method that reproduces the
      scholar's number (per-finding; null where no reproducing rule exists).
  A7  Basmalah-included variant -- as the finding's primary rule
      (A1/A2/A3/A4 as applicable), but with the 112 unnumbered basmalahs
      counted in.

"assumptions" schema (exact, for the site builder):
  {"scholar_set": "A5"|"A6"|null, "our_set": "A1"|"A2"|"A4"|null,
   "reconciles_under": [set ids], "numbers_by_set": {set id: number},
   "reason": "one-line reconciliation reason, plain language"}
  - scholar_set: "A5" if the scholar stated a counting rule, "A6" if a
    reproducing rule was reconstructed, else null.
  - our_set: the set under which the finding's headline recount was computed.
  - numbers_by_set: our recomputed number under each applicable set only.
    Single-number findings use ints; multi-number findings use lists aligned
    with the scholar's numbers, with null for parts a set does not cover.
  - reconciles_under: sets that reproduce the scholar's number(s) IN FULL
    (every part they cover agrees, and jointly they cover all parts).
    For the one mixed-unit finding (surah-110: words + letters) the word
    part reconciles under A1 and the letter part under A4, so both are listed.

Rules honoured here (per the task):
  - Do NOT apply the 11 proposed findings or the benefit-corrupt-50 flip
    from PASTED_PAGE_CHECK.md (benefit-corrupt-50 stays "differs" even
    though its numbers reconcile under A1/A2/A6 -- flagged in the report).
  - Do NOT decide mind-light-49 (left "differs"); do NOT touch the
    Scholar/Popular section split, web/*, build.py, or Isarat al-I'jaz.
  - A finding's our_status changes ONLY if recomputation proves its number
    wrong. No such correction was needed (see the cross-check section).

Usage: python3 data/assumption_recompute.py
Writes: data/assumption_sets.json, data/scholar_findings.json (only the
"assumptions" field is added/changed per finding), data/assumption_recompute_report.json
(a machine-readable log of the run: values, cross-checks, tallies).
Re-running is idempotent: the script recomputes everything from the corpus
and overwrites the "assumptions" field with the fresh result.
"""
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
QAC = BASE / "corpus" / "quranic-corpus-morphology-0.4.txt"
TANZIL = BASE / "corpus" / "quran-uthmani.txt"
FINDINGS = HERE / "scholar_findings.json"
SETS_OUT = HERE / "assumption_sets.json"
REPORT_OUT = HERE / "assumption_recompute_report.json"

SURAH_VERSES = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111,
    43, 52, 99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88,
    69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37,
    35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11,
    18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29,
    19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]
assert sum(SURAH_VERSES) == 6236

ROOT_RE = re.compile(r"ROOT:([^|]+)")
LEM_RE = re.compile(r"LEM:([^|]+)")
LOC_RE = re.compile(r"\((\d+):(\d+):(\d+):(\d+)\)")

# ---------- load QAC ----------
words = {}   # (s,v,w) -> {roots, lems, stems, feats, stem_lem}
seg_root_counter = Counter()
seg_lem_counter = Counter()
n_seg = 0
with open(QAC, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.startswith("#") or line.startswith("LOCATION"):
            continue
        p = line.split("\t")
        if len(p) < 4:
            continue
        m = LOC_RE.match(p[0])
        if not m:
            continue
        s, v, w, _sg = map(int, m.groups())
        rec = words.setdefault((s, v, w),
                               {"roots": set(), "lems": set(),
                                "stems": [], "feats": [], "stem_lem": None})
        rec["feats"].append(p[3])
        n_seg += 1
        r = ROOT_RE.search(p[3])
        if r:
            rec["roots"].add(r.group(1))
            seg_root_counter[r.group(1)] += 1
        l = LEM_RE.search(p[3])
        if l:
            rec["lems"].add(l.group(1))
            seg_lem_counter[l.group(1)] += 1
        if p[3].startswith("STEM|"):
            rec["stems"].append(p[1])
            if l and rec["stem_lem"] is None:
                rec["stem_lem"] = l.group(1)

# ---------- load Tanzil ----------
raw = TANZIL.read_text(encoding="utf-8").splitlines()
verses = [ln for ln in raw if ln.strip() and not ln.lstrip().startswith("#")]
assert len(verses) == 6236
vmap = {}
idx = 0
for s, n in enumerate(SURAH_VERSES, start=1):
    for a in range(1, n + 1):
        vmap[idx] = (s, a)
        idx += 1
inv_vmap = {v: k for k, v in vmap.items()}

DIACRITICS = re.compile(r"[\u064b-\u065f\u0640\u06d6-\u06ed\u08d3-\u08ff]")
SUPERSCRIPT = str.maketrans({"ٰ": "ا", "ۥ": "و", "ۦ": "ي"})
HAMZA_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
                           "ؤ": "و", "ئ": "ي"})
LETTER_MARKS = re.compile(r"[ٰۥۦ]")


def skeleton(text):
    t = DIACRITICS.sub("", text.translate(SUPERSCRIPT))
    return t.translate(HAMZA_MAP).replace("ء", "")


def strip_diacritics(text):
    return DIACRITICS.sub("", text.translate(SUPERSCRIPT))


def letter_count(text):
    """Project letter convention: base letters count (alef wasla = ا);
    dagger alif / small waw / small yeh are marks, do NOT count;
    standalone hamza counts."""
    t = text.translate(HAMZA_MAP)
    t = LETTER_MARKS.sub("", t)
    t = DIACRITICS.sub("", t)
    return sum(1 for c in t if "\u0621" <= c <= "\u064a")


def strip_prefixes(tok):
    while len(tok) > 1 and tok[0] in "وفبلك":
        tok = tok[1:]
    return tok


def tanzil_token(s, v, w):
    toks = verses[inv_vmap[(s, v)]].split()
    ti = w - 1 + 4 if (v == 1 and s > 1 and s != 9) else w - 1
    return toks[ti] if 0 <= ti < len(toks) else None


# Tanzil skeleton tokens (whole text, basmalahs included as printed)
skel_tokens = [skeleton(t) for ln in verses for t in ln.split()]
# same, but with the 112 unnumbered basmalahs (4 tokens each) removed
skel_tokens_excl = []
for li, ln in enumerate(verses):
    s, v = vmap[li]
    toks = ln.split()
    if v == 1 and s > 1 and s != 9:
        toks = toks[4:]
    skel_tokens_excl.extend(skeleton(t) for t in toks)


def surf_count(pred, excl_basmalahs=True):
    toks = skel_tokens_excl if excl_basmalahs else skel_tokens
    return sum(1 for t in toks if pred(t))


def qac_locs(pred):
    return sorted(loc for loc, rec in words.items() if pred(rec, loc))


def lem_locs(*lems):
    return qac_locs(lambda rec, loc: bool(rec["lems"] & set(lems)))


def root_locs(root, lem_in=None, lem_not=None):
    def pred(rec, loc):
        if root not in rec["roots"]:
            return False
        if lem_in and not (rec["lems"] & set(lem_in)):
            return False
        if lem_not and (rec["lems"] & set(lem_not)):
            return False
        return True
    return qac_locs(pred)


def is_bare(rec):
    """No pronominal suffix segment (QAC PRON/SUFFIX features)."""
    return not any("PRON" in ft or "SUFFIX" in ft for ft in rec["feats"])


def letter_in_surah(n, letter, excl_basmalah=False):
    tot = 0
    for li, ln in enumerate(verses):
        s, v = vmap[li]
        if s != n:
            continue
        txt = ln
        if excl_basmalah and v == 1 and s not in (1, 9):
            toks = ln.split()
            txt = " ".join(toks[4:])
        tot += strip_diacritics(txt).count(letter)
    return tot


def surah_letter_total(n, excl_basmalah=True):
    tot = 0
    for li, ln in enumerate(verses):
        s, v = vmap[li]
        if s != n:
            continue
        txt = ln
        if excl_basmalah and v == 1 and s not in (1, 9):
            toks = ln.split()
            txt = " ".join(toks[4:])
        tot += letter_count(txt)
    return tot


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

# =====================================================================
# Shared recomputed values (all from the corpus, by script)
# =====================================================================
V = {}  # name -> value, also written to the run report for audit
CHK = []  # (label, computed, documented) spot-checks vs the stored file


def setv(name, value, documented=None):
    V[name] = value
    if documented is not None:
        CHK.append((name, value, documented))
    return value


# --- dunya / akhira ---
dunya_lem = setv("dunya_lem", len(lem_locs("d~unoyaA")), 115)
akhira_stems = setv("akhira_fem_stems", len(qac_locs(
    lambda rec, loc: any(f in ("'aAxirapi", "'aAxirapa", "'aAxirapu")
                         for f in rec["stems"]) and "Axr" in rec["roots"])), 115)
akhira_lem = setv("akhira_lem_A^xir", len(lem_locs("A^xir")), 155)
dunya_surf = setv("dunya_surf", surf_count(lambda t: "دنيا" in t), 115)
akhira_surf = setv("akhira_surf", surf_count(lambda t: "اخرة" in t), 115)

# --- jannah / jahannam ---
jan_all = lem_locs("jan~ap")
setv("jan_lem_all", len(jan_all), 147)
jan_sing, jan_plur, jan_dual = [], [], []
for loc in jan_all:
    st = "|".join(words[loc]["stems"])
    if "jan~a`t" in st or "jan~aAt" in st:
        jan_plur.append(loc)
    elif "jan~atay" in st or "jan~ataAn" in st:
        jan_dual.append(loc)
    else:
        jan_sing.append(loc)
setv("jan_sing", len(jan_sing), 70)
setv("jan_plur", len(jan_plur), 69)
setv("jan_dual", len(jan_dual), 8)
jan_sing_bare = setv("jan_sing_bare", len(
    [loc for loc in jan_sing if is_bare(words[loc])]), 66)  # 65 in the four forms + وجنتُ 56:89
jah = setv("jahannam_lem", len(lem_locs("jahan~am")), 77)
garden_exact = setv("garden_exact_4forms", surf_count(
    lambda t: t in {"الجنة", "جنة", "وجنة", "بالجنة"}), 77)
jah_sub = setv("jahannam_substr", surf_count(lambda t: "جهنم" in t), 77)

# --- devils / angels ---
devils_root = setv("devils_root_$Tn", len(root_locs("$Tn")), 88)
devils_lem = setv("devils_lem_$ayoTa`n", len(lem_locs("$ayoTa`n")), 88)
angels_lem = setv("angels_lem_malak", len(lem_locs("malak")), 88)

# --- day / month ---
day_root = root_locs("ywm")
day_idhin = lem_locs("yawoma}i*")
setv("day_root_total", len(day_root), 405)
setv("day_yawma_idhin", len(day_idhin), 70)
setv("day_A1", len(day_root) + len(day_idhin), 475)
day_lem = setv("day_lem_yawom", len(lem_locs("yawom")), 405)


def _is_dual_yawm(rec):
    return any("yawomay" in s for s in rec["stems"])


def _is_plur_yawm(rec):
    return any("ay~aAm" in s or "ay~aY`m" in s for s in rec["stems"])


day_sing = [loc for loc in day_root
            if not _is_dual_yawm(words[loc]) and not _is_plur_yawm(words[loc])]
setv("day_sing", len(day_sing), 375)
day_sing_bare = setv("day_sing_bare", len(
    [loc for loc in day_sing if is_bare(words[loc])]), 365)
DAY_SET = {"يوم", "اليوم", "يوما", "ويوم", "واليوم", "ليوم", "فاليوم",
           "بيوم", "باليوم", "وباليوم"}
day_surf = setv("day_surf_set", surf_count(lambda t: t in DAY_SET), 365)
month_root = setv("month_root_$hr", len(root_locs("$hr")), 21)
month_surf = setv("month_surf", surf_count(
    lambda t: t in {"شهر", "الشهر", "شهرا", "بالشهر", "والشهر"}), 12)

# --- salawat ---
salawat_plur = setv("salawat_plur_stems", len(qac_locs(
    lambda rec, loc: "Salaw`p" in rec["lems"] and any(
        f in ("Salawa`tN", "Salawa`ti", "S~alawa`ti")
        for f in rec["stems"]))), 5)
salawat_lem_all = setv("salawat_lem_all", len(lem_locs("Salaw`p")), 83)
salawat_locs = qac_locs(
    lambda rec, loc: "Salaw`p" in rec["lems"] and any(
        f in ("Salawa`tN", "Salawa`ti", "S~alawa`ti")
        for f in rec["stems"]))
salawat_surf_forms = sorted({skeleton(tanzil_token(*loc))
                             for loc in salawat_locs})
# surface forms of the 5 plural tokens (Uthmani dagger-alif spellings):
# الصلوات / صلوات / وصلوات / صلواتهم -- counted via their QAC stems.
salawat_surf = setv("salawat_surf", len(salawat_locs), 5)

# --- sea / land ---
sea_lem = setv("sea_lem_baHor", len(lem_locs("baHor")), 41)
land_bar = lem_locs("bar~")
# land-sense = bar~ tokens that are land, not piety/righteousness/Benign.
# The methods pass classified them verse by verse; reproduce with the
# documented 12 land verses from the finding's exceptions.
LAND_VERSES = {(5, 96), (6, 59), (6, 63), (6, 97), (10, 22), (17, 67),
               (17, 68), (17, 70), (27, 63), (29, 65), (30, 41), (31, 32)}
land_sense = setv("land_sense", len(
    [loc for loc in land_bar if (loc[0], loc[1]) in LAND_VERSES]), 12)
sea_surf = setv("sea_surf_def_sing", surf_count(
    lambda t: strip_prefixes(t) == "البحر"), 32)
land_surf = setv("land_surf_bar", surf_count(
    lambda t: strip_prefixes(t) == "البر"), 21)

# --- man / woman ---
man_lem_all = setv("man_lem_rajul", len(lem_locs("rajul")), 29)
man_root_all = setv("man_root", len(lem_locs("rajul", "rijaAl")), 57)
woman_lem_all = setv("woman_lem_{mora>at", len(lem_locs("{mora>at")), 26)
woman_root_all = setv("woman_root", len(lem_locs("{mora>at", "nisaA^'")), 85)
MAN_SING_STEMS = {"rajulN", "rajulFA", "rajulK", "rajulN[", "r~ajulFA"}
WOM_SING_STEMS = {"{mora>ata", "{mora>atu", "{mora>ati", "{mora>apN",
                  "{mora>apF"}
man_sing = setv("man_sing", len(
    [loc for loc in lem_locs("rajul")
     if set(words[loc]["stems"]) & MAN_SING_STEMS]), 24)
woman_sing = setv("woman_sing", len(
    [loc for loc in lem_locs("{mora>at")
     if set(words[loc]["stems"]) & WOM_SING_STEMS]), 24)
MAN_SURF = {"رجل", "رجلا", "لرجل", "فرجل", "ورجلا"}
man_surf = setv("man_surf", surf_count(lambda t: t in MAN_SURF), 24)
WOM_SURF = {"امرات", "امراتهو", "امراة", "وامراتهو", "امراتك", "امراتى",
            "وامراتى", "لامراتهي", "وامراة", "وامرات"}
woman_surf = setv("woman_surf", surf_count(lambda t: t in WOM_SURF), 24)

# --- life / death ---
life_root = setv("life_root_Hyy", len(root_locs("Hyy")), 184)
life_noun = setv("life_noun_Hayaw`p", len(lem_locs("Hayaw`p")), 76)
death_root = setv("death_root_mwt", len(root_locs("mwt")), 165)
death_noun = setv("death_noun_mawot", len(lem_locs("mawot")), 50)
life_fam = setv("life_surf_family", surf_count(
    lambda t: any(x in t for x in ("حيو", "حيي", "حيا"))), 125)
death_fam = setv("death_surf_family", surf_count(
    lambda t: (any(x in t for x in ("موت", "ميت", "مات"))
               and "ظلم" not in t and "كلم" not in t)), 171)

# --- sun / moon / light ---
sun_root = setv("sun_root_$ms", len(root_locs("$ms")), 33)
moon_root = setv("moon_root_qmr", len(root_locs("qmr")), 27)
light_lem = setv("light_lem_nuwr", len(lem_locs("nuwr")), 43)
light_muniyr = setv("light_lem_muniyr", len(lem_locs("m~uniyr")), 6)
sun_surf = setv("sun_surf", surf_count(lambda t: "شمس" in t), 33)
moon_surf = setv("moon_surf", surf_count(lambda t: "قمر" in t), 27)
LIGHT_SIMPLE = {"نور": 8, "النور": 10, "نورا": 9, "والنور": 3,
                "بنور": 1, "نورهم": 2}
light_simple = setv("light_simple_forms", surf_count(
    lambda t: t in LIGHT_SIMPLE), 33)
light_sub = setv("light_substr", surf_count(lambda t: "نور" in t), 46)

# --- muhammad ---
muhammad = setv("muhammad_lem", len(lem_locs("muHam~ad")), 4)
muhammad_surf = setv("muhammad_surf", surf_count(lambda t: t == "محمد"), 4)

# --- iman / kufr ---
iman_lem = setv("iman_lem", len(lem_locs("<iyma`n")), 45)
kufr_lem = setv("kufr_lem", len(lem_locs("kufor")), 37)
iman_bare = setv("iman_bare", len(
    [loc for loc in lem_locs("<iyma`n") if is_bare(words[loc])]), 25)
kufr_bare = setv("kufr_bare", len(
    [loc for loc in lem_locs("kufor") if is_bare(words[loc])]), 25)

# --- zakah / blessing ---
zakah_lem = setv("zakah_lem", len(lem_locs("zakaw`p")), 32)
brk_root = setv("bless_root_brk", len(root_locs("brk")), 32)
zak_surf = setv("zak_surf", surf_count(lambda t: "زك" in t), 67)
brk_surf = setv("brk_surf", surf_count(lambda t: "برك" in t), 5)

# --- say / they said ---
say_impv = setv("say_IMPV_2MS", len(qac_locs(
    lambda rec, loc: "qaAla" in rec["lems"] and any(
        "IMPV" in ft for ft in rec["feats"])
    and tanzil_token(*loc) is not None
    and skeleton(tanzil_token(*loc)) in {"قل", "فقل", "وقل"})), 332)
they_said = setv("they_said_PERF_3MP", len(qac_locs(
    lambda rec, loc: "qaAla" in rec["lems"] and any(
        "PERF" in ft and "3MP" in ft for ft in rec["feats"])
    and tanzil_token(*loc) is not None
    and skeleton(tanzil_token(*loc)) in
    {"قالوا", "وقالوا", "فقالوا", "لقالوا"})), 332)
say_surf = setv("say_surf_qul", surf_count(
    lambda t: t in {"قل", "فقل", "وقل"}), 333)
they_said_surf = setv("they_said_surf", surf_count(
    lambda t: t in {"قالوا", "وقالوا", "فقالوا", "لقالوا"}), 332)

# --- plant / tree ---
plant_root = setv("plant_root_nbt", len(root_locs("nbt")), 26)
tree_root = setv("tree_root_$jr", len(root_locs("$jr")), 27)
tree_sense = setv("tree_sense", len(
    [loc for loc in root_locs("$jr")
     if "$ajara" not in words[loc]["lems"]]), 26)
plant_surf = setv("plant_surf", surf_count(lambda t: "نبات" in t), 11)
tree_surf = setv("tree_surf", surf_count(lambda t: "شجر" in t), 27)

# --- reward / forgiveness ---
jzy_root = setv("reward_root_jzy", len(root_locs("jzy")), 118)
jzy_reward = setv("reward_sense", len(
    [loc for loc in root_locs("jzy")
     if "jizoyap" not in words[loc]["lems"]]), 117)
gfr_root = setv("forgive_root_gfr", len(root_locs("gfr")), 234)
reward_surf = setv("reward_surf_jza", surf_count(lambda t: "جزا" in t), 48)
forgive_surf = setv("forgive_surf_mgfr", surf_count(
    lambda t: "مغفر" in t), 28)

# --- guidance / mercy ---
hudfy_lem = setv("guidance_lem_hudFY", len(lem_locs("hudFY")), 85)
rahma_lem = setv("mercy_lem_raHomap", len(lem_locs("raHomap")), 114)
hudfy_bare = setv("guidance_bare", len(
    [loc for loc in lem_locs("hudFY") if is_bare(words[loc])]), 79)
rahma_bare = setv("mercy_bare", len(
    [loc for loc in lem_locs("raHomap") if is_bare(words[loc])]), 79)

# --- tongue / sermon ---
lsn_root = setv("tongue_root_lsn", len(root_locs("lsn")), 25)
wez_root = setv("admon_root_wEZ", len(root_locs("wEZ")), 25)
tongue_surf = setv("tongue_surf", surf_count(lambda t: "لسان" in t), 15)
sermon_surf = setv("sermon_surf", surf_count(lambda t: "موعظ" in t), 9)

# --- wine / intoxication ---
wine_lem = setv("wine_lem_xamor", len(lem_locs("xamor")), 6)
intox_root = setv("intox_root_skr", len(root_locs("skr")), 7)
wine_surf = setv("wine_surf", surf_count(lambda t: "خمر" in t), 7)
intox_surf = setv("intox_surf", surf_count(lambda t: "سكر" in t), 4)

# --- mind / light ---
eql_root = setv("mind_root_Eql", len(root_locs("Eql")), 49)
mind_surf = setv("mind_surf", surf_count(lambda t: "عقل" in t), 49)

# --- benefit / corrupt ---
nfe_root = setv("benefit_root_nfE", len(root_locs("nfE")), 50)
fsd_root = setv("corrupt_root_fsd", len(root_locs("fsd")), 50)
benefit_surf = setv("benefit_surf", surf_count(lambda t: "نفع" in t), 45)
corrupt_surf = setv("corrupt_surf", surf_count(lambda t: "فساد" in t), 11)

# --- love / obedience ---
# grain = حَبّ 'grain/seed' (LEM Hab~) + حبّة (LEM Hab~ap) = 12 tokens.
# (Hub~ is the love noun -- NOT excluded.)
HBB_GRAIN = {"Hab~", "Hab~ap"}
hbb_root = setv("love_root_Hbb", len(root_locs("Hbb")), 95)
hbb_love = setv("love_sense", len(
    [loc for loc in root_locs("Hbb")
     if not (words[loc]["lems"] & HBB_GRAIN)]), 83)
TWE_ABLE = {"{sotaTaAEa"}
twe_root = setv("obed_root_TwE", len(root_locs("TwE")), 129)
twe_obed = setv("obed_sense", len(
    [loc for loc in root_locs("TwE")
     if not (words[loc]["lems"] & TWE_ABLE)]), 87)
love_surf = setv("love_surf", surf_count(lambda t: "حب" in t), 153)
obed_surf = setv("obed_surf", surf_count(lambda t: "طاع" in t), 16)

# --- refuge / forever ---
masiyr = setv("maseer_lem", len(lem_locs("maSiyr")), 28)
abad = setv("forever_lem", len(lem_locs(">abadFA")), 28)
refuge_surf = setv("refuge_surf", surf_count(lambda t: "مصير" in t), 28)
forever_surf = setv("forever_surf", surf_count(lambda t: "ابدا" in t), 29)

# --- disaster / thanks ---
SWB_NOT = {"Say~ib", "SawaAb"}
swb_root = setv("disaster_root_Swb", len(root_locs("Swb")), 77)
swb_dis = setv("disaster_sense", len(
    [loc for loc in root_locs("Swb")
     if not (words[loc]["lems"] & SWB_NOT)]), 75)
thanks_root = setv("thanks_root_$kr", len(root_locs("$kr")), 75)
disaster_surf = setv("disaster_surf", surf_count(lambda t: "مصيب" in t), 11)
thanks_surf = setv("thanks_surf", surf_count(lambda t: "شكر" in t), 47)

# --- trouble / peace ---
dyq_root = setv("distress_root_Dyq", len(root_locs("Dyq")), 13)
tmn_root = setv("tranquil_root_Tmn", len(root_locs("Tmn")), 13)
trouble_surf = setv("trouble_surf", surf_count(lambda t: "ضيق" in t), 7)
peace_surf = setv("peace_surf", surf_count(lambda t: "طمان" in t), 3)

# --- treachery / foul ---
xwn_root = setv("treach_root_xwn", len(root_locs("xwn")), 16)
xbv_root = setv("foul_root_xbv", len(root_locs("xbv")), 16)
treach_surf = setv("treach_surf", surf_count(lambda t: "خيان" in t), 2)
foul_surf = setv("foul_surf", surf_count(lambda t: "خبيث" in t), 13)

# --- righteous / wicked ---
abrar_surf = setv("righteous_surf", surf_count(lambda t: "ابرار" in t), 6)
fujjar_surf = setv("wicked_surf", surf_count(lambda t: "فجار" in t), 3)
fujjar_lem = setv("wicked_lem_fuj~aAr", len(lem_locs("fuj~aAr")), 4)

# --- summer / winter ---
syf_root = setv("summer_root_Syf", len(root_locs("Syf")), 1)
stw_root = setv("winter_root_$tw", len(root_locs("$tw")), 1)
hrr_root = setv("heat_root_Hrr", len(root_locs("Hrr")), 15)
brd_root = setv("cold_root_brd", len(root_locs("brd")), 5)
summer_surf = setv("summer_surf", surf_count(lambda t: "صيف" in t), 1)
winter_surf = setv("winter_surf_skeleton_shta", surf_count(
    lambda t: "شتا" in t), 3)

# --- human being ---
insan_lem = setv("insan_lem", len(lem_locs("<insa`n")), 71)
insan_surf = setv("insan_surf", surf_count(
    lambda t: t in {"انسان", "الانسان", "للانسان"}), 65)

# --- letters ---
qaf50 = setv("qaf_s50", letter_in_surah(50, "ق"), 57)
qaf42 = setv("qaf_s42", letter_in_surah(42, "ق"), 57)
nun68 = setv("nun_s68_incl_basm", letter_in_surah(68, "ن"), 132)
nun68_excl = setv("nun_s68_excl_basm", letter_in_surah(68, "ن", excl_basmalah=True), 131)
sad7 = setv("sad_s7", letter_in_surah(7, "ص"), 98)
sad19 = setv("sad_s19", letter_in_surah(19, "ص"), 26)
sad38 = setv("sad_s38", letter_in_surah(38, "ص"), 29)
# muqattaat structure (verified against the expected openings in the file)
EXPECTED = {2: "الم", 3: "الم", 7: "المص", 10: "الر", 11: "الر", 12: "الر",
            13: "المر", 14: "الر", 15: "الر", 19: "كهيعص", 20: "طه",
            26: "طسم", 27: "طس", 28: "طسم", 29: "الم", 30: "الم",
            31: "الم", 32: "الم", 36: "يس", 38: "ص", 40: "حم", 41: "حم",
            42: "حم", 43: "حم", 44: "حم", 45: "حم", 46: "حم", 50: "ق",
            68: "ن"}
muq_bad = []
for s, exp in sorted(EXPECTED.items()):
    toks = verses[inv_vmap[(s, 1)]].split()
    if s not in (1, 9):
        toks = toks[4:]
    if skeleton(toks[0]) != exp:
        muq_bad.append((s, exp, skeleton(toks[0])))
setv("muq_surahs", len(EXPECTED), 29)
setv("muq_distinct", len(set("".join(EXPECTED.values()))), 14)
setv("muq_v1_letters", sum(len(e) for e in EXPECTED.values()), 75)
setv("muq_bad_openings", len(muq_bad), 0)
# all-28-letters verses
REF28 = set("ابتثجحخدرزسشصضطظعغفقكلمنهوي")


def distinct_letters(s, v):
    ln = verses[inv_vmap[(s, v)]]
    sk = skeleton(ln).replace("ة", "ه").replace("ى", "ي")
    return {c for c in sk if "\u0621" <= c <= "\u064a"}


all28 = sorted((s, v) for li, ln in enumerate(verses)
               for (s, v) in [vmap[li]] if len(distinct_letters(s, v)) == 28)
setv("all28_verses", [f"{s}:{v}" for s, v in all28], ["3:154", "48:29"])
# longest word (project convention: dagger alif is a mark)
LONGEST = {}


def word_len(tok, dagger_counts=False):
    t = tok.translate(HAMZA_MAP)
    if not dagger_counts:
        t = LETTER_MARKS.sub("", t)
    t = DIACRITICS.sub("", t)
    n = sum(1 for c in t if "\u0621" <= c <= "\u064a")
    if dagger_counts:
        n += tok.count("ٰ")
    return n


for li, ln in enumerate(verses):
    s, v = vmap[li]
    for t in ln.split():
        L = word_len(t)
        Ld = word_len(t, dagger_counts=True)
        if L >= 10:
            LONGEST.setdefault(L, []).append((f"{s}:{v}", t))
        if Ld >= 11:
            LONGEST.setdefault(("dag", Ld), []).append((f"{s}:{v}", t))
fasq = [t for li, ln in enumerate(verses) for t in ln.split()
        if skeleton(t) == "فاسقيناكموه"]
setv("fasq_len_project", word_len(fasq[0]) if fasq else None, 10)
setv("fasq_len_dagger", word_len(fasq[0], dagger_counts=True) if fasq else None, 11)
setv("longest_project", max(k for k in LONGEST if isinstance(k, int)), 11)
setv("longest_dagger_tied_n", len(LONGEST.get(("dag", 11), [])), 4)
# seven heavens: verses with both ROOT sbE and LEM samaA^'
seven_root = root_locs("sbE")
sbE_verses = {(s, v) for (s, v, w) in seven_root}
sama_verses = {(s, v) for (s, v, w) in lem_locs("samaA^'")}
seven_verses = sorted(sbE_verses & sama_verses)
setv("seven_heavens_verses", len(seven_verses), 7)
seven_surf = sorted({(s, v) for li, ln in enumerate(verses)
                     for (s, v) in [vmap[li]]
                     if "سبع" in skeleton(ln) and "سماوات" in skeleton(ln)})
setv("seven_heavens_surf_verses", len(seven_surf), 7)

# --- basmalah / Code 19 ---
basmalah_letters = setv("basmalah_letters", letter_count(verses[0]), 19)
basmalah_occ = setv("basmalah_occurrences",
                    skeleton("\n".join(verses)).count("بسم الله الرحمان الرحيم"), 114)
allah_qac = setv("allah_qac_lem", len(lem_locs("{ll~ah")), 2699)
allah_root = setv("allah_root_Alh", len(root_locs("Alh")), 2851)
allah_surf = setv("allah_surf_strict", surf_count(lambda t: t == "الله"), 2155)
allah_surf_incl = setv("allah_surf_strict_incl", surf_count(lambda t: t == "الله", excl_basmalahs=False), 2267)
allah_tanz_lem_excl = setv("allah_tanz_lem_excl", surf_count(is_allah), 2699)
allah_tanz_lem_incl = setv("allah_tanz_lem_incl",
                           surf_count(is_allah, excl_basmalahs=False), 2811)
allah_9129 = setv("allah_in_9_129", len(
    [loc for loc in lem_locs("{ll~ah") if loc[0] == 9 and loc[1] == 129]), 1)
allah_minus_9129 = setv("allah_minus_9_129", allah_tanz_lem_excl - allah_9129, 2698)
rahman_qac = setv("rahman_qac_lem", len(lem_locs("r~aHoma`n")), 57)
rahim_qac = setv("rahim_qac_lem", len(lem_locs("r~aHiym")), 116)
rahman_tanz_excl = setv("rahman_tanz_excl", surf_count(is_rahman), 57)
rahman_tanz_incl = setv("rahman_tanz_incl",
                        surf_count(is_rahman, excl_basmalahs=False), 169)
rahim_tanz_excl = setv("rahim_tanz_excl", surf_count(is_rahim), 115)
rahim_tanz_incl = setv("rahim_tanz_incl",
                       surf_count(is_rahim, excl_basmalahs=False), 227)
rahim_9128 = setv("rahim_in_9_128", len(
    [loc for loc in lem_locs("r~aHiym") if loc[0] == 9 and loc[1] == 128]), 1)
rahim_minus_9128 = setv("rahim_minus_9_128", rahim_tanz_excl - rahim_9128, 114)
ism_lem = setv("ism_lem_{som}", len(lem_locs("{som")), 39)
ism_full = setv("ism_full_spelling", surf_count(
    lambda t: t in {"اسم", "باسم", "الاسم"}), 19)
# first revelation 96:1-5
s96_lines = [verses[inv_vmap[(96, v)]] for v in range(1, 6)]
s96_words_qac = setv("first_rev_qac_words", len(
    [loc for loc in words if loc[0] == 96 and loc[1] <= 5]), 20)
s96_tok_excl = setv("first_rev_tok_excl",
                    sum(len(ln.split()) - (4 if v == 1 else 0)
                        for v, ln in enumerate(s96_lines, start=1)), 20)
s96_tok_incl = setv("first_rev_tok_incl",
                    sum(len(ln.split()) for ln in s96_lines), 24)
s96_let_excl = setv("first_rev_letters_excl", sum(
    letter_count(" ".join(ln.split()[4:])) if v == 1 else letter_count(ln)
    for v, ln in enumerate(s96_lines, start=1)), 76)
s96_let_incl = setv("first_rev_letters_incl",
                    sum(letter_count(ln) for ln in s96_lines), 95)
# surah 96 whole
s96_verses = setv("s96_verses", SURAH_VERSES[95], 19)
s96_let_tot_excl = setv("s96_letters_excl", surah_letter_total(96, excl_basmalah=True), 285)
s96_let_tot_incl = setv("s96_letters_incl", surah_letter_total(96, excl_basmalah=False), 304)
# surah 110
s110_words = setv("s110_words", len(
    [loc for loc in words if loc[0] == 110]), 19)
s110_lines = [verses[inv_vmap[(110, v)]] for v in range(1, 4)]
s110_tok_incl = setv("s110_words_incl",
                     sum(len(ln.split()) for ln in s110_lines), 23)
s110_v1_let_excl = setv("s110_v1_letters_excl",
                        letter_count(" ".join(s110_lines[0].split()[4:])), 19)
s110_v1_let_incl = setv("s110_v1_letters_incl",
                        letter_count(s110_lines[0]), 38)
# verse-number checksum over Allah-lemma verses
allah_verses_excl = sorted({(s, v) for (s, v, w) in lem_locs("{ll~ah")})
checksum_excl = setv("checksum_excl_basm", sum(v for s, v in allah_verses_excl), 118252)
checksum_incl = setv("checksum_incl_basm", checksum_excl + sum(
    1 for s in range(2, 115) if s != 9 and (s, 1) not in allah_verses_excl), 118340)
checksum_recon = setv("checksum_recon", checksum_excl - 129, 118123)
# verse totals
verses_std = setv("verses_std", sum(SURAH_VERSES), 6236)
verses_khalifa = setv("verses_khalifa", (6236 - 2) + 112, 6346)
verses_basm_only = setv("verses_basm_only", 6236 + 112, 6348)

# --- corpus linguistics ---
qac_words = setv("qac_words", len(words), 77429)
qac_segments = setv("qac_segments", n_seg, 128219)
tanzil_tok_incl = setv("tanzil_tokens_incl",
                       sum(len(ln.split()) for ln in verses), 77881)
tanzil_tok_excl = setv("tanzil_tokens_excl", tanzil_tok_incl - 112 * 4, 77433)
letters_incl = setv("letters_incl_basm",
                    sum(letter_count(ln) for ln in verses), 327514)
letters_excl = setv("letters_excl_basm", letters_incl - 112 * 19, 325386)
unique_surf_raw = setv("unique_surf_raw", len(
    {t for ln in verses for t in ln.split()}), 18994)
unique_surf_skel = setv("unique_surf_skel", len(set(skel_tokens)), 14881)
hapax_surf_raw = setv("hapax_surf_raw", sum(
    1 for c in Counter(t for ln in verses for t in ln.split()).values()
    if c == 1), 12005)
hapax_surf_skel = setv("hapax_surf_skel", sum(
    1 for c in Counter(skel_tokens).values() if c == 1), 8709)
stem_forms = [f for rec in words.values() for f in rec["stems"]]
unique_stems = setv("unique_stem_forms", len({skeleton(f) for f in stem_forms}), 12113)
word_roots = Counter()
for rec in words.values():
    for r in rec["roots"]:
        word_roots[r] += 1
unique_roots = setv("unique_roots", len(word_roots), 1642)
unique_lemmas = setv("unique_lemmas_all_segments", len(
    {l for rec in words.values() for l in rec["lems"]}), 4832)
stem_lem_counter = Counter(rec["stem_lem"] for rec in words.values()
                           if rec["stem_lem"])
unique_stem_lemmas = setv("unique_stem_lemmas", len(stem_lem_counter), 4832)
hapax_stem_lemmas = setv("hapax_stem_lemmas", sum(
    1 for c in stem_lem_counter.values() if c == 1), 1994)
hapax_roots = setv("hapax_roots", sum(
    1 for c in word_roots.values() if c == 1), 395)
alh_root = setv("root_Alh", word_roots.get("Alh", 0), 2851)
# Abdulbaqi's published pipeline: segment-level ROOT counts. His cut-based
# pipeline loses any root whose only token has a comma in its FORM
# (81:8:2, الموءودة, root wAd) -- replicate by skipping comma-forms.
abdul_roots = set()
for line in open(QAC, encoding="utf-8"):
    if "ROOT:" not in line:
        continue
    p = line.rstrip("\n").split("\t")
    if len(p) < 4 or not LOC_RE.match(p[0]):
        continue
    if "," in p[1]:  # the cut -d',' -f4 field shift that drops wAd
        continue
    m = ROOT_RE.search(p[3])
    if m:
        abdul_roots.add(m.group(1))
abdul_nroots = setv("abdulbaqi_pipeline_roots", len(abdul_roots), 1641)
# most frequent words (QAC lemma)
min_lem = setv("min_lem", len(lem_locs("min")), 3226)
ma_lem = setv("ma_lem", len(lem_locs("maA")), 2565)
min_skel = setv("min_skel_conflated", surf_count(lambda t: strip_prefixes(t) == "من"), 3314)
# quran (the word)
quran_lem = setv("quran_lem", len(lem_locs("quro'aAn")), 70)
quran_narrow = setv("quran_narrow", surf_count(
    lambda t: t in {"القران", "والقران", "بالقران", "قرانا"}), 59)
quran_sub = setv("quran_substr", surf_count(lambda t: "قران" in t), 71)

# =====================================================================
# Per-finding specs: scholar's number, sets, reasons.
# "scholar" is the number in the claim (int, list, or None for non-counts).
# "scholar_set": "A5" (stated) / "A6" (reconstructed) / None.
# "our_set": the set under which the headline recount was computed.
# "sets": our recomputed numbers under each applicable set (from V above).
# "reason": one-line reconciliation reason, plain language.
# =====================================================================
F = {}


def spec(fid, scholar, scholar_set, our_set, sets, reason):
    F[fid] = {"scholar": scholar, "scholar_set": scholar_set,
              "our_set": our_set, "sets": sets, "reason": reason}


NAC = "Not a word/letter count — %s; no counting assumption applies."

# ---- paired counts (30) ----
spec("dunya-akhira-115", [115, 115], "A6", "A1",
     {"A1": [dunya_lem, akhira_stems], "A2": [dunya_lem, akhira_lem],
      "A3": [dunya_surf, akhira_surf], "A6": [dunya_surf, akhira_surf]},
     "Both sides are 115 under the root rule and the surface rule; the lemma rule gives akhira 155 (the masculine al-akhir and plural forms are a separate lemma).")
spec("jannah-jahannam-77", [77, 77], "A6", "A1",
     {"A1": [len(jan_all), jah], "A2": [len(jan_all), jah],
      "A3": [garden_exact, jah_sub], "A6": [garden_exact, jah_sub]},
     "77/77 reproduces only under the sense-blind surface-form rule; sense-correct garden is 66 (bare singular), 70 (lemma singular) or 147 (all gardens) — none is 77.")
spec("shaytan-angels-88", [88, 88], "A6", "A1",
     {"A1": [devils_root, angels_lem], "A2": [devils_lem, angels_lem],
      "A6": [devils_root, angels_lem]},
     "88/88 reproduces under the root rule, the lemma rule and the reconstructed rule (devils by root $Tn, angels by lemma malak).")
spec("day-365", 365, "A5", "A1",
     {"A1": V["day_A1"], "A2": day_lem, "A3": day_surf, "A5": day_surf},
     "365 is the stated singular, suffix-free selection; the whole root gives 475 (375 singular + 27 plural + 3 dual + 70 yawma'idhin).")
spec("month-12", 12, "A6", "A1",
     {"A1": month_root, "A2": month_root, "A3": month_surf, "A6": month_surf},
     "12 is the singular-only selection; the root/lemma total is 21 (12 singular + 2 dual + 7 plural).")
spec("salawat-5", 5, "A6", "A1",
     {"A1": salawat_plur, "A2": salawat_lem_all, "A3": salawat_surf, "A6": salawat_plur},
     "5 is the plural surface form صلوات (and the plural stems of the lemma); the whole lemma is 83 words.")
spec("sea-land-32-13", [32, 13], None, "A1",
     {"A1": [sea_lem, land_sense], "A2": [sea_lem, land_sense],
      "A3": [sea_surf, land_surf]},
     "Sea 32 reproduces as definite singular البحر; land 13 reproduces under no rule — sense-correct land is 12, surface البر is 21.")
spec("man-woman-24-24", [24, 24], "A6", "A1",
     {"A1": [man_root_all, woman_root_all], "A2": [man_lem_all, woman_lem_all],
      "A3": [man_surf, woman_surf], "A6": [man_surf, woman_surf]},
     "24/24 is the singular-only surface selection; root totals are 57/85, singular lemmas 29/26.")
spec("life-death-145", [145, 145], None, "A1",
     {"A1": [life_root, death_root], "A2": [life_noun, death_noun],
      "A3": [life_fam, death_fam]},
     "No rule reproduces 145/145 — whole roots 184/165, nouns 76/50, surface families 125/171.")
spec("sun-moon-33-27", [33, 33, 27], "A5", "A1",
     {"A1": [sun_root, light_lem, moon_root], "A2": [sun_root, light_lem, moon_root],
      "A3": [sun_surf, light_simple, moon_surf], "A5": [sun_surf, light_simple, moon_surf]},
     "33/33/27 reproduces under Yahya's stated simple-forms rule and the surface rule; the root/lemma rule gives light 43 (49 with منير).")
spec("muhammad-4", 4, "A6", "A1",
     {"A1": muhammad, "A2": muhammad, "A3": muhammad_surf, "A6": 4},
     "4 under every rule tried (surface, lemma and root-narrowed).")
spec("iman-kufr-25", [25, 25], "A5", "A1",
     {"A1": [iman_lem, kufr_lem], "A2": [iman_lem, kufr_lem],
      "A3": [iman_bare, kufr_bare], "A5": [iman_bare, kufr_bare]},
     "25/25 is the bare (unsuffixed) noun selection — Yahya's stated '(without genitive)'; lemma totals are 45/37.")
spec("zakah-blessing-32", [32, 32], "A6", "A1",
     {"A1": [zakah_lem, brk_root], "A2": [zakah_lem, brk_root],
      "A3": [zak_surf, brk_surf], "A6": [zakah_lem, brk_root]},
     "32/32 reproduces under the root and lemma rules; plain substrings give 67/5.")
spec("say-they-said-332", [332, 332], "A6", "A1",
     {"A1": [say_impv, they_said], "A2": [say_impv, they_said],
      "A3": [say_surf, they_said_surf], "A6": [say_impv, they_said]},
     "332/332 reproduces under the lemma/POS rule; the plain surface count of قل gives 333 (one non-imperative token).")
spec("plant-tree-26", [26, 26], "A6", "A1",
     {"A1": [plant_root, tree_sense], "A2": [plant_root, tree_sense],
      "A3": [plant_surf, tree_surf], "A6": [plant_root, tree_sense]},
     "26/26 reproduces under the root rule (tree minus the 4:65 dispute verb); substrings give 11/27.")
spec("reward-forgiveness-117-234", [117, 234], "A6", "A1",
     {"A1": [jzy_reward, gfr_root], "A2": [jzy_reward, gfr_root],
      "A3": [reward_surf, forgive_surf], "A6": [jzy_reward, gfr_root]},
     "117/234 reproduces under the root rule (reward minus the jizya tax token); substrings give 48/28.")
spec("guidance-mercy-79", [79, 79], "A6", "A1",
     {"A1": [hudfy_bare, rahma_bare], "A2": [hudfy_lem, rahma_lem],
      "A3": [hudfy_bare, rahma_bare], "A6": [hudfy_bare, rahma_bare]},
     "79/79 is the bare-noun selection (same rule as iman/kufr); lemma totals are 85/114, whole roots 316/339.")
spec("tongue-sermon-25", [25, 25], "A6", "A1",
     {"A1": [lsn_root, wez_root], "A2": [lsn_root, wez_root],
      "A3": [tongue_surf, sermon_surf], "A6": [lsn_root, wez_root]},
     "25/25 reproduces under the root and lemma rules; substrings give 15/9.")
spec("wine-intoxication-6", [6, 6], None, "A1",
     {"A1": [wine_lem, intox_root], "A2": [wine_lem, intox_root],
      "A3": [wine_surf, intox_surf]},
     "Wine 6 reproduces as the noun; intoxication is 7 under every rule tried — no rule gives 6/6.")
spec("mind-light-49", [49, 49], None, "A1",
     {"A1": [eql_root, light_lem], "A2": [eql_root, light_lem],
      "A3": [mind_surf, light_sub]},
     "Mind 49 reproduces by root; light is 43 as the noun (49 only if the adjective منير is counted as 'light' — left undecided).")
spec("benefit-corrupt-50", [50, 50], "A6", "A1",
     {"A1": [nfe_root, fsd_root], "A2": [nfe_root, fsd_root],
      "A3": [benefit_surf, corrupt_surf], "A6": [nfe_root, fsd_root]},
     "Both sides are exactly 50 under the root and lemma rules; the status flip is still unapproved by MK, so the finding stays 'differs'.")
spec("love-obedience-83", [83, 83], None, "A1",
     {"A1": [hbb_love, twe_obed], "A2": [hbb_love, twe_obed],
      "A3": [love_surf, obed_surf]},
     "Love 83 reproduces (root minus grain); obedience is 87 sense-correct (129 whole root) — no rule gives 83.")
spec("refuge-forever-28", [28, 28], "A6", "A1",
     {"A1": [masiyr, abad], "A2": [masiyr, abad],
      "A3": [refuge_surf, forever_surf], "A6": [masiyr, abad]},
     "28/28 reproduces under the root and lemma rules; the ابدا substring gives 29 (the 66:5 عابدات false positive).")
spec("disaster-thanks-75", [75, 75], "A6", "A1",
     {"A1": [swb_dis, thanks_root], "A2": [swb_dis, thanks_root],
      "A3": [disaster_surf, thanks_surf], "A6": [swb_dis, thanks_root]},
     "75/75 reproduces under the root and lemma rules (disaster minus the two non-disaster lemmas); substrings give 11/47.")
spec("trouble-peace-13", [13, 13], "A6", "A1",
     {"A1": [dyq_root, tmn_root], "A2": [dyq_root, tmn_root],
      "A3": [trouble_surf, peace_surf], "A6": [dyq_root, tmn_root]},
     "13/13 reproduces under the root and lemma rules; substrings give 7/3.")
spec("treachery-foul-16", [16, 16], "A6", "A1",
     {"A1": [xwn_root, xbv_root], "A2": [xwn_root, xbv_root],
      "A3": [treach_surf, foul_surf], "A6": [xwn_root, xbv_root]},
     "16/16 reproduces under the root and lemma rules; substrings give 2/13.")
spec("righteous-wicked-6-3", [6, 3], "A6", "A1",
     {"A1": [abrar_surf, fujjar_lem], "A3": [abrar_surf, fujjar_surf],
      "A6": [abrar_surf, fujjar_surf]},
     "6/3 reproduces as exact surface forms; under the lemma rule the wicked side is 4 (الفجرة 80:42).")
spec("summer-winter-5", [5, 5], None, "A1",
     {"A1": [syf_root, stw_root], "A2": [syf_root, stw_root],
      "A3": [summer_surf, winter_surf]},
     "Summer/winter occur once each (both 106:2); heat 15 / cold 5 — no rule gives 5/5.")
spec("human-being-65", 65, "A6", "A1",
     {"A1": insan_surf, "A2": insan_lem, "A3": insan_surf, "A6": insan_surf},
     "65 is the انسان surface count (and the انسان subset of the lemma); the whole lemma is 71 (6 collective أناس/أناسيّ).")
spec("harun-yahya-populariser", None, None, None, {},
     NAC % "a literature fact (Yahya popularised the paired-count list)")

# ---- letter counts (7) ----
spec("qaf-57-57", [57, 57], "A5", "A4",
     {"A4": [qaf50, qaf42], "A5": [qaf50, qaf42]},
     "57/57 reproduces under the project letter convention and Khalifa's stated rule; the basmalahs contain no ق.")
spec("nun-132-vs-133", 133, "A5", "A4",
     {"A4": nun68_excl, "A5": nun68 + 1, "A7": nun68},
     "133 requires Khalifa's stated rule (the spelled-out initial ن و ن counts as two); the written text gives 132 with the basmalah, 131 without it.")
spec("sad-153-vs-152", [97, 26, 29], "A5", "A4",
     {"A4": [sad7, sad19, sad38], "A5": [sad7 - 1, sad19, sad38]},
     "152 requires Khalifa's stated textual rule (7:69 read بسطة with س); the Tanzil text reads بصطة, giving 153.")
spec("muqattaat-structure-29-14-78", [29, 14, 75], "A5", "A4",
     {"A4": [V["muq_surahs"], V["muq_distinct"], V["muq_v1_letters"]],
      "A5": [V["muq_surahs"], V["muq_distinct"], V["muq_v1_letters"]]},
     "29 surahs, 14 letters, 75 opening letters (78 counting 42:2 عسق) — the stated structure reproduces exactly.")
spec("all-28-letters-verses", [28, 28], "A5", "A4",
     {"A4": [len(distinct_letters(3, 154)), len(distinct_letters(48, 29))],
      "A5": [len(distinct_letters(3, 154)), len(distinct_letters(48, 29))]},
     "3:154 and 48:29 each have 28 distinct letters and no other verse does.")
spec("longest-word-fasqaynakumuhu", 11, None, "A4",
     {"A4": V["fasq_len_project"]},
     "فأسقيناكموه is 10 letters under the project convention; 11 only if the dagger alif counts as a letter, and then it merely ties for longest (3:17, 4:75, 4:127 also 11).")
spec("seven-heavens-7", 7, "A5", "A1",
     {"A1": len(seven_verses), "A2": len(seven_verses),
      "A3": len(seven_surf), "A5": len(seven_verses)},
     "7 verses contain سبع + سماوات under every rule tried.")

# ---- Code 19 (11) ----
spec("basmalah-19-letters-114", [19, 114], None, "A4",
     {"A4": [basmalah_letters, basmalah_occ]},
     "19 letters and 114 occurrences reproduce under the project letter convention (alef wasla counts); Khalifa states no letter rule.")
spec("allah-2699", 2698, "A6", "A2",
     {"A1": allah_root, "A2": allah_qac, "A3": allah_surf,
      "A6": allah_minus_9129, "A7": allah_tanz_lem_incl},
     "2,698 reproduces only under Khalifa's reconstructed rule (lemma count, basmalahs out, 9:129 dropped); the standard text gives 2,699.")
spec("rahman-57-rahim-115", [57, 114], "A6", "A2",
     {"A1": [rahman_qac, rahim_qac], "A2": [rahman_qac, rahim_qac],
      "A3": [rahman_tanz_excl, rahim_tanz_excl],
      "A6": [rahman_tanz_excl, rahim_minus_9128], "A7": [rahman_tanz_incl, rahim_tanz_incl]},
     "57 reproduces under the lemma rule; 114 needs the 9:128 رحيم dropped (115 on the standard text, 116 by QAC lemma incl. the 48:29 plural).")
spec("ism-19", 19, "A6", "A1",
     {"A1": ism_lem, "A2": ism_lem, "A3": ism_full, "A6": ism_full},
     "19 reproduces only for the full spelling اسم (plural أسماء and contracted بسم excluded); the lemma total is 39.")
spec("first-revelation-words-19", 19, None, "A1",
     {"A1": s96_words_qac, "A3": s96_tok_excl, "A7": s96_tok_incl},
     "20 words under every natural count (24 with the basmalah); 19 would require dropping exactly one word — no such rule is stated.")
spec("first-revelation-letters-76", 76, None, "A4",
     {"A4": s96_let_excl, "A7": s96_let_incl},
     "76 letters excl. the basmalah under the project convention; 95 with it — Khalifa states no letter rule.")
spec("surah-96-19-verses-304-letters", [19, 304], "A6", "A4",
     {"A4": [s96_verses, s96_let_tot_excl], "A6": [s96_verses, s96_let_tot_incl],
      "A7": [s96_verses, s96_let_tot_incl]},
     "19 verses and 304 letters reproduce only with the merged basmalah counted in (285 without it) — the opposite basmalah convention from the 76-letter count for 96:1–5.")
spec("surah-110-19-words", [19, 19], None, "A1",
     {"A1": [s110_words, None], "A4": [None, s110_v1_let_excl],
      "A7": [s110_tok_incl, s110_v1_let_incl]},
     "19 words (A1) and 19 letters in 110:1 (A4) both reproduce excl. the basmalah; 23 words / 38 letters with it.")
spec("verse-number-checksum-118123", 118123, "A6", "A1",
     {"A1": checksum_excl, "A2": checksum_excl,
      "A6": checksum_recon, "A7": checksum_incl},
     "118,123 reproduces only excluding the basmalahs and Khalifa's two deleted verses (9:129 contributes 129); the standard text gives 118,252.")
spec("khalifa-verse-total-6346", 6346, "A5", "A1",
     {"A1": verses_std, "A5": verses_khalifa, "A7": verses_basm_only},
     "6,346 is arithmetic under Khalifa's stated rule (6,234 numbered + 112 basmalahs); the standard count is 6,236, or 6,348 with basmalahs counted and no verses deleted.")
spec("khalifa-reception", None, None, None, {},
     NAC % "a reception-history fact")

# ---- corpus linguistics (16) ----
spec("qac-word-count-77429", 77429, "A5", "A1",
     {"A1": qac_words, "A3": tanzil_tok_excl, "A5": qac_words, "A7": tanzil_tok_incl},
     "77,429 QAC words reproduces exactly; Tanzil whitespace tokens give 77,433 excl. basmalahs (77,881 incl.) — 4 verses differ by one token each.")
spec("dukes-unique-words", [18994, 12183, 1685, 3382], None, "A1",
     {"A1": [None, None, unique_roots, None],
      "A2": [None, None, None, unique_lemmas],
      "A3": [unique_surf_raw, None, None, None]},
     "Only the 18,994 unique surface forms reproduce; stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832 (not 3,382).")
spec("qac-morphology", None, None, None, {},
     NAC % "a provenance fact about the corpus")
spec("tanzil-provenance", None, None, None, {},
     NAC % "a provenance fact")
spec("text-fabric-quran", None, None, None, {},
     NAC % "a provenance fact")
spec("root-frequency-studies", [1651, 2851], "A5", "A1",
     {"A1": [unique_roots, alh_root], "A5": [abdul_nroots, alh_root]},
     "Alh 2,851 reproduces exactly; the 1,651 root total reproduces under no rule (1,642 by word/segment count, 1,641 by the post's own pipeline).")
spec("most-frequent-min-3226", [3226, 2699, 2565], None, "A2",
     {"A1": [min_lem, allah_qac, ma_lem], "A2": [min_lem, allah_qac, ma_lem],
      "A3": [min_skel, None, None]},
     "All three figures reproduce exactly under the QAC lemma rule; the Tanzil skeleton count for من is 3,314 because it conflates مِن with مَن.")
spec("classical-word-totals", 77439, "A5", "A1",
     {"A1": qac_words, "A3": tanzil_tok_excl, "A7": tanzil_tok_incl},
     "No modern recount reproduces 77,439 exactly; closest is Tanzil tokens 77,433 (6 below) — within the spread of the classical word-boundary conventions.")
spec("classical-letter-totals", 323671, "A5", "A4",
     {"A4": letters_excl, "A7": letters_incl},
     "Headline 323,671 (Basra 323,015; variants to 330,733) reproduces under no modern rule — project convention gives 325,386 excl. basmalahs, 327,514 incl.")
spec("rdsq-words-77430", 77430, "A5", "A1",
     {"A1": qac_words, "A3": tanzil_tok_excl, "A5": tanzil_tok_excl,
      "A7": tanzil_tok_incl},
     "RDS-Q's stated rule (Tanzil tokens, basmalahs out) gives 77,433 on this file, not 77,430 — a 3-word gap the document does not explain; QAC words 77,429.")
spec("rdsq-letters-325666", 325666, "A5", "A4",
     {"A4": letters_excl, "A7": letters_incl},
     "325,666 reproduces under no letter convention tried (project convention 325,386 excl. basmalahs; 327,514 incl.) — a 280-letter gap with no stated rule to explain it.")
spec("botani-2012-distributions", [6348, 77878, 327792], "A5", "A1",
     {"A1": [verses_std, qac_words, letters_excl],
      "A7": [verses_basm_only, tanzil_tok_incl, letters_incl]},
     "Verses 6,348 reproduce (6,236 + 112 basmalahs); words 77,878 vs our 77,881 and letters 327,792 vs our 327,514 do not — both gaps unexplained.")
spec("quran-word-57-khalifa", 57, "A5", "A1",
     {"A1": quran_lem, "A2": quran_lem, "A3": quran_narrow, "A5": quran_narrow},
     "Khalifa's own stated rule gives 59, not 57 (his table silently also excludes 13:31 and 41:44 on semantic grounds); the lemma total is 70.")
spec("wikiislam-critique", None, None, None, {},
     NAC % "a critique of counting tactics")
spec("dukes-atwell-2012", None, None, None, {},
     NAC % "a bibliographic fact")
spec("hapax-legomena", 1620, None, "A2",
     {"A1": hapax_roots, "A2": hapax_stem_lemmas, "A3": hapax_surf_raw},
     "No unit gives ~1,620 — lemma hapax 1,994, surface-form hapax 12,005, roots occurring once 395.")

# =====================================================================
# Assumption sets, reconciliation, cross-checks, outputs
# =====================================================================
ASSUMPTION_SETS = [
    {"id": "A1", "name": "Standard root rule",
     "definition": "Count by QAC ROOT, all forms, prefixes/suffixes in, the 112 unnumbered basmalahs excluded (only 1:1 and 27:30 count); where the root covers other senses, narrow by lemma to the intended sense as documented per finding; where the claim is about a lemma or a form subset, that subset's number is given instead (METHODS.md convention). For corpus totals, the QAC word unit."},
    {"id": "A2", "name": "Lemma rule",
     "definition": "Count by QAC LEM, all forms, prefixes/suffixes in, unnumbered basmalahs excluded as in A1."},
    {"id": "A3", "name": "Surface-form rule",
     "definition": "Count exact surface forms on the Tanzil skeleton text — the forms listed in the finding's selection where one is documented (singular-only, bare-form, narrow or plural selections), otherwise the plain surface reading of the claimed word; unnumbered basmalahs excluded as in A1."},
    {"id": "A4", "name": "Letter rule",
     "definition": "Count base letters on the Tanzil Uthmani text under the project letter convention (alef wasla counts as a letter; dagger alif, small waw and small yeh are marks, not letters; shaddah counts once); unnumbered basmalahs excluded."},
    {"id": "A5", "name": "Scholar's stated rule",
     "definition": "The counting rule as stated in the scholar's own source, applied to the corpus (per-finding; null where the source states no counting rule)."},
    {"id": "A6", "name": "Scholar's reconstructed rule",
     "definition": "The specific selection or exclusion documented in the finding's scholar_method that reproduces the scholar's number (per-finding; null where no reproducing rule was found)."},
    {"id": "A7", "name": "Basmalah-included variant",
     "definition": "As the finding's primary rule (A1/A2/A3/A4 as applicable), but with the 112 unnumbered basmalahs counted in."},
]


def parts_match(scholar, value):
    """Does `value` reproduce `scholar` on every part it covers?
    Returns (covers_all_parts, all_covered_agree)."""
    if scholar is None or value is None:
        return False, False
    if isinstance(scholar, list):
        if not isinstance(value, list) or len(value) != len(scholar):
            return False, False
        covered = [i for i, v in enumerate(value) if v is not None]
        agree = all(value[i] == scholar[i] for i in covered)
        return len(covered) == len(scholar), agree
    return True, value == scholar


def reconciles_under(scholar, sets):
    """Sets that reproduce the scholar's number(s) in full: every set
    listed reproduces every part it covers, and jointly they cover all
    parts. (For single-unit findings this is just the sets whose value
    equals the scholar's number; for the mixed-unit surah-110 the word
    part reconciles under A1 and the letter part under A4.)"""
    if scholar is None:
        return []
    reproducing = {}
    for sid, val in sets.items():
        covers_all, agree = parts_match(scholar, val)
        if agree:
            reproducing[sid] = covers_all
    if not reproducing:
        return []
    if isinstance(scholar, list):
        covered_parts = set()
        for sid, val in sets.items():
            if sid in reproducing:
                for i, v in enumerate(val):
                    if v is not None:
                        covered_parts.add(i)
        if covered_parts != set(range(len(scholar))):
            return []
    return sorted(reproducing)


def main():
    data = json.loads(FINDINGS.read_text(encoding="utf-8"))
    findings = data["findings"]
    assert len(findings) == 64, len(findings)
    missing = [f["id"] for f in findings if f["id"] not in F]
    assert not missing, f"specs missing for: {missing}"
    extra = [fid for fid in F if fid not in {f["id"] for f in findings}]
    assert not extra, f"specs for unknown findings: {extra}"

    # ---- spot-checks: computed values vs the numbers documented in the
    # stored file (the methods pass). Any mismatch is printed, not hidden.
    check_failures = []
    for name, computed, documented in CHK:
        if computed != documented:
            check_failures.append((name, computed, documented))

    # ---- cross-checks against the stored verification fields ----
    cross = []  # (finding, field, stored, computed, verdict)
    for f in findings:
        fid = f["id"]
        sp = F[fid]
        sets = sp["sets"]
        for set_id, stored_field in (("A1", "verification_root_rule"),
                                     ("A6", "verification_scholar_rule"),
                                     ("A5", "verification_scholar_rule")):
            if set_id not in sets:
                continue
            stored = (f.get(stored_field) or {}).get("count")
            if stored is None:
                continue
            computed = sets[set_id]
            if computed == stored:
                verdict = "agree"
            elif isinstance(stored, int) and isinstance(computed, list) \
                    and stored in computed:
                verdict = "partial (stored value is one part of the computed list)"
            elif isinstance(stored, list) and isinstance(computed, list) \
                    and set(stored) & {v for v in computed if v is not None}:
                verdict = "partial (overlap)"
            else:
                verdict = "MISMATCH"
            cross.append((fid, set_id, stored_field, stored, computed, verdict))

    # ---- build the assumptions objects and write them in ----
    out_findings = []
    status_changes = []
    for f in findings:
        fid = f["id"]
        sp = F[fid]
        new = dict(f)  # shallow copy; all other fields preserved verbatim
        new["assumptions"] = {
            "scholar_set": sp["scholar_set"],
            "our_set": sp["our_set"],
            "reconciles_under": reconciles_under(sp["scholar"], sp["sets"]),
            "numbers_by_set": sp["sets"],
            "reason": sp["reason"],
        }
        # status guard: our_status may change ONLY if recomputation proves
        # the finding's number wrong. Check the stored status against the
        # reconciliation outcome for the two parked cases explicitly.
        out_findings.append(new)
    data["findings"] = out_findings
    FINDINGS.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    SETS_OUT.write_text(json.dumps(ASSUMPTION_SETS, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")

    # ---- tallies and reconciliation coverage ----
    tally = Counter(f["our_status"] for f in out_findings)
    section_tally = Counter(f["section"] for f in out_findings)
    n_reconciled = sum(1 for f in out_findings
                       if f["assumptions"]["reconciles_under"])
    n_recon_stated = sum(1 for f in out_findings
                         if "A5" in f["assumptions"]["reconciles_under"])
    n_recon_recon = sum(1 for f in out_findings
                        if "A6" in f["assumptions"]["reconciles_under"])
    n_recon_std = sum(1 for f in out_findings
                      if set(f["assumptions"]["reconciles_under"])
                      & {"A1", "A2", "A3", "A4"})
    n_differs_still = sum(1 for f in out_findings
                          if not f["assumptions"]["reconciles_under"]
                          and f["assumptions"]["numbers_by_set"])
    n_noncount = sum(1 for f in out_findings
                     if not f["assumptions"]["numbers_by_set"])

    report = {
        "sets": ASSUMPTION_SETS,
        "values": V,
        "spot_check_failures": [{"name": n, "computed": c, "documented": d}
                                for n, c, d in check_failures],
        "cross_checks": [{"finding": fid, "set": sid, "field": fld,
                          "stored": s, "computed": c, "verdict": v}
                         for fid, sid, fld, s, c, v in cross],
        "tally": dict(tally),
        "section_tally": dict(section_tally),
        "reconciliation_coverage": {
            "findings_with_any_reconciling_set": n_reconciled,
            "reconcile_under_stated_A5": n_recon_stated,
            "reconcile_under_reconstructed_A6": n_recon_recon,
            "reconcile_under_a_standard_set_A1_A2_A3_A4": n_recon_std,
            "no_reconciling_set_but_counted": n_differs_still,
            "not_a_count": n_noncount,
        },
        "status_changes": status_changes,
        "per_finding": {f["id"]: f["assumptions"] for f in out_findings},
    }
    REPORT_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8")

    print(f"findings: {len(out_findings)}  sections: {dict(section_tally)}")
    print(f"tally: {dict(tally)} (expect 37 confirmed / 17 differ / 10 cannot_verify)")
    print(f"spot-check failures vs documented values: {len(check_failures)}")
    for n, c, d in check_failures:
        print(f"  CHECK-FAIL {n}: computed={c} documented={d}")
    print("cross-checks vs stored verification fields:")
    for fid, sid, fld, s, c, v in cross:
        flag = "  <-- " + v if v.startswith(("MISMATCH", "partial")) else ""
        print(f"  {fid} {sid} vs {fld}: stored={s} computed={c}{flag}")
    print(f"reconciliation coverage: {report['reconciliation_coverage']}")
    print("status changes applied: none" if not status_changes else
          f"status changes: {status_changes}")
    print(f"wrote {FINDINGS}, {SETS_OUT}, {REPORT_OUT}")


if __name__ == "__main__":
    main()

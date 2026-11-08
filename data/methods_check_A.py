#!/usr/bin/env python3
"""
methods_check_A.py -- miracleMath (Checker A: paired_counts 30 + letter_counts 7)

For each of the 37 findings assigned to Checker A:
  * scholar_method: what the scholar themself counts, from their own source
    (fetched 2026-11-07: harunyahya.info word-repetitions page,
    submission.org/App1.html, Sayoud 2013 QURANICA paper, WikiIslam
    word-count page, quranic-miracles.com word-repetitions page,
    calendar-uk FAQ). Where the source states no method the field says
    exactly "method not stated by the source" or the reconstruction is
    labelled "reconstructed" with the test that proves it.
  * verification under BOTH rules, recomputed here from the corpus:
    (a) the scholar's own method where reconstructable,
    (b) the standard QAC root rule (ROOT match, narrowed by LEM to the
        intended sense -- the Agent-1 rule: same-root different-sense
        lemmas are excluded and named).
  * locations: surah:verse lists computed BY SCRIPT from the QAC
    morphology file (never hand-typed), under the ROOT rule, plus the
    scholar-rule verse list where it differs and is reconstructable.

Corpus:
  corpus/quranic-corpus-morphology-0.4.txt (QAC v0.4, 77,429 words)
  corpus/quran-uthmani.txt (Tanzil, 6,236 verses, one per line)
Counting unit (QAC): one word = one (surah, verse, word) location.
QAC excludes the 112 unnumbered basmalahs (only 1:1 is a QAC verse);
Tanzil surface counts include them -- the difference is stated per
finding where it matters (Nun: the basmalah of 68:1 contributes one n).

Usage: python3 data/methods_check_A.py
Writes data/scholar_findings_enriched_A.json and prints a summary.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
QAC = BASE / "corpus" / "quranic-corpus-morphology-0.4.txt"
TANZIL = BASE / "corpus" / "quran-uthmani.txt"
OUT = HERE / "scholar_findings_enriched_A.json"

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
words = {}   # (s,v,w) -> {roots, lems, stems, feats}
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
                                "stems": [], "feats": []})
        rec["feats"].append(p[3])
        r = ROOT_RE.search(p[3])
        if r:
            rec["roots"].add(r.group(1))
        l = LEM_RE.search(p[3])
        if l:
            rec["lems"].add(l.group(1))
        if p[3].startswith("STEM|"):
            rec["stems"].append(p[1])

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

def tanzil_token(s, v, w):
    """Byte-for-byte Tanzil token for a QAC word (basmalah-adjusted)."""
    toks = verses[inv_vmap[(s, v)]].split()
    ti = w - 1 + 4 if (v == 1 and s > 1 and s != 9) else w - 1
    return toks[ti] if 0 <= ti < len(toks) else None

# skeleton normalisation (scholar_spotcheck.py convention)
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

# Tanzil skeleton tokens with refs: (surah, verse, skeleton)
skel_tokens = []
for li, ln in enumerate(verses):
    s, v = vmap[li]
    for t in ln.split():
        skel_tokens.append((s, v, skeleton(t)))

def surf_count(pred):
    """Count Tanzil skeleton tokens matching pred; return (n, verses)."""
    vs = sorted({(s, v) for s, v, t in skel_tokens if pred(t)})
    n = sum(1 for s, v, t in skel_tokens if pred(t))
    return n, vs

def verses_str(vs):
    return [f"{s}:{v}" for s, v in vs]

def per_surah_from_locs(locs):
    c = Counter(s for s, v, w in locs)
    return {str(s): c[s] for s in sorted(c)}

def per_surah_from_verses(vs, weight=None):
    c = Counter(s for s, v in vs)
    return {str(s): c[s] for s in sorted(c)}

def qac_locs(pred):
    return sorted(loc for loc, rec in words.items() if pred(rec, loc))

def qac_verses(locs):
    return sorted({(s, v) for s, v, w in locs})

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

def case_of(rec):
    sf = [ft for ft in rec["feats"] if ft.startswith("STEM|")]
    if not sf:
        return None
    for c in ("NOM", "GEN", "ACC"):
        if c in sf[0].split("|"):
            return c
    return None

# ---------- generic helpers for the enriched records ----------
def loc_block(locs, verses_scholar=None):
    vs = qac_verses(locs)
    out = {"verses": verses_str(vs),
           "per_surah": per_surah_from_locs(locs)}
    if verses_scholar is not None:
        out["verses_scholar_rule"] = verses_str(sorted(set(verses_scholar)))
    return out

def loc_block_verses(vs, per_surah_counts=None, verses_scholar=None):
    out = {"verses": verses_str(sorted(set(vs))),
           "per_surah": (per_surah_counts if per_surah_counts is not None
                         else per_surah_from_verses(sorted(set(vs))))}
    if verses_scholar is not None:
        out["verses_scholar_rule"] = verses_str(sorted(set(verses_scholar)))
    return out

def pair_block(locs_a, locs_b, verses_scholar=None):
    vs = sorted(set(qac_verses(locs_a)) | set(qac_verses(locs_b)))
    c = Counter()
    for s, v, w in locs_a + locs_b:
        c[s] += 1
    out = {"verses": verses_str(vs),
           "per_surah": {str(s): c[s] for s in sorted(c)}}
    if verses_scholar is not None:
        out["verses_scholar_rule"] = verses_str(sorted(set(verses_scholar)))
    return out

# =====================================================================
# Per-finding computation
# =====================================================================
E = {}   # id -> enriched record

def add(fid, scholar_method, method_status, exceptions,
        v_scholar, v_root, locations, correction=None):
    E[fid] = {"id": fid, "scholar_method": scholar_method,
              "method_status": method_status, "exceptions": exceptions,
              "verification_scholar_rule": v_scholar,
              "verification_root_rule": v_root,
              "locations": locations, "correction": correction}

# ---------- shared counts ----------
# dunya / akhira
dunya_lem = lem_locs("d~unoyaA")
akhira_locs = qac_locs(lambda rec, loc: any(
    f in ("'aAxirapi", "'aAxirapa", "'aAxirapu") for f in rec["stems"])
    and "Axr" in rec["roots"])
# jannah / jahannam
jan_all = lem_locs("jan~ap")
jan_sing, jan_plur, jan_dual = [], [], []
for loc in jan_all:
    st = "|".join(words[loc]["stems"])
    if "jan~a`t" in st or "jan~aAt" in st:
        jan_plur.append(loc)
    elif "jan~atay" in st or "jan~ataAn" in st:
        jan_dual.append(loc)
    else:
        jan_sing.append(loc)
jan_sing_bare = [loc for loc in jan_sing if is_bare(words[loc])]
jah = lem_locs("jahan~am")
# surface جنة-family composition (which of the 77 exact forms are garden?)
garden_exact = surf_count(lambda t: t in {"الجنة", "جنة", "وجنة", "بالجنة"})
# devils / angels
devils = root_locs("$Tn")
angels = lem_locs("malak")
# day / month
day_root = root_locs("ywm")
day_idhin = lem_locs("yawoma}i*")
month_root = root_locs("$hr")
# sea / land
sea_lem = lem_locs("baHor")
land_bar = lem_locs("bar~")
# man / woman
man_lem = lem_locs("rajul")
woman_lem = lem_locs("{mora>at")
man_plur = lem_locs("rijaAl")
woman_plur = lem_locs("nisaA^'")
# sun / moon / light
sun_root = root_locs("$ms")
moon_root = root_locs("qmr")
light_lem = lem_locs("nuwr")
light_muniyr = lem_locs("m~uniyr")
# muhammad
muhammad = lem_locs("muHam~ad")
# iman / kufr
iman_lem = lem_locs("<iyma`n")
kufr_lem = lem_locs("kufor")
iman_bare = [loc for loc in iman_lem if is_bare(words[loc])]
kufr_bare = [loc for loc in kufr_lem if is_bare(words[loc])]
# zakah / blessing
zakah_lem = lem_locs("zakaw`p")
bless_root = root_locs("brk")
# say / they said
say_impv_sg = qac_locs(lambda rec, loc: "qaAla" in rec["lems"] and any(
    "IMPV" in ft for ft in rec["feats"]) and tanzil_token(*loc) is not None
    and skeleton(tanzil_token(*loc)) in {
        "قل", "قل", "فقل", "وقل", "وقل", "فقل", "قل", "قل", "فقل"})
# (surface skeletons collapse قُلْ/قُل/قُلِ etc. -- recompute precisely below)
say_forms = Counter()
for loc in qac_locs(lambda rec, loc: "qaAla" in rec["lems"] and any(
        "IMPV" in ft for ft in rec["feats"])):
    say_forms[skeleton(tanzil_token(*loc))] += 1
say_sg_set = {"قل", "فقل", "وقل"}
say_sg_n = sum(n for f, n in say_forms.items() if f in say_sg_set)
they_said_n, they_said_vs = surf_count(
    lambda t: t in {"قالوا", "وقالوا", "فقالوا", "لقالوا"})
# plant / tree
plant_root = root_locs("nbt")
tree_root = root_locs("$jr")
tree_sense = [loc for loc in tree_root if "$ajara" not in words[loc]["lems"]]
# reward / forgiveness
jzy_root = root_locs("jzy")
jzy_reward = [loc for loc in jzy_root if "jizoyap" not in words[loc]["lems"]]
gfr_root = root_locs("gfr")
# guidance / mercy
hdy_root = root_locs("hdy")
rhm_root = root_locs("rHm")
hudfy = lem_locs("hudFY")
rahma_lem = lem_locs("raHomap")
# tongue / sermon
tongue_root = root_locs("lsn")
sermon_root = root_locs("wEZ")
# wine / intoxication
wine_lem = lem_locs("xamor")
intox_root = root_locs("skr")
# mind / light
mind_root = root_locs("Eql")
# benefit / corrupt
benefit_root = root_locs("nfE")
corrupt_root = root_locs("fsd")
# love / obedience
love_root = root_locs("Hbb", lem_not={"Hab~", "Hab~ap"})
obed_root = root_locs("TwE")
obed_sense = [loc for loc in obed_root
              if "{sotaTaAEa" not in words[loc]["lems"]]
# refuge / forever
maseer_lem = lem_locs("maSiyr")
forever_n, forever_vs = surf_count(lambda t: t == "ابدا")
# disaster / thanks
disaster_root = root_locs("Swb")
disaster_sense = [loc for loc in disaster_root
                  if not (words[loc]["lems"] & {"Say~ib", "SawaAb"})]
thanks_root = root_locs("$kr")
# trouble / peace
distress_root = root_locs("Dyq")
tranquil_root = root_locs("Tmn")
# treachery / foul
treach_root = root_locs("xwn")
foul_root = root_locs("xbv")
# righteous / wicked
righteous_surf_n, righteous_vs = surf_count(
    lambda t: t in {"الابرار", "للابرار"})
wicked_surf_n, wicked_vs = surf_count(
    lambda t: t in {"الفجار", "كالفجار"})
wicked_lem = lem_locs("fuj~aAr")
# summer / winter
summer_root = root_locs("Syf")
winter_root = root_locs("$tw")
heat_root = root_locs("Hrr")
cold_root = root_locs("brd")
# human being
insan_lem = lem_locs("<insa`n")
# life / death
life_noun = lem_locs("Hayaw`p")
death_noun = lem_locs("mawot")
life_root = root_locs("Hyy")
death_root = root_locs("mwt")
# seven heavens
seven_root = root_locs("sbE")
sky_lem = lem_locs("samaA^'")

# ---------- diagnostics printed for the report ----------
print("=== diagnostics ===")
print(f"QAC words: {len(words)}")
print(f"dunya LEM d~unoyaA: {len(dunya_lem)}; akhira fem stems: {len(akhira_locs)}")
print(f"jan~ap total {len(jan_all)}: singular {len(jan_sing)} "
      f"(bare {len(jan_sing_bare)}), plural {len(jan_plur)}, dual {len(jan_dual)}")
print(f"jannah exact surface forms: {garden_exact[0]}; "
      f"jahannam substr: {surf_count(lambda t: 'جهنم' in t)[0]}")
print(f"devils $Tn: {len(devils)}; angels malak: {len(angels)}")
print(f"day root ywm: {len(day_root)}; yawma'idhin: {len(day_idhin)}; "
      f"day simple+prefixed surface: "
      f"{surf_count(lambda t: t in {'يوم','اليوم','يوما','ويوم','واليوم','ليوم','فاليوم','بيوم','باليوم','وباليوم'})[0]}")
print(f"month root $hr: {len(month_root)}")
print(f"sea baHor: {len(sea_lem)}; bar~: {len(land_bar)}")
print(f"man rajul: {len(man_lem)}; woman {{mora>at: {len(woman_lem)}")
print(f"sun $ms: {len(sun_root)}; moon qmr: {len(moon_root)}; "
      f"light nuwr: {len(light_lem)}; muniyr: {len(light_muniyr)}")
print(f"muhammad: {len(muhammad)}")
print(f"iman noun: {len(iman_lem)} bare {len(iman_bare)}; "
      f"kufr noun: {len(kufr_lem)} bare {len(kufr_bare)}")
print(f"zakah zakaw`p: {len(zakah_lem)}; blessing brk: {len(bless_root)}")
print(f"say IMPV surface forms: {dict(say_forms)}")
print(f"say singular imperative: {say_sg_n}; they said قالوا: {they_said_n}")
print(f"plant nbt: {len(plant_root)}; tree $jr: {len(tree_root)} "
      f"tree-sense: {len(tree_sense)}")
print(f"reward jzy: {len(jzy_root)} minus jizya: {len(jzy_reward)}; "
      f"forgiveness gfr: {len(gfr_root)}")
print(f"guidance hdy: {len(hdy_root)} (hudFY noun {len(hudfy)}); "
      f"mercy rHm: {len(rhm_root)} (raHomap noun {len(rahma_lem)})")
print(f"tongue lsn: {len(tongue_root)}; sermon wEZ: {len(sermon_root)}")
print(f"wine xamor: {len(wine_lem)}; intoxication skr: {len(intox_root)}")
print(f"mind Eql: {len(mind_root)}")
print(f"benefit nfE: {len(benefit_root)}; corrupt fsd: {len(corrupt_root)}")
print(f"love Hbb excl grain: {len(love_root)}; obedience TwE: "
      f"{len(obed_root)} excl 'to be able': {len(obed_sense)}")
print(f"maseer maSiyr: {len(maseer_lem)}; forever ابدا: {forever_n}")
print(f"disaster Swb: {len(disaster_root)} disaster-sense: "
      f"{len(disaster_sense)}; thanks $kr: {len(thanks_root)}")
print(f"distress Dyq: {len(distress_root)}; tranquillity Tmn: {len(tranquil_root)}")
print(f"treachery xwn: {len(treach_root)}; foul xbv: {len(foul_root)}")
print(f"righteous surface: {righteous_surf_n}; wicked surface: "
      f"{wicked_surf_n}; wicked lemma fuj~aAr: {len(wicked_lem)}")
print(f"summer Syf: {len(summer_root)}; winter $tw: {len(winter_root)}; "
      f"heat Hrr: {len(heat_root)}; cold brd: {len(cold_root)}")
print(f"insan <insa`n: {len(insan_lem)}")
print(f"life noun: {len(life_noun)} root Hyy: {len(life_root)}; "
      f"death noun: {len(death_noun)} root mwt: {len(death_root)}")
print(f"seven sbE words: {len(seven_root)}")

# day: singular / dual / plural split of root ywm, and the 365 selection
DAY_SET = {"يوم", "اليوم", "يوما", "ويوم", "واليوم", "ليوم", "فاليوم",
           "بيوم", "باليوم", "وباليوم"}
def _is_dual(rec):
    return any("yawomay" in s for s in rec["stems"])
def _is_plur(rec):
    return any("ay~aAm" in s or "ay~aY`m" in s for s in rec["stems"])
day_sing = [loc for loc in day_root
            if not _is_dual(words[loc]) and not _is_plur(words[loc])]
day_dual = [loc for loc in day_root if _is_dual(words[loc])]
day_plur = [loc for loc in day_root if _is_plur(words[loc])]
day_sing_nosuf = [loc for loc in day_sing if is_bare(words[loc])]
day_sing_suf = [loc for loc in day_sing if not is_bare(words[loc])]
print(f"day: singular {len(day_sing)} (no-suffix {len(day_sing_nosuf)}, "
      f"suffixed {len(day_sing_suf)}), dual {len(day_dual)} "
      f"{verses_str(qac_verses(day_dual))}, plural {len(day_plur)}, "
      f"yawma'idhin {len(day_idhin)}; "
      f"total {len(day_sing) + len(day_dual) + len(day_plur)}")
print("day: suffixed singular yawm tokens:",
      [f"{s}:{v}" for s, v, w in day_sing_suf])
print("day: singular-no-suffix QAC words outside the 365 surface set:",
      [(f"{s}:{v}", words[loc]["stems"], tanzil_token(*loc))
       for loc in day_sing_nosuf
       for (s, v, w) in [loc]
       if skeleton(tanzil_token(*loc)) not in DAY_SET])
# jannah: bare singular garden tokens outside the 4-form surface set
print("jannah: bare singular jan~ap tokens outside "
      "{الجنة,جنة,وجنة,بالجنة}:",
      [(f"{loc[0]}:{loc[1]}", tanzil_token(*loc))
       for loc in jan_sing if is_bare(words[loc])
       and skeleton(tanzil_token(*loc)) not in
       {"الجنة", "جنة", "وجنة", "بالجنة"}])
# insan: surface breakdown of lemma <insa`n
print("insan: <insa`n surface skeletons:",
      Counter(skeleton(tanzil_token(*loc)) for loc in insan_lem))
# forever: QAC lemma >abadFA total + substring count
abad_lem = lem_locs(">abadFA")
abad_sub_n, abad_sub_vs = surf_count(lambda t: "ابدا" in t)
print(f"forever: LEM >abadFA = {len(abad_lem)}; substring ابدا = "
      f"{abad_sub_n}; exact ابدا = {forever_n}")
# 7:69 spelling
_v769 = verses[inv_vmap[(7, 69)]]
print("7:69 contains بصطة (Sad)?", "بصطة" in skeleton(_v769),
      "| contains بسطة (Seen)?", "بسطة" in skeleton(_v769))
# the 29th ابدا-substring token (LEM >abadFA = 28, substring = 29)
print("tokens with ابدا in skeleton (with QAC lemma):")
for li, ln in enumerate(verses):
    s, v = vmap[li]
    for ti, t in enumerate(ln.split()):
        if "ابدا" in skeleton(t) and skeleton(t) != "ابدا":
            w = ti + 1 - 4 if (v == 1 and s > 1 and s != 9) else ti + 1
            rec = words.get((s, v, w))
            print("   ", f"{s}:{v}", t,
                  sorted(rec["lems"]) if rec else None,
                  sorted(rec["roots"]) if rec else None)
# شتاء-substring tokens (root $tw = 1, substring = 3?)
print("tokens with شتاء in skeleton (with QAC lemma/root):")
for li, ln in enumerate(verses):
    s, v = vmap[li]
    for ti, t in enumerate(ln.split()):
        if "شتاء" in skeleton(t):
            w = ti + 1 - 4 if (v == 1 and s > 1 and s != 9) else ti + 1
            rec = words.get((s, v, w))
            print("   ", f"{s}:{v}", t,
                  sorted(rec["lems"]) if rec else None,
                  sorted(rec["roots"]) if rec else None)
# 42:22 jan~ap stems (plural or singular?)
print("42:22 QAC records:",
      [(loc, words[loc]["stems"], sorted(words[loc]["lems"]))
       for loc in sorted(words) if loc[0] == 42 and loc[1] == 22
       and "jan~ap" in words[loc]["lems"]])
# bone: QAC-based (surface contains عظام/عظم, bone-sense lemmas)
bone_locs = []
for li, ln in enumerate(verses):
    s, v = vmap[li]
    for ti, t in enumerate(ln.split()):
        sk = skeleton(t)
        if "عظام" in sk or sk in {"عظم", "بعظم", "والعظم", "العظم"}:
            w = ti + 1 - 4 if (v == 1 and s > 1 and s != 9) else ti + 1
            rec = words.get((s, v, w))
            if rec and (rec["lems"] & {"EaZiym", "EaZom"}):
                bone_locs.append((s, v, w))
print("human stages: bone words (QAC, عظام 13 + عظم 2):", len(bone_locs),
      verses_str(qac_verses(bone_locs)))
# guidance/mercy: bare (unsuffixed) noun counts -- the 79 test
hudfy_bare = [loc for loc in hudfy if is_bare(words[loc])]
rahma_bare = [loc for loc in rahma_lem if is_bare(words[loc])]
print(f"guidance/mercy bare nouns: hudFY bare {len(hudfy_bare)}; "
      f"raHomap bare {len(rahma_bare)}")
print("hudFY bare by stem:",
      Counter(tuple(words[loc]["stems"]) for loc in hudfy_bare).most_common(6))
print("raHomap bare by stem:",
      Counter(tuple(words[loc]["stems"]) for loc in rahma_bare).most_common(6))

# jannah: suffixed singular garden tokens (71 - 65 = 6)
print("jannah: suffixed singular jan~ap tokens:")
for loc in jan_sing:
    if not is_bare(words[loc]):
        print("   ", f"{loc[0]}:{loc[1]}:{loc[2]}",
              words[loc]["stems"], tanzil_token(*loc))
print("jannah: dual jan~ap stems:",
      Counter(tuple(words[loc]["stems"]) for loc in jan_dual))
# surface جنة-family composition: which exact-form tokens are NOT garden?
print("jannah: exact-form جنة-family tokens that are NOT lemma jan~ap:")
for li, ln in enumerate(verses):
    s, v = vmap[li]
    for ti, t in enumerate(ln.split()):
        if skeleton(t) in {"الجنة", "جنة", "وجنة", "بالجنة"}:
            w = ti + 1 - 4 if (v == 1 and s > 1 and s != 9) else ti + 1
            rec = words.get((s, v, w))
            if rec and "jan~ap" not in rec["lems"]:
                print("   ", f"{s}:{v}", t, sorted(rec["lems"]))

# sea: baHor surface forms (definite singular vs dual vs indefinite)
print("sea: baHor surface forms:",
      Counter(skeleton(tanzil_token(*loc)) for loc in sea_lem))
# land: bar~ classification (land vs other senses) -- by verse text
LAND_VERSES = {(5, 96), (6, 59), (6, 63), (6, 97), (10, 22), (17, 67),
               (17, 68), (17, 70), (27, 63), (29, 65), (30, 41), (31, 32)}
land_sense = [loc for loc in land_bar if (loc[0], loc[1]) in LAND_VERSES]
print(f"land: bar~ total {len(land_bar)}, land-sense {len(land_sense)}")
for loc in land_bar:
    print("   ", f"{loc[0]}:{loc[1]}", tanzil_token(*loc),
          "LAND" if (loc[0], loc[1]) in LAND_VERSES else "other-sense")

# forever: actual QAC lemma for ابدا
abada_verses = set()
for li, ln in enumerate(verses):
    s, v = vmap[li]
    for ti, t in enumerate(ln.split()):
        if skeleton(t) == "ابدا":
            w = ti + 1 - 4 if (v == 1 and s > 1 and s != 9) else ti + 1
            rec = words.get((s, v, w))
            abada_verses.add((s, v))
            if rec:
                print("abada token:", f"{s}:{v}:{w}", sorted(rec["lems"]),
                      sorted(rec["roots"]), t)
                break
print("abada distinct verses:", len(abada_verses))

# human-being stages
print("human stages: turaAb",
      len(lem_locs("turaAb")), "| n~uTofap", len(lem_locs("n~uTofap")),
      "| Ealaqap", len(lem_locs("Ealaqap")), "| Ealaq",
      len(lem_locs("Ealaq")), "| muDogap", len(lem_locs("muDogap")),
      "| laHom", len(lem_locs("laHom")))
# ajr / fa'il side-check (mentioned in harun-yahya-populariser note)
print("side-check ajr/fa'il: >ajor", len(lem_locs(">ajor")),
      "| root fEl", len(root_locs("fEl")),
      "| faAEil", len(lem_locs("faAEil")))

# ---------- letter counts ----------
def letter_in_surah(n, letter, excl_basmalah=False):
    tot = 0
    for li, ln in enumerate(verses):
        s, v = vmap[li]
        if s != n:
            continue
        txt = ln
        if excl_basmalah and v == 1 and s not in (1, 9):
            sk = skeleton(ln)
            if sk.startswith("بسم الله الرحمان الرحيم"):
                # drop the basmalah words from the raw line: first 4 tokens
                toks = ln.split()
                txt = " ".join(toks[4:])
        tot += strip_diacritics(txt).count(letter)
    return tot

qaf50 = letter_in_surah(50, "ق")
qaf42 = letter_in_surah(42, "ق")
nun68 = letter_in_surah(68, "ن")
nun68_excl = letter_in_surah(68, "ن", excl_basmalah=True)
sad7 = letter_in_surah(7, "ص")
sad19 = letter_in_surah(19, "ص")
sad38 = letter_in_surah(38, "ص")
print(f"letters: qaf 50={qaf50} 42={qaf42}; nun 68={nun68} "
      f"(excl basmalah {nun68_excl}); sad 7={sad7} 19={sad19} 38={sad38} "
      f"total={sad7 + sad19 + sad38}")
# 7:69 spelling
v769 = verses[inv_vmap[(7, 69)]]
print("7:69 skeleton:", skeleton(v769)[:60])
# verses containing the letter, per surah (locations)
def letter_verses(n, letter):
    out = []
    for li, ln in enumerate(verses):
        s, v = vmap[li]
        if s == n and letter in strip_diacritics(ln):
            out.append((s, v))
    return out

# muqattaat
EXPECTED = {2: "الم", 3: "الم", 7: "المص", 10: "الر", 11: "الر", 12: "الر",
            13: "المر", 14: "الر", 15: "الر", 19: "كهيعص", 20: "طه",
            26: "طسم", 27: "طس", 28: "طسم", 29: "الم", 30: "الم",
            31: "الم", 32: "الم", 36: "يس", 38: "ص", 40: "حم", 41: "حم",
            42: "حم", 43: "حم", 44: "حم", 45: "حم", 46: "حم", 50: "ق",
            68: "ن"}
MUQ_LETTERS = set("المصر كهيعطسح قن".replace(" ", ""))
muq_verses, muq_counts, muq_bad = [], {}, []
for s, exp in sorted(EXPECTED.items()):
    ln = verses[inv_vmap[(s, 1)]]
    toks = ln.split()
    if s not in (1, 9):
        toks = toks[4:]  # drop merged unnumbered basmalah
    first = skeleton(" ".join(toks[:1]))
    # initials may be split across tokens (e.g. حم عسق is verse 2 of 42)
    got = skeleton(toks[0]) if toks else ""
    # the opening token as written (letters only, no spaces)
    muq_verses.append((s, 1))
    muq_counts[s] = len(exp)
    if got != exp:
        muq_bad.append((s, exp, got))
print("muqattaat mismatches (verse-1 opening token vs expected):", muq_bad)
total_v1 = sum(len(e) for e in EXPECTED.values())
distinct = set("".join(EXPECTED.values()))
print(f"muqattaat: surahs {len(EXPECTED)}, distinct letters "
      f"{len(distinct)} {sorted(distinct)}, verse-1 letters {total_v1}, "
      f"+42:2 عسق = {total_v1 + 3}")
# 42:2 check
v422 = verses[inv_vmap[(42, 2)]]
print("42:2 skeleton:", skeleton(v422)[:20])

# all-28-letters
def distinct_letters(s, v):
    ln = verses[inv_vmap[(s, v)]]
    sk = skeleton(ln).replace("ة", "ه").replace("ى", "ي")
    return {c for c in sk if "\u0621" <= c <= "\u064a"}
ref28 = set("ابتثجحخدرزسشصضطظعغفقكلمنهوي")
all28 = []
for li, ln in enumerate(verses):
    s, v = vmap[li]
    if len(distinct_letters(s, v)) == 28:
        all28.append((s, v))
print("verses with all 28 distinct letters:", verses_str(all28),
      "| 3:154 missing:", sorted(ref28 - distinct_letters(3, 154)),
      "| 48:29 missing:", sorted(ref28 - distinct_letters(48, 29)))

# longest word
def word_len(tok, dagger_counts=False):
    t = tok.translate(HAMZA_MAP)
    if not dagger_counts:
        t = LETTER_MARKS.sub("", t)
    t = DIACRITICS.sub("", t)
    n = sum(1 for c in t if "\u0621" <= c <= "\u064a")
    if dagger_counts:
        n += tok.count("ٰ")  # dagger alif counts as a letter
    return n
longest, longest_dag = [], []
for li, ln in enumerate(verses):
    s, v = vmap[li]
    for t in ln.split():
        L = word_len(t)
        Ld = word_len(t, dagger_counts=True)
        if L >= 10:
            longest.append((L, f"{s}:{v}", t))
        if Ld >= 11:
            longest_dag.append((Ld, f"{s}:{v}", t))
print("longest words (project convention, >=10 letters):",
      sorted(longest, reverse=True)[:12])
print("longest words (dagger alif counts, >=11 letters):",
      sorted(longest_dag, reverse=True)[:12])
tok1522 = None
for li, ln in enumerate(verses):
    s, v = vmap[li]
    if (s, v) == (15, 22):
        for t in ln.split():
            if "سقين" in skeleton(t):
                tok1522 = t
print("15:22 fasqaynakumuhu token:", repr(tok1522),
      "letters (project convention):",
      word_len(tok1522) if tok1522 else None,
      "with dagger alif:",
      word_len(tok1522, dagger_counts=True) if tok1522 else None)

# seven heavens: verses with root sbE + LEM samaA^'
seven_verses = sorted({(s, v) for (s, v, w) in seven_root}
                      & {(s, v) for (s, v, w) in sky_lem})
print("seven-heavens verses (sbE + samaA^'):", verses_str(seven_verses))
print("sbE verses not samaA^':",
      verses_str(sorted({(s, v) for (s, v, w) in seven_root}
                        - {(s, v) for (s, v, w) in sky_lem})))

# guidance/mercy 79 variants
print("guidance/mercy variants: hudFY surface bare:",
      surf_count(lambda t: strip_prefixes(t) == "هدى")[0],
      "| raHomap surface bare:",
      surf_count(lambda t: strip_prefixes(t) == "رحمة")[0],
      "| hudFY total:", len(hudfy), "| raHomap total:", len(rahma_lem))
print("hudFY stems:", Counter(tuple(words[loc]["stems"]) for loc in hudfy).most_common(6))
print("raHomap stems:", Counter(tuple(words[loc]["stems"]) for loc in rahma_lem).most_common(6))

print("=== end diagnostics ===")

# =====================================================================
# Part 2: build the enriched records
# =====================================================================
# extra locs needed for scholar-rule verse lists
dunya_surf_n, dunya_surf_vs = surf_count(lambda t: "دنيا" in t)
akhira_surf_n, akhira_surf_vs = surf_count(lambda t: "اخرة" in t)
jannah_surf_n, jannah_surf_vs = surf_count(
    lambda t: t in {"الجنة", "جنة", "وجنة", "بالجنة"})
jahannam_surf_n, jahannam_surf_vs = surf_count(lambda t: "جهنم" in t)
shaytan_sing_n, _ = surf_count(lambda t: "شيط" in t)
shaytan_plur_n, _ = surf_count(lambda t: "شياط" in t)
day_surf_n, day_surf_vs = surf_count(lambda t: t in DAY_SET)
month_surf_n, month_surf_vs = surf_count(
    lambda t: t in {"شهر", "الشهر", "شهرا", "بالشهر", "والشهر"})
sea_surf_n, sea_surf_vs = surf_count(lambda t: t in {"البحر", "والبحر"})
sun_surf_n, sun_surf_vs = surf_count(lambda t: "شمس" in t)
moon_surf_n, moon_surf_vs = surf_count(lambda t: "قمر" in t)
LIGHT_SET = {"نور", "النور", "نورا", "والنور", "بنور", "نورهم"}
light_surf_n, light_surf_vs = surf_count(lambda t: t in LIGHT_SET)
muhammad_surf_n, muhammad_surf_vs = surf_count(lambda t: "محمد" in t)
insan_surf_n, insan_surf_vs = surf_count(lambda t: "انسان" in t)
# salawat plural (QAC stems)
salawat_locs = [loc for loc in lem_locs("Salaw`p")
                if any(st in ("Salawa`tN", "Salawa`ti", "S~alawa`ti")
                       for st in words[loc]["stems"])]
salawat_sing_locs = [loc for loc in lem_locs("Salaw`p")
                     if any(st in ("Salaw`ta", "Salaw`tu")
                            for st in words[loc]["stems"])]
# man / woman singular (duals excluded)
man_sing = [loc for loc in man_lem
            if not any("ajulay" in s or "ajulaA" in s
                       for s in words[loc]["stems"])]
man_dual = [loc for loc in man_lem if loc not in man_sing]
woman_sing = [loc for loc in woman_lem
              if not any("mora>atay" in s or "mora>ataA" in s
                         for s in words[loc]["stems"])]
woman_dual = [loc for loc in woman_lem if loc not in woman_sing]
# angels breakdown
ang_plur = [loc for loc in angels
            if any("}ika" in s for s in words[loc]["stems"])]
ang_dual = [loc for loc in angels
            if any("malakay" in s for s in words[loc]["stems"])]
ang_sing = [loc for loc in angels
            if loc not in ang_plur and loc not in ang_dual]
# say: singular-imperative locs + checks
say_sg_locs = [loc for loc in qac_locs(
    lambda rec, loc: "qaAla" in rec["lems"] and any(
        "IMPV" in ft for ft in rec["feats"]))
    if skeleton(tanzil_token(*loc)) in {"قل", "فقل", "وقل"}]
say_all_impv = qac_locs(lambda rec, loc: "qaAla" in rec["lems"] and any(
    "IMPV" in ft for ft in rec["feats"]))
qul_nonimpv = [(loc, tanzil_token(*loc)) for loc in qac_locs(
    lambda rec, loc: "qaAla" not in rec["lems"])
    if tanzil_token(*loc) is not None
    and skeleton(tanzil_token(*loc)) in {"قل", "فقل", "وقل"}]
they_said_qac = [loc for loc in qac_locs(
    lambda rec, loc: "qaAla" in rec["lems"] and any(
        "PERF" in ft and "3MP" in ft for ft in rec["feats"]))
    if tanzil_token(*loc) is not None
    and skeleton(tanzil_token(*loc)) in
    {"قالوا", "وقالوا", "فقالوا", "لقالوا"}]
print("say: singular-imperative locs:", len(say_sg_locs),
      "| all IMPV:", len(say_all_impv),
      "| non-qaAla tokens with قل skeleton:", qul_nonimpv,
      "| they-said QAC PERF 3MP:", len(they_said_qac))
print("angels: plural", len(ang_plur), "singular", len(ang_sing),
      "dual", len(ang_dual), "dual verses:",
      verses_str(qac_verses(ang_dual)))
print("man: singular", len(man_sing), "dual", len(man_dual),
      "| woman: singular", len(woman_sing), "dual", len(woman_dual))
print("salawat plural locs:", len(salawat_locs),
      verses_str(qac_verses(salawat_locs)),
      "| singular صلوة locs:", len(salawat_sing_locs),
      verses_str(qac_verses(salawat_sing_locs)))
print("shaytan substrings: شيط", shaytan_sing_n, "شياط", shaytan_plur_n)
print("insan surface:", insan_surf_n, "| <insa`n lemma:", len(insan_lem),
      "| <insa`n surface breakdown:",
      Counter(skeleton(tanzil_token(*loc)) for loc in insan_lem))
print("maseer/forever: maSiyr", len(maseer_lem),
      "| >abadFA", len(abad_lem), "| ابدا substr", abad_sub_n)

# ---------- 1. dunya-akhira-115 ----------
add("dunya-akhira-115",
    "method not stated by the source",
    "unstated",
    "29:20 (al-nash'a al-akhira, 'the latter creation') is inside the 115 "
    "akhira forms but means 'latter', not the Hereafter; it is counted as a "
    "form under both rules. Root dnw also gives adna (nearest/lower, 12), "
    "daniyah (3), dana (2) -- excluded by lemma. Root Axr (250 words) also "
    "gives masculine al-akhir ('the Last/the other') and plural forms -- "
    "excluded by the feminine-stem rule.",
    {"count": [115, 115],
     "note": "Reconstructed: plain substring count on the Tanzil skeleton "
             "text gives دنيا 115 and اخرة 115. The source states no method; "
             "this is the selection that reproduces the claim."},
    {"count": [115, 115],
     "note": "QAC: LEM d~unoyaA = 115; akhira = feminine al-akhira stem "
             "forms ('aAxirapi/'aAxirapa/'aAxirapu) = 115. Both rules agree."},
    pair_block(dunya_lem, akhira_locs,
               verses_scholar=sorted(set(dunya_surf_vs) | set(akhira_surf_vs))))

# ---------- 2. jannah-jahannam-77 ----------
add("jannah-jahannam-77",
    "method not stated by the source",
    "unstated",
    "The surface string الجنة/جنة does NOT mean 'garden' in 12 tokens that "
    "the popular 77 counts as paradise: جِنَّة (jinn/madness, LEM jin~ap) "
    "at 7:184, 11:119, 23:25, 23:70, 32:13, 34:8, 34:46, 37:158 (x2), 114:6, "
    "and جُنَّة (shield, LEM jun~ap) at 58:16, 63:2. A 13th look-alike, "
    "أَجِنَّة (ajinnah, 'fetuses', 53:32), is outside the four exact forms "
    "but inside the جنة substring (78 total). Plural جنات (69) and dual (8) "
    "are excluded by the singular-only reading.",
    {"count": [77, 77],
     "note": "Reconstructed (sense-blind): exact surface forms الجنة 56 + "
             "جنة 18 + وجنة 2 + بالجنة 1 = 77; جهنم substring = 77. This is "
             "the selection that reproduces the claim -- but it counts 12 "
             "non-garden tokens as 'paradise' (see exceptions)."},
    {"count": [147, 77],
     "note": "QAC: LEM jan~ap (all gardens) = 147 (singular 70 = 65 in the "
             "four surface forms + 1 construct spelling وجنتُ (56:89) + 4 "
             "suffixed; plural 69; dual 8); LEM jahan~am = 77. Sense-correct "
             "garden counts are 65 / 70 / 147 -- none is 77."},
    pair_block(jan_all, jah,
               verses_scholar=sorted(set(jannah_surf_vs) | set(jahannam_surf_vs))),
    correction={"field": "our_status", "was": "confirmed", "now": "differs",
                "why": "The filed note claimed the 77 exact surface forms "
                "were all singular 'garden'. They are not: 12 of the 77 are "
                "جِنَّة (jinn/madness, 10 tokens) and جُنَّة (shield, 2 "
                "tokens), named verse by verse above. Sense-correct garden "
                "counts are 65 (unsuffixed surface singular), 70 (QAC lemma "
                "singular) and 147 (all gardens) -- none is 77. Hell is 77 "
                "under both rules; the paradise side does not reproduce."})

# ---------- 3. shaytan-angels-88 ----------
add("shaytan-angels-88",
    "method not stated by the source",
    "unstated",
    "Bare surface ملك/الملك (63 tokens) mostly means 'king/sovereignty', "
    "not angel -- sense disambiguation by QAC lemma is required. Angel "
    "singulars (13): 6:8 x2 (ملك and ملكا, two tokens in one verse), 6:9, "
    "6:50, 11:12, 11:31, 12:31, 17:95, 25:7, 32:11 (ملك الموت, Angel of "
    "Death), 53:26, 69:17, 89:22. Duals (2): الملكين 2:102, ملكين 7:20. "
    "Plural ملائكة 73.",
    {"count": [88, 88],
     "note": "Reconstructed: شيط substring 70 + شياطين substring 18 = 88; "
             "angels by QAC lemma malak = 88 (73 plural + 13 singular + 2 "
             "dual). The source states no method; these are the selections "
             "that reproduce the claim."},
    {"count": [88, 88],
     "note": "QAC: ROOT $Tn (shaytan) = 88; LEM malak = 88. Whole ROOT mlk "
             "would be far larger (mulk dominion, malik king) -- the lemma "
             "narrowing is essential. Both rules agree."},
    pair_block(devils, angels))

# ---------- 4. day-365 ----------
add("day-365",
    "Yahya's page states it: '\"Day (yawm)\" is repeated 365 times in "
    "singular form, while its plural and dual forms \"days (ayyam and "
    "yawmayn)\" together are repeated 30 times.' Units: the singular form "
    "of yawm, with prefixes (wa-/fa-/bi-/li-) counted in and suffixed forms "
    "(possessive pronouns) counted out; dual and plural counted separately.",
    "stated",
    "Excluded by the stated singular-only rule, all named: 10 suffixed "
    "singulars (يومكم/يومهم at 6:130, 7:51, 21:103, 32:14, 39:71, 43:83, "
    "45:34, 51:60, 52:45, 70:42); 3 duals (يومين at 2:203, 41:9, 41:12); 27 "
    "plurals (أيام); 70 يومئذ (yawma'idhin, 'on that day' -- QAC gives it "
    "no ROOT, LEM yawoma}i* only). The Islamic year is 354/355 days, so the "
    "Gregorian-365 framing is itself a critique point (WikiIslam).",
    {"count": 365,
     "note": "Stated rule verified: singular yawm without suffixes = 365 "
             "(simple يوم/اليوم/يوما 274 + prefixed ويوم 44, واليوم 23, "
             "ليوم 8, فاليوم 8, بيوم 5, باليوم 2, وباليوم 1). QAC agrees: "
             "singular yawm = 375, minus 10 suffixed = 365."},
    {"count": 475,
     "note": "QAC: ROOT ywm = 405 (singular 375 + plural 27 + dual 3) + "
             "LEM yawoma}i* (yawma'idhin) 70 = 475. The 365 is a subset: it "
             "excludes the 10 suffixed singulars, 3 duals, 27 plurals and "
             "70 yawma'idhin (110 tokens)."},
    loc_block(day_root + day_idhin, verses_scholar=day_surf_vs))

# ---------- 5. month-12 ----------
add("month-12",
    "method not stated by the source",
    "unstated",
    "Excluded by the singular-only selection: 2 duals (شهرين at 4:92, "
    "58:4) and 7 plurals (أشهر 6 + الشهور 1 at 9:36). All 12 counted forms "
    "are singular شهر.",
    {"count": 12,
     "note": "Reconstructed: simple شهر/الشهر/شهرا 10 + بالشهر 1 + والشهر "
             "1 = 12. The source states no method; this is the selection "
             "that reproduces the claim."},
    {"count": 21,
     "note": "QAC: ROOT $hr / LEM $ahor = 21 (singular 12 + dual 2 + "
             "plural 7). The 12 is the singular-only subset."},
    loc_block(month_root, verses_scholar=month_surf_vs))

# ---------- 6. salawat-5 ----------
add("salawat-5",
    "method not stated by the source",
    "unstated",
    "The 5 plural صلوات are at 2:157, 2:238, 9:99, 22:40, 23:9. Two further "
    "tokens match the صلوات substring but are singular صلاة written صلوة in "
    "Uthmani (9:103, 11:87) -- excluded. Sense: only 3 of the 5 mean "
    "'prayers' (2:157 = blessings, 22:40 = synagogues/churches -- "
    "WikiIslam's sense critique).",
    {"count": 5,
     "note": "Reconstructed: plural surface form صلوات = 5 (QAC plural "
             "stems Salawa`tN/Salawa`ti/S~alawa`ti). The source states no "
             "method; this is the selection that reproduces the claim."},
    {"count": 5,
     "note": "QAC: LEM Salaw`p plural stems = 5; the same lemma covers "
             "singular صلاة (78 words, incl. the 2 صلوة spellings). Both "
             "rules agree on 5."},
    loc_block(salawat_locs,
              verses_scholar=qac_verses(salawat_locs)))

# ---------- 7. sea-land-32-13 ----------
add("sea-land-32-13",
    "method not stated by the source",
    "unstated",
    "Sea: البحر 23 + والبحر 9 = 32 (definite singular only); excluded are "
    "the dual البحرين (4), plural البحار (2), indefinite بحر (1), أبحر (1) "
    "and البحران (1) -- sea-sense total 41, plus بحيرة (a slit-eared camel, "
    "5:103) which shares ROOT bHr but is not sea. Land: LEM bar~ = 22 "
    "tokens, of which 12 are land-sense (5:96, 6:59, 6:63, 6:97, 10:22, "
    "17:67, 17:68, 17:70, 27:63, 29:65, 30:41, 31:32) and 10 are not land: "
    "الأبرار (the righteous) x6 (3:193, 3:198, 76:5, 82:13, 83:18, 83:22), "
    "برًّا (dutiful) x2 (19:14, 19:32), البرّ (the Benign, a divine name) "
    "52:28, بررة (dutiful) 80:16.",
    {"count": [32, None],
     "note": "Sea 32 reproduces under the definite-singular selection. "
             "Land 13 does NOT reproduce: sense-classified land = 12 (see "
             "exceptions). No stated or reconstructable rule gives 13."},
    {"count": [41, 12],
     "note": "QAC: LEM baHor (sea-sense) = 41; LEM bar~ land-sense = 12 "
             "(of 22 bar~ tokens; the rest are piety/righteousness). Whole "
             "ROOT brr = 32 (bar~ 22 + bir~ piety 8 + tabar~u 2) -- "
             "coincidentally the sea number, not the land number."},
    pair_block(sea_lem, land_sense,
               verses_scholar=sea_surf_vs),
    correction={"field": "our_status", "was": "cannot_verify",
                "now": "differs",
                "why": "Sense disambiguation -- which the filed note said "
                "had not been performed -- has now been performed verse by "
                "verse: land-sense البرّ occurs 12 times, not 13. The 10 "
                "remaining bar~ tokens are unambiguously piety/righteousness "
                "(listed in exceptions). Sea 32 is confirmed; the pair as "
                "claimed (32/13) differs on the land side by one."})

# ---------- 8. man-woman-24-24 ----------
add("man-woman-24-24",
    "method not stated by the source",
    "unstated",
    "Man singular (24): رجل 13 (رجلٌ 7 + رجلٍ 5 + رجلٌۢ 1) + رجلا 7 + لرجل "
    "2 + فرجل 1 + ورجلا 1. Woman singular (24): امرأت 6 + امرأته 5 + امرأة "
    "3 + وامرأته 2 + امرأتك 2 + امرأتي 2 + وامرأتي 1 + لامرأته 1 + وامرأة 1 + "
    "وامرأت 1. Excluded from the 24/24: duals (man رجلين/رجلان 5; woman "
    "امرأتان/امرأتين 2) and plurals (رجال 28, نساء 59). Yahya's own page "
    "gives 23/23 -- one short on each side -- and no principled exclusion "
    "produces 23 from the 24 singulars.",
    {"count": [24, 24],
     "note": "Reconstructed (Al-Suwaidan/Elias list, not Yahya's): singular "
             "surface forms = 24/24. Yahya's stated number is 23/23; the "
             "one-token exclusion that would give 23 is not stated anywhere "
             "and cannot be reconstructed. Scribd source for the "
             "Al-Suwaidan list was not fetched (Scribd blocks text fetch); "
             "the 24/24 is verified from the corpus, not from the source."},
    {"count": [57, 85],
     "note": "QAC: LEM rajul 29 (24 singular + 5 dual) + LEM rijaAl "
             "(men, plural) 28 = 57; LEM {mora>at 26 (24 singular + 2 dual) "
             "+ LEM nisaA^' (women) 59 = 85. The 24/24 is the singular-only "
             "subset on both sides."},
    pair_block(man_lem + man_plur, woman_lem + woman_plur,
               verses_scholar=sorted(set(qac_verses(man_sing))
                                     | set(qac_verses(woman_sing)))))

# ---------- 9. life-death-145 ----------
add("life-death-145",
    "method not stated by the source",
    "unstated",
    "Life: noun الحياة (LEM Hayaw`p) 76; whole ROOT Hyy 184 (noun 76 + أحيا "
    "'give life' 51 + حيّ 'living' 24 + يستحيي 9 -- of which 2:26 and 33:53 "
    "are 'shy', the rest 'spare alive' -- + تحية 'greeting' 6, حياة senses "
    "etc.); excluded: حيّة 'snake' (20:20) and shyness. Death: noun الموت "
    "(LEM mawot) 50; whole ROOT mwt 165 (noun 50 + مات 'died' 39 + ميّت "
    "'dead' 38 + أمات 'cause to die' 21 + ميتة 'carrion' 6 + موت forms). The "
    "circulating list (quranic-miracles.com, fetched 2026-11-07) states no "
    "method and gives no form list.",
    {"count": [None, None],
     "note": "No rule reproduces 145/145. Tested: noun 76/50; whole-root "
             "184/165; substring حياة-family 125 / موت-family 171 (after "
             "removing ظلمات/كلمات false positives); broad families "
             "(root_counts_script) do not reach 145 either."},
    {"count": [184, 165],
     "note": "QAC whole-root: Hyy 184, mwt 165. Noun-only: Hayaw`p 76, "
             "mawot 50. Neither pairing is 145/145."},
    pair_block(life_root, death_root))

# ---------- 10. sun-moon-33-27 ----------
add("sun-moon-33-27",
    "Yahya's page states for light: 'In counting the word \"light\" only "
    "the simple forms of the word were included.' Sun and moon carry no "
    "method statement on the page; the moon 27 is a separate claim "
    "(WikiIslam), not paired with sun by Yahya -- his page contains no "
    "'moon' at all. Units: simple surface forms.",
    "stated",
    "Light simple forms counted: نور 8 + النور 10 + نورا 9 + والنور 3 + "
    "بنور 1 + نورهم 2 = 33. Excluded: نورنا/نوركم (suffixed) and منير "
    "'shining' forms (6). Sun: شمس substring 33, all sun-sense, no "
    "look-alikes. Moon: قمر substring 27, all moon-sense.",
    {"count": [33, 33, 27],
     "note": "Stated rule verified: sun شمس substring = 33; light simple "
             "forms = 33 (selection above); moon قمر substring = 27. The "
             "pair is really sun/light 33/33 plus a separate moon 27."},
    {"count": [33, 27, 43],
     "note": "QAC: ROOT $ms (sun) = 33; ROOT qmr (moon) = 27; LEM nuwr "
             "(light) = 43, or 49 counting LEM m~uniyr ('shining', 6). "
             "Sun and moon agree under both rules; light is 33 only under "
             "Yahya's stated simple-forms selection."},
    pair_block(sun_root + light_lem, moon_root,
               verses_scholar=sorted(set(sun_surf_vs) | set(moon_surf_vs)
                                     | set(light_surf_vs))))

# ---------- 11. muhammad-4 ----------
add("muhammad-4",
    "method not stated by the source",
    "unstated",
    "The name occurs at 3:144, 33:40, 47:2, 48:29. Excluded: أحمد (Ahmad, "
    "61:6) -- a different name for the same person, not counted. The "
    "attribution to Yahya's list rests on the wider list tradition: the "
    "fetched Yahya article page does not contain 'Muhammad 4' verbatim.",
    {"count": 4,
     "note": "Reconstructed: plain surface count محمد = 4. The source "
             "states no method; this is the selection that reproduces the "
             "claim."},
    {"count": 4,
     "note": "QAC: LEM muHam~ad = 4. Both rules agree."},
    loc_block(muhammad, verses_scholar=muhammad_surf_vs))

# ---------- 12. iman-kufr-25 ----------
add("iman-kufr-25",
    "Yahya's page states the qualifier: 'The word faith (iman) (without "
    "genitive) is repeated 25 times throughout the Qur'an as is also the "
    "word infidelity (kufr).' Units: the nouns إيمان / كفر, with the "
    "genitive excluded. What '(without genitive)' means in practice is "
    "reconstructed below (see verification note); the qualifier itself is "
    "verbatim from the source.",
    "stated",
    "Genitive in Arabic covers the possessive pronoun suffixes "
    "(إيمانهم/إيمانكم/كفرهم -- the suffix is a genitive pronoun). Bare "
    "(unsuffixed) tokens: iman 25 (GEN-case 12 + ACC-case 11 + NOM-case 2); "
    "kufr 25 (ACC-case 14 + GEN-case 10 + NOM-case 1). Suffixed tokens "
    "excluded: iman 20, kufr 12. The alternative reading -- excluding all "
    "GEN-case tokens -- gives 21 (iman) and 20 (kufr) and does NOT "
    "reproduce 25. The circulating list (quranic-miracles.com) gives "
    "iman/kufr as 17, not 25.",
    {"count": [25, 25],
     "note": "Reconstructed implementation of the stated qualifier: bare "
             "(unsuffixed) noun forms give exactly 25/25 (QAC LEM <iyma`n "
             "bare 25; LEM kufor bare 25). Both words occur together in "
             "several of the same verses (2:108, 3:167, 3:177, 9:23, "
             "16:106, 49:7)."},
    {"count": [45, 37],
     "note": "QAC noun-only (root narrowed by lemma to the intended sense): "
             "LEM <iyma`n = 45, LEM kufor = 37. The 25/25 is the bare-noun "
             "subset. Broader sense-level families: belief (verb آمن 537 + "
             "مؤمن 202 + إيمان 45 + مؤمنات 22 + مؤمنة 6) = 812; disbelief "
             "(ROOT kfr minus كفّارة 'expiation') = 507."},
    pair_block(iman_lem, kufr_lem,
               verses_scholar=sorted(set(qac_verses(iman_bare))
                                     | set(qac_verses(kufr_bare)))),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "Yahya's '(without genitive)' reproduces exactly "
                "once it is read as 'without the genitive/possessive "
                "pronominal suffixes': bare إيمان = 25 and bare كفر = 25 "
                "(QAC, script-counted, both sides). The filed note said no "
                "clean rule reproduces 25/25; the bare-form rule does, on "
                "both sides at once."})

# ---------- 13. zakah-blessing-32 ----------
add("zakah-blessing-32",
    "method not stated by the source",
    "unstated",
    "Zakah: noun الزكاة (LEM zakaw`p) 32; excluded are the same-root purify "
    "verbs (زكّى 12, تزكّى 8, أزكى 4, زكيّ 2 -- ROOT zkw total 59). "
    "Blessing: ROOT brk 32, all blessing-sense lemmas (مبارك 8, تبارك 9, "
    "بركة 3, بارك 8, مباركة 4). The برك substring (5) misses بارك/تبارك "
    "because of the alif; the زك substring (67) catches the purify verbs.",
    {"count": [32, 32],
     "note": "Reconstructed: zakah noun (LEM zakaw`p) = 32; blessing by "
             "ROOT brk = 32. The source states no method; these are the "
             "selections that reproduce the claim."},
    {"count": [32, 32],
     "note": "QAC: LEM zakaw`p = 32; ROOT brk = 32. Both rules agree."},
    pair_block(zakah_lem, bless_root),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note used substrings (زك 67, برك 5), "
                "which miss بارك/تبارك (alif) and catch the purify verbs. "
                "By lemma/root, zakah (LEM zakaw`p) is exactly 32 and "
                "blessing (ROOT brk) is exactly 32."})

# ---------- 14. say-they-said-332 ----------
add("say-they-said-332",
    "method not stated by the source",
    "unstated",
    "\"Say\" is the 2nd-person masculine singular imperative قُلْ: قُلْ 293 "
    "(قُلْ 218 + قُل 45 + قُلِ 30) + فَقُلْ 18 + وَقُلْ 21 = 332. Excluded "
    "from 'say': plural/dual/feminine imperatives قولوا (17 tokens: وقولوا "
    "8, قولوا 2, فقولوا 2, فقولا 3, فقولي 1, وقلن 1) and the jussive "
    "وَلْيَقُولُوا (1) -- 350 imperatives in all. 'They said' is the "
    "perfect 3rd-person masculine plural قالوا (332: قالوا/وقالوا/فقالوا/"
    "لقالوا); the imperfect يقولون ('they say') is a different form and is "
    "excluded.",
    {"count": [332, 332],
     "note": "Reconstructed: singular imperative قل (QAC LEM qaAla, IMPV, "
             "2MS) = 332; قالوا = 332 (surface and QAC PERF 3MP agree). The "
             "source states no method; these are the selections that "
             "reproduce the claim."},
    {"count": [332, 332],
     "note": "QAC: LEM qaAla IMPV 2MS = 332; LEM qaAla PERF 3MP قالوا = "
             "332. Whole ROOT qwl = 1722 (all 'say/said' forms). Both rules "
             "agree on 332/332."},
    pair_block(say_sg_locs, they_said_qac,
               verses_scholar=sorted(set(qac_verses(say_sg_locs))
                                     | set(they_said_vs))),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed 333 for 'say' does not reproduce: the "
                "singular imperative قل is 332 exactly (293 + 18 + 21 by "
                "prefix, QAC LEM qaAla IMPV 2MS), and قالوا is 332. The "
                "333rd token in a surface count is قَلَّ 'it became little' "
                "(4:7, QAC LEM qal~a, ROOT qll) -- not a 'say' at all. "
                "(350 counts every imperative form, including plurals.)"})

# ---------- 15. plant-tree-26 ----------
add("plant-tree-26",
    "method not stated by the source",
    "unstated",
    "Plant: ROOT nbt 26 (أنبت verbs 16 + نبات nouns 9 + تنبت 1). Tree: ROOT "
    "$jr 27, of which 1 is the dispute verb شَجَرَ (4:65, LEM $ajara, "
    "'what has arisen/disputed between them') -- not a tree. Tree-sense = "
    "26 (شجرة 19 + شجر 7).",
    {"count": [26, 26],
     "note": "Reconstructed: plant by ROOT nbt = 26; tree by ROOT $jr "
             "minus the dispute verb = 26. The source states no method; "
             "these are the selections that reproduce the claim."},
    {"count": [26, 26],
     "note": "QAC: ROOT nbt = 26; ROOT $jr tree-sense = 26 (whole root 27 "
             "incl. the 4:65 dispute verb). Both rules agree."},
    pair_block(plant_root, tree_sense),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note used substrings (نبات 11, شجر 27). "
                "By root, plant (nbt) is exactly 26, and tree ($jr) is 27 "
                "of which one token (شَجَرَ, 4:65) is the verb 'to dispute', "
                "not a tree -- tree-sense 26. Both sides reproduce under "
                "the project's standard root rule with sense-narrowing."})

# ---------- 16. reward-forgiveness-117-234 ----------
add("reward-forgiveness-117-234",
    "method not stated by the source",
    "unstated",
    "Reward: ROOT jzy 118 = جزى verbs (jazaY` 73) + جزاء nouns (jazaA^' "
    "42) + جازٍ 'one who avails' (31:33) + نجازي 'We recompense' (34:17) + "
    "الجزية 'jizya tax' (9:29). Only the jizya (1 token) is not reward. "
    "Forgiveness: ROOT gfr 234 = غفور 91 + غفر 65 + استغفر 40 + مغفرة 28 + "
    "غفّار 5 + غافر 2 + غفران 1 + مستغفرين 1 + استغفار 1 -- all "
    "forgiveness-sense.",
    {"count": [117, 234],
     "note": "Reconstructed: reward by ROOT jzy minus the jizya tax token "
             "= 117; forgiveness by ROOT gfr = 234. The source states no "
             "method; these are the selections that reproduce the claim."},
    {"count": [117, 234],
     "note": "QAC: ROOT jzy reward-sense = 117 (whole root 118 incl. "
             "jizya 9:29); ROOT gfr = 234. Both rules agree."},
    pair_block(jzy_reward, gfr_root),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note said reward needs 'an unstated "
                "one-token exclusion' from ROOT jzy = 118. The exclusion is "
                "identified: الجزية (jizya tax, 9:29, LEM jizoyap) is the "
                "only non-reward lemma in the root; every other jzy token "
                "is recompense/reward-sense. Reward-sense = 117, "
                "forgiveness = 234 exactly."})

# ---------- 17. guidance-mercy-79 ----------
add("guidance-mercy-79",
    "method not stated by the source",
    "unstated",
    "Guidance: noun هدى (LEM hudFY) 85 total, of which 79 are bare "
    "(unsuffixed) -- QAC stem forms hudFY 43 + hudaY` 24 + hudaY 7 + "
    "hudaY`^ 5; the 6 suffixed tokens (هداه/هداهم...) are excluded. Mercy: "
    "noun رحمة (LEM raHomap) 114 total, of which 79 are bare (unsuffixed) -- "
    "stem forms raHomapF 34 + raHomapN 12 + raHomapK 11 + r~aHomapi 5 + "
    "raHomata 3 + raHomapi 3 and 11 further bare forms; the 35 suffixed "
    "tokens (رحمته/رحمتهم/رحمتك...) are excluded. Whole roots: hdy 316, "
    "rHm 339. This is the same bare-form (unsuffixed noun) rule that "
    "reproduces iman/kufr 25/25 -- Yahya's '(without genitive)' for iman "
    "is the same idea (no possessive/genitive suffix).",
    {"count": [79, 79],
     "note": "Reconstructed: bare (unsuffixed) noun forms give exactly "
             "79/79 (QAC LEM hudFY bare 79; LEM raHomap bare 79). The "
             "source states no method; this is the selection that "
             "reproduces the claim."},
    {"count": [79, 79],
     "note": "QAC: bare nouns hudFY 79 / raHomap 79. Noun totals 85/114; "
             "whole-root 316/339. The 79/79 is the bare-noun subset on "
             "both sides."},
    pair_block(hudfy_bare, rahma_bare),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note tested substrings (هد 432, رحم 318) "
                "and noun totals (85/114) and found no 79. The bare "
                "(unsuffixed) noun forms -- the same rule that reproduces "
                "iman/kufr 25/25 -- give exactly 79/79: hudFY bare 79 "
                "(85 minus 6 suffixed) and raHomap bare 79 (114 minus 35 "
                "suffixed), script-counted on QAC."})

# ---------- 18. tongue-sermon-25 ----------
add("tongue-sermon-25",
    "method not stated by the source",
    "unstated",
    "Tongue: ROOT lsn 25, all LEM lisaAn -- singular لسان plus plural "
    "ألسنة (the substring لسان 15 misses the plurals). Sermon: the counted "
    "word is موعظة 'admonition', not 'sermon' (WikiIslam: 'sermon' as such "
    "does not appear in the Quran). ROOT wEZ 25 = وعظ verbs 15 + موعظة 9 + "
    "واعظين 1 (the substring موعظ 9 misses the verbs).",
    {"count": [25, 25],
     "note": "Reconstructed: tongue by ROOT lsn = 25; admonition by ROOT "
             "wEZ = 25. The source states no method; these are the "
             "selections that reproduce the claim."},
    {"count": [25, 25],
     "note": "QAC: ROOT lsn = 25; ROOT wEZ = 25. Both rules agree."},
    pair_block(tongue_root, sermon_root),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note used substrings (لسان 15, موعظ 9), "
                "which miss the plural ألسنة and the وعظ verb forms. By "
                "root, tongue (lsn) is exactly 25 and admonition (wEZ) is "
                "exactly 25. The English gloss 'sermon' is wrong "
                "(موعظة = admonition), but the counts reproduce."})

# ---------- 19. wine-intoxication-6 ----------
add("wine-intoxication-6",
    "method not stated by the source",
    "unstated",
    "Wine: noun خمر (LEM xamor) 6; the 7th ROOT xmr token is خمرهن 'their "
    "veils' (24:31, LEM xumur) -- not wine. Intoxication: ROOT skr 7, all "
    "intoxication-sense -- سكرت 15:15, سكرتهم 15:72, سكرا 16:67, سكرة "
    "الموت 50:19, سكارى x3 (4:43, 22:2 x2). No token can be excluded on "
    "sense grounds; intoxication is 7, not 6.",
    {"count": [6, None],
     "note": "Wine 6 reproduces as the noun (LEM xamor). Intoxication does "
             "not reproduce as 6: ROOT skr = 7, all intoxication-sense. No "
             "stated or reconstructable rule gives 6/6."},
    {"count": [6, 7],
     "note": "QAC: LEM xamor (wine noun) = 6 (whole ROOT xmr 7 incl. "
             "veils 24:31); ROOT skr (intoxication) = 7. The pair differs "
             "by one on the intoxication side."},
    pair_block(wine_lem, intox_root))

# ---------- 20. mind-light-49 ----------
add("mind-light-49",
    "method not stated by the source",
    "unstated",
    "Mind: ROOT Eql 49 -- all verb forms (تعقلون 'you use reason' etc.); "
    "there is no noun عقل in the Quran, so the 'mind' count is already a "
    "root count over verbs. Light: LEM nuwr 43; LEM m~uniyr ('shining, "
    "illuminating', adjective) 6; nuwr + muniyr = 49. ROOT nwr as a whole "
    "is 194 because it includes نار 'fire' (145) -- not light. The 49 for "
    "light therefore requires counting منير as 'light', which mixes the "
    "noun with the adjective (WikiIslam's route to 49).",
    {"count": [49, None],
     "note": "Mind 49 reproduces by ROOT Eql. Light 49 reproduces ONLY as "
             "nuwr 43 + muniyr 6; the noun alone is 43. No stated method; "
             "the light side needs the adjective included."},
    {"count": [49, 43],
     "note": "QAC: ROOT Eql = 49; LEM nuwr = 43 (49 with m~uniyr). Under "
             "the plain lemma rule the pair is 49/43; under a root rule "
             "that counts منير as light it is 49/49. NOT proposed as a "
             "correction: the prior team explicitly rejected mixing the "
             "noun with the adjective, and the choice is a judgement call "
             "for the coordinator/MK."},
    pair_block(mind_root, light_lem))

# ---------- 21. benefit-corrupt-50 ----------
add("benefit-corrupt-50",
    "method not stated by the source",
    "unstated",
    "Benefit: ROOT nfE 50 (نفع verb 31 + نفع noun 11 + منافع 8). Corrupt: "
    "ROOT fsd 50 (مفسد 21 + أفسد 15 + فساد 11 + فسدت 3). The old differs "
    "rested on substrings (نفع 45, فساد 11).",
    {"count": [50, 50],
     "note": "Reconstructed: both sides are exactly 50 under the QAC root "
             "rule (nfE 50, fsd 50)."},
    {"count": [50, 50],
     "note": "QAC: ROOT nfE = 50; ROOT fsd = 50. Both rules agree. NOTE: "
             "this is the same result as the benefit-corrupt-50 flip "
             "proposed in PASTED_PAGE_CHECK.md, which is still UNAPPROVED "
             "by MK -- so NO correction is recorded here, per the task "
             "instructions. The numbers are reported; the status change is "
             "left to the coordinator/MK."},
    pair_block(benefit_root, corrupt_root),
    correction=None)

# ---------- 22. love-obedience-83 ----------
add("love-obedience-83",
    "method not stated by the source",
    "unstated",
    "Love: ROOT Hbb 95, minus grain (حبّ 'grain/seed' 7 + حبّة 5 = 12) = "
    "83 love-sense (أحبّ verbs 64 + حبّ noun 9 + استحبّ 4 + أحبّ 3 + "
    "أحبّاء 1 + محبّة 1 + حبّب 1). Obedience: ROOT TwE 129, minus استطاع "
    "'to be able' (LEM {sotaTaAEa, 42) = 87 obedience-sense (أطاع 72 + "
    "طوع 4 + طاعة 3 + تطوّع 2 + يطاع 2 + طواعية 1 + مطوّعين 1 + طائعين 1 + "
    "مطاع 1). Love reproduces (83); obedience is 87, four over.",
    {"count": [83, None],
     "note": "Love 83 reproduces under root-minus-grain. Obedience does "
             "not reproduce as 83: obedience-sense root = 87, whole root = "
             "129. No stated or reconstructable rule gives 83/83."},
    {"count": [83, 87],
     "note": "QAC: ROOT Hbb love-sense = 83 (whole root 95 incl. grain "
             "12); ROOT TwE obedience-sense = 87 (whole root 129 incl. "
             "'to be able' 42). The pair differs by four on the obedience "
             "side."},
    pair_block(love_root, obed_sense))

# ---------- 23. refuge-forever-28 ----------
add("refuge-forever-28",
    "method not stated by the source",
    "unstated",
    "The filed Arabic ملجأ (malja', 'refuge') was wrong -- Yahya's page "
    "says 'refuge (maseer)', i.e. المصير 'destination/return'. مصير "
    "substring = 28 (المصير 23 + مصيرا/ومصيرا/مصيركم forms); LEM maSiyr = "
    "28. Forever: ابدا = 28 by exact surface form and by QAC lemma "
    ">abadFA (28 verses). The earlier '29' was a substring false positive: "
    "the ابدا substring also catches عابدات 'devout [women]' (66:5, LEM "
    "Ea`bida`t, ROOT Ebd), which is not أبدا at all.",
    {"count": [28, 28],
     "note": "Reconstructed: maseer (LEM maSiyr) = 28; forever (LEM "
             ">abadFA, exact form) = 28. The source states no method; these "
             "are the selections that reproduce the claim."},
    {"count": [28, 28],
     "note": "QAC: LEM maSiyr = 28; LEM >abadFA = 28. Both rules agree."},
    pair_block(maseer_lem, abad_lem),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note said forever was 29 ('ابدا substring "
                "29 -- one over 28'). The 29th hit is عابدات (66:5), a "
                "substring false positive: its skeleton عابدات contains "
                "ابدا, but the word is 'devout [women]' (LEM Ea`bida`t), "
                "not أبدا. Exact-form and QAC-lemma counts both give 28, "
                "so the pair is 28/28."})

# ---------- 24. disaster-thanks-75 ----------
add("disaster-thanks-75",
    "method not stated by the source",
    "unstated",
    "Disaster: ROOT Swb 77 = أصاب 'befall/afflict' verbs 64 + مصيبة 10 + "
    "مصيب 'one who is struck' (11:81) 1 + صيّب 'rainstorm' (2:19) 1 + "
    "صواب 'what is right' (78:38) 1. The last two are not disaster-sense; "
    "excluding them gives 75. Thanks: ROOT $kr 75, all thanks-sense "
    "(شكر 46 + شاكر 14 + شكور 10 + مشكور 2 + شكور 2 + شكر 1).",
    {"count": [75, 75],
     "note": "Reconstructed: disaster by ROOT Swb minus the two "
             "non-disaster lemmas (صيّب, صواب) = 75; thanks by ROOT $kr = "
             "75. The source states no method; these are the selections "
             "that reproduce the claim."},
    {"count": [75, 75],
     "note": "QAC: ROOT Swb disaster-sense = 75 (whole root 77); ROOT $kr "
             "= 75. Both rules agree."},
    pair_block(disaster_sense, thanks_root),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note used substrings (مصيب 11, شكر 47). "
                "By root, thanks ($kr) is exactly 75, and disaster (Swb) "
                "is 77 of which two tokens are not disaster at all -- "
                "صيّب 'rainstorm' (2:19) and صواب 'what is right' (78:38) "
                "-- leaving disaster-sense 75. Same sense-narrowing the "
                "project already applies (grain out of Hbb, expiation out "
                "of kfr)."})

# ---------- 25. trouble-peace-13 ----------
add("trouble-peace-13",
    "method not stated by the source",
    "unstated",
    "The counted words are الضيق (distress) and الطمأنينة (tranquillity) -- "
    "the filed Arabic ضر/سلام was wrong. Yahya's English page just says "
    "'trouble' and 'peace' with no Arabic, so the word identification is "
    "itself reconstructed from the root counts. Distress: ROOT Dyq 13 "
    "(ضاق verbs 7 + ضيق 2 + ضيق 2 + ضائق 1 + تضيق 1). Tranquillity: ROOT "
    "Tmn 13 (اطمأنّ 9 + مطمئن 2 + مطمئنة 2). Plain substrings give ضيق 7 "
    "and طمأن 3 -- the 13/13 needs root counting, not substrings.",
    {"count": [13, 13],
     "note": "Reconstructed: ROOT Dyq = 13 and ROOT Tmn = 13. The source "
             "states no method and gives no Arabic; this is the selection "
             "that reproduces the claim."},
    {"count": [13, 13],
     "note": "QAC: ROOT Dyq = 13; ROOT Tmn = 13. Both rules agree."},
    pair_block(distress_root, tranquil_root))

# ---------- 26. treachery-foul-16 ----------
add("treachery-foul-16",
    "method not stated by the source",
    "unstated",
    "Treachery: ROOT xwn 16 (خان 5 + خائنين 3 + يختانون 2 + خوّان 2 + "
    "خائنة 2 + خيانة 2). Foul: ROOT xbv 16 (خبيث 9 + خبيثة 4 + خبيثات 2 + "
    "خبث 1). The substrings (خيان 2, خبيث 13) miss the verb forms.",
    {"count": [16, 16],
     "note": "Reconstructed: treachery by ROOT xwn = 16; foul by ROOT xbv "
             "= 16. The source states no method; these are the selections "
             "that reproduce the claim."},
    {"count": [16, 16],
     "note": "QAC: ROOT xwn = 16; ROOT xbv = 16. Both rules agree."},
    pair_block(treach_root, foul_root),
    correction={"field": "our_status", "was": "differs", "now": "confirmed",
                "why": "The filed note used substrings (خيان 2, خبيث 13). "
                "By root, treachery (xwn) is exactly 16 and foul (xbv) is "
                "exactly 16 -- the verb forms the substrings miss supply "
                "the difference."})

# ---------- 27. righteous-wicked-6-3 ----------
add("righteous-wicked-6-3",
    "method not stated by the source",
    "unstated",
    "The filed Arabic صالح/طالح was wrong -- Yahya's words are الأبرار "
    "(the righteous) and الفجار (the wicked). أبرار substring 6 (الأبرار 5 "
    "+ للأبرار 1); فجار substring 3 (الفجار 2 + كالفجار 1). Under the lemma "
    "rule the wicked side is 4, not 3: LEM fuj~aAr also covers الفجرة "
    "(80:42, a different plural pattern of the same lemma). The righteous "
    "side is 6 under both rules (LEM bar~ does not separate الأبرار from "
    "البرّ, so the surface form is the identifier).",
    {"count": [6, 3],
     "note": "Reconstructed: surface forms أبرار 6 / فجار 3. The source "
             "states no method; this is the selection that reproduces the "
             "claim."},
    {"count": [6, 4],
     "note": "QAC: righteous (surface الأبرار) = 6; wicked by LEM fuj~aAr "
             "= 4 (الفجار 3 + الفجرة 80:42). The two rules differ by the "
             "one 80:42 token; the finding stands confirmed on the "
             "surface-form rule."},
    pair_block(
        [loc for loc in lem_locs("bar~")
         if skeleton(tanzil_token(*loc)) in {"الابرار", "للابرار"}],
        wicked_lem,
        verses_scholar=sorted(set(righteous_vs) | set(wicked_vs))))

# ---------- 28. summer-winter-5 ----------
add("summer-winter-5",
    "method not stated by the source",
    "unstated",
    "Summer: ROOT Syf = 1 (الصيف, 106:2 only). Winter: ROOT $tw = 1 "
    "(الشتاء, 106:2 only -- Uthmani spelling الشتآء, which is why a raw "
    "search for شتاء finds nothing) -- both words occur in a single verse. "
    "The nearest neighbours do not give 5/5 either: heat ROOT Hrr = 15 "
    "(حرور, حرّ, تحرير...), cold ROOT brd = 5 (برد 2 + بارد 2 + برد 1). "
    "Cold alone is 5; heat is 15 and summer/winter are 1 each.",
    {"count": [None, None],
     "note": "No rule reproduces 5/5. Summer/winter by root = 1/1 (each "
             "occurs once, both in 106:2); heat/cold by root = 15/5."},
    {"count": [1, 1],
     "note": "QAC: ROOT Syf = 1; ROOT $tw = 1; ROOT Hrr (heat) = 15; ROOT "
             "brd (cold) = 5. Locations are the single verse 106:2, which "
             "contains both words."},
    loc_block_verses([(106, 2)], per_surah_counts={"106": 2}))

# ---------- 29. human-being-65 ----------
add("human-being-65",
    "method not stated by the source",
    "unstated",
    "Human being: انسان substring 65; QAC LEM <insa`n = 71, of which 65 "
    "are انسان (الانسان 58 + للانسان 6 + انسان 1) and 6 are أناس/أناسيّ "
    "(people/mankind collective: أناس 5 + وأناسيّ 1) -- a different word, "
    "excluded. Creation stages (Yahya's table, "
    "verified here by lemma/form): soil تراب (LEM turaAb) 17 -- the "
    "substring 20 catches أتراب 'peers' (3 tokens); drop نطفة (LEM "
    "n~uTofap) 12; embryo علقة (LEM Ealaqap) 5 + علق (LEM Ealaq, 96:2) 1 = "
    "6 -- كالمعلقة 'like one suspended' (4:129, LEM muEal~aqap) is NOT an "
    "embryo and is excluded; lump مضغة (LEM muDogap) 3; bone عظام 13 + عظم "
    "(6:146, 19:4) 2 = 15; flesh لحم (LEM laHom) 12 -- the substring 58 "
    "catches لحوم 'meats' and other forms. Stages sum: 17+12+6+3+15+12 = 65.",
    {"count": 65,
     "note": "Reconstructed: انسان surface count = 65; the stage table "
             "reproduces exactly under lemma/form rules (see exceptions). "
             "The source states no method; these are the selections that "
             "reproduce the claim."},
    {"count": 65,
     "note": "QAC: LEM <insa`n = 71 (65 انسان + 6 أناس/أناسيّ collective); "
             "انسان on its own = 65. Both rules agree on 65 for the word "
             "as claimed."},
    loc_block([loc for loc in insan_lem
               if skeleton(tanzil_token(*loc)) in
               ("الانسان", "للانسان", "انسان")],
              verses_scholar=insan_surf_vs),
    correction={"field": "our_note",
                "was": "the creation-stage reading (the stages of human "
                "creation summing to 65) does not reproduce: تراب 20 + "
                "نطفة 12 + علقة 6 + مضغة 3 + عظام 13 + لحم 58 = 112",
                "now": "the stage table reproduces under lemma/form rules: "
                "soil (turaAb) 17 + drop (n~uTofap) 12 + clot (Ealaqap 5 + "
                "Ealaq 96:2) 6 + lump (muDogap) 3 + bone (عظام 13 + عظم "
                "6:146, 19:4) 15 + flesh (laHom) 12 = 65",
                "why": "The filed note tested substrings, which are "
                "polluted (أتراب 'peers' inside تراب 20; لحوم 'meats' "
                "inside لحم 58). Lemma counts give Yahya's table exactly: "
                "17/12/6/3/15/12. Status stays confirmed; only the note "
                "was wrong."})

# ---------- 30. harun-yahya-populariser ----------
add("harun-yahya-populariser",
    "method not stated by the source",
    "unstated",
    "Not a word count: a literature fact (Yahya popularised the paired-count "
    "list in Miracles of the Qur'an). The full list is published at "
    "harunyahya.info (fetched 2026-11-07); it does not include life/death "
    "145, which circulates on other sites. The list also contains one pair "
    "this file omits: 'reward' (ajr) and 'action' (fa'il), both 107 times "
    "-- side-check here: LEM >ajor (ajr noun) = 105, ROOT fEl = 108, LEM "
    "faAEil = 9; the 107/107 does not reproduce under the QAC rules tested.",
    {"count": None,
     "note": "Not applicable -- no count is claimed."},
    {"count": None,
     "note": "Not applicable -- no count is claimed."},
    {"verses": [], "per_surah": {},
     "note": "locations: not applicable -- this is a literature fact, not "
             "a word count."})

# ---------- 31. qaf-57-57 ----------
add("qaf-57-57",
    "Khalifa states it (Appendix 1, fetched 2026-11-07): 'The computer data "
    "showed that the text of the only Q-initialed suras, 42 and 50, "
    "contained the same number of Q's, 57 and 57.' Units: occurrences of "
    "the letter ق in the text of surahs 42 and 50. The unnumbered basmalahs "
    "contain no ق, so basmalah handling does not affect the count.",
    "stated",
    "None. The letter ق occurs in surah 50 (57) and surah 42 (57); the "
    "initial ق of 50:1 itself counts. No textual variant is involved.",
    {"count": [57, 57],
     "note": "Stated rule verified: letter ق in surah 50 = 57, in surah "
             "42 = 57, under the project letter convention."},
    {"count": [57, 57],
     "note": "Same count -- this is a letter count, not a word count, so "
             "the 'root rule' is the project letter convention (base "
             "letters count; dagger alif/small waw/small yeh are marks). "
             "Both agree: 57/57."},
    loc_block_verses(sorted(set(letter_verses(42, "ق"))
                            | set(letter_verses(50, "ق"))),
                     per_surah_counts={"42": 57, "50": 57}))

# ---------- 32. nun-132-vs-133 ----------
add("nun-132-vs-133",
    "Khalifa states it (Appendix 1, fetched 2026-11-07): the initial 'is "
    "unique; it occurs in one sura, 68, and the name of the letter is "
    "spelled out as three letters -- Noon Wow Noon -- in the original text, "
    "and is therefore counted as two N's. The total count of this letter in "
    "the N-initialed sura is 133.' Units: occurrences of the letter ن in "
    "surah 68, with the 68:1 initial counted as two.",
    "stated",
    "The orthodox written initial is a single ن (68:1), counted once under "
    "the project convention. The unnumbered basmalah prepended to 68:1 "
    "contributes exactly one ن (in الرحمن): surah 68 has 132 ن including "
    "it, 131 without it. Khalifa's 133 = 132 + 1 for the spelled-out "
    "initial.",
    {"count": 133,
     "note": "Stated rule verified arithmetically: our count 132 + 1 for "
             "the spelled-out initial (ن و ن) = 133. The rule itself is "
             "Khalifa's, stated in the source."},
    {"count": 132,
     "note": "Project letter convention: ن in surah 68 = 132 (131 in the "
             "surah text proper + 1 from the unnumbered basmalah in 68:1). "
             "Differs from Khalifa's 133 by exactly the spelled-out "
             "initial."},
    loc_block_verses(letter_verses(68, "ن"),
                     per_surah_counts={"68": 132}))

# ---------- 33. sad-153-vs-152 ----------
add("sad-153-vs-152",
    "Khalifa states it (Appendix 1, Table 2, fetched 2026-11-07): S in "
    "sura 7 = 97, sura 19 = 26, sura 38 = 29, total 152. He also states the "
    "textual rule: in 7:69 'the word \"Bastatan\" is written in some "
    "printings with a \"Saad,\" instead of \"Seen.\" This is an erroneous "
    "distortion... By looking at the oldest available copy of the Quran, "
    "the Tashkent Copy, it was found that the word \"Bastatan\" is "
    "correctly written with a \"Seen\".' Units: occurrences of the letter ص "
    "in surahs 7, 19 and 38, with 7:69 read بسطة (Seen).",
    "stated",
    "The Tanzil text reads 7:69 as بصطة (with ص, small seen above it) -- "
    "verified by script: the skeleton of 7:69 contains بصطة, not بسطة. "
    "That one ص is the whole difference: surah 7 has 98 ص under Tanzil "
    "against Khalifa's 97. Surahs 19 (26) and 38 (29) agree. The unnumbered "
    "basmalahs contain no ص.",
    {"count": [97, 26, 29],
     "note": "Stated rule verified arithmetically: 97+26+29 = 152 requires "
             "7:69 read بسطة (Seen). Under the Tanzil reading (بصطة) the "
             "counts are 98/26/29 = 153."},
    {"count": [98, 26, 29],
     "note": "Project letter convention on the Tanzil text: ص in surah 7 "
             "= 98, surah 19 = 26, surah 38 = 29; total 153. Differs from "
             "Khalifa's 152 by exactly the one ص in 7:69."},
    loc_block_verses(sorted(set(letter_verses(7, "ص"))
                            | set(letter_verses(19, "ص"))
                            | set(letter_verses(38, "ص"))),
                     per_surah_counts={"7": 98, "19": 26, "38": 29}))

# ---------- 34. muqattaat-structure-29-14-78 ----------
add("muqattaat-structure-29-14-78",
    "Sayoud states it (QURANICA 5(2), 2013, fetched 2026-11-07): 'there "
    "exist 29 Surahs that begin with... \"muqattaat letters\"... There are "
    "fourteen of such letters in total'; 'There are 3 Surahs that begin "
    "with 1 disjointed letter (character-monogram); 10 Surahs that begin "
    "with 2 disjointed letters (character-bigram); 13 Surahs that begin "
    "with 3 disjointed letters (character-trigram); 2 Surahs that begin "
    "with 4 disjointed letters (character-tetragram); 1 Surah that begins "
    "with 5 disjointed letters (character-pentagram).' Units: the opening "
    "letters of verse 1 of each initialed surah (surah 42's second set عسق "
    "is in 42:2, counted separately).",
    "stated",
    "All 29 verse-1 openings match the expected initials (verified by "
    "script after stripping the merged unnumbered basmalah from verse 1). "
    "Breakdown: monograms ص (38), ق (50), ن (68); bigrams طه (20), طس "
    "(27), يس (36), حم (40-46); trigrams الم (2, 3, 29-32), الر (10-12, "
    "14, 15), طسم (26, 28); tetragrams المص (7), المر (13); pentagram "
    "كهيعص (19). Distinct letters 14: ا ل م ص ر ك ه ي ع ط س ح ق ن. Total "
    "75 letters in the verse-1 openings (3x1 + 10x2 + 13x3 + 2x4 + 1x5), or "
    "78 counting 42:2 عسق separately.",
    {"count": [29, 14, 75],
     "note": "Stated structure verified: 29 surahs, 14 distinct letters, "
             "75 letters in verse-1 openings (78 with 42:2)."},
    {"count": [29, 14, 75],
     "note": "Same -- this is a structural count of opening verses, not a "
             "word count; both rules are the same count. 78 counting 42:2 "
             "عسق separately."},
    loc_block_verses(sorted(set(muq_verses) | {(42, 2)}),
                     per_surah_counts={str(s): len(EXPECTED[s])
                                       for s in sorted(EXPECTED)}))

# ---------- 35. all-28-letters-verses ----------
add("all-28-letters-verses",
    "Classical/traditional observation; the claim itself states the method: "
    "a verse contains all 28 letters of the Arabic alphabet (distinct-"
    "letter count per verse). No source URL (previously cited to Khalifa's "
    "Appendix 1, which contains no such claim; re-cited as a traditional "
    "observation).",
    "stated",
    "Distinct-letter count per verse on the Tanzil skeleton text (ة counted "
    "as ه, ى as ي, per the project convention). Only two verses in the "
    "whole Quran have 28 distinct letters: 3:154 and 48:29 (verified by "
    "script over all 6,236 verses; neither verse is a verse 1, so no "
    "basmalah is involved).",
    {"count": [28, 28],
     "note": "Stated rule verified: 3:154 and 48:29 each have 28 distinct "
             "letters, none missing; no other verse does."},
    {"count": [28, 28],
     "note": "Same -- distinct-letter count per verse under the project "
             "letter convention. Both agree."},
    loc_block_verses([(3, 154), (48, 29)],
                     per_surah_counts={"3": 28, "48": 28}))

# ---------- 36. longest-word-fasqaynakumuhu ----------
add("longest-word-fasqaynakumuhu",
    "Classical observation, repeated in modern Quran-statistics pages "
    "(calendar-uk FAQ, fetched 2026-11-07: 'The longest word in the Qur'an "
    "is: \"fa'asqaynākumūhu\" (فَأَسْقَيْنَاكُمُوهُ)'). The source states "
    "the word but gives no letter figure and no counting convention -- the "
    "'11 letters' figure is convention-dependent, not stated by the source. "
    "Units: the longest whitespace token in the Quran, by letter count.",
    "stated",
    "فأسقيناكموه (15:22) is 10 letters under the project convention (the "
    "dagger alif is a mark, not a letter); it is 11 letters under a "
    "convention counting the dagger alif as a letter -- in which case it "
    "ties for longest with والمستغفرين (3:17) and والمستضعفين (4:75, "
    "4:127), all 11 letters. Under the project convention the longest "
    "words are those three 11-letter tokens; the next tier is 10 letters "
    "(اقترفتموها 9:24, وبالمؤمنين 8:62, فسينفقونها 8:36, ...).",
    {"count": 11,
     "note": "Under a dagger-alif-counts convention, فأسقيناكموه is 11 "
             "letters and tied for longest (with 3:17, 4:75, 4:127). The "
             "source does not state this convention."},
    {"count": 11,
     "note": "Project convention (dagger alif is a mark): فأسقيناكموه is "
             "10 letters; the longest words are والمستغفرين (3:17) and "
             "والمستضعفين (4:75, 4:127) at 11 letters. The claim 'longest "
             "word' fails under this convention and ties under the other."},
    loc_block_verses([(3, 17), (4, 75), (4, 127), (15, 22)],
                     per_surah_counts={"3": 1, "4": 2, "15": 1}))

# ---------- 37. seven-heavens-7 ----------
add("seven-heavens-7",
    "Phrase count, stated in the claim itself (Yahya's page: 'The statement "
    "of \"seven heavens\" is repeated seven times'): verses containing سبع "
    "('seven') together with سماوات ('heavens'). WikiIslam's verse-by-verse "
    "analysis agrees on the 7 verses.",
    "stated",
    "The 7 verses are 2:29, 17:44, 23:86, 41:12, 65:12, 67:3, 71:15. "
    "Further سبع + heaven-ish verses (WikiIslam's 9 total): 'seven paths' "
    "(طرائق, 23:17), 'seven hard years' (12:48, سنين) and 'seven strong' "
    "(شدادا, 78:12) -- these are سبع with a different second word, not "
    "سماوات, and are excluded from the 7.",
    {"count": 7,
     "note": "Stated rule verified: 7 verses contain سبع + سماوات."},
    {"count": 7,
     "note": "QAC: verses containing both ROOT sbE and LEM samaA^' = 7 "
             "(same verses). Both rules agree."},
    loc_block_verses(seven_verses,
                     per_surah_counts={str(s): 1 for s, v in seven_verses}))

# ---------- write output ----------
ORDER = ["dunya-akhira-115", "jannah-jahannam-77", "shaytan-angels-88",
         "day-365", "month-12", "salawat-5", "sea-land-32-13",
         "man-woman-24-24", "life-death-145", "sun-moon-33-27",
         "muhammad-4", "iman-kufr-25", "zakah-blessing-32",
         "say-they-said-332", "plant-tree-26", "reward-forgiveness-117-234",
         "guidance-mercy-79", "tongue-sermon-25", "wine-intoxication-6",
         "mind-light-49", "benefit-corrupt-50", "love-obedience-83",
         "refuge-forever-28", "disaster-thanks-75", "trouble-peace-13",
         "treachery-foul-16", "righteous-wicked-6-3", "summer-winter-5",
         "human-being-65", "harun-yahya-populariser", "qaf-57-57",
         "nun-132-vs-133", "sad-153-vs-152", "muqattaat-structure-29-14-78",
         "all-28-letters-verses", "longest-word-fasqaynakumuhu",
         "seven-heavens-7"]
assert set(ORDER) == set(E), set(ORDER) ^ set(E)
assert len(ORDER) == 37
# method_status post-pass: "reconstructed" where a specific selection rule
# was identified that reproduces the claimed numbers exactly (the rule is
# spelled out in verification_scholar_rule.note). "stated" (10) is where
# the source itself states a method. The remaining 7 are "unstated": no
# method stated and no reproducing rule found (sea-land, life-death, wine,
# mind-light [49 needs the adjective muniyr counted as "light" -- borderline,
# left for the coordinator], love-obedience, summer-winter, populariser).
RECONSTRUCTED = {
    "dunya-akhira-115", "jannah-jahannam-77", "shaytan-angels-88",
    "month-12", "salawat-5", "man-woman-24-24", "muhammad-4",
    "zakah-blessing-32", "say-they-said-332", "plant-tree-26",
    "reward-forgiveness-117-234", "guidance-mercy-79", "tongue-sermon-25",
    "benefit-corrupt-50", "refuge-forever-28", "disaster-thanks-75",
    "trouble-peace-13", "treachery-foul-16", "righteous-wicked-6-3",
    "human-being-65"}
for _r in E.values():
    if _r["id"] in RECONSTRUCTED:
        assert _r["method_status"] == "unstated", _r["id"]
        _r["method_status"] = "reconstructed"
out = {"checker": "A (paired_counts 30 + letter_counts 7)",
       "generated_by": "data/methods_check_A.py (run it to regenerate)",
       "corpus": "QAC morphology v0.4 (77,429 words) + Tanzil Uthmani "
                 "(6,236 verses)",
       "count_rule_note": "verification_root_rule.count is [a, b] for "
       "paired findings (side a, side b), a single number otherwise; "
       "verification_scholar_rule.count is null where no rule reproduces "
       "the claim. locations.verses is the deduplicated surah:verse list "
       "under the ROOT rule (occurrence counts in per_surah); "
       "verses_scholar_rule is included where the scholar rule differs "
       "and is reconstructable.",
       "findings": [E[i] for i in ORDER]}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"Wrote {OUT} with {len(out['findings'])} findings")
from collections import Counter as _C
print("method_status:", dict(_C(r["method_status"] for r in out["findings"])))
print("corrections proposed:",
      [r["id"] for r in out["findings"] if r["correction"]])
print("locations coverage:",
      sum(1 for r in out["findings"] if r["locations"]["verses"]),
      "of 37 with verse lists; 1 N/A (populariser)")

#!/usr/bin/env python3
"""
names_script.py — Count the 99 Names of God (Asma al-Husna) in the Quran.

PRIMARY SOURCE: Quranic Arabic Corpus (QAC), morphology v0.4
  file: corpus/quranic-corpus-morphology-0.4.txt
  (128,219 data lines; 77,429 words; 6,236 verses; 114 surahs)
  Counts are based on the corpus annotation: match by LEM: (preferred,
  a Name is a specific lemma), cross-checked by ROOT:. Display Arabic is
  copied byte-for-byte from the Tanzil Uthmani text at the same surah:verse.
CROSS-CHECK SOURCE: Tanzil Quran Text, Uthmani script
  file: corpus/quran-uthmani.txt (6,236 verses; 77,881 whitespace tokens)

Counting principle (applied to every Name): a segment counts only when it
is the divine Name — i.e. the word is predicated of God (or stands in
apposition to Allah / huwa / rabb), not when the same lemma describes a
human, an angel, a prophet, a created thing (Throne, Book, provision,
reward), a place, or an abstract noun (justice, truth as a concept,
sovereignty, light as guidance). Where a lemma is ambiguous, the script
uses an explicit whitelist/blacklist of verse references, decided by
reading every occurrence of that lemma in context (see the per-name
`notes` and `excluded` fields in names.json).

Usage:  python3 names_script.py
Outputs (written next to this script):
  names.json, name_edges.json
"""
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
QAC_PATH = HERE.parent / "corpus" / "quranic-corpus-morphology-0.4.txt"
TANZIL_PATH = HERE.parent / "corpus" / "quran-uthmani.txt"

QAC_SHA256 = "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
TANZIL_SHA256 = "ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af"

# Standard ayah counts per surah, in order (verified: sum == 6236).
# NOTE: the brief's table listed surahs 5 and 6 as 165, 120; the correct
# order is 120 (Al-Ma'idah) then 165 (Al-An'am). The sum is 6236 either
# way, but the order matters for verse references. Fixed here.
AYAH_COUNTS = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111,
    43, 52, 99, 128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88,
    69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37,
    35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11,
    18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29,
    19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]
assert sum(AYAH_COUNTS) == 6236 and len(AYAH_COUNTS) == 114

# ---------------------------------------------------------------------------
# Normalisation (Tanzil Arabic -> comparable stem form)
# ---------------------------------------------------------------------------
# Diacritics stripped EXCEPT shadda (U+0651), which is kept: it separates
# e.g. al-Ali (al-Ealiy~, with shadda) from the preposition EalaY (no
# shadda). Dagger alef (U+0670) becomes a plain alef (so Uthmani
# al-r-RaHmAn -> alrHmAn and maAlik (1:4, written m-l-k with dagger alef)
# -> mAlik, distinct from mulk 'kingdom'). Hamza (U+0621) is dropped;
# alef variants and alef wasla become plain alef; waw-with-hamza -> waw,
# yeh-with-hamza -> yeh. Teh marbuta and alef maksura are KEPT, so e.g.
# Hikma 'wisdom' never matches Hakam/Hakim, and baqiya 'a remaining (f.)'
# never matches al-Baqi.
_STRIP = (set(range(0x064B, 0x0651)) | {0x0652, 0x0653, 0x0654, 0x0655, 0x0640}
          | set(range(0x06D6, 0x06EE)) | {0x06DF})


def norm_ar(s):
    s = s.replace("\u0671", "ا").replace("\u0670", "ا")
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ء", "")
    s = s.replace("ؤ", "و").replace("ئ", "ي")
    return "".join(ch for ch in s if ord(ch) not in _STRIP)


def stem_candidates(token):
    """Normalised stem forms a Tanzil token could be, for the raw
    (un-disambiguated) cross-check count and the display-Arabic lookup.
    Strips conjunction/preposition prefixes, the article, a trailing
    accusative alef, plural/dual endings (-un/-in/-an) and pronoun
    suffixes; folds alef maksura (U+0649) into yeh (U+064A) — Uthmani
    writes many final yehs as maksura (al-Hayy, al-Ealiyy, qawiyy) — and
    drops shadda, so this is a RAW count that over-counts homonyms
    (see methodology)."""
    t = norm_ar(token).replace("\u0651", "")
    base = {t, t.replace("\u0649", "\u064a")}
    # Strip prefixes to a fixpoint (bounded): conjunction waw/fa, then
    # prepositions ba/lam/kaf, then the article. Repeated stripping is
    # needed for doubled prefixes such as li-l-RaHman (للرحمن, 'to the
    # Most Gracious') and wa-l-... forms.
    variants = set(base)
    for _ in range(4):
        new = set()
        for v in variants:
            for p in ("و", "ف"):
                if v.startswith(p) and len(v) > 1:
                    new.add(v[1:])
            for p in ("ب", "ل", "ك"):
                if v.startswith(p) and len(v) > 1:
                    new.add(v[1:])
            if v.startswith("ال") and len(v) > 2:
                new.add(v[2:])
        if new <= variants:
            break
        variants |= new
    cands = set()
    for v in variants:
        x = v
        if x.endswith("ا") and len(x) > 2:
            cands.add(x[:-1])
        cands.add(x)
        if x.startswith("ال"):
            cands.add(x[2:])
            if x[2:].endswith("ا") and len(x[2:]) > 2:
                cands.add(x[2:-1])
        for suf in ("ون", "ين", "ان"):
            if x.endswith(suf) and len(x) - len(suf) >= 2:
                cands.add(x[:-len(suf)])
                if x[:-len(suf)].startswith("ال"):
                    cands.add(x[:-len(suf)][2:])
        for suf in ("هما", "هم", "هن", "كم", "كن", "نا", "ها", "ه", "ك", "ي"):
            if x.endswith(suf) and len(x) - len(suf) >= 2:
                cands.add(x[:-len(suf)])
                if x[:-len(suf)].startswith("ال"):
                    cands.add(x[:-len(suf)][2:])
    return cands


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_qac(path):
    """Return list of word dicts: {surah, ayah, word, form, tag, lemma,
    root, definite, features} — one entry per (surah:verse:word)."""
    words = {}
    n_seg = 0
    for line in open(path, encoding="utf-8"):
        if not line.startswith("("):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 4:
            continue
        m = re.match(r"\((\d+):(\d+):(\d+):(\d+)\)", parts[0])
        if not m:
            continue
        s, v, w, seg = map(int, m.groups())
        n_seg += 1
        key = (s, v, w)
        entry = words.setdefault(key, {"surah": s, "ayah": v, "word": w,
                                       "form": "", "tag": "", "features": [],
                                       "lemma": None, "root": None,
                                       "definite": False})
        entry["form"] += parts[1]
        entry["features"].append(parts[3])
        if "STEM" in parts[3]:
            entry["tag"] = parts[2]
        if "PREFIX|Al+" in parts[3]:
            entry["definite"] = True
        lm = re.search(r"LEM:([^|]+)", parts[3])
        if lm:
            entry["lemma"] = lm.group(1)
        rt = re.search(r"ROOT:([^|]+)", parts[3])
        if rt:
            entry["root"] = rt.group(1)
    return list(words.values()), n_seg


def load_tanzil(path):
    lines = open(path, encoding="utf-8").read().splitlines()[:6236]
    verses = {}  # (surah, ayah) -> list of tokens (basmalah included)
    idx = 0
    for s, n in enumerate(AYAH_COUNTS, 1):
        for a in range(1, n + 1):
            verses[(s, a)] = lines[idx].split()
            idx += 1
    return verses


def tanzil_word_tokens(verses, s, v):
    """Tokens of a verse as the QAC sees them: the surah-initial basmalah
    (4 tokens) is present in Tanzil but is not a numbered verse in QAC,
    except in 1:1 (where the basmalah IS the verse) and surah 9 (none)."""
    toks = verses[(s, v)]
    if v == 1 and s not in (1, 9):
        return toks[4:]
    return toks


# ---------------------------------------------------------------------------
# The 99 Names — Tirmidhi enumeration (as at openarabic.org/99-names-of-allah
# and asmaulhusna.com; the list in widest circulation). Arabic below is the
# conventional vowelled form; for Names with count > 0 the script replaces
# it with the exact Uthmani token copied from the Tanzil corpus.
# Fields per Name:
#   qac_lemmas : QAC LEM: values counted (Buckwalter)
#   rule       : 'all' | 'whitelist' | 'blacklist' | 'none' | 'phrase'
#   include    : whitelist refs [(s,v)] or [(s,v,w)]
#   exclude    : blacklist refs [(s,v)] or [(s,v,w)]
#   related    : [{lemma, count, note}] — same-root/same-attribute forms
#                NOT in the primary count
#   tanzil_stems : normalised stems for the raw Tanzil cross-check
#   notes      : why the rule is what it is
# ---------------------------------------------------------------------------
# fmt: off
NAMES = [
 # id, arabic, transliteration, meaning, root, qac_lemmas, rule, include, exclude, related, tanzil_stems, notes
 (1, "الرَّحْمَٰنُ", "Ar-Rahman", "The Most Gracious", "ر ح م", ["r~aHoma`n"], "all", [], [],
  [], ["رحمان"], "QAC excludes the 113 surah-initial basmalahs (they are not numbered verses except 1:1), so the QAC count 57 is the familiar figure; Tanzil text has 57 + 112 = 169 (the other 112 basmalahs)."),
 (2, "الرَّحِيمُ", "Ar-Rahim", "The Most Merciful", "ر ح م", ["r~aHiym"], "blacklist", [], [[9,128]],
  [{"lemma": "r~a`Himiyn", "count": 6, "note": "arHam ar-raHimiyn, 'most merciful of the merciful' (7:151, 12:64, 12:92, 21:83, 23:109, 23:118) — plural form of the same attribute, not in the primary count."}],
  ["رحيم"], "9:128 (ra'uwf raHiym) describes the Messenger, not God, and is excluded. The often-quoted 114 is the number of basmalahs, not the count of the Name: QAC has 115 non-basmalah + 2 basmalah occurrences."),
 (3, "الْمَلِكُ", "Al-Malik", "The King", "م ل ك", ["ma`lik", "malik"], "whitelist",
  [[1,4],[3,26],[20,114],[23,116],[59,23],[62,1],[114,2]], [],
  [{"lemma": "mulok", "count": 48, "note": "mulk, 'kingdom/sovereignty' (e.g. lahu al-mulk, 'to Him belongs the kingdom') — the attribute's noun, not the Name."},
   {"lemma": "malak", "count": 88, "note": "malak, 'angel' — a different word from the same root."}],
  ["مالك","ملك"], "ma`lik (mAlik) is the construct form: 1:4 malik yawm ad-din, 3:26 malik al-mulk; malik (malik) is the King: 20:114, 23:116, 59:23, 62:1 and 114:2 malik an-nas. Other malik tokens are human kings (12:43-76, Yusuf's king; 2:246-247 Talut; 18:79; 5:20, 27:34 plurals) or owners (36:71 malikun, 'they own them')."),
 (4, "الْقُدُّوسُ", "Al-Quddus", "The Most Holy", "ق د س", ["qud~uws"], "all", [], [],
  [{"lemma": "qudus", "count": 4, "note": "qudus in ruH al-qudus, 'the Holy Spirit' (2:87, 2:253, 5:110, 16:102) — not the Name."}],
  ["قدوس"], "Both occurrences are in the name sequences 59:23 and 62:1."),
 (5, "السَّلَامُ", "As-Salam", "The Peace", "س ل م", ["sala`m"], "whitelist", [[59,23]], [],
  [{"lemma": "sala`m", "count": 41, "note": "41 other salaam tokens: greetings (salaamun Ealaykum), dar as-salaam 'abode of peace' (6:127, 10:25), subul as-salaam (5:16), salaam as safety (21:69) — all 'peace', not the Name."}],
  ["سلام"], "The Name as-salaam occurs once, in the 59:22-24 sequence. Every other salaam is the greeting or the noun 'peace'."),
 (6, "الْمُؤْمِنُ", "Al-Mu'min", "The Giver of Security", "أ م ن", ["mu&omin"], "whitelist", [[59,23]], [],
  [{"lemma": "mu&omin", "count": 201, "note": "201 other mu'min tokens are believers (singular, plural al-mu'minun, feminine) — the same lemma, a human referent."}],
  ["مومن"], "The Name al-mu'min occurs once (59:23). All other mu'min are believers."),
 (7, "الْمُهَيْمِنُ", "Al-Muhaymin", "The Guardian over all", "ه ي م ن", ["muhayomin"], "whitelist", [[59,23]], [],
  [{"lemma": "muhayomin", "count": 1, "note": "5:48 muhayminan Ealayhi — 'a guardian over it' describes the revealed Book, not God; excluded by the predication rule (the popular figure 2 counts it)."}],
  ["مهيمن"], "QAC lemma muhayomin, root hmn. Only 59:23 predicates the Name of God."),
 (8, "الْعَزِيزُ", "Al-Aziz", "The Exalted in Might", "ع ز ز", ["Eaziyz"], "blacklist", [],
  [[5,54],[9,128],[11,91],[12,30],[12,51],[12,78],[12,88],[27,34],[41,41],[44,49]],
  [], ["عزيز"],
  "101 lemma tokens; 10 excluded: aEizza (believers mighty, 5:54; chiefs, 27:34), al-Eaziz the Egyptian minister / Joseph as minister (12:30, 12:51, 12:78, 12:88), Eaziz Ealayhi 'grievous to him' of the Prophet (9:128), 'you are not mighty among us' of ShuEayb (11:91), kitab Eaziz 'a mighty Book' (41:41), and the sarcastic 'you are the mighty, the noble' to a damned man (44:49). The familiar figure 92 counts 41:41; this count excludes it because the adjective predicates the Book, not God."),
 (9, "الْجَبَّارُ", "Al-Jabbar", "The Compeller", "ج ب ر", ["jab~aAr"], "whitelist", [[59,23]], [],
  [{"lemma": "jab~aAr", "count": 9, "note": "9 other jabbar tokens are human tyrants/giants: 5:22, 11:59, 14:15, 19:14 (John), 19:32 (Jesus), 26:130, 28:19, 40:35, 50:45."}],
  ["جبار"], "The Name al-jabbar occurs once (59:23)."),
 (10, "الْمُتَكَبِّرُ", "Al-Mutakabbir", "The Supreme in Greatness", "ك ب ر", ["mutakab~ir"], "whitelist", [[59,23]], [],
  [{"lemma": "mutakab~ir", "count": 6, "note": "6 other mutakabbir tokens are arrogant humans: al-mutakabbirin in Hell (16:29, 39:60, 39:72, 40:76) and kull mutakabbir (40:27, 40:35)."}],
  ["متكبر"], "The Name al-mutakabbir occurs once (59:23)."),
 (11, "الْخَالِقُ", "Al-Khaliq", "The Creator", "خ ل ق", ["xa`liq"], "blacklist", [], [[52,35]],
  [], ["خالق"],
  "12 lemma tokens; 52:35 al-khaliqun ('or are they the creators?') is rhetorical, of humans, and is excluded. The plurals al-khaliqin 'best of creators' (23:14, 37:125) and naHnu al-khaliqun (56:59) are God speaking and are counted."),
 (12, "الْبَارِئُ", "Al-Bari", "The Maker", "ب ر أ", ["baAri}"], "whitelist", [[59,24],[2,54]], [],
  [], ["باري"], "59:24 al-bari' and 2:54 bari'ikum 'your Maker' (twice in the verse)."),
 (13, "الْمُصَوِّرُ", "Al-Musawwir", "The Fashioner of forms", "ص و ر", ["muSaw~ir"], "all", [], [],
  [], ["مصور"], "Occurs once, 59:24."),
 (14, "الْغَفَّارُ", "Al-Ghaffar", "The Repeatedly Forgiving", "غ ف ر", ["gaf~aAr"], "all", [], [],
  [], ["غفار"], "5 occurrences, all divine (20:82, 38:66, 39:5, 40:42, 71:10)."),
 (15, "الْقَهَّارُ", "Al-Qahhar", "The Subduer", "ق ه ر", ["qah~aAr"], "all", [], [],
  [], ["قهار"], "6 occurrences, all 'al-waHid al-qahhar' (12:39, 13:16, 14:48, 38:65, 39:4, 40:16)."),
 (16, "الْوَهَّابُ", "Al-Wahhab", "The Bestower", "و ه ب", ["wah~aAb"], "all", [], [],
  [], ["وهاب"], "3 occurrences (3:8, 38:9, 38:35)."),
 (17, "الرَّزَّاقُ", "Ar-Razzaq", "The Provider", "ر ز ق", ["r~az~aAq"], "all", [], [],
  [{"lemma": "r~a`ziqiyn", "count": 6, "note": "khayr ar-raziqin, 'best of providers' (5:114, 15:20, 22:58, 23:72, 34:39, 62:11) — plural form of the same attribute, not in the primary count."}],
  ["رزاق"], "Occurs once, 51:58."),
 (18, "الْفَتَّاحُ", "Al-Fattah", "The Opener", "ف ت ح", ["fat~aAH"], "all", [], [],
  [], ["فتاح"], "Occurs once, 34:26 (al-fattaH al-Ealim)."),
 (19, "الْعَلِيمُ", "Al-Alim", "The All-Knowing", "ع ل م", ["Ealiym"], "blacklist", [],
  [[12,55],[7,109],[26,34],[26,37],[26,197],[35,28]],
  [{"lemma": "Ea`lim", "count": 18, "note": "Ealim al-ghayb, 'Knower of the unseen' (6:73, 9:94, 9:105, 13:9, 23:92, 32:6, 39:46, 59:22, 62:8, 64:18 and others) — the same attribute in participle form, not in the primary count."}],
  ["عليم"],
  "163 lemma tokens; 6 excluded: Joseph's 'I am a guardian, knowing' (12:55), 'a knowledgeable sorcerer' of Moses as alleged by Pharaoh's people (7:109, 26:34, 26:37), and the scholars (Eulama') of Israel (26:197) and of God's servants (35:28). Result 157 matches the commonly quoted figure."),
 (20, "الْقَابِضُ", "Al-Qabid", "The Withholder", "ق ب ض", [], "none", [], [],
  [{"lemma": "qaboD", "count": 1, "note": "qabDa, 'a handful' (20:96, the Samaritan's handful of dust) — the verb yaqbiD 'He withholds' occurs (2:245 wa-llahu yaqbiDu wa-yabsuT) but the Name al-qabiD never appears as a noun."}],
  ["قابض"], "ZERO occurrences. The Name is drawn from the verb in 2:245, not from a noun in the text."),
 (21, "الْبَاسِطُ", "Al-Basit", "The Extender", "ب س ط", ["ba`siT"], "blacklist", [], [[5,28],[6,93],[13,14],[18,18]],
  [], ["باسط"],
  "ZERO occurrences. All 4 basiT tokens are non-divine: Abel 'I will not stretch my hand' (5:28), the angels stretching their hands (6:93), the simile of one stretching his hands to water (13:14), and the dog stretching its forelegs (18:18)."),
 (22, "الْخَافِضُ", "Al-Khafid", "The One who lowers", "خ ف ض", ["xaAfiDap"], "blacklist", [], [[56,3]],
  [], ["خافض"], "ZERO occurrences. The only khafiDa (56:3, 'it will bring low') is the feminine adjective of the Event (the Hour), not the Name."),
 (23, "الرَّافِعُ", "Ar-Rafi", "The One who raises", "ر ف ع", ["raAfiE"], "whitelist", [[3,55]], [],
  [{"lemma": "r~aAfiEap", "count": 1, "note": "rafiEa (56:3, 'it will raise high') — the feminine adjective of the Event, not the Name."}],
  ["رافع"], "1 occurrence: 3:55 wa-rafiEuka ilayya, 'and I will raise you to Me' (God to Jesus)."),
 (24, "الْمُعِزُّ", "Al-Mu'izz", "The Giver of Honour", "ع ز ز", [], "none", [], [],
  [{"lemma": "tuEiz~u", "count": 1, "note": "tuEizzu man tasha', 'You honour whom You will' (3:26) — the verb only; the Name al-muEizz never appears."}],
  ["معز"], "ZERO occurrences. Drawn from the verb in 3:26."),
 (25, "الْمُذِلُّ", "Al-Mudhill", "The Giver of Dishonour", "ذ ل ل", [], "none", [], [],
  [], ["مذل"], "ZERO occurrences. No mu*ill lemma in the corpus; the verb form is in 3:26 (wa-tu*illu)."),
 (26, "السَّمِيعُ", "As-Sami", "The All-Hearing", "س م ع", ["samiyE"], "blacklist", [], [[11,24],[76,2]],
  [], ["سميع"],
  "47 lemma tokens; 2 excluded: the parable of the deaf/blind vs the hearing/seeing (11:24) and 'We made him hearing, seeing' of man (76:2). Result 45."),
 (27, "الْبَصِيرُ", "Al-Basir", "The All-Seeing", "ب ص ر", ["baSiyr"], "blacklist", [],
  [[6,50],[11,24],[12,93],[12,96],[13,16],[20,125],[35,19],[40,58],[76,2]],
  [], ["بصير"],
  "51 lemma tokens; 9 excluded, all 'seeing' of humans: the blind-vs-seeing parables (6:50, 11:24, 13:16, 35:19, 40:58), Jacob regaining sight (12:93, 12:96), the raised-blind man (20:125), and man made 'hearing, seeing' (76:2). Result 42."),
 (28, "الْحَكَمُ", "Al-Hakam", "The Judge", "ح ك م", ["Hakam"], "whitelist", [[6,114]], [],
  [{"lemma": "Hukom", "count": 30, "note": "30 Hukom tokens are the noun 'judgment/decree/ruling' (e.g. inna al-Hukm illa lillah, 'the judgment belongs to Allah alone', 6:57, 12:40, 12:67) — a different lemma from Hakam 'judge'."}],
  ["حكم"],
  "1 occurrence: 6:114 afa-ghayra allahi abtaghi Hakaman, 'shall I seek a judge other than Allah?' — the judge sought is God Himself. The other 2 Hakam tokens are human arbitrators in a marital dispute (4:35, twice). Note: the familiar 'the judgment belongs to Allah' verses (6:57, 12:40, 12:67) use the different lemma Hukom, not Hakam."),
 (29, "الْعَدْلُ", "Al-Adl", "The Utterly Just", "ع د ل", ["Eadol"], "none", [], [],
  [{"lemma": "Eadol", "count": 14, "note": "14 Eadl tokens are all the noun 'justice' (e.g. 16:90 'God commands justice') or 'equivalent/ransom' (2:48, 5:95) — never the personal Name."}],
  ["عدل"], "ZERO occurrences as the Name."),
 (30, "اللَّطِيفُ", "Al-Latif", "The Subtle and Kind", "ل ط ف", ["laTiyf"], "all", [], [],
  [], ["لطيف"], "7 occurrences, all divine (6:103, 12:100, 22:63, 31:16, 33:34, 42:19, 67:14)."),
 (31, "الْخَبِيرُ", "Al-Khabir", "The All-Aware", "خ ب ر", ["xabiyr"], "all", [], [],
  [], ["خبير"], "45 occurrences, all divine (including 25:59 'ask about Him of one All-Aware')."),
 (32, "الْحَلِيمُ", "Al-Halim", "The Forbearing", "ح ل م", ["Haliym"], "blacklist", [],
  [[9,114],[11,75],[11,87],[37,101]],
  [], ["حليم"],
  "15 lemma tokens; 4 excluded, all of humans: Abraham 'forbearing' (9:114, 11:75), ShuEayb mocked as 'the forbearing, the rightly-guided' (11:87), and 'a forbearing boy' Ishmael (37:101). Result 11."),
 (33, "الْعَظِيمُ", "Al-Azim", "The Magnificent", "ع ظ م", ["EaZiym"], "whitelist",
  [[2,255],[42,4],[56,74],[56,96],[69,33],[69,52]], [],
  [{"lemma": "EaZiym", "count": 114, "note": "114 other EaZiym tokens describe things: al-fawz al-EaZiym 'the great success', *u al-faDl al-EaZiym 'the great bounty', al-Earsh al-EaZiym 'the great Throne' (9:129, 23:86, 27:26), al-Qur'an al-EaZiym (15:87), al-EiZam 'bones' (2:259, 23:14, 36:78), and indefinite EaZiym of punishments, rewards and sins."}],
  ["عظيم"],
  "Only 6 occurrences predicate greatness of God/Lord (al-Ealiy al-EaZiym; rabbika al-EaZiym; billah al-EaZiym). The raw surface count of EaZiym is 120, which is why naive counts of 'al-EaZiym' overstate the Name."),
 (34, "الْغَفُورُ", "Al-Ghafur", "The All-Forgiving", "غ ف ر", ["gafuwr"], "all", [], [],
  [{"lemma": "gaAfir", "count": 2, "note": "ghafir a*-*anb 'Forgiver of sin' (40:3) and khayr al-ghafirin 'best of forgivers' (7:155) — the same attribute in participle/plural form, not in the primary count."}],
  ["غفور"], "91 occurrences, all divine (overwhelmingly ghafur raHim)."),
 (35, "الشَّكُورُ", "Ash-Shakur", "The Most Appreciative", "ش ك ر", ["$akuwr"], "whitelist",
  [[35,30],[35,34],[42,23],[64,17]], [],
  [{"lemma": "$akuwr", "count": 6, "note": "6 other shakur tokens describe grateful humans: likulli Sabbar shakur 'for every patient, grateful one' (14:5, 31:31, 34:19, 42:33), Eabdan shakura 'a grateful servant', Noah (17:3), and al-shakur among God's servants (34:13)."}],
  ["شكور"], "Only 4 occurrences are divine (all ghafur shakur / shakur Halim of God)."),
 (36, "الْعَلِيُّ", "Al-Aliyy", "The Most High", "ع ل و", ["Ealiy~"], "blacklist", [], [[19,50],[19,57],[43,4]],
  [], ["علي"],
  "11 lemma tokens; 3 excluded: lisan Sidq Ealiyya 'a lofty reputation' (19:50), makanan Ealiyya 'a lofty place', Idris (19:57), and laEaliy Hakkim 'exalted, wise' of the Book (43:4). Result 8. (QAC's lemma cleanly separates Ealiy~ the Name from the preposition EalaY.)"),
 (37, "الْكَبِيرُ", "Al-Kabir", "The Most Great", "ك ب ر", ["kabiyr"], "whitelist",
  [[13,9],[22,62],[31,30],[34,23],[40,12],[4,34]], [],
  [{"lemma": "kabiyr", "count": 34, "note": "34 other kabir tokens: al-faDl al-kabir / al-fawz al-kabir 'the great bounty/success' (35:32, 42:22, 85:11), kabir/kabira of sins, punishments, rewards, debts, idols, old men and 'your chief' (20:71, 26:49), and >akobar 'greater' (24 tokens, incl. allahu >akobar) — a separate elative lemma."}],
  ["كبير"],
  "6 occurrences: al-kabir al-mutaEal (13:9), al-Ealiy al-kabir (22:62, 31:30, 34:23, 40:12) and wa-kana allahu Ealiyyan kabira (4:34)."),
 (38, "الْحَفِيظُ", "Al-Hafiz", "The Preserver", "ح ف ظ", ["HafiyZ", "Ha`fiZ"], "whitelist",
  [[11,57],[34,21],[42,6],[12,64],[15,9],[21,82]], [],
  [{"lemma": "HafiyZ", "count": 9, "note": "9 other HafiZ tokens: the Prophet 'not a guardian over you' (4:80, 6:104, 6:107, 11:86, 42:48), Joseph 'I am a guardian, knowing' (12:55), guardian angels (6:61, 82:10), kitab HafiZ 'a preserving Book' (50:4), and a keeper of the covenant (50:32)."},
   {"lemma": "Ha`fiZ", "count": 10, "note": "10 other Ha'fiZ tokens: guardians of chastity/bounds (9:112, 23:5, 33:35, 70:29), Joseph's brothers (12:12, 12:63, 12:81), 'we were not keepers of the unseen' (12:81), and the angel-guardian over every soul (86:4)."}],
  ["حفيظ","حافظ"],
  "Two forms of one attribute are counted together: HafiZ (3: 11:57, 34:21, 42:6) and HafiZ the participle (3: 12:64 khayr HafiZa, 15:9 la-HafiZun of the Quran, 21:82 HafiZin of the devils) — all predicated of God."),
 (39, "الْمُقِيتُ", "Al-Muqit", "The Nourisher", "ق و ت", ["m~uqiyt"], "all", [], [],
  [], ["مقيت"], "Occurs once, 4:85 (wa-kana allahu Eala kulli shay'in muqita)."),
 (40, "الْحَسِيبُ", "Al-Hasib", "The Reckoner", "ح س ب", ["Hasiyb"], "blacklist", [], [[17,14]],
  [], ["حسيب"],
  "4 lemma tokens; 17:14 ('sufficient is your own self against you today as a reckoner') is one's own self, not God. Result 3 (4:6, 4:86, 33:39)."),
 (41, "الْجَلِيلُ", "Al-Jalil", "The Majestic", "ج ل ل", [], "none", [], [],
  [{"lemma": "jala`l", "count": 2, "note": "jalaal occurs only inside *u al-jalaal wa-l-ikraam, 'Owner of Majesty and Honour' (55:27, 55:78) — see Name 85. The Name al-jalil itself never appears."}],
  ["جليل"], "ZERO occurrences."),
 (42, "الْكَرِيمُ", "Al-Karim", "The Most Generous", "ك ر م", ["kariym"], "whitelist", [[82,6],[27,40]], [],
  [{"lemma": "kariym", "count": 28, "note": "28 other karim tokens: rizq karim 'generous provision', ajr karim 'generous reward', qur'an karim (56:77), rasul karim (44:17, 69:40, 81:19), malak karim 'a noble angel' (12:31), kitab karim 'a noble letter' (27:29), rabb al-Earsh al-karim 'Lord of the Noble Throne' (23:116), al-Eaziz al-karim addressed sarcastically to a damned man (44:49), and noble places, spouses, plants and scribes."}],
  ["كريم"], "Only 2 occurrences predicate generosity of God: rabbika al-karim (82:6) and rabbi ghaniy karim (27:40)."),
 (43, "الرَّقِيبُ", "Ar-Raqib", "The Watchful", "ر ق ب", ["raqiyb"], "whitelist", [[4,1],[5,117],[33,52]], [],
  [{"lemma": "raqiyb", "count": 2, "note": "2 other raqib tokens: ShuEayb 'I am a watcher with you' (11:93) and raqib Eatid, the recording watcher-angel (50:18)."}],
  ["رقيب"], "3 occurrences, all divine (4:1, 5:117 'You are the Watcher over them', 33:52)."),
 (44, "الْمُجِيبُ", "Al-Mujib", "The Answerer of prayer", "ج و ب", ["m~ujiyb"], "all", [], [],
  [], ["مجيب"], "2 occurrences: 11:61 (rabbi qarib mujib) and 37:75 (fa-niEma al-mujibun, 'how excellent are We as Responders' — plural of majesty)."),
 (45, "الْوَاسِعُ", "Al-Wasi", "The All-Encompassing", "و س ع", ["wa`siE"], "all", [], [],
  [{"lemma": "wa`siEap", "count": 4, "note": "4 feminine wasiEa tokens: 'My earth is vast' / 'God's earth is vast' (4:97, 29:56, 39:10) and wasiEa raHmatuhu (6:147) — vastness of earth/mercy, not the Name."}],
  ["واسع"], "9 occurrences, all divine (overwhelmingly wa-llahu wasiE Ealim)."),
 (46, "الْحَكِيمُ", "Al-Hakim", "The All-Wise", "ح ك م", ["Hakiym"], "blacklist", [],
  [[10,1],[31,2],[36,2],[43,4],[44,4]],
  [], ["حكيم"],
  "97 lemma tokens; 5 excluded, all predicated of the Book/decree: al-kitab al-Hakim 'the Wise Book' (10:1, 31:2), al-Qur'an al-Hakim (36:2), laEaliy Hakim of the Book (43:4), and amr Hakim 'a wise decree' (44:4). Result 92."),
 (47, "الْوَدُودُ", "Al-Wadud", "The Most Loving", "و د د", ["waduwd"], "all", [], [],
  [], ["ودود"], "2 occurrences: 11:90 (rabbi raHim wadud) and 85:14 (al-ghafur al-wadud)."),
 (48, "الْمَجِيدُ", "Al-Majid", "The All-Glorious", "م ج د", ["m~ajiyd"], "whitelist", [[11,73],[85,15]], [],
  [{"lemma": "m~ajiyd", "count": 2, "note": "2 other majid tokens describe the Quran: wa-l-Qur'an al-majid (50:1) and qur'an majid (85:21)."}],
  ["مجيد"], "2 occurrences: 11:73 (innahu Hamid majid) and 85:15 (*u al-Earsh al-majid, where al-majid is nominative and describes *u/Allah, not the Throne)."),
 (49, "الْبَاعِثُ", "Al-Ba'ith", "The Resurrector", "ب ع ث", [], "none", [], [],
  [], ["باعث"], "ZERO occurrences. Only the verb yabEa*u 'He resurrects' occurs; the Name al-baEi* never appears as a noun."),
 (50, "الشَّهِيدُ", "Ash-Shahid", "The Witness", "ش ه د", ["$ahiyd"], "blacklist", [],
  [[2,23],[2,133],[2,143],[2,282],[3,140],[4,41],[4,69],[4,72],[4,135],[4,159],[5,8],[5,44],[5,117,15],[6,144],[6,150],[16,84],[16,89],[22,78],[24,4],[24,6],[24,13],[28,75],[39,69],[41,47],[50,21],[50,37],[57,19],[100,7]],
  [], ["شهيد"],
  "56 lemma tokens; 36 excluded — all human/angelic witnesses: legal witnesses (2:282, 24:4, 24:6, 24:13), prophets as witnesses (4:41, 16:84, 16:89, 22:78, 28:75, 4:159), martyrs (4:69, 3:140-class, 39:69, 57:19), Jesus as witness over his people (5:117 w15), and man as witness to his own ingratitude (100:7). Result 20, all 'Allah is witness' / 'sufficient is Allah as witness' / 'You are witness over all things' (5:117 w29)."),
 (51, "الْحَقُّ", "Al-Haqq", "The Truth", "ح ق ق", ["Haq~"], "whitelist",
  [[6,62],[10,30],[18,44],[20,114],[23,116],[22,6],[22,62],[31,30],[24,25,10]], [],
  [{"lemma": "Haq~", "count": 238, "note": "238 other Haqq tokens are 'the truth' as a concept: ja'a al-Haqq 'the truth has come', al-Haqq min rabbik 'the truth from your Lord', din al-Haqq 'the religion of truth', etc."}],
  ["حق"],
  "Only 9 occurrences predicate Truth of God: huwa al-Haqq (22:6, 22:62, 31:30), al-malik al-Haqq (20:114, 23:116), mawlahum al-Haqq (6:62, 10:30), lillah al-Haqq (18:44), and huwa al-Haqq al-mubin (24:25, word 10 — the verse's first Haqq, w5, is dinahum al-Haqq 'their true due'). The raw surface count of al-Haqq is 247."),
 (52, "الْوَكِيلُ", "Al-Wakil", "The Trustee", "و ك ل", ["wakiyl"], "whitelist",
  [[3,173],[4,81],[4,132],[4,171],[6,102],[11,12],[12,66],[17,2],[17,65],[17,68],[28,28],[33,3],[33,48],[39,62],[73,9]], [],
  [{"lemma": "wakiyl", "count": 9, "note": "9 other wakil tokens: the Prophet 'I am not a guardian over you' (6:66, 6:107, 10:108, 17:54, 39:41, 42:6), a human advocate (4:109), a guardian for a person (25:43), and an advocate against God (17:86)."}],
  ["وكيل"],
  "15 occurrences, all predicated of God (overwhelmingly wa-kafa bi-llah wakila)."),
 (53, "الْقَوِيُّ", "Al-Qawiyy", "The All-Strong", "ق و ي", ["qawiY~"], "blacklist", [], [[27,39],[28,26]],
  [], ["قوي"],
  "11 lemma tokens; 2 excluded: the jinn 'I am strong, trustworthy' (27:39) and Moses 'the strong, the trustworthy' (28:26). Result 9."),
 (54, "الْمَتِينُ", "Al-Matin", "The Firm", "م ت ن", ["matiyn"], "whitelist", [[51,58]], [],
  [{"lemma": "matiyn", "count": 2, "note": "2 other matin tokens are inna kaydi matin, 'My scheme is firm' (7:183, 68:45) — firmness predicated of God's scheme, not of God; excluded by the predication rule."}],
  ["متين"], "1 occurrence: 51:58 (*u al-quwwa al-matin)."),
 (55, "الْوَلِيُّ", "Al-Waliyy", "The Protecting Friend", "و ل ي", ["waliY~"], "blacklist", [],
  [[2,282],[2,257,12],[3,28],[3,175],[4,75],[4,76],[4,89],[4,119],[4,139],[4,144],[5,51],[5,57],[5,81],[6,121],[6,128],[7,3],[7,27],[7,30],[8,34],[8,72],[8,73],[9,23],[9,71],[10,62],[11,20],[11,113],[13,16],[16,63],[17,33],[17,97],[17,111],[18,50],[18,102],[19,5],[19,45],[25,18],[27,49],[29,41],[33,6],[39,3],[41,31],[41,34],[42,6],[42,9,5],[42,46],[45,10],[45,19,11],[46,32],[60,1],[62,6]],
  [], ["ولي"],
  "86 lemma tokens; 53 excluded: all plural awliya' (allies — of disbelievers, Satan, Jews/Christians, believers among themselves, angels as protectors in 41:31, and 'friends of Allah' as saints in 10:62 and 62:6) and singular wali as a human guardian/heir (2:282 debtor's guardian; 17:33, 27:49 heirs; 19:5 Zakariya's heir; 4:75 a human protector; 19:45 Satan's ally; 41:34 a close friend; 17:111 'He has no protector out of weakness' — negating God HAVING a protector, not predicating God AS one; 16:63 Satan as protector). Result 33, all predicated of God ('Allah is the Protector', 'no protector besides God', 'sufficient is Allah as Protector', 'You are our Protector')."),
 (56, "الْحَمِيدُ", "Al-Hamid", "The Praiseworthy", "ح م د", ["Hamiyd"], "all", [], [],
  [], ["حميد"], "17 occurrences, all divine (overwhelmingly al-ghaniy al-Hamid)."),
 (57, "الْمُحْصِي", "Al-Muhsi", "The One who counts all things", "ح ص ي", [], "none", [], [],
  [], ["محصي"], "ZERO occurrences. Only the verb aHSa 'He counted' occurs (e.g. 19:94, 72:28); the Name al-muHSI never appears."),
 (58, "الْمُبْدِئُ", "Al-Mubdi", "The Originator of creation", "ب د أ", ["mubodiy"], "blacklist", [], [[33,37]],
  [], ["مبدي"],
  "ZERO occurrences of the Name. The only mubdi token (33:37 mubdihi, 'what Allah will disclose') is from a different root (b-d-w, 'to disclose'), not b-d-' (the Name's root); the verb yubdi'u 'He originates' is what the Name is drawn from."),
 (59, "الْمُعِيدُ", "Al-Mu'id", "The Restorer", "ع و د", [], "none", [], [],
  [], ["معيد"], "ZERO occurrences. Only the verb yuEidu 'He restores' occurs; the Name al-muEid never appears."),
 (60, "الْمُحْيِي", "Al-Muhyi", "The Giver of Life", "ح ي ي", ["muHoY"], "all", [], [],
  [], ["محيي","محي"],
  "2 occurrences, both la-muHyi al-mawta 'the Reviver of the dead' (30:50, 41:39) — the Name's only Quranic form; the definite al-muHyi never appears. (Uthmani writes the form defectively, la-muHyi, with a single yeh.)"),
 (61, "الْمُمِيتُ", "Al-Mumit", "The Bringer of Death", "م و ت", [], "none", [], [],
  [], ["مميت"], "ZERO occurrences. Only the verb yumitu 'He gives death' occurs; the Name al-mumit never appears."),
 (62, "الْحَيُّ", "Al-Hayy", "The Ever-Living", "ح ي ي", ["Hay~"], "whitelist",
  [[2,255],[3,2],[20,111],[25,58],[40,65]], [],
  [{"lemma": "Hay~", "count": 19, "note": "19 other Hayy tokens are 'the living' as creatures: yukhrij al-Hayy min al-mayyit 'He brings the living from the dead' (3:27, 6:95, 10:31, 30:19), martyrs alive (2:154, 3:169), 'every living thing' (21:30), and John/Jesus 'alive' (19:15, 19:31, 19:33, 19:66)."}],
  ["حي"], "5 occurrences, all al-Hayy (al-Hayy al-qayyum in 2:255, 3:2, 20:111; 25:58; 40:65)."),
 (63, "الْقَيُّومُ", "Al-Qayyum", "The Self-Subsisting", "ق و م", ["qay~uwm"], "all", [], [],
  [], ["قيوم"], "3 occurrences (2:255, 3:2, 20:111), always with al-Hayy."),
 (64, "الْوَاجِدُ", "Al-Wajid", "The Finder", "و ج د", [], "none", [], [],
  [], ["واجد"], "ZERO occurrences. No wa'jid lemma; only the verb wajada 'he found' occurs."),
 (65, "الْمَاجِدُ", "Al-Maajid", "The Illustrious", "م ج د", [], "none", [], [],
  [], ["ماجد"], "ZERO occurrences. The lemma ma'jid never appears; only al-majid (48, a different pattern of the same root) occurs."),
 (66, "الْوَاحِدُ", "Al-Wahid", "The One", "و ح د", ["wa`Hid"], "whitelist",
  [[12,39],[13,16],[14,48],[38,65],[39,4],[40,16],[2,133],[2,163],[4,171],[5,73],[6,19],[9,31],[14,52],[16,22],[16,51],[18,110],[21,108],[22,34],[29,46],[37,4],[38,5],[41,6]], [],
  [{"lemma": "wa`Hidap", "count": 31, "note": "31 feminine waHida tokens: umma waHida 'one community', nafs waHida 'one soul', SayHa waHida 'one cry' — the numeral, not the Name."}],
  ["واحد"],
  "22 occurrences: 6 definite al-waHid (all al-waHid al-qahhar) and 16 bare waHid in 'ilah waHid / ilahan waHidan' ('one God') phrases (including 38:5, where disbelievers mock 'has he made the gods one God?' — the referent is still God as One). The other 8 bare waHid are the numeral: one food (2:61), one daughter / one sibling (4:11, 4:12), one gate (12:67), one water (13:4), one each (24:2), one destruction (25:14), one man (54:24)."),
 (67, "الْأَحَدُ", "Al-Ahad", "The Indivisible One", "أ ح د", [">aHad"], "whitelist", [[112,1]], [],
  [{"lemma": ">aHad", "count": 73, "note": "73 other aHad tokens are the indefinite pronoun 'one / anyone' (aHadukum, aHad al-nas, ma kana MuHammad aba aHad, lam yakun lahu kufuwan aHad in 112:4)."}],
  ["احد"], "1 occurrence: 112:1 qul huwa allahu aHad. The definite al-aHad never occurs."),
 (68, "الصَّمَدُ", "As-Samad", "The Eternal Refuge", "ص م د", ["S~amad"], "all", [], [],
  [], ["صمد"], "Occurs once, 112:2."),
 (69, "الْقَادِرُ", "Al-Qadir", "The Able", "ق د ر", ["qadiyr", "qaAdir"], "blacklist", [], [[10,24],[68,25]],
  [], ["قادر","قدير"],
  "Two forms of one attribute are counted together: qadir (45 tokens, overwhelmingly 'ala kulli shay'in qadir, 'powerful over all things') and qadir (14 tokens, of which 2 are human: 'they think they are able', 10:24, and the garden owners 'able to prevent the poor', 68:25). Result 57. Note the Quran's usual form is qadir; the Tirmidhi form al-qadir (definite, qadir pattern) never occurs — the definite form that does occur is al-qaadir (6:65)."),
 (70, "الْمُقْتَدِرُ", "Al-Muqtadir", "The Omnipotent", "ق د ر", ["m~uqotadir"], "all", [], [],
  [], ["مقتدر"], "4 occurrences, all divine (18:45, 43:42 plural of majesty, 54:42, 54:55)."),
 (71, "الْمُقَدِّمُ", "Al-Muqaddim", "The One who brings forward", "ق د م", [], "none", [], [],
  [], ["مقدم"], "ZERO occurrences. No muqaddim lemma; only verbs (qaddama, yastaqdimun) occur."),
 (72, "الْمُؤَخِّرُ", "Al-Mu'akhkhir", "The One who delays", "أ خ ر", [], "none", [], [],
  [], ["موخر"], "ZERO occurrences. Only the verb yu'akhkhiru 'He delays' occurs."),
 (73, "الْأَوَّلُ", "Al-Awwal", "The First", "أ و ل", [">aw~al"], "whitelist", [[57,3]], [],
  [{"lemma": ">aw~al", "count": 81, "note": "81 other awwal tokens: al-awwalun/al-awwalin 'the former peoples', al-ula 'the former (life)', awwal al-muslimin/al-mu'minin 'first of the Muslims/believers', and al-khalq al-awwal 'the first creation' (50:15)."}],
  ["اول"], "1 occurrence: 57:3 huwa al-awwal wa-l-akhir. The definite al-awwal as the Name occurs only here."),
 (74, "الْآخِرُ", "Al-Akhir", "The Last", "أ خ ر", ["A^xir"], "whitelist", [[57,3]], [],
  [{"lemma": "A^xir", "count": 154, "note": "154 other a'khir tokens are al-yawm al-akhir 'the Last Day' (and al-akhirin 'the later ones'). The related lemma A^xar (70 tokens) is al-akhira 'the Hereafter'."}],
  ["اخر"], "1 occurrence: 57:3. The raw surface count of al-akhir is 155, of which 154 are 'the Last Day'."),
 (75, "الظَّاهِرُ", "Az-Zahir", "The Manifest", "ظ ه ر", ["Za`hir"], "whitelist", [[57,3]], [],
  [{"lemma": "Za`hir", "count": 7, "note": "7 other Zahir tokens are 'outward/apparent': bi-Zahir min al-qawl 'outward speech' (13:33), Zahiran 'openly' (18:22), Zahir min al-Haya 'the outward of (worldly) life' (30:7), and the Za`haru/Zahiyr verb and noun forms."}],
  ["ظاهر"], "1 occurrence: 57:3."),
 (76, "الْبَاطِنُ", "Al-Batin", "The Hidden", "ب ط ن", ["baATin"], "whitelist", [[57,3]], [],
  [{"lemma": "baATin", "count": 2, "note": "2 other baTin tokens: Zahir/batin of sin (6:120) and baTinuhu 'its inside' (57:13). The feminine baTinatan, 'hidden (blessings)' (31:20), is the separate lemma baATinap."}],
  ["باطن"], "1 occurrence: 57:3."),
 (77, "الْوَالِي", "Al-Wali", "The Patron", "و ل ي", ["waAl"], "all", [], [],
  [], ["والي","وال"],
  "1 occurrence: 13:11 wa-ma lahum min dunihi min wal, 'they have no protector besides Him' — the defective form wal (the final ya' drops in the indefinite nominative/genitive). The definite al-wali never occurs. (QAC's lemma waAl is distinct from the preposition ila and from waliY~ the Protecting Friend, Name 55.)"),
 (78, "الْمُتَعَالِي", "Al-Muta'ali", "The Most Exalted", "ع ل و", ["mutaEaAl"], "all", [], [],
  [], ["متعالي","متعال"],
  "1 occurrence: 13:9 al-kabir al-mutaEal — the defective form al-mutaEal (final ya' dropped); the full form al-mutaEali never occurs."),
 (79, "الْبَرُّ", "Al-Barr", "The Source of Goodness", "ب ر ر", ["bar~"], "whitelist", [[52,28]], [],
  [{"lemma": "bar~", "count": 21, "note": "21 other barr tokens: al-barr 'the land' (vs the sea, 12 times), al-abrar 'the righteous' (3:193, 3:198, 76:5, 82:13, 83:18, 83:22), barra 'dutiful' of John and Jesus (19:14, 19:32), and barara 'noble scribes' (80:16). The related lemma bir~ (8 tokens) is al-birr 'piety/righteousness'."}],
  ["بر"], "1 occurrence: 52:28 innahu huwa al-barr al-raHim. (The definite al-barr is otherwise always 'the land'.)"),
 (80, "التَّوَّابُ", "At-Tawwab", "The Ever-Accepting of Repentance", "ت و ب", ["taw~aAb"], "blacklist", [], [[2,222]],
  [], ["تواب"],
  "12 lemma tokens; 1 excluded: al-tawwabin 'those who repent' (2:222, humans God loves). Result 11."),
 (81, "الْمُنْتَقِمُ", "Al-Muntaqim", "The Avenger", "ن ق م", ["muntaqimuwn"], "all", [], [],
  [], ["منتقم"],
  "3 occurrences, all in the plural muntaqimun of God speaking in the plural of majesty (32:22, 43:41, 44:16: inna muntaqimun, 'We are the Avenger'). The singular al-muntaqim never occurs."),
 (82, "الْعَفُوُّ", "Al-Afuww", "The Pardoner", "ع ف و", ["Eafuw~"], "all", [], [],
  [{"lemma": "Eafow", "count": 2, "note": "2 Eafw tokens are the noun 'pardon/forbearance': qul al-Eafw 'say: pardoning' (what to spend, 2:219) and khu* al-Eafw 'take forbearance' (7:199)."}],
  ["عفو"], "5 occurrences, all divine (4:43, 4:99, 4:149, 22:60, 58:2 — all Eafuw ghafur)."),
 (83, "الرَّؤُوفُ", "Ar-Ra'uf", "The Most Kind", "ر أ ف", ["ra'uwf"], "blacklist", [], [[9,128]],
  [], ["روف"],
  "11 lemma tokens; 1 excluded: 9:128 ra'uwf raHim of the Messenger. Result 10. (The definite ar-ra'uwf never occurs; all 10 are bare ra'uwf, usually la-ra'uwf.)"),
 (84, "مَالِكُ الْمُلْكِ", "Malik al-Mulk", "Owner of All Sovereignty", "م ل ك", ["ma`lik"], "phrase", [[3,26]], [],
  [], ["مالك الملك"],
  "1 occurrence: 3:26 qul allahumma malik al-mulk. Counted as its own Name here and also inside Name 3 (Al-Malik), where the same token is counted."),
 (85, "ذُو الْجَلَالِ وَالْإِكْرَامِ", "Dhu al-Jalal wa-l-Ikram", "Owner of Majesty and Honour", "ج ل ل + ك ر م", ["jala`l"], "phrase", [[55,27],[55,78]], [],
  [], ["ذو الجلال والاكرام","ذي الجلال والاكرام"],
  "2 occurrences: 55:27 (*u al-jalaal wa-l-ikraam, nominative) and 55:78 (*i al-jalaal wa-l-ikraam, genitive after rabbik)."),
 (86, "الْمُقْسِطُ", "Al-Muqsit", "The Equitable", "ق س ط", ["muqosiTiyn"], "blacklist", [], [[5,42],[49,9],[60,8]],
  [], ["مقسط"],
  "ZERO occurrences as the Name. The only muqsiT tokens are the plural al-muqsiTin 'the just ones' (humans God loves) in 5:42, 49:9, 60:8; the singular al-muqsiT never occurs."),
 (87, "الْجَامِعُ", "Al-Jami", "The Gatherer", "ج م ع", ["jaAmiE"], "whitelist", [[3,9],[4,140]], [],
  [{"lemma": "jaAmiE", "count": 1, "note": "1 other jamiE token: amr jamiE 'a common matter' (24:62) — not the Name."}],
  ["جامع"], "2 occurrences: 3:9 (innaka jamiE an-nas) and 4:140 (inna allaha jamiE al-munafiqin)."),
 (88, "الْغَنِيُّ", "Al-Ghani", "The Self-Sufficient", "غ ن ي", ["ganiY~"], "blacklist", [],
  [[2,273],[3,181],[4,6],[4,135],[9,93],[59,7]],
  [], ["غني"],
  "24 lemma tokens; 6 excluded, all rich humans: aghniya' 'the rich' (2:273, 3:181, 9:93, 59:7) and ghaniyyan 'rich' of a guardian or a person (4:6, 4:135). Result 18."),
 (89, "الْمُغْنِي", "Al-Mughni", "The Enricher", "غ ن ي", [], "none", [], [],
  [], ["مغني"], "ZERO occurrences. Only the verb yughni 'He enriches' occurs; the Name al-mughni never appears."),
 (90, "الْمَانِعُ", "Al-Mani", "The Preventer", "م ن ع", [], "none", [], [],
  [], ["مانع"], "ZERO occurrences. No maniE lemma; only the verb manaEa 'he prevented' occurs."),
 (91, "الضَّارُّ", "Ad-Darr", "The Bringer of Adversity", "ض ر ر", ["DaA^r~"], "blacklist", [], [[2,102],[58,10]],
  [], ["ضار"],
  "ZERO occurrences as the Name. The 2 Da'rr tokens are 'harming': bi-Darrin bihi 'they cannot harm anyone with it' (2:102, sorcerers) and bi-Darrihim 'harming them' (58:10, Satan's whispering). The noun Darr 'harm' (10 tokens) is a different lemma."),
 (92, "النَّافِعُ", "An-Nafi", "The Bringer of Benefit", "ن ف ع", [], "none", [], [],
  [], ["نافع"], "ZERO occurrences. No nafiE lemma; only the verb nafaEa 'it benefited' occurs."),
 (93, "النُّورُ", "An-Nur", "The Light", "ن و ر", ["nuwr"], "whitelist", [[24,35,2]], [],
  [{"lemma": "nuwr", "count": 42, "note": "42 other nur tokens: light as guidance/revelation (5:15, 5:44, 14:1, 64:8), 'the light of Allah' (9:32, 61:8), believers' light on the Day (57:12, 57:13, 66:8), the moon as a light (10:5, 71:16), and the other four nur tokens in 24:35 itself (w6, w33, w35, w38 — 'His light', 'light upon light')."}],
  ["نور"],
  "1 occurrence: 24:35 allahu nur as-samawati wa-l-arD, 'Allah is the Light of the heavens and the earth' (word 2 of the verse). Every other nur is a created light, guidance, or the light OF God, not God Himself."),
 (94, "الْهَادِي", "Al-Hadi", "The Guide", "ه د ي", ["haAd", "haAdiy"], "whitelist", [[22,54],[25,31]], [],
  [{"lemma": "haAd", "count": 6, "note": "6 other had tokens are generic 'a guide / no guide': wa-likulli qawmin had 'for every people a guide' (13:7), fa-ma lahu min had 'he has no guide' (13:33, 39:23, 39:36, 40:33), and bi-hadi al-Eumy 'guide of the blind', of the Prophet (30:53)."},
   {"lemma": "haAdiy", "count": 1, "note": "1 other hadi token: fa-la hadiya lahu 'no guide for him' (7:186)."}],
  ["هادي","هاد"],
  "2 occurrences: 22:54 (wa-inna allaha la-had alladhina amanu) and 25:31 (wa-kafa bi-rabbika hadiyyan wa-naSira). The definite al-hadi never occurs; both counted forms are the defective/bare participle."),
 (95, "الْبَدِيعُ", "Al-Badi", "The Incomparable Originator", "ب د ع", ["badiyE"], "all", [], [],
  [], ["بديع"], "2 occurrences: 2:117 and 6:101 (badiE as-samawati wa-l-arD, 'Originator of the heavens and the earth')."),
 (96, "الْبَاقِي", "Al-Baqi", "The Everlasting", "ب ق ي", ["baAq", "baAqiyap", "baqiy~at", "baAqiyn"], "blacklist", [],
  [[2,248],[11,86],[11,116],[16,96],[26,120],[37,77],[43,28],[69,8]],
  [], ["باقي","باق"],
  "ZERO occurrences as the Name. The 8 baq- tokens are all 'remaining': baqiyyat 'a remnant' (2:248, 11:86, 11:116), wa-ma Einda allahi baq 'what is with Allah remains' (16:96 — endurance predicated of what is with Allah, not of Allah), al-baqin 'the remaining ones' (26:120, 37:77), kalima baqiya 'an enduring word' (43:28), baqiya 'any survivor' (69:8)."),
 (97, "الْوَارِثُ", "Al-Warith", "The Inheritor", "و ر ث", ["waAriv"], "whitelist", [[15,23],[21,89],[28,58]], [],
  [{"lemma": "waAriv", "count": 4, "note": "4 other wari* tokens are human inheritors: al-wari*un 'they are the inheritors' of Paradise, the believers (23:10), wa-najEaluhum al-wari*in 'We make them the inheritors', the oppressed Israelites (28:5), and the heirs in the inheritance laws (2:233, 26:85)."}],
  ["وارث"],
  "3 occurrences, all in the plural: wa-naHnu al-wari*un (15:23, 28:58) and khayr al-wari*in (21:89). The singular al-wari* never occurs."),
 (98, "الرَّشِيدُ", "Ar-Rashid", "The Guide to the Right Path", "ر ش د", ["r~a$iyd", "r~a`$iduwn"], "blacklist", [],
  [[11,78],[11,87],[11,97],[49,7]],
  [], ["رشيد"],
  "ZERO occurrences as the Name. rashiyd tokens: rajul rashiyd 'a right-minded man' (11:78), al-Halim ar-rashiyd mocked of ShuEayb (11:87), bi-rashiyd 'not rightly guided', Pharaoh's command (11:97), and ar-rashidun 'the rightly-guided' believers (49:7)."),
 (99, "الصَّبُورُ", "As-Sabur", "The Most Patient", "ص ب ر", [], "none", [], [],
  [{"lemma": "Sab~aAr", "count": 4, "note": "Sabbar 'most patient' (4 tokens, e.g. likulli Sabbar shakur) is a different word — the patient human, not the Name."}],
  ["صبور"], "ZERO occurrences. The Name aS-Sabur never appears in the Quran."),
]
# fmt: on

EXPECTED = {1: 57, 2: 115, 3: 7, 4: 2, 5: 1, 6: 1, 7: 1, 8: 91, 9: 1, 10: 1,
            11: 11, 12: 3, 13: 1, 14: 5, 15: 6, 16: 3, 17: 1, 18: 1, 19: 157,
            20: 0, 21: 0, 22: 0, 23: 1, 24: 0, 25: 0, 26: 45, 27: 42, 28: 1,
            29: 0, 30: 7, 31: 45, 32: 11, 33: 6, 34: 91, 35: 4, 36: 8, 37: 6,
            38: 6, 39: 1, 40: 3, 41: 0, 42: 2, 43: 3, 44: 2, 45: 9, 46: 92,
            47: 2, 48: 2, 49: 0, 50: 20, 51: 9, 52: 15, 53: 9, 54: 1, 55: 33,
            56: 17, 57: 0, 58: 0, 59: 0, 60: 2, 61: 0, 62: 5, 63: 3, 64: 0,
            65: 0, 66: 22, 67: 1, 68: 1, 69: 57, 70: 4, 71: 0, 72: 0, 73: 1,
            74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 11, 81: 3, 82: 5,
            83: 10, 84: 1, 85: 2, 86: 0, 87: 2, 88: 18, 89: 0, 90: 0, 91: 0,
            92: 0, 93: 1, 94: 2, 95: 2, 96: 0, 97: 3, 98: 0, 99: 0}

# ---------------------------------------------------------------------------
# Counting
# ---------------------------------------------------------------------------
def ref_matches(ref, s, v, w):
    if len(ref) == 2:
        return ref[0] == s and ref[1] == v
    return ref[0] == s and ref[1] == v and ref[2] == w


def count_name(defn, words_by_lemma):
    """Return (occurrences, counted_by_lemma, excluded_refs_seen).
    occurrences: list of (surah, ayah, word, lemma) counted."""
    (nid, arabic, tr, meaning, root, lemmas, rule, include, exclude,
     related, stems, notes) = defn
    occ = []
    counted_by_lemma = Counter()
    for lemma in lemmas:
        for w in words_by_lemma.get(lemma, []):
            s, v, wd = w["surah"], w["ayah"], w["word"]
            if rule == "none":
                continue
            if rule == "whitelist" or rule == "phrase":
                if not any(ref_matches(r, s, v, wd) for r in include):
                    continue
            elif rule == "blacklist":
                if any(ref_matches(r, s, v, wd) for r in exclude):
                    continue
            # rule "all" and "phrase" (phrase names use a whitelist) fall through
            occ.append((s, v, wd, lemma))
            counted_by_lemma[lemma] += 1
    occ.sort()
    return occ, counted_by_lemma


def display_arabic(verses, s, v, w, stems):
    """Return the exact Uthmani token for a counted QAC word, plus a
    warning string or None. The surah-initial basmalah adds 4 Tanzil
    tokens before the first verse's words (except surahs 1 and 9); the
    four merged-word verses are handled by the stem-search fallback."""
    toks = tanzil_word_tokens(verses, s, v)
    # Phrase Names (84, 85): find the phrase as consecutive tokens.
    for st in stems:
        if " " in st:
            words = st.split()
            normed = [norm_ar(t).replace("\u0651", "")
                      .replace("\u0649", "\u064a") for t in toks]
            for i in range(len(normed) - len(words) + 1):
                if normed[i:i + len(words)] == words:
                    return " ".join(toks[i:i + len(words)]), None
            return None, (f"{s}:{v} w{w}: phrase {st!r} not found in "
                          f"Tanzil verse")
    idx = w - 1
    if 0 <= idx < len(toks) and stems and (set(stems) & stem_candidates(toks[idx])):
        return toks[idx], None
    # Fallback: tokens in this verse whose stem matches, in order.
    matches = [t for t in toks if stems and (set(stems) & stem_candidates(t))]
    if matches:
        # If the direct index hit, prefer it even if the stem test failed
        # (e.g. a suffixed form the stem table does not cover).
        if 0 <= idx < len(toks):
            return toks[idx], (
                f"{s}:{v} w{w}: token {toks[idx]!r} did not stem-match "
                f"{stems}; used it anyway (fallback)")
        return matches[0], None
    return None, f"{s}:{v} w{w}: no Tanzil token matched stems {stems}"


def tanzil_raw_count(verses, stems, _cache={}):
    """Raw (un-disambiguated) count of tokens whose stem matches, over
    the whole Tanzil text including basmalahs. This over-counts homonyms
    (e.g. Eali 'high' vs the preposition EalaY, aHad 'anyone', Haqq
    'truth') and is a cross-check only, never the reported count."""
    if "token_cands" not in _cache:
        _cache["token_cands"] = Counter()
        for toks in verses.values():
            for t in toks:
                _cache["token_cands"][frozenset(stem_candidates(t))] += 1
    stems = set(stems)
    # Phrase Names (stems containing a space) are counted by substring
    # on the normalised verse text, not by single tokens.
    if any(" " in st for st in stems):
        if "verse_text" not in _cache:
            _cache["verse_text"] = []
            for toks in verses.values():
                _cache["verse_text"].append(
                    norm_ar(" ".join(toks)).replace("\u0651", "")
                    .replace("\u0649", "\u064a"))
        return sum(txt.count(st) for txt in _cache["verse_text"] for st in stems)
    return sum(n for cands, n in _cache["token_cands"].items()
               if stems & cands)


def main():
    for path, want in ((QAC_PATH, QAC_SHA256), (TANZIL_PATH, TANZIL_SHA256)):
        if not path.exists():
            sys.exit(f"missing corpus file: {path}")
        got = sha256(path)
        if got != want:
            sys.exit(f"SHA-256 mismatch for {path}: {got} != {want}")
    words, n_seg = load_qac(QAC_PATH)
    verses = load_tanzil(TANZIL_PATH)
    assert len(words) == 77429, len(words)
    assert n_seg == 128219, n_seg
    assert len(verses) == 6236, len(verses)
    words_by_lemma = defaultdict(list)
    for w in words:
        if w["lemma"]:
            words_by_lemma[w["lemma"]].append(w)
    lemma_totals = {L: len(v) for L, v in words_by_lemma.items()}

    warnings = []
    names_out = []
    verse_occ = defaultdict(set)   # (s,v) -> set of name ids
    surah_occ = defaultdict(set)   # s -> set of name ids
    total_counted = 0

    for defn in NAMES:
        (nid, arabic, tr, meaning, root, lemmas, rule, include, exclude,
         related, stems, notes) = defn
        occ, counted_by_lemma = count_name(defn, words_by_lemma)
        # Assert the computed count equals the verified expected count.
        exp = EXPECTED[nid]
        if len(occ) != exp:
            sys.exit(
                f"Name {nid} {tr}: computed {len(occ)} != expected {exp}; "
                f"occurrences: {occ}")
        # Verify every related-form count against the corpus lemma total:
        # total tokens of that lemma == counted-from-it + related count.
        related_out = []
        for rel in related:
            total = lemma_totals.get(rel["lemma"], 0)
            counted_here = counted_by_lemma.get(rel["lemma"], 0)
            if total != counted_here + rel["count"]:
                sys.exit(
                    f"Name {nid} {tr}: related lemma {rel['lemma']} total "
                    f"{total} != counted {counted_here} + related "
                    f"{rel['count']}")
            related_out.append({
                "lemma": rel["lemma"],
                "count": rel["count"],
                "note": rel["note"],
            })
        # Phrase vs standalone: an occurrence is 'phrase' when another
        # counted Name occurs in the same verse within word distance <= 2.
        by_verse = defaultdict(list)
        for (s, v, w, lemma) in occ:
            by_verse[(s, v)].append(w)
            verse_occ[(s, v)].add(nid)
            surah_occ[s].add(nid)
        # distance uses the full occurrence map (all names), built after
        # the loop below; here we record per-occurrence verse/word only.
        # Phrase classification is computed in the second pass.
        total_counted += len(occ)
        # Display Arabic from the first counted occurrence's Tanzil token.
        disp = arabic
        if occ:
            s0, v0, w0, _ = occ[0]
            tok, warn = display_arabic(verses, s0, v0, w0, stems)
            if tok:
                disp = tok
            if warn:
                warnings.append(f"Name {nid} {tr}: {warn}")
        # Basmalah occurrences (only Rahman/Rahim have them in QAC).
        basmalah = 0
        if nid in (1, 2):
            basmalah = sum(1 for (s, v, w, _l) in occ
                           if (s, v) in ((1, 1), (27, 30)))
        example_refs = [{"surah": s, "ayah": v} for (s, v, _w, _l) in occ[:5]]
        names_out.append({
            "id": nid,
            "arabic": disp,
            "transliteration": tr,
            "meaning_en": meaning,
            "root": root,
            "count": len(occ),
            "standalone_count": None,  # filled in second pass
            "phrase_count": None,
            "qac_lemmas": lemmas,
            "lemma_counts": dict(sorted(counted_by_lemma.items())),
            "counting_rule": rule,
            "notes": notes,
            "related_forms": related_out,
            "excluded_refs": [{"surah": r[0], "ayah": r[1],
                               **({"word": r[2]} if len(r) == 3 else {})}
                              for r in exclude],
            "tanzil_raw_count": tanzil_raw_count(verses, stems),
            "basmalah_count": basmalah,
            "verse_count": len(by_verse),
            "surah_count": len({s for (s, _v) in by_verse}),
            "example_refs": example_refs,
            "_occ": occ,
        })

    # Second pass: phrase/standalone classification. Two counted Names in
    # the same verse within word distance <= 2 form a phrase pair.
    occ_words = {}  # (s,v) -> list of (word, name_id)
    for n in names_out:
        for (s, v, w, _l) in n["_occ"]:
            occ_words.setdefault((s, v), []).append((w, n["id"]))
    for n in names_out:
        stand = phr = 0
        for (s, v, w, _l) in n["_occ"]:
            others = [(w2, i2) for (w2, i2) in occ_words[(s, v)]
                      if i2 != n["id"] and abs(w2 - w) <= 2]
            if others:
                phr += 1
            else:
                stand += 1
        n["standalone_count"] = stand
        n["phrase_count"] = phr
        del n["_occ"]

    # Co-occurrence graph.
    verse_edges = Counter()
    verse_edge_refs = defaultdict(list)
    for (s, v), ids in sorted(verse_occ.items()):
        for a, b in combinations(sorted(ids), 2):
            verse_edges[(a, b)] += 1
            if len(verse_edge_refs[(a, b)]) < 3:
                verse_edge_refs[(a, b)].append({"surah": s, "ayah": v})
    surah_edges = Counter()
    for s, ids in sorted(surah_occ.items()):
        for a, b in combinations(sorted(ids), 2):
            surah_edges[(a, b)] += 1

    name_by_id = {n["id"]: n for n in names_out}
    nodes = [{"id": n["id"], "transliteration": n["transliteration"],
              "arabic": n["arabic"], "count": n["count"]}
             for n in names_out]
    ranked = sorted(verse_edges.items(), key=lambda kv: (-kv[1], kv[0]))
    keep = set(kv[0] for kv in ranked[:150]) | {k for k, c in verse_edges.items() if c >= 2}
    verse_edge_list = [{
        "a": a, "b": b, "weight": c,
        "example_refs": verse_edge_refs[(a, b)],
    } for (a, b), c in ranked if (a, b) in keep]
    surah_edge_list = [{
        "a": a, "b": b, "weight": c,
    } for (a, b), c in sorted(surah_edges.items(), key=lambda kv: (-kv[1], kv[0]))]

    zero = [n["id"] for n in names_out if n["count"] == 0]
    methodology = {
        "corpus": {
            "primary": "Quranic Arabic Corpus, morphology version 0.4, "
                       "Copyright (C) 2011 Kais Dukes, GNU GPL. "
                       "File corpus/quranic-corpus-morphology-0.4.txt, "
                       "SHA-256 " + QAC_SHA256 + ", 6,309,503 bytes, "
                       "128,276 lines, 128,219 data lines = 77,429 words, "
                       "6,236 verses, 114 surahs.",
            "provenance": "corpus.quran.com's official download page "
                          "serves v0.4 only behind an email form and "
                          "publishes no direct file URL; the Java API "
                          "(JQuranTree) is a Java library, not a REST API. "
                          "The file was fetched from the "
                          "textminingthequran.com mirror of the identical "
                          "v0.4 file and verified against the corpus's own "
                          "published figures (128,276 lines; 77,429 words; "
                          "header copyright block verbatim). It was NOT "
                          "downloaded directly from corpus.quran.com.",
            "display_and_cross_check": "Tanzil Quran Text, Uthmani script, "
                          "corpus/quran-uthmani.txt, SHA-256 "
                          + TANZIL_SHA256 + ", 1,334,737 bytes, 6,236 "
                          "verses, 77,881 whitespace tokens. Used only for "
                          "display Arabic (copied byte-for-byte) and for a "
                          "raw stem cross-check (tanzil_raw_count).",
            "download_date": "2026-11-06",
        },
        "name_list_source": "Standard 99-name Tirmidhi enumeration "
            "(Jami' at-Tirmidhi 3507), as tabulated at "
            "openarabic.org/99-names-of-allah/ and cross-checked against "
            "asmaulhusna.com and getlivingquran.com. Caveat: the hadith "
            "affirms 99 Names, but the enumeration itself is a weaker "
            "narration; some compilations count Allah itself as first. "
            "Two duplicate-transliteration pairs exist in the list: "
            "48 Al-Majid (al-majiyd) vs 65 Al-Majid (al-maajid, rendered "
            "'Al-Maajid' here), and 55 Al-Waliyy (al-waliyy) vs 77 "
            "Al-Wali (al-waalii, defective form wal).",
        "counting_rules": [
            "Primary count = QAC segments whose LEM: is the Name's lemma "
            "and whose referent is God. A word counts only when it is "
            "predicated of God (or in apposition to Allah / huwa / rabb), "
            "NOT when the same lemma describes a human, angel, prophet, "
            "the Book/Quran, the Throne, provisions, rewards, places, or "
            "abstract nouns (justice, truth as a concept, sovereignty, "
            "light as guidance).",
            "Where a lemma is ambiguous, the script uses an explicit "
            "whitelist or blacklist of verse references (see each Name's "
            "notes and excluded_refs), decided by reading every occurrence "
            "of that lemma in context.",
            "Plural forms sharing the Name's lemma are counted when "
            "divine (e.g. al-khaliqun 56:59, al-warithun 15:23, "
            "muntaqimun 32:22/43:41/44:16, al-mujibun 37:75, al-qadirun "
            "77:23) and excluded when human (e.g. al-tawwabin 2:222, "
            "al-muqsiTin 5:42/49:9/60:8).",
            "Related-form lemmas (a different lemma of the same attribute, "
            "e.g. Ealim al-ghayb for Al-Alim, ghafir a*-*anb for Al-Ghafur, "
            "arHam ar-raHimin, khayr ar-raziqin, allahu >akobar) are "
            "reported separately as related_forms and are NOT in the "
            "primary count — except where the Name never occurs in its "
            "exact lemma and only a variant/plural form is attested "
            "(qadir, muHyi, had, mutaEal, wal, muntaqimun plural, "
            "wari*un plural), where the counted variant LEM: is listed "
            "explicitly in qac_lemmas.",
            "QAC counts exclude the 113 surah-initial basmalahs (they are "
            "not numbered verses except 1:1). The basmalah at 1:1 and the "
            "inline basmalah at 27:30 ARE in QAC; basmalah_count records "
            "how many of a Name's occurrences are basmalahs (Rahman 2, "
            "Rahim 2). Tanzil text has 112 further basmalahs, so the "
            "Tanzil totals are Rahman 57+112=169 and Rahim 115+112=227.",
            "Phrase vs standalone: an occurrence is 'phrase' when another "
            "counted Name occurs in the same verse within word distance "
            "<= 2 (covers ar-Rahman ar-Rahim, Eaziz Hakim, ghafur raHim, "
            "samiE Ealim, and the 59:22-24 sequence); otherwise "
            "'standalone'.",
            "Display Arabic: the exact Uthmani token from the Tanzil "
            "corpus at the same surah:verse, copied byte-for-byte, never "
            "retyped. For Names with count 0, the conventional vowelled "
            "form from the name-list source is used.",
            "Tanzil cross-check (tanzil_raw_count): raw count of tokens "
            "whose normalised stem matches the Name, over the whole "
            "Tanzil text including basmalahs. It is deliberately "
            "un-disambiguated — it over-counts homonyms (Eali 'high' vs "
            "the preposition EalaY, aHad 'anyone', Haqq 'truth') and "
            "under/over-counts where the Name's form is defective or "
            "plural. It is a sanity check only; the QAC count is the "
            "reported count.",
        ],
        "ayah_table_correction": "The brief's ayah-count table listed "
            "surahs 5 and 6 as 165, 120; the correct order is 120 "
            "(Al-Ma'idah) then 165 (Al-An'am). The sum is 6236 either "
            "way, but the order matters for verse references; the table "
            "in this script is corrected.",
        "qac_vs_tanzil": "QAC has 77,429 segmented words; Tanzil has "
            "77,881 whitespace tokens. Difference 452 = 448 (112 "
            "surah-initial basmalahs x 4 words, present in Tanzil but not "
            "numbered in QAC) + 4 verses where QAC merges two Tanzil "
            "tokens into one word: 2:181, 8:6, 13:37, 37:130. Only 4 of "
            "6,236 verses differ in word count.",
        "script": "data/names_script.py — run with `python3 "
                  "names_script.py` from the data/ directory. It "
                  "re-parses both corpora, re-counts, and asserts every "
                  "Name's count equals the verified expected count and "
                  "every related-form count reconciles with the corpus "
                  "lemma total; it exits non-zero on any mismatch.",
    }
    totals = {
        "names_with_count_gt_0": 99 - len(zero),
        "zero_occurrence_count": len(zero),
        "total_occurrences": total_counted,
        "total_unique_word_occurrences": total_counted - 1,
        "double_counted_note": "Name 84 (Malik al-Mulk, 3:26) counts the "
            "same word that Name 3 (Al-Malik) counts, so the sum of the 99 "
            "counts (1120) exceeds the number of distinct Quranic words "
            "bearing a Name (1119) by 1. Name 85's two jala`l tokens are "
            "not counted under any other Name (Al-Jalil is 0).",
        "distinct_verses_with_at_least_one_name": len(verse_occ),
        "distinct_surahs_with_at_least_one_name": len(surah_occ),
        "verse_edges_total": len(verse_edges),
        "verse_edges_kept": len(verse_edge_list),
        "verse_edges_cutoff": "Top 150 edges by weight, plus all edges "
                              "with weight >= 2.",
        "surah_edges_total": len(surah_edges),
    }
    names_json = {
        "methodology": methodology,
        "names": names_out,
        "totals": totals,
        "zero_occurrence": zero,
    }
    edges_json = {
        "nodes": nodes,
        "verse_edges": verse_edge_list,
        "surah_edges": surah_edge_list,
        "edge_cutoff_note": "verse_edges: top 150 edges by weight, plus "
                            "all edges with weight >= 2 ("
                            f"{len(verse_edge_list)} of "
                            f"{len(verse_edges)} total edges kept). "
                            "surah_edges: all pairs, weaker link (same "
                            "surah).",
    }
    (HERE / "names.json").write_text(
        json.dumps(names_json, ensure_ascii=False, indent=2), encoding="utf-8")
    (HERE / "name_edges.json").write_text(
        json.dumps(edges_json, ensure_ascii=False, indent=2), encoding="utf-8")

    top = sorted(names_out, key=lambda n: -n["count"])[:5]
    print(f"QAC words: {len(words)}  segments: {n_seg}  verses: {len(verses)}")
    print(f"Total counted occurrences: {total_counted}")
    print("Top 5:", [(n["transliteration"], n["count"]) for n in top])
    print(f"Zero-occurrence Names ({len(zero)}): "
          f"{[name_by_id[i]['transliteration'] for i in zero]}")
    print(f"Verse edges: {len(verse_edges)} total, {len(verse_edge_list)} kept; "
          f"surah edges: {len(surah_edges)}")
    print("Strongest verse pairs:")
    for (a, b), c in ranked[:10]:
        print(f"  {name_by_id[a]['transliteration']} + "
              f"{name_by_id[b]['transliteration']}: {c}")
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print("  " + w)


if __name__ == "__main__":
    main()

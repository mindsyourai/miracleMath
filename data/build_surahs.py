#!/usr/bin/env python3
"""
build_surahs.py -- miracleMath (Agent A: surah list)

Builds data/surahs.json from the 114-surah list MK pasted (Turkish
transliteration name, verse count, Mekki/Medeni, Arabic name as he gave
it). The paste below is verbatim -- nothing in it was hand-corrected,
including the Arabic spellings (e.g. surah 14 "ابراهيم" and surah 76
"الانسان" carry no hamza on the alif, as pasted; surah 40 is listed
under its Turkish name "Mü'min" with Arabic "غافر").

Output: one object per surah --
  {"n": 1, "name_tr": "Fâtiha", "name_ar": "الفاتحة",
   "verses": 7, "type": "Meccan"|"Medinan", "recite": "https://quran.com/1"}

The verse counts are taken from the paste and then verified by
data/surahs_check.py against QAC v0.4 and the Tanzil Uthmani text --
this script does NOT verify; it only parses.

Usage: python3 data/build_surahs.py [--out PATH]
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE / "surahs.json"

# MK's pasted list, verbatim (header: Sureler 114, Cüzler 30, Sayfalar 604).
PASTE = """1 Fâtiha 7 Mekkî الفاتحة
2 Bakara 286 Medenî البقرة
3 Âl-i İmrân 200 Medenî آل عمران
4 Nisâ 176 Medenî النساء
5 Mâide 120 Medenî المائدة
6 En'âm 165 Mekkî الأنعام
7 A'râf 206 Mekkî الأعراف
8 Enfâl 75 Medenî الأنفال
9 Tevbe 129 Medenî التوبة
10 Yûnus 109 Mekkî يونس
11 Hûd 123 Mekkî هود
12 Yûsuf 111 Mekkî يوسف
13 Ra'd 43 Medenî الرعد
14 İbrâhîm 52 Mekkî ابراهيم
15 Hicr 99 Mekkî الحجر
16 Nahl 128 Mekkî النحل
17 İsrâ 111 Mekkî الإسراء
18 Kehf 110 Mekkî الكهف
19 Meryem 98 Mekkî مريم
20 Tâhâ 135 Mekkî طه
21 Enbiyâ 112 Mekkî الأنبياء
22 Hac 78 Medenî الحج
23 Mü'minûn 118 Mekkî المؤمنون
24 Nûr 64 Medenî النور
25 Furkân 77 Mekkî الفرقان
26 Şuarâ 227 Mekkî الشعراء
27 Neml 93 Mekkî النمل
28 Kasas 88 Mekkî القصص
29 Ankebût 69 Mekkî العنكبوت
30 Rûm 60 Mekkî الروم
31 Lokmân 34 Mekkî لقمان
32 Secde 30 Mekkî السجدة
33 Ahzâb 73 Medenî الأحزاب
34 Sebe' 54 Mekkî سبإ
35 Fâtır 45 Mekkî فاطر
36 Yâsîn 83 Mekkî يس
37 Sâffât 182 Mekkî الصافات
38 Sâd 88 Mekkî ص
39 Zümer 75 Mekkî الزمر
40 Mü'min 85 Mekkî غافر
41 Fussilet 54 Mekkî فصلت
42 Şûrâ 53 Mekkî الشورى
43 Zuhruf 89 Mekkî الزخرف
44 Duhân 59 Mekkî الدخان
45 Câsiye 37 Mekkî الجاثية
46 Ahkâf 35 Mekkî الأحقاف
47 Muhammed 38 Medenî محمد
48 Fetih 29 Medenî الفتح
49 Hucurât 18 Medenî الحجرات
50 Kâf 45 Mekkî ق
51 Zâriyât 60 Mekkî الذاريات
52 Tûr 49 Mekkî الطور
53 Necm 62 Mekkî النجم
54 Kamer 55 Mekkî القمر
55 Rahmân 78 Medenî الرحمن
56 Vâkıa 96 Mekkî الواقعة
57 Hadîd 29 Medenî الحديد
58 Mücâdele 22 Medenî المجادلة
59 Haşr 24 Medenî الحشر
60 Mümtehine 13 Medenî الممتحنة
61 Saf 14 Medenî الصف
62 Cuma 11 Medenî الجمعة
63 Münâfikûn 11 Medenî المنافقون
64 Tegâbün 18 Medenî التغابن
65 Talâk 12 Medenî الطلاق
66 Tahrîm 12 Medenî التحريم
67 Mülk 30 Mekkî الملك
68 Kalem 52 Mekkî القلم
69 Hâkka 52 Mekkî الحاقة
70 Meâric 44 Mekkî المعارج
71 Nûh 28 Mekkî نوح
72 Cin 28 Mekkî الجن
73 Müzzemmil 20 Mekkî المزمل
74 Müddessir 56 Mekkî المدثر
75 Kıyâmet 40 Mekkî القيامة
76 İnsân 31 Medenî الانسان
77 Mürselât 50 Mekkî المرسلات
78 Nebe 40 Mekkî النبإ
79 Naziât 46 Mekkî النازعات
80 Abese 42 Mekkî عبس
81 Tekvîr 29 Mekkî التكوير
82 İnfitâr 19 Mekkî الإنفطار
83 Mutaffifîn 36 Mekkî المطففين
84 İnşikâk 25 Mekkî الإنشقاق
85 Burûc 22 Mekkî البروج
86 Târık 17 Mekkî الطارق
87 A'lâ 19 Mekkî الأعلى
88 Gâşiye 26 Mekkî الغاشية
89 Fecr 30 Mekkî الفجر
90 Beled 20 Mekkî البلد
91 Şems 15 Mekkî الشمس
92 Leyl 21 Mekkî الليل
93 Duhâ 11 Mekkî الضحى
94 İnşirâh 8 Mekkî الشرح
95 Tîn 8 Mekkî التين
96 Alak 19 Mekkî العلق
97 Kadir 5 Mekkî القدر
98 Beyyine 8 Medenî البينة
99 Zilzâl 8 Medenî الزلزلة
100 Âdiyât 11 Mekkî العاديات
101 Kâria 11 Mekkî القارعة
102 Tekâsür 8 Mekkî التكاثر
103 Asr 3 Mekkî العصر
104 Hümeze 9 Mekkî الهمزة
105 Fîl 5 Mekkî الفيل
106 Kureyş 4 Mekkî قريش
107 Maûn 7 Mekkî الماعون
108 Kevser 3 Mekkî الكوثر
109 Kâfirûn 6 Mekkî الكافرون
110 Nasr 3 Medenî النصر
111 Tebbet 5 Mekkî المسد
112 İhlâs 4 Mekkî الإخلاص
113 Felak 5 Mekkî الفلق
114 Nâs 6 Mekkî الناس"""

LINE_RE = re.compile(r"^(\d+)\s+(.+?)\s+(\d+)\s+(Mekkî|Medenî)\s+(.+)$")
TYPE = {"Mekkî": "Meccan", "Medenî": "Medinan"}


def parse_paste(text):
    surahs = []
    for raw in text.strip().splitlines():
        m = LINE_RE.match(raw.strip())
        assert m, f"unparsable paste line: {raw!r}"
        n, name_tr, verses, typ, name_ar = m.groups()
        surahs.append({
            "n": int(n),
            "name_tr": name_tr,
            "name_ar": name_ar,
            "verses": int(verses),
            "type": TYPE[typ],
            "recite": f"https://quran.com/{int(n)}",
        })
    return surahs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    surahs = parse_paste(PASTE)
    assert len(surahs) == 114, f"expected 114 surahs, got {len(surahs)}"
    assert [s["n"] for s in surahs] == list(range(1, 115)), \
        "surah numbers are not 1..114 in order"
    total = sum(s["verses"] for s in surahs)
    mecc = sum(1 for s in surahs if s["type"] == "Meccan")
    medi = sum(1 for s in surahs if s["type"] == "Medinan")

    out = Path(args.out)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"surahs": surahs}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {out}: {len(surahs)} surahs, "
          f"total verses (paste) = {total}, "
          f"Meccan {mecc} / Medinan {medi}")
    print("NOTE: verse counts are from MK's paste only -- run "
          "data/surahs_check.py to verify them against the corpus.")


if __name__ == "__main__":
    main()

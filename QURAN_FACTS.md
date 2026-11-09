# About the Quran — facts and corpus numbers

Research-redesign input (Agent A). Machine-readable versions:
`data/quran_facts.json` (facts) and `data/corpus_numbers.json`
(numbers). Scripts: `data/letter_count.py`, `data/corpus_numbers_check.py`
— run either with `python3` to reproduce every script-computed figure
below. Nothing was pushed; this is working-copy only.

## 1. Facts about the Quran

Every fact carries a proper Islamic source. Where traditions differ on a
count, the standard figure is given and the variant is noted in the same
line — no contested count is presented as the only number.

| Fact | Value | Source |
|---|---|---|
| Surahs | 114 | Al-Suyuti, *al-Itqan fi Ulum al-Quran*; Shaykh Anas al-Musa, SeekersGuidance. Minority view counts al-Anfal and al-Bara'ah (8–9) as one surah, giving 113. |
| Verses (ayahs) | 6,236 | Kufi count, used in the standard Madinan mushaf (al-Suyuti, *al-Itqan*, quoting Abu Amr al-Dani); verified by script on QAC v0.4 and the Tanzil text. Variants: Basri 6,204, Madani 6,214 / 6,217, Shami 6,226 — same text, different verse divisions. |
| Meccan / Medinan surahs | 86 Meccan / 28 Medinan | Standard classification by time of revelation relative to the Hijra (IslamWeb fatwa 343273, citing al-Suyuti, *al-Itqan*). Classical reports differ — al-Suyuti reports 83 / 31 and 85 / 29 variants — so the split is approximate, not exact. |
| Revelation period | 23 years | Sahih al-Bukhari 3902 (Ibn Abbas): revelation began at age 40, 13 years in Mecca, 10 as an emigrant in Medina, died at 63. Another report (Bukhari 4979) counts 10 + 10, reconciled by scholars as excluding the pause in revelation (*fatrat al-wahy*). |
| First revelation | Quran 96:1–5 | Sahih al-Bukhari 3 (Aisha): the angel's "Read in the name of your Lord who created…" in the cave of Hira. A minority view names al-Muddaththir (74:1–5) as first (noted by Ibn Hajar, *Fath al-Bari*). |
| Night revelation began | Laylat al-Qadr, in Ramadan | Quran 97:1 ("We sent it down during the Night of Decree") and 2:185 (Ramadan is the month "in which was revealed the Quran"); Tafsir Ibn Kathir on 97:1: sent down to the lowest heaven on that night, then in parts over 23 years. |
| Juz / Hizb | 30 juz / 60 hizb | Later scholarly division for recitation, traced to the era of al-Hajjaj ibn Yusuf (Ibn Taymiyyah, *Majmu al-Fatawa* 13/409–410), not part of the revelation itself; each juz = 2 hizb. |
| Longest surah | Al-Baqarah (2), 286 verses | Tanzil Uthmani text, script count; standard Kufi verse table. |
| Shortest surah | Al-Kawthar (108), 3 verses | Tanzil Uthmani text, script count. Tied with Al-Asr (103) and An-Nasr (110), also 3 verses each. |
| Surahs opening with the Basmalah | 113 | Tanzil Uthmani text, script count: every surah except At-Tawbah (9). Total Basmalah occurrences 114, including the one inside verse 27:30. |
| Pages (standard Madinah mushaf) | 604 | King Fahd Complex, Mushaf al-Madinah: 604 pages at 15 lines per page, ~20 pages per juz. Tanzil's quran-data.xml metadata records the same 604 Medina Mushaf page boundaries. This is the printed edition's page count, not a property of the text — other prints differ (a 16-line print is ~548 pages). |

No fact was dropped: all ten target facts were sourced properly. No
popular-apologetics source (no Yahya, no miracle-websites) was used for
any of them. The 604-pages fact (eleventh) was added 2026-11-09, sourced
to the King Fahd Complex print and Tanzil's metadata.

## 2. Corpus numbers (all by script)

From `corpus/quranic-corpus-morphology-0.4.txt` (QAC v0.4) and
`corpus/quran-uthmani.txt` (Tanzil Uthmani). **Every number reproduced
exactly** — none had to be corrected.

| Number | Value | How counted |
|---|---|---|
| Surahs | 114 | Distinct surah numbers in QAC; 6,236 Tanzil verse lines across 114 surahs |
| Verses | 6,236 | Distinct (surah, verse) locations in QAC; equals the Tanzil lines and the Kufi table |
| Words (QAC v0.4) | 77,429 | One QAC word = one (surah, verse, word) location; multi-segment words count once |
| Segments (QAC v0.4) | 128,219 | One QAC data line = one segment |
| Unique surface forms | 18,994 | Distinct whitespace-separated tokens in the Tanzil text as printed (diacritics kept), incl. the 112 unnumbered basmalahs; excl. basmalahs 18,993 |
| Unique stems (QAC v0.4) | 12,113 | Distinct FORM values on STEM segments (Buckwalter) |
| Unique roots (QAC v0.4) | 1,642 | Distinct ROOT: values |
| Unique lemmas (QAC v0.4) | 4,832 | Distinct LEM: values |
| Tanzil whitespace tokens | 77,881 incl. basmalahs / 77,433 excl. | 452 more than QAC words incl. basmalahs (448 basmalah words + 4 segmentation differences); 4 more excl. |
| Basmalah | 19 letters; 114 occurrences | 113 surah openings + 27:30 |

## 3. Letter count — rule, headline, and the 323,671 comparison

**Rule (project convention A4, `data/letter_count.py`):** count base
letters only (U+0621–U+064A, one each). Diacritics / tashkil do not
count — vowel marks, shaddah, sukun, maddah, tatweel and Quranic
annotation marks are stripped, so a doubled (shaddah) letter counts
once, not twice. Hamza forms count as letters: standalone hamza (ء)
counts once, and hamza on a carrier (أ إ آ ؤ ئ) counts as the carrier
letter, once. Alef wasla (ٱ) counts as a letter. Dagger alif (ٰ),
small waw (ۥ) and small yeh (ۦ) are marks, not letters, and are dropped.

**Basmalah treatment:** the Tanzil file prepends the Basmalah to the
first verse line of every surah except 9; only 1:1 is a numbered verse.
Reported both ways:

- **Headline: 325,386 letters — unnumbered basmalahs excluded.** This is
  the figure to lead with: it matches the QAC word-count convention,
  which likewise excludes the 112 unnumbered basmalahs (QAC contains
  only 1:1 as words), and it is the convention the project's earlier
  letter findings (A4) and the RDS-Q count use.
- 327,514 letters — basmalahs as printed included (+2,128 = 112 × 19).

**Comparison with 323,671:** the widely quoted classical total,
reported from Ibn Abbas via al-Suyuti, *al-Itqan fi Ulum al-Quran*
(1/231). It reproduces under **no** rule tried on this text: our count
is 1,715 higher excluding the basmalahs and 3,843 higher including
them. Variants tested (excl. basmalahs): dagger alif / small letters
counted as letters → 337,326; alef wasla not counted → 311,903;
standalone hamza not counted → 322,604; shaddah doubled → 348,064.
None lands on 323,671. The classical authorities disagree among
themselves by far more than the gap (Basra reciters 323,015; Mujahid
321,000; Ibn Mas'ud 300,670; Salam Abu Muhammad 340,740 — SeekersGuidance,
Shaykh Anas al-Musa, citing al-Suyuti / al-Zarkashi), and their counts
were hand counts on early manuscripts with a different rasm (omitted
alifs, hamzat al-wasl treatment) and no stated reproducible rule. The
stated classical explanation — a doubled letter counted as two — does
not reproduce it either: doubling shaddah gives 348,064, far above
every classical figure. So 323,671 is cited as a classical report, not
as the script count. (Nearby modern figure for context: RDS-Q No. 4
gives 325,666 letters on the same Tanzil text, basmalahs excluded —
280 above ours; the cause of that gap is unidentified, as recorded in
the project's earlier reconciliation work.)

## 4. Reproduce

```sh
python3 data/letter_count.py          # headline 325,386 / 327,514 + variants
python3 data/corpus_numbers_check.py  # all corpus numbers; writes data/corpus_numbers.json
```

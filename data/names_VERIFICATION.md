# Names of God (Asma al-Husna) — Verification Note

## Script
`data/names_script.py` — run with `python3 names_script.py` from the
`data/` directory. It re-parses both corpora from disk, re-counts all 99
Names, and **asserts every Name's count equals the verified expected
count and every related-form count reconciles with the corpus lemma
total**; it exits non-zero on any mismatch. It also verifies both corpora
by SHA-256 before counting. Outputs: `names.json`, `name_edges.json`.

## Corpora
- **Primary: Quranic Arabic Corpus (QAC), morphology v0.4** —
  `corpus/quranic-corpus-morphology-0.4.txt`, SHA-256
  `a1d12923…75d8c46`, 77,429 words / 6,236 verses / 114 surahs.
  Provenance: corpus.quran.com serves v0.4 only behind an email form
  and publishes no direct file URL; the Java API is a Java library, not
  a REST API. The file was fetched from the textminingthequran.com
  mirror of the identical v0.4 file and verified against the corpus's
  own published figures (128,276 lines; 77,429 words; header copyright
  block verbatim). It was **not** downloaded directly from
  corpus.quran.com.
- **Display / cross-check: Tanzil Uthmani** —
  `corpus/quran-uthmani.txt`, SHA-256 `ac072479…0c667af`, 6,236 verses,
  77,881 whitespace tokens. Display Arabic is copied byte-for-byte
  from it; it is never the counting source.
- **Name list:** the standard 99-name Tirmidhi enumeration
  (Jami' at-Tirmidhi 3507), as tabulated at
  openarabic.org/99-names-of-allah/ and cross-checked against
  asmaulhusna.com and getlivingquran.com. Caveat: the hadith affirms 99
  Names, but the enumeration itself is a weaker narration; some
  compilations count Allah itself as first.

## Headline numbers
- **Total counted occurrences: 1,120** across 99 Names (1,119 distinct
  Quranic words — the word at 3:26 is counted twice, as both Al-Malik
  and Malik al-Mulk).
- **75 Names occur; 24 do not** (see below). Names occur in **727
  verses** and **83 surahs**.
- **Top 5 by count:** Al-Alim 157 · Ar-Rahim 115 · Al-Hakim 92 ·
  Al-Aziz 91 · Al-Ghafur 91.
- **Strongest co-occurring pairs (same verse):** Ar-Rahim + Al-Ghafur
  72 verses · Al-Aziz + Al-Hakim 47 · Al-Alim + Al-Hakim 36 · Al-Alim +
  As-Sami 32 · Ar-Rahim + Al-Aziz 13. 135 verse edges total, all kept
  (fewer than the 150-edge cap; 37 have weight ≥ 2). 1,056 surah edges.
- **Mostly phrase-bound Names:** Ar-Rahim (110 of 115 in phrases,
  overwhelmingly *ghafur raHim*), Al-Ghafur (88 of 91), Al-Aziz (84 of
  91, overwhelmingly *Eaziz Hakim*), Al-Hakim (most with Al-Aziz or
  Al-Alim). **Mostly standalone:** Ash-Shahid (20 of 20), Al-Waliyy
  (32 of 33), Ar-Rahman (51 of 57).

## Zero-occurrence Names (24)
Al-Qabid (20), Al-Basit (21), Al-Khafid (22), Al-Mu'izz (24),
Al-Mudhill (25), Al-Adl (29), Al-Jalil (41), Al-Ba'ith (49),
Al-Muhsi (57), Al-Mubdi (58), Al-Mu'id (59), Al-Mumit (61),
Al-Wajid (64), Al-Maajid (65), Al-Muqaddim (71), Al-Mu'akhkhir (72),
Al-Muqsit (86), Al-Mughni (89), Al-Mani (90), Ad-Darr (91),
An-Nafi (92), Al-Baqi (96), Ar-Rashid (98), As-Sabur (99).
In most cases the Quran has the verb the Name is drawn from
(*tuEizzu* 3:26, *yuEidu*, *yumitu*, *yu'akhkhiru*, *yughni*) but
never the Name as a noun. Notable near-misses, all excluded by the
predication rule (the word describes something/someone else):
Al-Basit's 4 tokens are Abel, angels, a simile and a dog; Al-Muqsit's
only tokens are just humans (5:42, 49:9, 60:8); Al-Baqi's tokens are
'remaining' things, never God; Al-Mubdi's only token (33:37) is from a
different root (*b-d-w*, 'disclose'), not *b-d-'*.

## Counts that disagree with commonly quoted figures
- **Ar-Rahim 115, not 114** — 114 is the number of basmalahs; the
  Quran has 115 non-basmalah occurrences of the Name (116 lemma tokens
  minus 9:128, where *ra'uwf raHim* describes the Messenger).
- **Al-Aziz 91, not 92** — the popular 92 counts 41:41 (*kitab Eaziz*,
  'a mighty Book'), which predicates the adjective of the Book.
- **Al-Muhaymin 1, not 2** — the popular 2 counts 5:48 (*muhayminan*),
  which describes the revealed Book, not God.
- **Al-Hakam 1, not 0** — the Name occurs once, 6:114 ('shall I seek
  a judge other than Allah?'). The familiar 'the judgment belongs to
  Allah' verses (6:57, 12:40, 12:67) use a different lemma (*Hukom*,
  'judgment'), and 4:35's two *Hakam* tokens are human arbitrators.
- **Ar-Rahman 57** (QAC, excluding surah-initial basmalahs) matches
  the famous 57; the full Tanzil text has 169 (57 + 112 basmalahs).
- **Al-Alim 157** matches the commonly quoted 157.
- **Al-Awwal / Al-Akhir / Az-Zahir / Al-Batin: 1 each** (57:3 only).
  The raw surface counts (e.g. *al-akhir* 155) are almost all *al-yawm
  al-akhir*, 'the Last Day'.
- **Al-Haqq 9, not ~247** — the raw surface count of *al-Haqq* is
  247, but 238 are 'the truth' as a concept; only 9 predicate Truth
  of God.
- **Al-Qadir 57** = 45 *qadir* + 12 *qadir* (the Quran's usual form
  is *qadir*; the Tirmidhi form *al-qadir* never occurs in the
  definite — the definite form that does occur is *al-qaadir*, 6:65).
- **An-Nur 1** — 24:35 *allahu nur* only; the other 42 *nur* tokens
  are light as guidance, 'the light of Allah', or believers' light.

## Counting rules (summary; full text in `names.json` methodology)
Primary count = QAC segments whose `LEM:` is the Name's lemma **and**
whose referent is God. A word counts only when predicated of God (or
in apposition to Allah / *huwa* / *rabb*), not when the same lemma
describes a human, angel, prophet, the Book/Quran, the Throne,
provisions, rewards, places, or abstract nouns. Ambiguous lemmas use
an explicit whitelist/blacklist of verse references, decided by
reading every occurrence in context. Plural forms sharing the Name's
lemma count when divine (e.g. *al-khaliqun* 56:59, *muntaqimun*
32:22/43:41/44:16) and not when human. Related-form lemmas (a
different lemma of the same attribute, e.g. *Ealim al-ghayb*,
*ghafir a*-*anb*, *arHam ar-raHimin*, *allahu >akobar*) are reported
separately as `related_forms` and are **not** in the primary count,
except where the Name never occurs in its exact lemma and only a
variant/plural form is attested (*qadir*, *muHyi*, *had*,
*mutaEal*, *wal*, *muntaqimun*, *wari*un*). Phrase vs standalone: an
occurrence is 'phrase' when another counted Name occurs in the same
verse within word distance ≤ 2.

## QAC vs Tanzil reconciliation
QAC 77,429 segmented words vs Tanzil 77,881 whitespace tokens.
Difference **452 = 448 + 4**: 448 = 112 surah-initial basmalahs × 4
words (Tanzil prepends them; QAC has the basmalah only as 1:1 and
inline at 27:30), plus 4 verses where QAC merges two Tanzil tokens
into one word: 2:181, 8:6, 13:37, 37:130. Only 4 of 6,236 verses
differ in word count. The Tanzil raw stem cross-check
(`tanzil_raw_count`) is deliberately un-disambiguated — it over-counts
homonyms (e.g. Al-Aliyy's raw count is 1,467 because the preposition
*EalaY* 'upon' folds to the same stem, and Al-Haqq's raw count
includes 'the truth' as a concept) and under-counts where the Name's
form is defective or plural (Al-Alim raw 161 vs QAC 163: the two
plural *ulama'* tokens, 26:197 and 35:28, do not match the stem
*Ealiym*). It is a sanity check only; the QAC count is the reported
count.

## Ayah-table correction
The brief's ayah-count table listed surahs 5 and 6 as 165, 120; the
correct order is **120 (Al-Ma'idah) then 165 (Al-An'am)**. The sum is
6236 either way, but the order matters for verse references; the
script's table is corrected.

## How to re-run
```
cd ~/workspace/projects/miracle-math/data
python3 names_script.py
```
Expected output: `Total counted occurrences: 1120`, top 5 as above,
24 zero-occurrence Names, strongest pair Ar-Rahim + Al-Ghafur: 72,
and no warnings. Any count mismatch aborts with a non-zero exit and
names the Name, the computed count, and the expected count.

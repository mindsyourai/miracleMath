# Surah list — verification note (Agent A, 2026-11-09)

Source: the 114-surah list MK pasted (Turkish transliteration name,
verse count, Mekkî/Medenî, Arabic name). Machine-readable:
`data/surahs.json` (one object per surah: `n`, `name_tr`, `name_ar`,
`verses`, `type` "Meccan"|"Medinan", `recite` `https://quran.com/<n>`).
Built by `data/build_surahs.py`, which embeds the paste verbatim and
parses it — no hand-typed counts. Turkish transliteration and Arabic
kept exactly as pasted, including the Arabic spellings without hamza
on the alif in surah 14 (ابراهيم) and surah 76 (الانسان), and surah 40
listed under its Turkish name "Mü'min" with Arabic "غافر".

## Verification — 0 diffs

`data/surahs_check.py` checks every pasted verse count three ways and
exits non-zero on any mismatch (a pasted count is never silently
"fixed"):

1. **QAC v0.4** — max (surah, verse) per surah, parsed from the
   location field of `corpus/quranic-corpus-morphology-0.4.txt`.
2. **Standard Kufi ayah-count table** — `AYAH_COUNTS` in
   `data/letter_count.py` (itself asserted equal to the QAC maxima in
   `data/corpus_numbers_check.py`).
3. **Tanzil Uthmani text** — 6,236 non-comment lines, re-segmented
   per surah from the surah boundaries in the file itself: every
   surah except 9 opens with the Basmalah prepended to its first
   verse, so the 113 lines starting with the Basmalah mark the surah
   starts. Surahs 8 and 9 share one segment (9 has no Basmalah), so
   their split is checked as a combined 204 verses (75 + 129).

Result (2026-11-09): **diff count 0 — all 114 pasted counts match
all three sources. Total verses 6,236. Meccan / Medinan split 86 /
28**, counted from the pasted list.

Two details the check turned up (both in the script, not worked
around):

- Surahs **95 and 97** write the opening Basmalah with a shaddah on
  the ba (بِّسْمِ) where the other 111 write بِسْمِ — same words,
  Uthmani spelling variant. A naive `startswith("بِسْمِ")` finds only
  111 surah starts; the script matches both forms.
- Verse **27:30** contains the Basmalah mid-verse (it does not start
  a surah), and **11:41** contains بِسْمِ mid-verse as well
  ("بِسْمِ ٱللَّهِ مَجْر۪ىٰهَا"); neither is counted as a surah
  start.

## Classification — source and variants

The Meccan/Medinan split follows the **standard Turkish / Diyanet
classification**, as in the list MK pasted (86 Meccan / 28 Medinan).
It is a classification by time of revelation relative to the Hijra,
and it is approximate, not exact: the project's facts file already
notes classical reports differ (al-Suyuti reports 83 / 31 and 85 /
29 variants — see `data/quran_facts.json`, `meccan_medinan`).

One example, stated honestly rather than smoothed over: **surah 99,
Az-Zalzalah, is classed Medinan in this list, but Meccan in some
traditions** (and the same kind of disagreement exists for a handful
of other surahs, e.g. 22, 55, 76 in some listings). No classification
was changed from the paste.

## Recite links — sample check

Each surah links to `https://quran.com/<n>` (label "Recite"). Sample
checked 2026-11-09 by HTTP request (7 URLs spread across the range):
**1, 2, 36, 55, 67, 112, 114 — all HTTP 200.** All 114 were not
fetched, to avoid hammering quran.com; the pattern is uniform
(`quran.com/<n>`) and the page builds the link from the surah number.

## Reproduce

```sh
python3 data/build_surahs.py   # paste -> data/surahs.json
python3 data/surahs_check.py   # 0 diffs, total 6,236, split 86/28
```

# More than 99 Names — verification note (Agent A, 2026-11-09)

Machine-readable: `data/more_names.json`. Script:
`data/more_names_check.py` (run it to reproduce everything below).
The existing 99 cards, graph and "24 never occur" data in
`data/names.json` are unchanged — this only adds.

## The point

Allah has **more than 99** names. The ninety-nine are the names whose
memorisation the hadith promises Paradise for — not a count of all
His names. No total number of additional names is claimed here: the
note states "more than 99" with the verified examples below and
leaves it there.

## The hadith — verified

> "Allah has ninety-nine Names, one-hundred less one; and he who
> memorized them all by heart will enter Paradise." — Abu Huraira

- **Sahih al-Bukhari 7392** (Book 97, Hadith 21) — verified against
  sunnah.com, https://sunnah.com/bukhari/97/21
- **Sahih Muslim 2677a** (Book 48, Hadith 5) and **2677b** (Book 48,
  Hadith 6) — verified against sunnah.com,
  https://sunnah.com/muslim/48/5

Important, and easy to get wrong: **neither narration lists the
names.** The familiar enumerated list of 99 comes from a narration in
Jami' at-Tirmidhi 3507; the Bukhari/Muslim narrations give the number
and the reward, not the list.

## Verified additional names (3)

Each was found by skeleton search over all 6,236 verses of the
Tanzil Uthmani text (diacritics stripped, alef variants and dagger
alef normalised to plain alef), cross-checked in QAC v0.4 (the verse
exists and carries the phrase's roots), and checked against
`data/names.json` to confirm it is **not** already one of the 99.
Arabic is the phrase exactly as printed in the Tanzil text.

| Name | Arabic (as printed) | Verses | Note |
|---|---|---|---|
| Khayrul-Makirin — the Best of Planners | خَيْرُ ٱلْمَٰكِرِينَ | 3:54, 8:30 | Occurs nowhere else in the Quran. |
| Ahsanul-Khaliqin — the Best of Creators | أَحْسَنُ ٱلْخَٰلِقِينَ | 23:14, 37:125 | Occurs nowhere else. Distinct from card #11 Al-Khaliq (the single word); the full superlative phrase is not among the 99. |
| Rabbul-Arshil-Azim — Lord of the Mighty Throne | رَبُّ ٱلْعَرْشِ ٱلْعَظِيمِ | 9:129, 23:86, 27:26 | The brief listed only 9:129 and 27:26; the script found a **third occurrence at 23:86**, included here. Distinct from card #33 Al-Azim (the single word). |

## Checked but NOT additional (1)

**Dhul-Jalali wal-Ikram** (ذُو ٱلْجَلَٰلِ وَٱلْإِكْرَامِ) does occur —
55:27 (nominative ذُو) and 55:78 (genitive ذِي, written ذِى with alef
maksura in the Uthmani text) — but it is **already card #85 of the
99** ("Dhu al-Jalal wa-l-Ikram", count 2). It is recorded in
`more_names.json` under `checked_but_already_in_99` so the check is
auditable, and it is **not** listed as an extra name. Nothing was
dropped for failing to occur: all four candidates occur in the Quran.

## Method note (one trap, for the record)

A first skeleton search found **none** of the four phrases, because
the dagger alef (U+0670) in words like الجلال / الماكرين / الخالقين
was stripped as a diacritic — deleting a letter and turning الجلال
into الجلل. In the Uthmani spelling the dagger alef stands in for a
written alef, so for skeleton matching it normalises *to* alef. (The
project's letter-count rule in `data/letter_count.py` still treats
it as a mark, not a letter — that is a different question, counting
letters, not matching words.)

## Reproduce

```sh
python3 data/more_names_check.py   # writes data/more_names.json; exits non-zero if a QAC root cross-check fails
```

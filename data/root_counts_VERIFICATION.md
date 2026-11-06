# root_counts — verification note (miracleMath, Agent 1)

## What this is

Machine-readable pair counts for the Quran, computed from the **Quranic
Arabic Corpus (QAC), morphology v0.4**, matched by `ROOT:` and cross-checked
by `LEM:`. Display Arabic comes byte-for-byte from the Tanzil Uthmani text
at the same surah:verse. Full method lives in the `methodology` field of
`root_counts.json`; this note is the short human-readable check.

## Files

- `root_counts.json` — the data (13 pairs + 10 extras, refs, methodology).
- `root_counts_script.py` — the counting script. Re-run it with:
  `python3 root_counts_script.py` (from this directory; `--qac`, `--tanzil`,
  `--out` flags available). It regenerates `root_counts.json` and prints a
  summary plus a `DIAGNOSTICS` section. No network, no extra packages.
- `root_counts_VERIFICATION.md` — this file.

## Headline numbers (QAC words)

| Pair | a | b | Ratio a:b |
|---|---|---|---|
| Heaven / Hell (jannah / jahannam) | 147 | 77 | 1.91 |
| Heaven / Hell-fire (jannah / nar) | 147 | 145 | 1.01 |
| This world / Hereafter (dunya / akhira) | 115 | 115 | 1.00 |
| Life / Death (hayat / mawt, nouns) | 76 | 50 | 1.52 |
| Angels / Devils (mala'ikah / shayatin) | 88 | 88 | 1.00 |
| Belief / Disbelief (iman / kufr families) | 812 | 507 | 1.60 |
| Reward / Punishment (ajr / adhab families) | 105 | 373 | 0.28 |
| Day / Night (yawm / layl) | 475 | 92 | 5.16 |
| Sun / Moon (shams / qamar) | 33 | 27 | 1.22 |
| Man / Woman (rajul / imra'ah + nisa') | 57 | 85 | 0.67 |
| Love / Hate (hubb / kurh, hate-sense) | 83 | 27 | 3.07 |
| Rich / Poor (ghani / faqir, adjectives) | 24 | 14 | 1.71 |
| Good / Evil (khayr / sharr) | 188 | 30 | 6.27 |

Sanity anchor: **Allah = 2699** (LEM `{ll~ah`), the standard figure,
reproduced exactly. `Allahumma` 5 and generic `ilah` 147 are separate.
Totals: QAC 77,429 words / 128,219 segments / 6,236 verses / 114 surahs;
Tanzil 77,881 whitespace tokens (see reconciliation below).

## What was checked

1. **Corpus identity.** QAC SHA-256
   `a1d12923…d8c46`, 6,309,503 bytes, 128,276 lines, 128,219 data lines,
   77,429 words — all match the corpus's published figures. Tanzil SHA-256
   `ac072479…667af`, 1,334,737 bytes.
2. **Verse mapping.** The ayah-count table sums to 6236 (verified in-script,
   assertion). **Correction:** the table supplied with the task had Surahs 5
   and 6 transposed (165, 120). Standard counts are 5:120, 6:165, confirmed
   against QAC itself (max verse per surah). The sum is 6236 either way, so
   the swap only showed up in the verse-alignment audit (phantom 5:121–165
   and shifted Surah 6 references). Fixed in the script; noted here.
3. **Refs.** All 108 example references were re-checked independently
   against the Tanzil file: each Arabic token occurs in its verse line and
   each verse quote is byte-identical. 108/108 pass, 0 unaligned words.
4. **Basmalah count.** The brief said 111 lines start with the basmalah.
   Actually 113 lines do (1:1 + 112 prepended): Surahs 95 and 97 spell it
   with a doubled ba (`بِّسْمِ`), which a plain `startswith("بِسْمِ")`
   misses. QAC contains only the 1:1 basmalah as words, so QAC counts
   exclude 112 basmalahs — this is exactly the Allah gap (2699 + 112 = 2811
   Tanzil-surface Allah tokens, verified by direct count).
5. **Tanzil vs QAC totals.** 77,881 − 77,429 = 452 = **448** (112 basmalahs ×
   4 words) + **4** segmentation differences, found verse by verse: QAC
   writes `بعدما` as one word where Tanzil has two tokens (`بعد ما`) in
   2:181, 8:6, 13:37, and writes `إل ياسين` as one word where Tanzil has two
   (`إل ياسين`) in 37:130. Only 4 verses in the whole Quran differ.
6. **QAC annotation quirks recorded in the data:** `shaytan` has ROOT `$Tn`
   (not `$yT`); `adhab` has ROOT `E*b` (`*` = dhal in QAC Buckwalter);
   `yawma'idhin` ("on that day", 70 words) has its own LEM and **no ROOT**,
   so it is matched by LEM and listed separately; `jahannam` (proper noun)
   has no ROOT and is matched by LEM.

## Counts that disagree with commonly quoted figures

- **Day = 475, not 365.** The widely quoted "yawm 365 times" does not
  reproduce under any clean rule on this text: singular `yawm` alone is 378
  (incl. `al-yawm` "today"), + `yawma'idhin` = 448, + plural `ayyam` = 475.
  Night = 92 (not a round number either).
- **Life / death = 76 : 50 (nouns), not 145 : 145.** The famous 145 : 145
  does not reproduce under any clean QAC rule: whole-root counts are
  Hyy 184 : mwt 165; broad sense families as defined in the JSON are
  169 : 165. The 145 figure appears to come from a different counting
  convention (or edition) that could not be reconstructed here.
- **Angels = 88, not 73.** A plain surface count of `ملائكة` gives 73, but
  QAC shows 15 more singular `malak` words meaning "angel" (incl. dual
  `al-malakayn`, 2:102, and collective singulars 69:17, 89:22). The 73 is
  the plural only.
- **Confirmed exactly:** jannah 147, jahannam 77, dunya : akhira 115 : 115,
  Allah 2699, iman (noun `إيمان` alone) 45, nar 145, shaytan 88.
- **Akhira, fine print:** 115 `al-akhira` forms include one that means
  "latter", not "the Hereafter" (29:20, "the latter creation"), so the
  strict hereafter-sense count is 114. The pair is reported as 115 : 115
  with this flagged in the JSON.

## Known limits

- Sense splits rely on QAC v0.4's `LEM:` assignments (e.g. `iman` vs
  `ayman` "oaths", `malak` angel vs `malik` king, `habb` love vs grain).
  Where a single lemma still mixes senses, the script splits by verse and
  the split is documented (hate: `karhan` "unwillingly" ×5 and `kurhan`
  "in hardship" ×2 excluded, but `kurh` at 2:216 "fighting is hateful to
  you" included; life: greeting/shyness/snake senses excluded).
- Counts are QAC-word counts. They exclude the 112 prepended basmalahs
  (QAC does not contain them as words); a Tanzil-surface count of the same
  concepts would be higher exactly where a concept word occurs in a
  basmalah (only Allah, +112).
- No English translation was used as a counting source.

# Methods + locations check — Checker A (paired_counts 30 + letter_counts 7)

**Scope:** all 37 findings in `data/scholar_findings.json` that are `paired_counts` (30) or
`letter_counts` (7). Script: `data/methods_check_A.py` (re-run it to regenerate
`data/scholar_findings_enriched_A.json`). Corpus: QAC morphology v0.4 (77,429 words) +
Tanzil Uthmani (6,236 verses). All counts and all verse references are script-computed
from that corpus — nothing hand-typed. Nothing was pushed; the main JSON was not edited.

## Method coverage (37)

- **stated — 10:** the source itself states a method. day-365 (Yahya: singular form only;
  plural+dual = 30), sun-moon-33-27 (Yahya, for light: "only the simple forms"),
  iman-kufr-25 (Yahya: "(without genitive)"), qaf-57-57, nun-132-vs-133, sad-153-vs-152
  (Khalifa, submission.org), muqattaat-structure-29-14-78 (Sayoud 2013),
  all-28-letters-verses, longest-word-fasqaynakumuhu, seven-heavens-7.
- **reconstructed — 20:** no method stated, but a specific selection rule reproduces the
  claimed numbers exactly, and the rule is spelled out in `verification_scholar_rule.note`.
  dunya-akhira-115, jannah-jahannam-77, shaytan-angels-88, month-12, salawat-5,
  man-woman-24-24, muhammad-4, zakah-blessing-32, say-they-said-332, plant-tree-26,
  reward-forgiveness-117-234, guidance-mercy-79, tongue-sermon-25, benefit-corrupt-50,
  refuge-forever-28, disaster-thanks-75, trouble-peace-13, treachery-foul-16,
  righteous-wicked-6-3, human-being-65.
- **unstated — 7:** no method stated and no reproducing rule found. sea-land-32-13,
  life-death-145, wine-intoxication-6, mind-light-49, love-obedience-83,
  summer-winter-5, harun-yahya-populariser (not a count).

The most useful pattern found: several of Yahya's pairs reproduce under **bare
(unsuffixed) noun forms** — iman/kufr 25/25 and guidance/mercy 79/79. His "(without
genitive)" for iman is the same idea (no possessive/genitive suffix).

## Corrections proposed (13)

Status flips — differs → confirmed (10):
- **iman-kufr-25** — bare إيمان = 25, bare كفر = 25 (QAC). "(without genitive)" =
  without the possessive suffix. Case-reading (exclude GEN) gives 21/20 and fails.
- **zakah-blessing-32** — LEM zakaw`p = 32; ROOT brk = 32. Substrings (زك 67, برك 5)
  were the wrong test (alif in بارك/تبارك; purify verbs).
- **say-they-said-332** — singular imperative قل = 332 (293+18+21); قالوا = 332.
  The 333rd surface token is قَلَّ "it became little" (4:7, LEM qal~a, ROOT qll),
  not a "say".
- **plant-tree-26** — ROOT nbt = 26; ROOT $jr = 27 minus the dispute verb شَجَرَ
  (4:65) = 26.
- **reward-forgiveness-117-234** — ROOT jzy = 118 minus jizya tax (9:29) = 117;
  ROOT gfr = 234.
- **guidance-mercy-79** — bare nouns hudFY = 79 (85−6 suffixed) and raHomap = 79
  (114−35 suffixed). Same bare-form rule as iman/kufr.
- **tongue-sermon-25** — ROOT lsn = 25 (incl. plurals ألسنة); ROOT wEZ = 25
  (وعظ verbs 15 + موعظة 9 + واعظين 1). "Sermon" mistranslates موعظة (admonition).
- **refuge-forever-28** — LEM maSiyr = 28; LEM >abadFA = 28. The earlier "29" was a
  substring false positive: عابدات "devout [women]" (66:5) contains ابدا in its
  skeleton but is not أبدا.
- **disaster-thanks-75** — ROOT Swb disaster-sense = 75 (excl. صيّب rainstorm 2:19,
  صواب "right" 78:38); ROOT $kr = 75.
- **treachery-foul-16** — ROOT xwn = 16; ROOT xbv = 16.

Status flips — confirmed → differs (1):
- **jannah-jahannam-77** — 12 of the 77 exact surface forms are not "garden":
  جِنَّة (jinn/madness, 10 tokens: 7:184, 11:119, 23:25, 23:70, 32:13, 34:8,
  34:46, 37:158 ×2, 114:6) and جُنَّة (shield, 2: 58:16, 63:2). Sense-correct
  garden counts are 65 (unsuffixed surface singular), 70 (QAC lemma singular),
  147 (all gardens) — none is 77. Hell is 77 under both rules.

Status flips — cannot_verify → differs (1):
- **sea-land-32-13** — sea: definite singular البحر/والبحر = 32 (LEM baHor = 41 total).
  Land: land-sense البرّ = 12, not 13 (the other 10 LEM bar~ tokens are
  piety/righteousness: الأبرار ×6, برًّا dutiful ×2, البرّ the Benign 52:28,
  بررة 80:16). Also بحيرة 5:103 is a camel, not sea.

Note-only correction (1):
- **human-being-65** (status stays confirmed) — the creation-stage table DOES
  reproduce: soil 17 + drop 12 + clot 6 + lump 3 + bone 15 + flesh 12 = 65.
  (The 6 extra <insa`n tokens are أناس/أناسيّ "people", not الإنس.)

**If the coordinator accepts all 12 status flips**, overall tallies move from
28 confirmed / 25 differ / 11 cannot_verify to **37 confirmed / 17 differ /
10 cannot_verify** (64 total). The main JSON was not changed — these live only in
each finding's `correction` field.

Explicitly NOT proposed: **benefit-corrupt-50** (ROOT nfE 50 / fsd 50 — numbers
reported, status flip parked per MK's unapproved PASTED_PAGE_CHECK.md proposal);
**mind-light-49** (ROOT Eql 49; light is 43 by lemma, 49 only if the adjective
منير "shining" counts as "light" — the prior team rejected that reading; needs a
coordinator/MK call).

## Locations coverage

- **36 of 37** findings have script-computed verse lists (deduplicated surah:verse
  under the ROOT rule) plus per-surah occurrence counts. Totals: **3,680 root-rule
  verse references, 1,538 scholar-rule verse references** (13 findings include a
  `verses_scholar_rule` list where the scholar rule differs and is reconstructable).
- **1 N/A:** harun-yahya-populariser — not a word count ("locations: not applicable").
- Consistency check: per-surah occurrence sums equal the root-rule count totals for
  all 35 count findings. Two structural exceptions: muqattaat (count [29, 14, 75] is
  a summary triple — 29 surahs, 14 letters, 75 verse-1 letters; per-surah = 75)
  and longest-word (count 11 is a letter length; locations list the 4 longest words:
  3:17, 4:75, 4:127, 15:22).
- Notable script catches: the 42:22 garden token is plural (stem jan~aAti, not
  jan~a`ti — singular is 70, plural 69, dual 8); the man duals رَّجُلَيْنِ carry the
  stem prefix r~ (stem r~ajulayoni) — dual detection now matches on "ajulay";
  الشتاء is spelled الشتآء in Uthmani (raw search for شتاء finds nothing);
  7:69 reads بصطة (Sad), not بسطة — confirmed in the text.

## Still unverified / open

- **man-woman-24-24:** Yahya's own page gives 23/23 and no principled one-token
  exclusion produces 23 from the 24 singulars; the 24/24 comes from the
  Al-Suwaidan/Elias list, whose Scribd source could not be fetched (Scribd blocks
  text fetch). The 24/24 itself is verified from the corpus, not from the source.
- **life-death-145:** no rule gives 145/145 (nouns 76/50; whole roots 184/165).
  Stays differs.
- **summer-winter-5:** no rule gives 5/5 (summer/winter by root 1/1, both in 106:2;
  heat/cold 15/5). Stays differs.
- **love-obedience-83:** love-sense 83 vs obedience-sense 87 (ROOT TwE 129 minus
  استطاع "to be able" 42). Stays differs.
- **wine-intoxication-6:** wine 6 vs intoxication 7 (all 7 are intoxication-sense).
  Stays differs.
- **mind-light-49:** borderline (see above) — 49/49 requires منير as "light".
- **benefit-corrupt-50:** numbers reproduce (50/50) but the flip is parked, awaiting
  MK's approval.

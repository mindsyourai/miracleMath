# Methods — how each scholar's count was understood, verified, and located

Date: 2026-11-08 (methods + locations pass). Companion to `RECONCILIATION.md`
(2026-11-07, which fixed statuses and confidence labels) and `PASTED_PAGE_CHECK.md`
(2026-11-07, whose 11 proposed findings and the benefit–corrupt-50 flip remain
**unapproved and are NOT applied here**). The İşârâtü'l-İ'câz strand is still
parked by MK's decision and is not covered here.

## 2026-11-09 — Yahya re-attribution (MK's decision)

Harun Yahya is no longer used as a source anywhere on the site. The 21
confirmed counts formerly sourced to his list were independently re-counted
from the corpus (20 reproduce exactly; righteous/wicked 6/3 holds only under
the surface-form rule — the lemma rule gives 6/4) and are now presented as
the site's own script-verified counts ("Counted by this site, QAC v0.4").
The 7 counts from that list our recount could not confirm stay on the
unverified page, re-attributed to the circulating popular list. The
literature-fact finding about Yahya himself was dropped. Tallies are now
**37 confirmed / 17 differ / 9 cannot verify** (63 findings: 35 Scholar
Findings / 21 Counted by this site / 7 Popular claims). The sections below
that describe the 2026-11-07 and 2026-11-08 passes are left as written;
only the live coverage numbers in this section were updated.

## The two rules every finding was tested under

Each finding carries two scripted verifications in `data/scholar_findings.json`
(`verification_scholar_rule` and `verification_root_rule`):

1. **The scholar's own rule** — what the scholar themself counts, as stated in
   their own source (units: root, lemma, surface form; prefixes/clitics in or
   out; basmalah in or out; singular/plural/dual handling). Where the source
   states no method, the field says "method not stated by the source" and the
   method status is `unstated`. Where the method can only be inferred from the
   numbers, it is labelled `reconstructed` and the test that reproduces the
   number is shown. **No method was invented for any scholar.**
2. **Our standard QAC root rule** — the recount rule used throughout this site:
   count by Quranic Arabic Corpus v0.4 **root** (ROOT field), all forms, all
   prefixes/suffixes, basmalah excluded except the two numbered basmalahs
   (1:1, 27:30). Where a claim is about a lemma or a surface form rather than a
   root, the root-rule verification says so and gives the lemma/form number
   instead. Where the two rules agree, the verification says so in one line;
   where they differ, it names the tokens that are in under one rule and out
   under the other, with verse examples.

## Method coverage (63 findings)

| Method status | Count | Meaning |
|---|---|---|
| `stated` | 19 | The source states its counting rule |
| `reconstructed` | 24 | No stated rule, but a rule that reproduces the number was found and is shown with its test |
| `unstated` | 14 | No stated rule and no reproducing rule found |
| `not_a_count` | 6 | The finding is not a word/letter count (a provenance fact, an inventory, a literature fact, a critique) |

By category: paired counts 3 stated / 20 reconstructed / 6 unstated;
letter counts 7 stated; Code 19 1 stated / 4 reconstructed / 5 unstated /
1 not a count; corpus linguistics 8 stated / 3 unstated / 5 not a count.
By section: Scholar Findings 15 stated / 5 reconstructed / 9 unstated /
6 not a count; Counted by this site 4 stated / 17 reconstructed;
Popular claims (circulating) 2 reconstructed / 5 unstated.

The pattern is the story of this pass: **the paired-count list almost never states a
method** — 19 of its claims reproduce only under a rule reconstructed from
the numbers, and 6 do not reproduce under any rule we could find. **Rashad
Khalifa states almost no method either** (Appendix 1 "Simple Facts" gives no
rule for root/lemma, prefixes, plurals or letters) — 5 stated / 4 reconstructed /
5 unstated across his 14 findings — and two of his figures use **opposite
basmalah conventions**: surah 96's 304 letters needs the basmalah INCLUDED,
while the 76 letters of 96:1–5 need it EXCLUDED.

## The reconstructed rules that matter

- **Bare (unsuffixed) nouns — "without genitive".** The list's "(without
  genitive)" reproduces exactly once read as *no possessive pronominal suffix*,
  prefixes allowed: bare إيمان 25 and bare كفر 25; bare هدى 79 and bare رحمة
  79. Counting with no prefix at all gives 7/4/32/40 — the rule is
  specifically *no suffix, prefixes allowed*.
- **Root rules.** plant (nbt) 26; tree ($jr) 27 minus the verb شَجَرَ
  ("to dispute", 4:65) = 26; reward (jzy) 118 minus the jizya tax (9:29) = 117;
  forgiveness (gfr) 234; tongue (lsn) 25; admonition (wEZ) 25; disaster (Swb)
  77 minus صيّب (rainstorm, 2:19) and صواب ("right", 78:38) = 75; thanks ($kr)
  75; treachery (xwn) 16; foul (xbv) 16; blessing (brk) 32.
- **Say / they said.** Singular imperative قل is 332 exactly
  (293 no-prefix + 18 fa- + 21 wa-, QAC LEM qaAla IMPV 2MS); قالوا is 332
  (QAC PERF 3MP qaAlu).
- **Jannah.** The 77 exact surface forms are **not** all "garden": 12 are
  جِنَّة (jinn/madness, 10 tokens) and جُنَّة (shield, 2). Sense-correct garden
  counts are 65 (unsuffixed singular), 70 (QAC lemma singular), 147 (all
  gardens) — none is 77. Hell (jahannam) is 77 under both rules.
- **Sea / land.** Definite singular البحر is 32; land-sense البرّ is 12, not
  13 — the other 10 LEM bar~ tokens are piety/righteousness (الأبرار ×6,
  برًّا ×2, 52:28 "the Benign", 80:16 بررة).
- **Most frequent words.** QAC lemma min (preposition) 3,226; ma 2,565;
  Allah 2,699 — all three reproduce exactly under the same lemma rule. The
  old "differs" rested on a Tanzil skeleton count (3,314) that conflates
  مِن with مَن.

## Per-scholar method table

| Scholar / source | Findings | Stated | Reconstructed | Unstated | Not a count |
|---|---|---|---|---|---|
| Counted by this site | 21 | 4 | 17 | 0 | 0 |
| Rashad Khalifa | 14 | 5 | 4 | 5 | 0 |
| Popular claim (circulating) | 7 | 0 | 2 | 5 | 0 |
| Kais Dukes (QAC figures) | 3 | 1 | 0 | 1 | 1 |
| al-Suyuti (via SeekersGuidance) | 2 | 2 | 0 | 0 | 0 |
| Eueung Mulyana | 2 | 2 | 0 | 0 | 0 |
| Delshad Botani | 1 | 1 | 0 | 0 | 0 |
| Halim Sayoud | 1 | 1 | 0 | 0 | 0 |
| Abdul Baqi | 1 | 1 | 0 | 0 | 0 |
| Tariq Al-Suwaidan / circulating lists | 2 | 0 | 1 | 1 | 0 |
| Kais Dukes & Eric Atwell | 1 | 0 | 0 | 0 | 1 |
| Dirk Roorda & Cornelis van Lit | 1 | 0 | 0 | 0 | 1 |
| WikiIslam | 1 | 0 | 0 | 0 | 1 |
| Tanzil Project | 1 | 0 | 0 | 0 | 1 |
| Khalifa / Gardner / Philips / Sardar / Yüksel (reception) | 1 | 0 | 0 | 0 | 1 |
| Classical/traditional observations | 2 | 2 | 0 | 0 | 0 |
| arabiantongue.com | 1 | 0 | 0 | 1 | 0 |
| Words of Quran (QAC data) | 1 | 0 | 0 | 1 | 0 |

## Corrections made in this pass

Tallies move **28 confirmed / 25 differ / 11 cannot verify → 37 confirmed /
17 differ / 10 cannot verify**. Per section: Scholar Findings 16 / 10 / 9;
Popular Claims 21 / 7 / 1.

### Status flips (14 — each re-verified by the coordinator's own scripts)

| Finding | Was | Now | Why |
|---|---|---|---|
| iman-kufr-25 | differs | confirmed | Bare (unsuffixed) nouns: 25 / 25 |
| zakah-blessing-32 | differs | confirmed | Lemma/root: zakah 32, blessing (brk) 32 |
| say-they-said-332 | differs | confirmed | قل 332 (IMPV 2MS), قالوا 332 (PERF 3MP) |
| plant-tree-26 | differs | confirmed | nbt 26; $jr 26 after excluding the 4:65 verb |
| reward-forgiveness-117-234 | differs | confirmed | jzy 117 after excluding jizya tax (9:29); gfr 234 |
| guidance-mercy-79 | differs | confirmed | Bare nouns: hudFY 79, raHomap 79 |
| tongue-sermon-25 | differs | confirmed | lsn 25; wEZ 25 ("sermon" = admonition) |
| refuge-forever-28 | differs | confirmed | maSiyr 28; >abadFA 28 (old "29" was عابدات 66:5, a substring false positive) |
| disaster-thanks-75 | differs | confirmed | $kr 75; Swb 75 after excluding 2:19 and 78:38 |
| treachery-foul-16 | differs | confirmed | xwn 16; xbv 16 |
| jannah-jahannam-77 | confirmed | differs | 12 of the 77 surface forms are jinn/shield, not garden |
| sea-land-32-13 | cannot_verify | differs | Land-sense is 12, not 13 (sense disambiguation now done verse by verse) |
| most-frequent-min-3226 | differs | confirmed | QAC lemma min 3,226; ma 2,565; Allah 2,699 |
| dukes-unique-words | confirmed | differs | Only the 18,994 surface-form figure reproduces; stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832 (not 3,382) |

### Note-only corrections (6)

- **human-being-65** — the creation-stage table now reproduces under
  lemma/form rules: soil (turaAb) 17 + drop (n~uTofap) 12 + clot (Ealaqap 5 +
  Ealaq 96:2) 6 + lump (muDogap) 3 + bone (عظام 13 + عظم 6:146, 19:4) 15 +
  flesh (laHom) 12 = 65. (The old note said the stage arithmetic did not
  reproduce; it used substring counts.)
- **hapax-legomena** — stem-lemma hapax is 1,994 (verified by recount);
  surface-form hapax (Tanzil whitespace tokens occurring once) is 12,005.
- **rdsq-words-77430** — the odd/even verse-group totals 38,716 / 38,714 DO
  reproduce under the document's own stated criterion, odd/even C+V parity
  (chapter + verse number): 38,715 / 38,714 on QAC data, 38,717 / 38,716 on
  Tanzil — within the same 3-word gap as the headline total.
- **text-fabric-quran** — the Zenodo DOI 10.5281/zenodo.2532177 is now
  confirmed: doi.org resolves it to `q-ran/quran: Initial quranic text-fabric
  data release` (HTTP 200).
- **dukes-atwell-2012** — the DOI formerly cited (10.1007/s10579-012-9205-0)
  is wrong: it resolves to Klapaftis & Manandhar (2013), "Evaluating Word
  Sense Induction and Disambiguation Methods". The link was removed. The real
  items are Dukes & Atwell (2012), "LAMP", Proc. LREC'12, pp. 3268–3275, and
  Dukes, Atwell & Habash (2013), *Language Resources and Evaluation* 47(1),
  33–62, DOI 10.1007/s10579-011-9167-7 (verified via Crossref).
- **qac-morphology** — the 128,076-morpheme figure is from the QAC v0.3
  announcement dated **12 March 2011**, not 14 March (Corpora-List archive,
  "Sat Mar 12 17:23:42 UTC 2011").

### Not changed (still parked / undecided)

- **benefit-corrupt-50** — the proposed differs→confirmed flip from
  `PASTED_PAGE_CHECK.md` is still unapproved; the finding stays `differs`.
- **mind-light-49** — borderline: 49 reproduces only if the adjective منير
  ("shining") is counted as "light". Left as `differs` for MK's call.

## Locations — where each count occurs

`data/locations.json` (also served as `web/locations.js`) holds, per finding:

- `verses` — the deduplicated list of `surah:verse` places containing a
  counted token, under the standard QAC root rule. Computed by script from
  `corpus/quranic-corpus-morphology-0.4.txt` — never hand-typed.
- `per_surah` — the number of listed verses in each surah (sums to the verse
  count). One convention for all findings: Checker A originally emitted
  occurrence counts per surah and Checker B verse counts; the merge
  (`merge_enriched.py`) normalises both to verses per surah, because the site
  headline is "Locations (N verses)". Occurrence totals are in the
  verification lines, not in `per_surah`.
- `verses_scholar_rule` — the verse list under the scholar's own reconstructed
  rule, where it differs and is reconstructable.
- `not_applicable` — for the 14 findings that are not word/letter counts
  (whole-Quran totals, inventories, provenance/reception facts, the critique).

Coverage: **50 findings carry verse lists** (13,359 root-rule verse references
+ 5,400 scholar-rule references), **14 are not applicable**. The largest list
is Allah (1,821 verses). On the site each finding has an expandable
"Method & where it occurs" block: method, exceptions, both-rule verification,
per-surah breakdown, and the full verse list (scrollable for large counts).

Locations were spot-checked against the corpus by script (every listed verse
actually contains a counted token) — see the verification section below.

## How the numbers were produced (scripts)

- `data/methods_check_A.py` — Checker A (paired counts + letter counts, 37
  findings): recomputes every count under both rules and emits locations.
- `data/methods_check_B.py` (+ `methods_check_B_probes.py`,
  `methods_check_B_probes2.py`, `build_enriched_B.py`) — Checker B (Code 19 +
  corpus linguistics, 27 findings). Note: the v1 probe script has a known
  line-index bug in its token-alignment helper; per-verse counters were
  unaffected and probes2 re-does the token checks correctly.
- `merge_enriched.py` — merges the two enriched files into
  `data/scholar_findings.json` and extracts `data/locations.json`; recomputes
  tallies; applies only the coordinator-verified corrections listed above.
- `build.py` — rebuilds `web/data.js` (findings now carry the method fields)
  and `web/locations.js` from `data/locations.json`.
- `regen_findings_md.py` — regenerates `data/scholar_findings.md`, now with
  per-finding method, exceptions, both-rule verification, and a locations
  summary (full list for ≤ 60 verses; per-surah breakdown + first 20 for
  larger counts).

## Still unverified (carried forward)

- The 280-letter gap in the RDS-Q letter total and the 278-letter gap in the
  Botani letter total: dagger-alif, small-letter and shaddah variants were
  tested and none explains either gap.
- Abdulbaqi's 1,651 roots and Dukes' 12,183 stems / 1,685 roots / 3,382 lemmas
  do not reproduce under any rule tried; possibly an older QAC version —
  unproven.
- arabiantongue's ~1,620 hapax (lemma-based figure was not recounted against
  QAC; our stem-lemma hapax is 1,994, surface-form hapax 12,005).
- The RDS-Q 3-word gap; the first-revelation 19 words (no rule gives 19).
- The Khalifa reception quotation (Canadian Council, April 1983) is
  unverified; the Gardner date conflict (1980 per Philips vs 1981 per
  Yüksel) is unresolved (Philips treated as the stronger witness).
- The Dukes & Atwell 2012 LRE 46(3) 475–489 citation was not located; the
  man–woman 24:24 Scribd source (Al-Suwaidan / Elias) is unfetchable.
- life–death 145, summer–winter 5, love–obedience 83, wine–intoxication 6
  stay `differs` — no reproducing rule was found.

# Methods + Locations Check — Checker B (code19 + corpus_linguistics)

Checker B pass, 2026-11-08. All 27 findings (11 code19 + 16 corpus_linguistics)
from `data/scholar_findings.json`, section "scholarly" (preserved, unchanged).
Nothing was pushed; `data/scholar_findings.json` was not edited — corrections
below are proposals in `data/scholar_findings_enriched_B.json` only.

## Outputs

- `data/scholar_findings_enriched_B.json` — one object per finding id:
  `scholar_method`, `method_status`, `exceptions`,
  `verification_scholar_rule`, `verification_root_rule`, `locations`,
  `correction` (null unless listed below).
- `data/methods_check_B.py` — the verification script (re-run it to reproduce
  every number; writes `data/methods_check_B_results.json`).
- `data/methods_check_B_probes.py`, `data/methods_check_B_probes2.py` —
  follow-up probes (Rahim 116 vs 115, min 3,314 vs 3,226, Quran lemma,
  Abdulbaqi pipeline, hapax by POS). Probes 1 has a known alignment bug in
  its `tanzil_token` helper (wrong line-index map); its per-verse counters
  are unaffected and probes2 re-does the token checks with the fixed map.
- `data/build_enriched_B.py` — assembles the enriched JSON from the results.

Corpus: QAC v0.4 morphology file + Tanzil Uthmani text, both local.
Counting rules follow the project's existing scripts (skeleton normalisation,
clitic stripping, project letter convention). Every verse reference in
`locations` was computed by script from the QAC morphology data (or, for
Tanzil-surface counts, from the Tanzil file) — none hand-typed. All location
lists were validated: sorted, deduplicated, per-surah sums match.

## Method coverage (27)

| status | n | findings |
|---|---|---|
| stated | 9 | khalifa-verse-total-6346, qac-word-count-77429, root-frequency-studies, classical-word-totals, classical-letter-totals, rdsq-words-77430, rdsq-letters-325666, botani-2012-distributions, quran-word-57-khalifa |
| reconstructed | 4 | allah-2699, rahman-57-rahim-115, ism-19, verse-number-checksum-118123 |
| unstated | 8 | basmalah-19-letters-114, first-revelation-words-19, first-revelation-letters-76, surah-96-19-verses-304-letters, surah-110-19-words, dukes-unique-words, most-frequent-min-3226, hapax-legomena |
| not_a_count | 6 | khalifa-reception, qac-morphology, tanzil-provenance, text-fabric-quran, wikiislam-critique, dukes-atwell-2012 |

Headline: Khalifa states almost no counting method. His Appendix 1 presents
the counts as "Simple Facts" verifiable from the Arabic text, with no rule
for root vs lemma, prefixes, plurals, or letter conventions. The four
"reconstructed" findings reproduce only with the stated exclusions
(9:128-129 dropped; basmalahs excluded; plural/contracted forms excluded).
Two of his figures use opposite basmalah conventions (see below).

## Corrections proposed (7, in the enriched JSON)

1. **most-frequent-min-3226 — `our_status`: differs → confirmed.**
   QAC lemma `min` (preposition) = **3,226 exactly**; the site's other two
   figures also reproduce exactly under the same rule (lemma `maA` = 2,565;
   lemma `{ll~ah` = 2,699). The "differs" verdict rested on the Tanzil
   skeleton-lemma count (3,314), a different unit: diacritic-stripping
   conflates مِن (preposition, 2,499 of those tokens) with مَن (relative
   pronoun, 806), plus 6 verb `man~a` tokens and 3 alignment artifacts at
   13:37. The earlier note's "88 above" is arithmetic coincidence, not an
   explanation.
2. **dukes-unique-words — `our_status`: confirmed → differs.**
   Recounted from QAC v0.4: only the 18,994 surface-form figure reproduces
   exactly. Stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832
   (not 3,382). No natural POS subset reproduces 3,382. The figures may come
   from an older QAC version (v0.3: 77,430 words) or a different
   lemmatisation — recorded as hypothesis, not fact.
3. **rdsq-words-77430 — `our_note` (odd/even totals).** The note claimed the
   38,716/38,714 odd/even totals "did not reproduce under any natural
   grouping" and dropped them. They DO reproduce under the document's own
   stated criterion, odd/even **C+V parity** (chapter + verse number):
   QAC data gives exactly 38,715/38,714 (the document's own Dukes-data
   figures, p. 20); Tanzil gives 38,717/38,716 — within the same 3-word gap
   as the headline total. The earlier draft never tried C+V parity. Letters
   odd/even C+V: ours 162,684/162,702 vs the document's 162,821/162,845
   (gap 137/143 = the 280 letter gap).
4. **text-fabric-quran — `our_note` (DOI).** The Zenodo DOI
   10.5281/zenodo.2532177 is now confirmed: doi.org resolves it to
   "q-ran/quran: Initial release", published 5 January 2019, v0.1, Dirk
   Roorda. (The Zenodo record lists Roorda alone; van Lit is repo co-author.)
5. **dukes-atwell-2012 — `source.url` (DOI wrong).** DOI
   10.1007/s10579-012-9205-0 resolves to "Evaluating Word Sense Induction
   and Disambiguation Methods" (Manandhar et al., 2013) — a different paper
   by different authors. The cited journal article (LRE 46(3), 475-489) could
   not be located. Real items: Dukes & Atwell (2012), "LAMP", Proc. LREC'12,
   pp. 3268-3275; Dukes, Atwell & Habash (2013), LRE 47(1), 33-62, DOI
   10.1007/s10579-011-9167-7. The exact title belongs to Dukhovny & Atwell,
   LREC 2009.
6. **hapax-legomena — `our_note` (lemma figure now recounted).** QAC
   stem-lemma hapax = **1,994** (in 1,528 verses), not ~1,620. No POS subset
   reproduces ~1,620 (nouns only 1,249; N+ADJ+V 1,943; excl. proper nouns
   1,954). Surface-form hapax (raw) = 12,005, confirmed.
7. **qac-morphology — `our_note` (date).** The v0.3 announcement is dated
   **12 March 2011** in the Corpora-List archive, not 14 March. The
   128,076-morpheme figure itself is confirmed verbatim from that
   announcement.

## Locations coverage (13 with verse lists, 14 not applicable)

| finding | verses (root rule) | scholar-rule verses |
|---|---|---|
| basmalah-19-letters-114 | 114 | — |
| allah-2699 | 1,821 | 1,820 (minus 9:129) |
| rahman-57-rahim-115 | 166 (Rahman ∪ Rahim) | 165 (minus 9:128) |
| ism-19 | 19 | — |
| first-revelation-words-19 | 96:1-5 | — |
| first-revelation-letters-76 | 96:1-5 | — |
| surah-96-19-verses-304-letters | 96:1-19 | — |
| surah-110-19-words | 110:1-3 | — |
| verse-number-checksum-118123 | 1,821 | 1,820 (minus 9:129) |
| root-frequency-studies | 1,879 (ROOT Alh) | — |
| most-frequent-min-3226 | 2,230 (LEM min) | — |
| quran-word-57-khalifa | 69 (LEM quro'aAn) | 57 (narrow forms in Table 21) |
| hapax-legomena | 1,528 (hapax lemmas) | — |

Not applicable (whole-Quran totals, inventories, or literature facts):
khalifa-verse-total-6346, khalifa-reception, qac-word-count-77429,
dukes-unique-words, qac-morphology, tanzil-provenance, text-fabric-quran,
classical-word-totals, classical-letter-totals, rdsq-words-77430,
rdsq-letters-325666, botani-2012-distributions, wikiislam-critique,
dukes-atwell-2012.

## Key verification results (all recomputed by script)

- **Allah 2,698** reproduces only as 2,699 (lemma, excl. basmalahs) minus
  9:129. Strict surface الله = 2,267; incl. basmalahs 2,811.
  Checksum 118,123 reproduces only as 118,252 − 129 (root rule 118,340).
- **Rahim 114**: Tanzil surface-lemma 115 − 9:128 = 114. QAC lemma gives
  **116**, because it also counts the plural رُحَمَاءُ at 48:29 — so
  Khalifa's 114 works only under the singular-form rule, not the QAC lemma
  rule. Rahman 57 is exact under both rules.
- **Ism 19**: full spelling only (اسم 14 + باسم 4 + الاسم 1); QAC lemma
  `{som` = 39 (19 + 12 plural أسماء + 5 suffixed singular + 3 contracted
  بسم at 1:1, 11:41, 27:30). No "no plural forms" rule exists in Appendix 1.
- **First revelation 19 words: no rule gives 19.** 20 words excl. basmalah
  under every natural count (Tanzil tokens 20; QAC words 20), 24 incl.
  Letters 76 excl. basmalah confirmed.
- **Surah 96, 304 letters: requires the basmalah INCLUDED** (285 + 19).
  Khalifa's 76 letters for 96:1-5 requires it EXCLUDED — his two figures
  use opposite basmalah conventions.
- **Quran 57: does not reproduce under Khalifa's own stated rule.**
  Narrow forms = 59; 10:15's token (بقرآن) is outside the narrow set, so
  the stated exclusion changes nothing. His 57 = the 57 narrow-form verses
  in his Table 21; the table also silently excludes 13:31 and 41:44 (both
  قرآنا). His headline 58 = 57 + 10:15. Table 21 has 66 rows, not 58;
  all-forms verse set is 69. Substring count 71 catches one verb,
  قَرَأْنَاهُ "We recited it" (75:18:2, lemma qara>a). "12 verses" for other
  grammatical forms: 9 Table-21 verses contain only non-narrow forms
  (11 tokens); with 10:15 that is 10 verses, not 12.
- **Roots**: unique roots 1,642 (word level = segment level). Abdulbaqi's
  printed 1,651 reproduces under no rule; his own published pipeline re-run
  on this file gives 1,641 — it loses root wAd (81:8:2, الْمَوْءُودَة)
  because that word's FORM `mawo'u,dapu` contains a comma, shifting
  `cut -d',' -f4`. Top roots reproduce exactly: Alh 2,851, qwl 1,722,
  kwn 1,390, rbb 980; Ḥ-S-N 194. Exactly one word has two root-bearing
  segments (20:94:2, يَا بْنَ أُمَّ "O son of my mother").
- **QAC totals**: 77,429 words / 128,219 segments — exact. Tanzil tokens
  excl. basmalahs 77,433 (4-gap: 2:181, 8:6, 13:37, 37:130).
- **Unique lemmas**: QAC stem lemmas = 4,832 (= wordsofquran's figure, not
  Dukes' 3,382). Unique stem forms 12,113.
- **RDS-Q letter gap (280) still unexplained.** Variants tested: +dagger
  alif = 335,224; +dagger+small letters = 337,438; shaddah doubled =
  348,402. None gives +280. Botani's letter gap (278, incl. basmalahs) is
  in the same family but differs by 2, so one unknown convention difference
  cannot explain both exactly. Botani words incl. basmalahs: ours 77,881
  vs his 77,878 (3 above).
- **Classical totals**: SeekersGuidance page confirmed — words 77,439
  (Basra), Kufan 77,430, Ata' 77,437; letters 323,015 (Basra), Mujahid
  321,000, Ibn Mas'ud 300,670, Salam 340,740. Stated causes: فِي السَّمَاء
  as one vs two words; shaddah as one vs two letters.
- **Khalifa reception**: Gardner (Scientific American, Sept 1980, p. 22,
  "ingenious study") confirmed via Philips' book; Skeptical Inquirer 21(5),
  Sept-Oct 1997 confirmed as the issue; Philips 1987/1407, 76 pp., 2nd ed.
  2002 confirmed; Submission.org 2002 recount confirmed verbatim on
  App1.html. **Not verified**: Canadian Council on the Study of Religion,
  Quarterly Review, April 1983 quotation. Note the Gardner date conflict:
  Yuksel's material says September 1981, pp. 22-24; Philips (stronger
  witness) says September 1980, p. 22.
- **Tanzil provenance**: CC BY 3.0 verbatim-only licence and Medina Mushaf /
  Hafs narration both confirmed from Tanzil's own docs.
- **WikiIslam**: tactics page confirmed (selective forms, prefixes/suffixes,
  sense conflation, cherry-picking); zakah/blessing 32 sub-article and the
  Zahid Aziz quotation individually located. Al-Roomi point still not
  located in the fetched text.

## Still unverified / open

- The **280-letter RDS-Q gap** and the **278-letter Botani gap**: cause
  unidentified after testing dagger-alif, small-letter and shaddah variants.
- **Abdulbaqi's 1,651 roots** and **Dukes' 12,183 stems / 1,685 roots /
  3,382 lemmas**: reproduce under no rule tried; possibly an older QAC
  version or a different lemmatisation — not proven.
- **Arabiantongue's ~1,620 hapax**: no rule tried reproduces it.
- **RDS-Q's 3-word gap** (77,433 vs 77,430 on the same Tanzil text):
  unexplained at token level.
- **First-revelation 19 words**: no stated or reconstructed rule gives 19.
- **Khalifa reception**: Canadian Council April 1983 quotation unverified;
  Gardner date conflict (1980 vs 1981) unresolved in favour of Philips.
- **Dukes & Atwell 2012 journal citation** (LRE 46(3), 475-489): no such
  paper located; the DOI is proven wrong (see correction 5).
- The 11 proposed findings / benefit-corrupt-50 flip from
  PASTED_PAGE_CHECK.md were NOT applied (still unapproved). İşârâtü'l-İ'câz
  untouched. No finding's `our_status` was changed in the main JSON — only
  proposals in the enriched file.

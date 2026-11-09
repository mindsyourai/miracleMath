# Assumption sets — how each scholar's number was reconciled

Date: 2026-11-08 (research redesign, Agent A). Companion to `METHODS.md`
(2026-11-08, methods + locations pass) and `RECONCILIATION.md` (2026-11-07).
All numbers below were recomputed by script from the corpus
(QAC v0.4 morphology + Tanzil Uthmani) by `data/assumption_recompute.py`
(re-runnable, idempotent); the run log is
`data/assumption_recompute_report.json`. The 11 proposed findings and the
benefit–corrupt-50 flip from `PASTED_PAGE_CHECK.md` remain **unapproved and
are NOT applied here**; mind-light-49 is left as `differs` for MK's call;
the Scholar/Popular section split is untouched; İşârâtü'l-İ'câz is still parked.

## The sets

| Set | Name | Definition |
|-----|------|------------|
| A1 | Standard root rule | Count by QAC ROOT, all forms, prefixes/suffixes in, the 112 unnumbered basmalahs excluded (only 1:1 and 27:30 count); where the root covers other senses, narrow by lemma to the intended sense as documented per finding; where the claim is about a lemma or a form subset, that subset's number is given instead (METHODS.md convention). For corpus totals, the QAC word unit. |
| A2 | Lemma rule | Count by QAC LEM, all forms, prefixes/suffixes in, unnumbered basmalahs excluded as in A1. |
| A3 | Surface-form rule | Count exact surface forms on the Tanzil skeleton text — the forms listed in the finding's selection where one is documented (singular-only, bare-form, narrow or plural selections), otherwise the plain surface reading of the claimed word; unnumbered basmalahs excluded as in A1. |
| A4 | Letter rule | Count base letters on the Tanzil Uthmani text under the project letter convention (alef wasla counts as a letter; dagger alif, small waw and small yeh are marks, not letters; shaddah counts once); unnumbered basmalahs excluded. |
| A5 | Scholar's stated rule | The counting rule as stated in the scholar's own source, applied to the corpus (per-finding; null where the source states no counting rule). |
| A6 | Scholar's reconstructed rule | The specific selection or exclusion documented in the finding's scholar_method that reproduces the scholar's number (per-finding; null where no reproducing rule was found). |
| A7 | Basmalah-included variant | As the finding's primary rule (A1/A2/A3/A4 as applicable), but with the 112 unnumbered basmalahs counted in. |

How to read the table: **scholar's number** is the number in the claim;
**our number** is the recount under `our_set` (our standard rule for that
finding — A1 root rule for most, A2 lemma rule where the count is a lemma
count, A4 letter rule for letter findings); **reconciles under** lists the
sets that reproduce the scholar's number(s) in full. A set is listed only
if it reproduces every part it covers, and the listed sets jointly cover
all parts — so for the one mixed-unit finding (surah-110: 19 words + 19
letters) both A1 (words) and A4 (letters) are listed. `numbers_by_set` in
`data/scholar_findings.json` holds the number under every applicable set;
multi-number values are lists in the same order as the scholar's numbers,
with `null` for parts a set does not cover. Sets that do not apply to a
finding are omitted. Seven findings are not word/letter counts at all
(literature/provenance/bibliographic facts) and carry no numbers.

Coverage: **40 of 63** findings reconcile under at least one set — 11 under
the scholar's stated rule (A5), 25 under the reconstructed rule (A6), 33
under one of the standard sets (A1–A4). **17** counted findings reconcile
under no set. **7** are not counts.

## Per-finding reconciliation

| id | scholar's number | our number | reconciles under | reason |
|----|------------------|------------|------------------|--------|
| dunya-akhira-115 | 115/115 | 115/115 | A1, A3, A6 | Both sides are 115 under the root rule and the surface rule; the lemma rule gives akhira 155 (the masculine al-akhir and plural forms are a separate lemma). |
| jannah-jahannam-77 | 77/77 | 147/77 | A3, A6 | 77/77 reproduces only under the sense-blind surface-form rule; sense-correct garden is 66 (bare singular), 70 (lemma singular) or 147 (all gardens) — none is 77. |
| shaytan-angels-88 | 88/88 | 88/88 | A1, A2, A6 | 88/88 reproduces under the root rule, the lemma rule and the reconstructed rule (devils by root $Tn, angels by lemma malak). |
| day-365 | 365 | 475 | A3, A5 | 365 is the stated singular, suffix-free selection; the whole root gives 475 (375 singular + 27 plural + 3 dual + 70 yawma'idhin). |
| month-12 | 12 | 21 | A3, A6 | 12 is the singular-only selection; the root/lemma total is 21 (12 singular + 2 dual + 7 plural). |
| salawat-5 | 5 | 5 | A1, A3, A6 | 5 is the plural surface form صلوات (and the plural stems of the lemma); the whole lemma is 83 words. |
| sea-land-32-13 | 32/13 | 41/12 | — | Sea 32 reproduces as definite singular البحر; land 13 reproduces under no rule — sense-correct land is 12, surface البر is 21. |
| man-woman-24-24 | 24/24 | 57/85 | A3, A6 | 24/24 is the singular-only surface selection; root totals are 57/85, singular lemmas 29/26. |
| life-death-145 | 145/145 | 184/165 | — | No rule reproduces 145/145 — whole roots 184/165, nouns 76/50, surface families 125/171. |
| sun-moon-33-27 | 33/33/27 | 33/43/27 | A3, A5 | 33/33/27 reproduces under the stated simple-forms rule and the surface rule; the root/lemma rule gives light 43 (49 with منير). |
| muhammad-4 | 4 | 4 | A1, A2, A3, A6 | 4 under every rule tried (surface, lemma and root-narrowed). |
| iman-kufr-25 | 25/25 | 45/37 | A3, A5 | 25/25 is the bare (unsuffixed) noun selection — the stated '(without genitive)'; lemma totals are 45/37. |
| zakah-blessing-32 | 32/32 | 32/32 | A1, A2, A6 | 32/32 reproduces under the root and lemma rules; plain substrings give 67/5. |
| say-they-said-332 | 332/332 | 332/332 | A1, A2, A6 | 332/332 reproduces under the lemma/POS rule; the plain surface count of قل gives 333 (one non-imperative token). |
| plant-tree-26 | 26/26 | 26/26 | A1, A2, A6 | 26/26 reproduces under the root rule (tree minus the 4:65 dispute verb); substrings give 11/27. |
| reward-forgiveness-117-234 | 117/234 | 117/234 | A1, A2, A6 | 117/234 reproduces under the root rule (reward minus the jizya tax token); substrings give 48/28. |
| guidance-mercy-79 | 79/79 | 79/79 | A1, A3, A6 | 79/79 is the bare-noun selection (same rule as iman/kufr); lemma totals are 85/114, whole roots 316/339. |
| tongue-sermon-25 | 25/25 | 25/25 | A1, A2, A6 | 25/25 reproduces under the root and lemma rules; substrings give 15/9. |
| wine-intoxication-6 | 6/6 | 6/7 | — | Wine 6 reproduces as the noun; intoxication is 7 under every rule tried — no rule gives 6/6. |
| mind-light-49 | 49/49 | 49/43 | — | Mind 49 reproduces by root; light is 43 as the noun (49 only if the adjective منير is counted as 'light' — left undecided). |
| benefit-corrupt-50 | 50/50 | 50/50 | A1, A2, A6 | Both sides are exactly 50 under the root and lemma rules; the status flip is still unapproved by MK, so the finding stays 'differs'. |
| love-obedience-83 | 83/83 | 83/87 | — | Love 83 reproduces (root minus grain); obedience is 87 sense-correct (129 whole root) — no rule gives 83. |
| refuge-forever-28 | 28/28 | 28/28 | A1, A2, A6 | 28/28 reproduces under the root and lemma rules; the ابدا substring gives 29 (the 66:5 عابدات false positive). |
| disaster-thanks-75 | 75/75 | 75/75 | A1, A2, A6 | 75/75 reproduces under the root and lemma rules (disaster minus the two non-disaster lemmas); substrings give 11/47. |
| trouble-peace-13 | 13/13 | 13/13 | A1, A2, A6 | 13/13 reproduces under the root and lemma rules; substrings give 7/3. |
| treachery-foul-16 | 16/16 | 16/16 | A1, A2, A6 | 16/16 reproduces under the root and lemma rules; substrings give 2/13. |
| righteous-wicked-6-3 | 6/3 | 6/4 | A3, A6 | 6/3 reproduces as exact surface forms; under the lemma rule the wicked side is 4 (الفجرة 80:42). |
| summer-winter-5 | 5/5 | 1/1 | — | Summer/winter occur once each (both 106:2); heat 15 / cold 5 — no rule gives 5/5. |
| human-being-65 | 65 | 65 | A1, A3, A6 | 65 is the انسان surface count (and the انسان subset of the lemma); the whole lemma is 71 (6 collective أناس/أناسيّ). |
| qaf-57-57 | 57/57 | 57/57 | A4, A5 | 57/57 reproduces under the project letter convention and Khalifa's stated rule; the basmalahs contain no ق. |
| nun-132-vs-133 | 133 | 131 | A5 | 133 requires Khalifa's stated rule (the spelled-out initial ن و ن counts as two); the written text gives 132 with the basmalah, 131 without it. |
| sad-153-vs-152 | 97/26/29 | 98/26/29 | A5 | 152 requires Khalifa's stated textual rule (7:69 read بسطة with س); the Tanzil text reads بصطة, giving 153. |
| muqattaat-structure-29-14-78 | 29/14/75 | 29/14/75 | A4, A5 | 29 surahs, 14 letters, 75 opening letters (78 counting 42:2 عسق) — the stated structure reproduces exactly. |
| all-28-letters-verses | 28/28 | 28/28 | A4, A5 | 3:154 and 48:29 each have 28 distinct letters and no other verse does. |
| longest-word-fasqaynakumuhu | 11 | 10 | — | فأسقيناكموه is 10 letters under the project convention; 11 only if the dagger alif counts as a letter, and then it merely ties for longest (3:17, 4:75, 4:127 also 11). |
| seven-heavens-7 | 7 | 7 | A1, A2, A3, A5 | 7 verses contain سبع + سماوات under every rule tried. |
| basmalah-19-letters-114 | 19 | 19/114 | A4 | 19 letters and 114 occurrences reproduce under the project letter convention (alef wasla counts); Khalifa states no letter rule. |
| allah-2699 | 2698 | 2699 | A6 | 2,698 reproduces only under Khalifa's reconstructed rule (lemma count, basmalahs out, 9:129 dropped); the standard text gives 2,699. |
| rahman-57-rahim-115 | 57/114 | 57/116 | A6 | 57 reproduces under the lemma rule; 114 needs the 9:128 رحيم dropped (115 on the standard text, 116 by QAC lemma incl. the 48:29 plural). |
| ism-19 | 19 | 39 | A3, A6 | 19 reproduces only for the full spelling اسم (plural أسماء and contracted بسم excluded); the lemma total is 39. |
| first-revelation-words-19 | 19 | 20 | — | 20 words under every natural count (24 with the basmalah); 19 would require dropping exactly one word — no such rule is stated. |
| first-revelation-letters-76 | 76 | 76 | A4 | 76 letters excl. the basmalah under the project convention; 95 with it — Khalifa states no letter rule. |
| surah-96-19-verses-304-letters | 19/304 | 19/285 | A6, A7 | 19 verses and 304 letters reproduce only with the merged basmalah counted in (285 without it) — the opposite basmalah convention from the 76-letter count for 96:1–5. |
| surah-110-19-words | 19/19 | 19/— | A1, A4 | 19 words (A1) and 19 letters in 110:1 (A4) both reproduce excl. the basmalah; 23 words / 38 letters with it. |
| verse-number-checksum-118123 | 118123 | 118252 | A6 | 118,123 reproduces only excluding the basmalahs and Khalifa's two deleted verses (9:129 contributes 129); the standard text gives 118,252. |
| khalifa-verse-total-6346 | 6346 | 6236 | A5 | 6,346 is arithmetic under Khalifa's stated rule (6,234 numbered + 112 basmalahs); the standard count is 6,236, or 6,348 with basmalahs counted and no verses deleted. |
| khalifa-reception | — | — | — | Not a word/letter count — a reception-history fact; no counting assumption applies. |
| qac-word-count-77429 | 77429 | 77429 | A1, A5 | 77,429 QAC words reproduces exactly; Tanzil whitespace tokens give 77,433 excl. basmalahs (77,881 incl.) — 4 verses differ by one token each. |
| dukes-unique-words | 18994/12183/1685/3382 | —/—/1642/— | — | Only the 18,994 unique surface forms reproduce; stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832 (not 3,382). |
| qac-morphology | — | — | — | Not a word/letter count — a provenance fact about the corpus; no counting assumption applies. |
| tanzil-provenance | — | — | — | Not a word/letter count — a provenance fact; no counting assumption applies. |
| text-fabric-quran | — | — | — | Not a word/letter count — a provenance fact; no counting assumption applies. |
| root-frequency-studies | 1651/2851 | 1642/2851 | — | Alh 2,851 reproduces exactly; the 1,651 root total reproduces under no rule (1,642 by word/segment count, 1,641 by the post's own pipeline). |
| most-frequent-min-3226 | 3226/2699/2565 | 3226/2699/2565 | A1, A2 | All three figures reproduce exactly under the QAC lemma rule; the Tanzil skeleton count for من is 3,314 because it conflates مِن with مَن. |
| classical-word-totals | 77439 | 77429 | — | No modern recount reproduces 77,439 exactly; closest is Tanzil tokens 77,433 (6 below) — within the spread of the classical word-boundary conventions. |
| classical-letter-totals | 323671 | 325386 | — | Headline 323,671 (Basra 323,015; variants to 330,733) reproduces under no modern rule — project convention gives 325,386 excl. basmalahs, 327,514 incl. |
| rdsq-words-77430 | 77430 | 77429 | — | RDS-Q's stated rule (Tanzil tokens, basmalahs out) gives 77,433 on this file, not 77,430 — a 3-word gap the document does not explain; QAC words 77,429. |
| rdsq-letters-325666 | 325666 | 325386 | — | 325,666 reproduces under no letter convention tried (project convention 325,386 excl. basmalahs; 327,514 incl.) — a 280-letter gap with no stated rule to explain it. |
| botani-2012-distributions | 6348/77878/327792 | 6236/77429/325386 | — | Verses 6,348 reproduce (6,236 + 112 basmalahs); words 77,878 vs our 77,881 and letters 327,792 vs our 327,514 do not — both gaps unexplained. |
| quran-word-57-khalifa | 57 | 70 | — | Khalifa's own stated rule gives 59, not 57 (his table silently also excludes 13:31 and 41:44 on semantic grounds); the lemma total is 70. |
| wikiislam-critique | — | — | — | Not a word/letter count — a critique of counting tactics; no counting assumption applies. |
| dukes-atwell-2012 | — | — | — | Not a word/letter count — a bibliographic fact; no counting assumption applies. |
| hapax-legomena | 1620 | 1994 | — | No unit gives ~1,620 — lemma hapax 1,994, surface-form hapax 12,005, roots occurring once 395. |

## Status corrections

**None.** Recomputation confirmed every stored `our_status`. The tallies
moved to 37 confirmed / 17 differ / 9 cannot verify (35 Scholar
Findings / 21 Counted by this site / 7 Popular claims) when the
harun-yahya-populariser literature fact was dropped in the 2026-11-09
re-attribution; no stored status itself changed. Two numbers in the stored prose were found
to be one off, neither changing any status, and are recorded here rather
than by editing the stored fields:

- **jannah-jahannam-77** — the sense-correct bare-singular garden count is
  **66**, not 65: the 65 bare tokens in the four surface forms plus the
  construct spelling وجنتُ (56:89), which is a bare singular garden token.
  The stored note's '65 (unsuffixed singular)' counts only the four-form
  bare tokens. The finding stays `differs` (none of 66 / 70 / 147 is 77).
- **nun-132-vs-133** — the stored root-rule count 132 is the
  **basmalah-included** count (the merged basmalah of 68:1 contributes one
  ن); the strict A4 count with basmalahs excluded is **131**. The finding
  stays `differs` (133 requires Khalifa's stated spelled-out-initial rule).

## Parked / undecided (unchanged)

- **benefit-corrupt-50** — both sides are exactly 50 under A1, A2 and A6,
  so it reconciles under those sets in the table above; the
  differs→confirmed flip from `PASTED_PAGE_CHECK.md` is still unapproved
  by MK, so `our_status` stays `differs`.
- **mind-light-49** — light is 43 as the noun; 49 only if the adjective
  منير ('shining') is counted as 'light'. Left as `differs` for MK's call;
  no assumption set is recorded as reconciling it.
- **quran-word-57-khalifa** and **rdsq-words-77430** — the scholars' own
  stated rules, applied to the corpus, do NOT reproduce their claimed
  figures (59 not 57; 77,433 not 77,430). Both stay `differs`.
- **allah-2699 / verse-number-checksum-118123 / classical-word-totals /**
  **rdsq-words-77430 / dukes-unique-words / hapax-legomena** — the stored
  `verification_root_rule.count` field holds a different unit's number
  than A1 for these findings (lemma total, basmalah-included sum, Tanzil
  token count, or lemma hapax). The per-set numbers in the JSON are the
  corrected, unit-labelled figures; the stored fields were left untouched.


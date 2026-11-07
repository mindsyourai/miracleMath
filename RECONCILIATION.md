# Reconciliation — scholar findings vs our recount (2026-11-07)

MK's brief: reconcile the scholar findings against our findings, double-check everything, and explain
every difference. Two independent checkers did the work: **Checker A** re-ran all three counting scripts
and independently re-derived every `our_note` number from the corpus; **Checker B** verified every
scholar claim against its cited source (fetching the source pages). This file lists what changed.

## New tallies (64 findings)

| | Before | After |
|---|---|---|
| ✅ confirmed | 29 | **28** |
| ❌ differs | 28 | **25** |
| ❓ cannot verify | 7 | **11** |

`our_status` and `confidence` now agree on all 64 findings (confirmed ↔ "confirmed by our recount",
differs ↔ contested, cannot verify ↔ "reported, method unclear"). The old 29-vs-25 mismatch was 4
literature/provenance findings wrongly labelled "confirmed" although no scripted recount had reproduced
them (see below). By category now: paired counts 12/16/2, letter counts 4/3/0, Code 19 8/2/1,
corpus linguistics 4/4/8.

## Status flips (7 findings)

| Finding | Before → After | Why |
|---|---|---|
| `shaytan-angels-88` | differs → **confirmed** | Angels are 88 by QAC lemma `malak`: plural ملائكة 73 + 13 singular + 2 duals (2:102, 7:20). Our earlier note counted only 12 non-plural forms (missing the second 6:8 token, the 7:20 dual and 17:95) and stopped three short at ~85. |
| `trouble-peace-13` | differs → **confirmed** | The filed Arabic (ضر/سلام) was wrong. The counted words are الضيق/الطمأنينة; by QAC root D-y-q = 13 and T-m-n = 13 exactly. |
| `righteous-wicked-6-3` | differs → **confirmed** | The filed Arabic (صالح/طالح) was wrong. Yahya's words are الأبرار/الفجار: أبرار substring 6, فجار substring 3 — exact. |
| `harun-yahya-populariser` | confirmed → cannot verify | A literature fact, not a scripted recount — no count was reproduced for it. Same reason for the next three. |
| `khalifa-reception` | confirmed → cannot verify | Literature fact; also 5 cited items (Gardner SI p. 58; Sardar 1989; Yüksel 2011; Arik 2012; Stanley 2016) were not individually verified and are now flagged as such instead of asserted. |
| `tanzil-provenance` | confirmed → cannot verify | Literature/provenance fact; citation re-pointed to tanzil.net/docs/text_license and /docs/Medina_Mushaf (the download page shows neither). |
| `wikiislam-critique` | confirmed → cannot verify | Literature fact; Dr. Fahd al-Roomi's point was not located in the fetched WikiIslam text and is no longer asserted. |

## Scholar-side corrections (Checker B)

- **Man/woman 24/24 is not Yahya's.** Yahya's page says **23/23** (twice, with the 23-chromosomes gloss). The 24/24 figure is re-attributed to Tariq Al-Suwaidan's circulating list (also Mufti Afzal Hoosen Elias). Our recount still gives singular 24/24, so the status stays confirmed.
- **Life/death 145 is not Yahya's.** The words "life"/"death" do not occur on Yahya's page at all. Re-attributed to the circulating list (quranic-miracles.com, Al-Suwaidan, Elias). Status stays differs (no clean rule reproduces 145/145).
- **Sun/moon 33/27 conflated two claims.** Yahya pairs **sun with light, 33/33** ("only the simple forms of the word were included"); his page contains no "moon". Moon 27 is a separate widely-circulated claim (WikiIslam). The finding now states both separately; sun 33 and moon 27 reproduce exactly, light 33 only under the stated narrow selection of simple forms.
- **Four wrong Arabic terms in the Yahya pairs** (numbers were right, words were wrong): reward ثواب → **الجزاء**; refuge ملجأ → **المصير**; trouble/peace ضر/سلام → **الضيق/الطمأنينة**; righteous/wicked صالح/طالح → **الأبرار/الفجار**. With the right words, refuge is 28 exact (its pair differs by one on the 'forever' side, ابدا 29) and trouble/peace and righteous/wicked both become confirmed (see above).
- **Khalifa citations pointed at the wrong appendix page.** The Rahman/Rahim, Ism and Quran-57 tables are in **Appendix 1 Part 2** (submission.org/App1_p2.html), not Part 1. Quran-57 is also narrowed as Khalifa states it: raw 58, minus 10:15's "another Quran" = 57 "this Quran" (our recount gives 59 for the narrow selection, so it still differs).
- **Muqatta'at: wrong author, wrong arithmetic.** Author is **Halim Sayoud**, not "Khalifa Sayoud" (QURANICA 5(2), Dec 2013). The 3/10/13/2/1 breakdown sums to **75**, not 78; 78 counts surah 42's second set (عسق) separately. The SeekersGuidance URL cited contained none of this structure and is dropped.
- **All-28-letters verses: wrong citation.** Khalifa's Appendix 1 contains no such claim. Re-cited as a classical/traditional observation; the fact itself is verified by our recount (28 distinct letters in both 3:154 and 48:29).
- **QAC version confusion.** The v0.4 figure is **77,429** words, not 77,430 (77,430 is v0.3); **128,076 morphemes** is the v0.3 announcement, not v0.4 (our count of the v0.4 file is 128,219 segments).
- **Dead URLs fixed:** Dukes unique-words blogspot (404) — figures re-cited as the widely published estimate, Dukes-blog authorship unconfirmed, unverified "at most 7,000 unique words" dropped; abdulbaqi.io post moved to /2019/01/15/quranic_roots/ (that post is Abdul Baqi's; Dukes is the data source, not co-author).
- **Classical totals: variants real, citation incomplete.** The 77,797/77,934-word and 323,671/330,733-letter variants are genuine al-Suyuti variants but are not on the cited SeekersGuidance page (which gives only 77,439/77,437 words and 323,015 letters); the notes now cite al-Suyuti via the witnesses that carry them.
- **"Goodword Books, 2005" imprint dropped everywhere (29 Yahya sources).** It could not be confirmed; harunyahya.info's own book page cites "Araştırma Press", a circulating edition is Global Publishing, Istanbul.
- **Longest word:** the cited source (calendar-uk FAQ) confirms فأسقيناكموه as the longest word but gives no "11 letters" figure — the 11 is convention-dependent (10 under our convention), so the claim no longer asserts it.
- **Muhammad 4:** the figure is verified by our recount, but we could not locate it verbatim on the fetched Yahya article page — the note now says so honestly instead of implying a seen citation.

## Our-side corrections (Checker A — 12 items in `our_note` prose)

All three scripts re-ran byte-identical and **no Agent 1 (pairs) or Agent 2 (Names) number changed**. The
errors were in Agent 3's hand-written notes:

1. `human-being-65`: علقة is **6**, not 7 (the 7th is bare علق, 96:2).
2. `man-woman-24-24`: امرا substring is **46**, not 45; the extra token is سَامِرًا (23:67), not السامري; the -hu/-hi suffix labels were swapped; "with duals" now reads "with duals (plurals excluded)".
3. `muqattaat-structure-29-14-78`: initials match **29/29**, not 28/29; breakdown sums to 75, not 78 (see above).
4. `jannah-jahannam-77`: the extra جنة-substring token is **أَجِنَّةٌ (fetuses, 53:32)**, not a construct form. The note now also explains 77 vs 147: strict singular "garden" = 77; all gardens by lemma = 147 (Agent 1's pair) — both true under different stated rules; jahannam is 77 under both.
5. `wine-intoxication-6`: سكرة (50:19) was already inside the سكر 4, so it cannot be added; سكارى is **3** tokens (4:43 ×1, 22:2 ×2), not 2. Family total 7 either way.
6. `life-death-145`: **23** ظلم-forms contain مات (الظلمات 14 + ظلمات 8 + كظلمات 1), not 22.
7. `rdsq-words-77430`: the odd/even verse-group totals 38,716/38,714 did not reproduce under any natural grouping and are dropped.
8. `qac-word-count-77429` / `rdsq-words-77430`: the 77,433-vs-77,429 gap is **4 verses**, not just 37:130 — exactly 2:181, 8:6, 13:37 (بعدما) and 37:130 (آل ياسين), each differing by one token.
9. `reward-forgiveness-117-234`: forgiveness reproduces exactly as QAC root gh-f-r = **234**; reward root j-z-y = **118**, one more than the claimed 117.
10. `mind-light-49`: added the nur 43 (lemma) + muneer 6 route WikiIslam notes, and why we do not accept it (mixes noun "light" with adjective "shining").
11. `root-frequency-studies`: our recount gives **1,642** distinct roots, not 1,651 (and not Dukes' 1,685) — the root total depends on how rare/derived forms are grouped.
12. `tongue-sermon-25`: the counted word is "admonition", not "sermon".

## What did NOT change

- All Agent 1 pair counts and Agent 2 Name counts re-ran byte-identical; the independent recount confirmed them (including angels/devils 88:88 and Allah 2,699).
- 45 of 64 scholar claims were verified as stated, including all of the Code 19 anchors that reproduce (basmalah 19/114, qaf 57/57, surah 96, surah 110, verse checksum 118,123 under Khalifa's exclusions) and the corpus-linguistics figures that reproduce (18,994 unique surface forms, min 3,226 as published vs our 3,314 by lemma).
- 0 scholar claims were untraceable to any source — the failures were misattribution, wrong Arabic terms, wrong citations, or wrong sub-numbers, not invented claims.

## Remaining caveats

- `muhammad-4`: figure verified, Yahya attribution rests on the wider list tradition (see above).
- `khalifa-reception`: 5 items listed but explicitly not individually verified (see the finding).
- `text-fabric-quran`: the Zenodo DOI appears only as a badge image on the fetched repo page, so the DOI number was not legibly confirmed from that page.
- The reconciliation re-checked the findings against the corpus; the counts were not re-counted a third time beyond Checker A's independent verifier and the three scripts' re-runs.

## How to reproduce

`reconcile.py` applies every change above to `data/scholar_findings.json` (change log printed on stdout);
`regen_findings_md.py` regenerates `data/scholar_findings.md` from the JSON; `build.py` rebuilds `web/data.js`.
Checker A's verifier: `/tmp/checkerA_verify.py` (values in `/tmp/checkerA_values.json`); merge verification:
`/tmp/merge_verify.py`, `/tmp/merge_verify2.py`, `/tmp/merge_verify3.py`, `/tmp/mv4.py`.

# Scholar findings on the Quran corpus — miracleMath

Date: 2026-11-06. Corpus: Tanzil Quran Text, Uthmani script (corpus/quran-uthmani.txt), 6,236 verses, downloaded 2026-11-06 from tanzil.net.

Reconciled 2026-11-07 — every finding now states the scholar claim as sourced, our recount number, and the reason for any difference (see RECONCILIATION.md).

Methods pass 2026-11-08 — every finding now also carries the scholar's own method (stated / reconstructed / unstated / not a count), the exceptions to that method, verification under both the scholar's rule and our standard QAC root rule, and script-computed verse locations (see METHODS.md; full location lists in data/locations.json). Tallies after this pass: 37 confirmed / 17 differ / 10 cannot verify.

Assumptions pass 2026-11-08 — every finding now also carries named assumption sets (A1–A7) with per-set numbers and which sets reconcile the scholar's number with ours (see ASSUMPTIONS.md). Tallies unchanged: 37 confirmed / 17 differ / 10 cannot verify.

> **Read this first:** disputed numerology is presented here as *reported findings* — each with a source and a status — never as settled fact. “Confirmed” means our own scripted recount on the Tanzil file reproduces the claimed figure under a stated method; “differs” means it does not; “cannot verify” means no recount was possible or the claim needs sense disambiguation. The Nursi strand (Isaratul-I'jaz) is parked by MK's decision and is **not** covered here.

## Tally

- **Total findings: 64** — ✅ confirmed 37 · ❌ differs 17 · ❓ cannot verify 10

- Paired-count claims: 30 (confirmed 21, differs 8, cannot verify 1)
- Letter counts and the disconnected letters (muqatta'at): 7 (confirmed 4, differs 3, cannot verify 0)
- Code 19 — Rashad Khalifa's 'mathematical miracle': 11 (confirmed 8, differs 2, cannot verify 1)
- Modern corpus linguistics: 16 (confirmed 4, differs 4, cannot verify 8)

## Sections (split 2026-11-07)

- Scholar findings: 35 (confirmed 16, differs 10, cannot verify 9)
- Popular claims (Harun Yahya, Adnan Oktar): 29 (confirmed 21, differs 7, cannot verify 1)

Harun Yahya is the pen name of Adnan Oktar, a Turkish popular creationist author — not a scholarly source. He was convicted in Turkey in 2022 (8,658-year sentence, upheld 2024). His widely circulated claims are included so they can be tested against the corpus; inclusion is not endorsement. Each claim carries its recount label.

## Recount method

Whitespace tokens. Skeleton normalisation for matching: diacritics/tatweel removed; hamza variants normalised (أ إ آ ٱ → ا, ؤ → و, ئ → ي, ء dropped); dagger alif ٰ → ا, small waw ۥ → و, small yeh ۦ → ي are kept as letters for matching. Letter-counting convention: base letters count, including alef wasla ٱ as ا; dagger alif, small waw and small yeh are marks and do NOT count; standalone hamza ء counts. This convention reproduces the anchors: basmalah = 19 letters, 96:1-5 = 76 letters, 110:1 = 19 letters. 'Excl. unnumbered basmalahs' means excluding the 112 basmalahs merged into verse 1 of surahs 2-8 and 10-114 (the 2 numbered basmalahs, 1:1 and 27:30, are kept). Surah boundaries use the standard Hafs verse-count table (sums to 6,236).

Spot-recount script: [`scholar_spotcheck.py`](scholar_spotcheck.py) (corpus totals, Code 19 anchors, paired counts, letter counts, muqatta'at). The remaining Harun Yahya pairs were checked with a one-off substring batch (not kept as a deliverable; its numbers are quoted in the notes below).

## Paired-count claims

### dunya-akhira-115

**Claim:** The words 'world' (dunya) and 'hereafter' (akhira) each occur 115 times in the Quran.

**Arabic:** الدنيا / الآخرة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Our substring recount on the Tanzil Uthmani text: دنيا 115, اخرة 115 — exact match.

**Scholar's method (reconstructed):** plain substring count on the Tanzil skeleton text gives دنيا 115 and اخرة 115.

**Exceptions:** 29:20 (al-nash'a al-akhira, 'the latter creation') is inside the 115 akhira forms but means 'latter', not the Hereafter; it is counted as a form under both rules. Root dnw also gives adna (nearest/lower, 12), daniyah (3), dana (2) -- excluded by lemma. Root Axr (250 words) also gives masculine al-akhir ('the Last/the other') and plural forms -- excluded by the feminine-stem rule.

**Verification — scholar's rule:** 115 / 115 — Reconstructed: plain substring count on the Tanzil skeleton text gives دنيا 115 and اخرة 115. The source states no method; this is the selection that reproduces the claim.

**Verification — root rule:** 115 / 115 — QAC: LEM d~unoyaA = 115; akhira = feminine al-akhira stem forms ('aAxirapi/'aAxirapa/'aAxirapu) = 115. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A3, A6 · numbers by set: A1: 115 / 115, A2: 115 / 155, A3: 115 / 115, A6: 115 / 115 · Both sides are 115 under the root rule and the surface rule; the lemma rule gives akhira 155 (the masculine al-akhir and plural forms are a separate lemma).

**Locations (170 verses; verses per surah — 2: 13, 3: 12, 4: 5, 5: 3, 6: 7, 7: 7, 8: 2, 9: 5, 10: 7, 11: 6, 12: 4, 13: 2, 14: 2, 16: 7, 17: 7, 18: 4, 20: 3, 22: 3, 23: 3, 24: 4, 27: 4, 28: 7, 29: 4, 30: 2, 31: 3, 33: 3, 34: 3, 35: 1, 37: 1, 38: 1, 39: 4, 40: 3, 41: 4, 42: 2, 43: 2, 45: 2, 46: 1, 47: 1, 53: 3, 57: 1, 59: 1, 60: 1, 67: 1, 68: 1, 74: 1, 75: 1, 79: 2, 87: 2, 92: 1, 93: 1):** first 20: 2:4, 2:85, 2:86, 2:94, 2:102, 2:114, 2:130, 2:200, 2:201, 2:204, 2:212, 2:217, 2:220, 3:14, 3:22, 3:45, 3:56, 3:77, 3:85, 3:117 … (full list in data/locations.json)
**Locations — scholar's rule (170 verses):** 2:4, 2:85, 2:86, 2:94, 2:102, 2:114, 2:130, 2:200, 2:201, 2:204, 2:212, 2:217, 2:220, 3:14, 3:22, 3:45, 3:56, 3:77, 3:85, 3:117, 3:145, 3:148, 3:152, 3:176, 3:185, 4:74, 4:77, 4:94, 4:109, 4:134, 5:5, 5:33, 5:41, 6:29, 6:32, 6:70, 6:92, 6:113, 6:130, 6:150, 7:32, 7:45, 7:51, 7:147, 7:152, 7:156, 7:169, 8:42, 8:67, 9:38, 9:55, 9:69, 9:74, 9:85, 10:7, 10:23, 10:24, 10:64, 10:70, 10:88 …

### jannah-jahannam-77

**Claim:** The words 'paradise' (jannah) and 'hell' (jahannam) each occur 77 times.

**Arabic:** الجنة / جهنم

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Strict singular forms (الجنة/جنة with prefixes: الجنة 56 + جنة 18 + وجنة 2 + بالجنة 1) = 77; جهنم substring 77. The جنة substring alone is 78 — the one extra token is أَجِنَّةٌ (ajinnah, 'fetuses', 53:32), not a form of 'garden' (an earlier draft of this note called it a construct form). The popular 77/77 claim counts singular 'garden' only. Counting every garden by root/lemma (QAC lemma jan~ap: singular 71 + plural جنات 69 + dual 7) gives 147 — that is the 147 in Agent 1's heaven/hell pair (147:77), while hell (jahannam) is 77 under both rules. Both numbers are true under different stated rules: singular garden vs all gardens.

Methods pass (2026-11-08): confirmed→differs: 12 of the 77 exact surface forms are not 'garden' — جِنَّة (jinn/madness, 10 tokens) and جُنَّة (shield, 2). Sense-correct garden counts are 65 (unsuffixed singular), 70 (QAC lemma singular), 147 (all gardens) — none is 77. Hell is 77 under both rules.

**Scholar's method (reconstructed):** (sense-blind): exact surface forms الجنة 56 + جنة 18 + وجنة 2 + بالجنة 1 = 77; جهنم substring = 77.

**Exceptions:** The surface string الجنة/جنة does NOT mean 'garden' in 12 tokens that the popular 77 counts as paradise: جِنَّة (jinn/madness, LEM jin~ap) at 7:184, 11:119, 23:25, 23:70, 32:13, 34:8, 34:46, 37:158 (x2), 114:6, and جُنَّة (shield, LEM jun~ap) at 58:16, 63:2. A 13th look-alike, أَجِنَّة (ajinnah, 'fetuses', 53:32), is outside the four exact forms but inside the جنة substring (78 total). Plural جنات (69) and dual (8) are excluded by the singular-only reading.

**Verification — scholar's rule:** 77 / 77 — Reconstructed (sense-blind): exact surface forms الجنة 56 + جنة 18 + وجنة 2 + بالجنة 1 = 77; جهنم substring = 77. This is the selection that reproduces the claim -- but it counts 12 non-garden tokens as 'paradise' (see exceptions).

**Verification — root rule:** 147 / 77 — QAC: LEM jan~ap (all gardens) = 147 (singular 70 = 65 in the four surface forms + 1 construct spelling وجنتُ (56:89) + 4 suffixed; plural 69; dual 8); LEM jahan~am = 77. Sense-correct garden counts are 65 / 70 / 147 -- none is 77.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A3, A6 · numbers by set: A1: 147 / 77, A2: 147 / 77, A3: 77 / 77, A6: 77 / 77 · 77/77 reproduces only under the sense-blind surface-form rule; sense-correct garden is 66 (bare singular), 70 (lemma singular) or 147 (all gardens) — none is 77.

**Locations (220 verses; verses per surah — 2: 9, 3: 10, 4: 11, 5: 5, 6: 2, 7: 13, 8: 3, 9: 13, 10: 2, 11: 3, 13: 4, 14: 3, 15: 2, 16: 3, 17: 6, 18: 10, 19: 5, 20: 4, 21: 2, 22: 3, 23: 2, 25: 6, 26: 5, 29: 3, 31: 1, 32: 2, 34: 2, 35: 2, 36: 4, 37: 1, 38: 3, 39: 6, 40: 5, 41: 1, 42: 2, 43: 3, 44: 2, 45: 1, 46: 2, 47: 3, 48: 3, 50: 4, 51: 1, 52: 2, 53: 1, 54: 1, 55: 4, 56: 2, 57: 2, 58: 2, 59: 1, 61: 1, 64: 1, 65: 1, 66: 3, 67: 1, 68: 2, 69: 1, 70: 2, 71: 1, 72: 2, 74: 1, 76: 1, 78: 2, 79: 1, 81: 1, 85: 2, 88: 1, 89: 2, 98: 2):** first 20: 2:25, 2:35, 2:82, 2:111, 2:206, 2:214, 2:221, 2:265, 2:266, 3:12, 3:15, 3:133, 3:136, 3:142, 3:162, 3:185, 3:195, 3:197, 3:198, 4:13 … (full list in data/locations.json)
**Locations — scholar's rule (150 verses):** 2:35, 2:82, 2:111, 2:206, 2:214, 2:221, 2:265, 2:266, 3:12, 3:133, 3:142, 3:162, 3:185, 3:197, 4:55, 4:93, 4:97, 4:115, 4:121, 4:124, 4:140, 4:169, 5:72, 7:18, 7:19, 7:22, 7:27, 7:40, 7:41, 7:42, 7:43, 7:44, 7:46, 7:49, 7:50, 7:179, 7:184, 8:16, 8:36, 8:37, 9:35, 9:49, 9:63, 9:68, 9:73, 9:81, 9:95, 9:109, 9:111, 10:26, 11:23, 11:108, 11:119, 13:18, 13:35, 14:16, 14:29, 15:43, 16:29, 16:32 …

### shaytan-angels-88

**Claim:** The words 'devil' (shaytan) and 'angel' each occur 88 times.

**Arabic:** الشيطان / الملائكة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Devils: شيط 70 + شياطين 18 = 88. Angels: QAC lemma malak = 88 — plural ملائكة 73 + 13 singular + 2 duals (الملكين 2:102, ملكين 7:20). The singulars: 6:8 ×2 (ملك and ملكا — two tokens in one verse), 6:9, 6:50, 11:12, 11:31, 12:31, 17:95, 25:7, 32:11 (ملك الموت, Angel of Death), 53:26, 69:17, 89:22. Our earlier note counted only 12 non-plural forms (missing the second 6:8 token, the 7:20 dual and 17:95) and so stopped three short at about 85. The pair 88:88 is confirmed. Note: the bare surface form ملك/الملك totals 63 and mostly means 'king/sovereignty' — sense disambiguation is required, which the lemma count provides.

**Scholar's method (reconstructed):** شيط substring 70 + شياطين substring 18 = 88; angels by QAC lemma malak = 88 (73 plural + 13 singular + 2 dual).

**Exceptions:** Bare surface ملك/الملك (63 tokens) mostly means 'king/sovereignty', not angel -- sense disambiguation by QAC lemma is required. Angel singulars (13): 6:8 x2 (ملك and ملكا, two tokens in one verse), 6:9, 6:50, 11:12, 11:31, 12:31, 17:95, 25:7, 32:11 (ملك الموت, Angel of Death), 53:26, 69:17, 89:22. Duals (2): الملكين 2:102, ملكين 7:20. Plural ملائكة 73.

**Verification — scholar's rule:** 88 / 88 — Reconstructed: شيط substring 70 + شياطين substring 18 = 88; angels by QAC lemma malak = 88 (73 plural + 13 singular + 2 dual). The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 88 / 88 — QAC: ROOT $Tn (shaytan) = 88; LEM malak = 88. Whole ROOT mlk would be far larger (mulk dominion, malik king) -- the lemma narrowing is essential. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 88 / 88, A2: 88 / 88, A6: 88 / 88 · 88/88 reproduces under the root rule, the lemma rule and the reconstructed rule (devils by root $Tn, angels by lemma malak).

**Locations (162 verses; verses per surah — 2: 16, 3: 11, 4: 11, 5: 2, 6: 12, 7: 8, 8: 5, 11: 2, 12: 4, 13: 2, 14: 1, 15: 5, 16: 7, 17: 7, 18: 2, 19: 4, 20: 2, 21: 2, 22: 4, 23: 2, 24: 1, 25: 5, 26: 2, 27: 1, 28: 1, 29: 1, 31: 1, 32: 1, 33: 2, 34: 1, 35: 2, 36: 1, 37: 3, 38: 4, 39: 1, 41: 3, 42: 1, 43: 5, 47: 2, 53: 2, 58: 2, 59: 1, 66: 2, 67: 1, 69: 1, 70: 1, 74: 1, 78: 1, 81: 1, 89: 1, 97: 1):** first 20: 2:14, 2:30, 2:31, 2:34, 2:36, 2:98, 2:102, 2:161, 2:168, 2:177, 2:208, 2:210, 2:248, 2:268, 2:275, 2:285, 3:18, 3:36, 3:39, 3:42 … (full list in data/locations.json)

### day-365

**Claim:** The word 'day' (yawm) occurs 365 times, matching the days of a (Gregorian) year.

**Arabic:** يوم

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source; our recount reproduces 365 only under a stated selective method (see note).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Simple forms يوم/اليوم/يوما = 274; plus prefixed ويوم 44, واليوم 23, ليوم 8, فاليوم 8, بيوم 5, باليوم 2, وباليوم 1 = 365 exactly. Caveat: suffixed forms (يومكم, يومهم, يومئذ 65+), dual يومين and plural أيام are excluded by this method; all tokens containing يوم = 590, polluted by belief verbs (يؤمنون). The Islamic calendar has 354/355 days, so the Gregorian-365 framing is itself a critique point (WikiIslam).

**Scholar's method (stated):** Yahya's page states it: '"Day (yawm)" is repeated 365 times in singular form, while its plural and dual forms "days (ayyam and yawmayn)" together are repeated 30 times.' Units: the singular form of yawm, with prefixes (wa-/fa-/bi-/li-) counted in and suffixed forms (possessive pronouns) counted out; dual and plural counted separately.

**Exceptions:** Excluded by the stated singular-only rule, all named: 10 suffixed singulars (يومكم/يومهم at 6:130, 7:51, 21:103, 32:14, 39:71, 43:83, 45:34, 51:60, 52:45, 70:42); 3 duals (يومين at 2:203, 41:9, 41:12); 27 plurals (أيام); 70 يومئذ (yawma'idhin, 'on that day' -- QAC gives it no ROOT, LEM yawoma}i* only). The Islamic year is 354/355 days, so the Gregorian-365 framing is itself a critique point (WikiIslam).

**Verification — scholar's rule:** 365 — Stated rule verified: singular yawm without suffixes = 365 (simple يوم/اليوم/يوما 274 + prefixed ويوم 44, واليوم 23, ليوم 8, فاليوم 8, بيوم 5, باليوم 2, وباليوم 1). QAC agrees: singular yawm = 375, minus 10 suffixed = 365.

**Verification — root rule:** 475 — QAC: ROOT ywm = 405 (singular 375 + plural 27 + dual 3) + LEM yawoma}i* (yawma'idhin) 70 = 475. The 365 is a subset: it excludes the 10 suffixed singulars, 3 duals, 27 plurals and 70 yawma'idhin (110 tokens).

**Assumptions:** scholar set A5 · our set A1 · reconciles under: A3, A5 · numbers by set: A1: 475, A2: 405, A3: 365, A5: 365 · 365 is the stated singular, suffix-free selection; the whole root gives 475 (375 singular + 27 plural + 3 dual + 70 yawma'idhin).

**Locations (437 verses; verses per surah — 1: 1, 2: 22, 3: 17, 4: 10, 5: 9, 6: 10, 7: 10, 8: 3, 9: 12, 10: 8, 11: 14, 12: 2, 14: 8, 15: 3, 16: 10, 17: 7, 18: 6, 19: 8, 20: 10, 21: 3, 22: 8, 23: 6, 24: 5, 25: 9, 26: 8, 27: 3, 28: 9, 29: 4, 30: 7, 31: 1, 32: 5, 33: 3, 34: 4, 35: 1, 36: 5, 37: 5, 38: 6, 39: 8, 40: 14, 41: 7, 42: 3, 43: 5, 44: 4, 45: 7, 46: 5, 50: 8, 51: 3, 52: 5, 54: 4, 55: 2, 56: 2, 57: 4, 58: 4, 60: 2, 62: 1, 64: 1, 65: 1, 66: 2, 68: 3, 69: 7, 70: 7, 73: 2, 74: 2, 75: 8, 76: 4, 77: 15, 78: 5, 79: 4, 80: 4, 82: 4, 83: 6, 85: 1, 86: 1, 88: 2, 89: 2, 90: 1, 99: 2, 100: 1, 101: 1, 102: 1):** first 20: 1:4, 2:8, 2:48, 2:62, 2:80, 2:85, 2:113, 2:123, 2:126, 2:174, 2:177, 2:184, 2:185, 2:196, 2:203, 2:212, 2:228, 2:232, 2:249, 2:254 … (full list in data/locations.json)
**Locations — scholar's rule (341 verses):** 1:4, 2:8, 2:48, 2:62, 2:85, 2:113, 2:123, 2:126, 2:174, 2:177, 2:212, 2:228, 2:232, 2:249, 2:254, 2:259, 2:264, 2:281, 3:9, 3:25, 3:30, 3:55, 3:77, 3:106, 3:114, 3:155, 3:161, 3:166, 3:180, 3:185, 3:194, 4:38, 4:39, 4:59, 4:87, 4:109, 4:136, 4:141, 4:159, 4:162, 5:3, 5:5, 5:14, 5:36, 5:64, 5:69, 5:109, 5:119, 6:12, 6:15, 6:22, 6:73, 6:93, 6:128, 6:141, 6:158, 7:14, 7:32, 7:51, 7:53 …

### month-12

**Claim:** The word 'month' (shahr) occurs 12 times, matching the months of a year.

**Arabic:** شهر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source; our recount reproduces 12 only under a stated selective method (see note).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Simple شهر/الشهر/شهرا = 10; plus بالشهر 1, والشهر 1 = 12 exactly. Dual شهرين (2) and plural أشهر (5) + الأشهر (1) are excluded by this method.

**Scholar's method (reconstructed):** simple شهر/الشهر/شهرا 10 + بالشهر 1 + والشهر 1 = 12.

**Exceptions:** Excluded by the singular-only selection: 2 duals (شهرين at 4:92, 58:4) and 7 plurals (أشهر 6 + الشهور 1 at 9:36). All 12 counted forms are singular شهر.

**Verification — scholar's rule:** 12 — Reconstructed: simple شهر/الشهر/شهرا 10 + بالشهر 1 + والشهر 1 = 12. The source states no method; this is the selection that reproduces the claim.

**Verification — root rule:** 21 — QAC: ROOT $hr / LEM $ahor = 21 (singular 12 + dual 2 + plural 7). The 12 is the singular-only subset.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A3, A6 · numbers by set: A1: 21, A2: 21, A3: 12, A6: 12 · 12 is the singular-only selection; the root/lemma total is 21 (12 singular + 2 dual + 7 plural).

**Locations (17 verses):** 2:185, 2:194, 2:197, 2:217, 2:226, 2:234, 4:92, 5:2, 5:97, 9:2, 9:5, 9:36, 34:12, 46:15, 58:4, 65:4, 97:3
**Locations — scholar's rule (9 verses):** 2:185, 2:194, 2:217, 5:2, 5:97, 9:36, 34:12, 46:15, 97:3

### salawat-5

**Claim:** The word for the (five daily) prayers (salawat) occurs 5 times.

**Arabic:** صلوات

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 7 tokens match صلوات, at 2:157, 2:238, 9:99, 9:103, 11:87, 22:40, 23:9. The 5 plural صلوات are 2:157, 2:238, 9:99, 22:40, 23:9; 9:103 and 11:87 are singular صلاة written صلوة in Uthmani. Only 3 of the 5 mean 'prayers' (2:157 = blessings, 22:40 = synagogues) — WikiIslam's sense critique.

**Scholar's method (reconstructed):** plural surface form صلوات = 5 (QAC plural stems Salawa`tN/Salawa`ti/S~alawa`ti).

**Exceptions:** The 5 plural صلوات are at 2:157, 2:238, 9:99, 22:40, 23:9. Two further tokens match the صلوات substring but are singular صلاة written صلوة in Uthmani (9:103, 11:87) -- excluded. Sense: only 3 of the 5 mean 'prayers' (2:157 = blessings, 22:40 = synagogues/churches -- WikiIslam's sense critique).

**Verification — scholar's rule:** 5 — Reconstructed: plural surface form صلوات = 5 (QAC plural stems Salawa`tN/Salawa`ti/S~alawa`ti). The source states no method; this is the selection that reproduces the claim.

**Verification — root rule:** 5 — QAC: LEM Salaw`p plural stems = 5; the same lemma covers singular صلاة (78 words, incl. the 2 صلوة spellings). Both rules agree on 5.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A3, A6 · numbers by set: A1: 5, A2: 83, A3: 5, A6: 5 · 5 is the plural surface form صلوات (and the plural stems of the lemma); the whole lemma is 83 words.

**Locations (5 verses):** 2:157, 2:238, 9:99, 22:40, 23:9
**Locations — scholar's rule (5 verses):** 2:157, 2:238, 9:99, 22:40, 23:9

### sea-land-32-13

**Claim:** The word 'sea' occurs 32 times and 'land' 13 times (the ratio 13/45 = 29% land, 71% sea, matching the Earth's surface).

**Arabic:** البحر / البر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Sea: البحر 23 + والبحر 9 = 32 confirmed (all بحر tokens 40, incl. dual البحرين 4). Land: the البر-form total is 21 (البر 19 + prefixed forms), mixing 'land' and 'righteousness/piety' senses (e.g. 2:177); the figure 13 requires sense disambiguation we did not perform, so the pair as stated cannot be verified. The 29:71 land/sea ratio claim therefore cannot be verified as stated.

Methods pass (2026-11-08): cannot_verify→differs: land-sense البرّ occurs 12 times, not 13 (the other 10 LEM bar~ tokens are piety/righteousness). Sea (definite singular البحر) is 32, confirmed.

**Scholar's method (unstated):** method not stated by the source

**Exceptions:** Sea: البحر 23 + والبحر 9 = 32 (definite singular only); excluded are the dual البحرين (4), plural البحار (2), indefinite بحر (1), أبحر (1) and البحران (1) -- sea-sense total 41, plus بحيرة (a slit-eared camel, 5:103) which shares ROOT bHr but is not sea. Land: LEM bar~ = 22 tokens, of which 12 are land-sense (5:96, 6:59, 6:63, 6:97, 10:22, 17:67, 17:68, 17:70, 27:63, 29:65, 30:41, 31:32) and 10 are not land: الأبرار (the righteous) x6 (3:193, 3:198, 76:5, 82:13, 83:18, 83:22), برًّا (dutiful) x2 (19:14, 19:32), البرّ (the Benign, a divine name) 52:28, بررة (dutiful) 80:16.

**Verification — scholar's rule:** 32 / None — Sea 32 reproduces under the definite-singular selection. Land 13 does NOT reproduce: sense-classified land = 12 (see exceptions). No stated or reconstructable rule gives 13.

**Verification — root rule:** 41 / 12 — QAC: LEM baHor (sea-sense) = 41; LEM bar~ land-sense = 12 (of 22 bar~ tokens; the rest are piety/righteousness). Whole ROOT brr = 32 (bar~ 22 + bir~ piety 8 + tabar~u 2) -- coincidentally the sea number, not the land number.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: 41 / 12, A2: 41 / 12, A3: 32 / 21 · Sea 32 reproduces as definite singular البحر; land 13 reproduces under no rule — sense-correct land is 12, surface البر is 21.

**Locations (42 verses):** 2:50, 2:164, 5:96, 6:59, 6:63, 6:97, 7:138, 7:163, 10:22, 10:90, 14:32, 16:14, 17:66, 17:67, 17:68, 17:70, 18:60, 18:61, 18:63, 18:79, 18:109, 20:77, 22:65, 24:40, 25:53, 26:63, 27:61, 27:63, 29:65, 30:41, 31:27, 31:31, 31:32, 35:12, 42:32, 44:24, 45:12, 52:6, 55:19, 55:24, 81:6, 82:3
**Locations — scholar's rule (31 verses):** 2:50, 2:164, 5:96, 6:59, 6:63, 6:97, 7:138, 7:163, 10:22, 10:90, 14:32, 16:14, 17:66, 17:67, 17:70, 18:61, 18:63, 18:79, 18:109, 20:77, 22:65, 26:63, 27:63, 30:41, 31:27, 31:31, 42:32, 44:24, 45:12, 52:6, 55:24

### man-woman-24-24

**Claim:** The words 'man' and 'woman' (singular) each occur 24 times.

**Arabic:** رجل / امرأة

**Source:** Tariq Al-Suwaidan (circulating list; also Mufti Afzal Hoosen Elias, 'Astonishing Facts about the Qur'aan'), *'Mathematical Miracles of the Holy Quran' (circulating list)* — <https://www.scribd.com/document/45864275/Mathematical-Miracles-of-the-Holy-Quran>

**Section:** Scholar findings

**Corpus and method:** Method not stated by the source. (Note: Harun Yahya's published list gives 23/23; the 24/24 figure is from the circulating Al-Suwaidan/Elias list.)

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Man singular (رجل family): رجل 13 + رجلا 7 + لرجل 2 + فرجل 1 + ورجلا 1 = 24. Woman singular (امرأة family): امرات 6 + امراتهو 5 + امراة 3 + وامراتهو 2 + امراتك 2 + امراتى 2 + وامراتى 1 + لامراتهي 1 + وامراة 1 + وامرات 1 = 24. (An earlier draft of this note mislabelled the -hu/-hi suffixes as امراتهي/لامراتهو — corrected here.) Harun Yahya's own list gives 23/23 — one short on each side — so the 24/24 figure belongs to the circulating Al-Suwaidan/Elias list, not to Yahya. With duals (plurals excluded): man 30, woman 26; with plurals (رجال 27, نساء 59) the root totals are 57/85. Naive substrings: رجل 45, امرا 46 — the امرا count includes امرأ 'man' 19 and the extra token سَامِرًا (23:67, 'chatting by night'), not السامري as an earlier draft said (السامري contains no امرا substring).

**Scholar's method (reconstructed):** (Al-Suwaidan/Elias list, not Yahya's): singular surface forms = 24/24.

**Exceptions:** Man singular (24): رجل 13 (رجلٌ 7 + رجلٍ 5 + رجلٌۢ 1) + رجلا 7 + لرجل 2 + فرجل 1 + ورجلا 1. Woman singular (24): امرأت 6 + امرأته 5 + امرأة 3 + وامرأته 2 + امرأتك 2 + امرأتي 2 + وامرأتي 1 + لامرأته 1 + وامرأة 1 + وامرأت 1. Excluded from the 24/24: duals (man رجلين/رجلان 5; woman امرأتان/امرأتين 2) and plurals (رجال 28, نساء 59). Yahya's own page gives 23/23 -- one short on each side -- and no principled exclusion produces 23 from the 24 singulars.

**Verification — scholar's rule:** 24 / 24 — Reconstructed (Al-Suwaidan/Elias list, not Yahya's): singular surface forms = 24/24. Yahya's stated number is 23/23; the one-token exclusion that would give 23 is not stated anywhere and cannot be reconstructed. Scribd source for the Al-Suwaidan list was not fetched (Scribd blocks text fetch); the 24/24 is verified from the corpus, not from the source.

**Verification — root rule:** 57 / 85 — QAC: LEM rajul 29 (24 singular + 5 dual) + LEM rijaAl (men, plural) 28 = 57; LEM {mora>at 26 (24 singular + 2 dual) + LEM nisaA^' (women) 59 = 85. The 24/24 is the singular-only subset on both sides.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A3, A6 · numbers by set: A1: 57 / 85, A2: 29 / 26, A3: 24 / 24, A6: 24 / 24 · 24/24 is the singular-only surface selection; root totals are 57/85, singular lemmas 29/26.

**Locations (115 verses; verses per surah — 2: 12, 3: 5, 4: 20, 5: 2, 6: 1, 7: 9, 9: 1, 10: 1, 11: 3, 12: 5, 14: 1, 15: 1, 16: 2, 17: 1, 18: 2, 19: 2, 21: 1, 22: 1, 23: 2, 24: 3, 25: 1, 27: 3, 28: 5, 29: 3, 33: 9, 34: 2, 36: 1, 38: 1, 39: 1, 40: 2, 43: 1, 48: 1, 49: 1, 51: 1, 58: 2, 65: 2, 66: 2, 72: 1, 111: 1):** first 20: 2:49, 2:187, 2:222, 2:223, 2:226, 2:228, 2:231, 2:232, 2:235, 2:236, 2:239, 2:282, 3:14, 3:35, 3:40, 3:42, 3:61, 4:1, 4:3, 4:4 … (full list in data/locations.json)
**Locations — scholar's rule (43 verses):** 2:282, 3:35, 3:40, 4:12, 4:128, 6:9, 7:63, 7:69, 7:83, 7:155, 10:2, 11:71, 11:78, 11:81, 12:21, 12:30, 12:51, 15:60, 17:47, 18:37, 19:5, 19:8, 23:25, 23:38, 25:8, 27:23, 27:57, 28:9, 28:20, 29:32, 29:33, 33:4, 33:50, 34:7, 34:43, 36:20, 39:29, 40:28, 43:31, 51:29, 66:10, 66:11, 111:4

### life-death-145

**Claim:** The words 'life' (hayat) and 'death' (mawt) each occur 145 times.

**Arabic:** الحياة / الموت

**Source:** Circulating list (quranic-miracles.com; Tariq Al-Suwaidan; Mufti Afzal Hoosen Elias), *'Word repetitions' — circulating mathematical-miracle list* — <https://www.quranic-miracles.com/miracles/mathematical/word-repetitions>

**Section:** Scholar findings

**Corpus and method:** Method not stated by the source. (Note: Harun Yahya's published list does not include this pair; it circulates on other sites, e.g. quranic-miracles.com.)

**Our status:** ❌ differs · **confidence:** contested

**Our note:** حياة family (حيو/حيي/حيا) = 125; الحياة noun = 67. موت family = 171 (موت/ميت/مات, after removing the 23 ظلم-forms (الظلمات 14 + ظلمات 8 + كظلمات 1) and 14 كلمات-forms false positives caught by the مات substring — an earlier draft of this note said 22 ظلم-forms, omitting كظلمات); الموت noun = 35; موت substring = 91. No straightforward form/root count reproduces 145/145. This pair is not in Harun Yahya's published list; it circulates on other sites.

**Scholar's method (unstated):** method not stated by the source

**Exceptions:** Life: noun الحياة (LEM Hayaw`p) 76; whole ROOT Hyy 184 (noun 76 + أحيا 'give life' 51 + حيّ 'living' 24 + يستحيي 9 -- of which 2:26 and 33:53 are 'shy', the rest 'spare alive' -- + تحية 'greeting' 6, حياة senses etc.); excluded: حيّة 'snake' (20:20) and shyness. Death: noun الموت (LEM mawot) 50; whole ROOT mwt 165 (noun 50 + مات 'died' 39 + ميّت 'dead' 38 + أمات 'cause to die' 21 + ميتة 'carrion' 6 + موت forms). The circulating list (quranic-miracles.com, fetched 2026-11-07) states no method and gives no form list.

**Verification — scholar's rule:** None / None — No rule reproduces 145/145. Tested: noun 76/50; whole-root 184/165; substring حياة-family 125 / موت-family 171 (after removing ظلمات/كلمات false positives); broad families (root_counts_script) do not reach 145 either.

**Verification — root rule:** 184 / 165 — QAC whole-root: Hyy 184, mwt 165. Noun-only: Hayaw`p 76, mawot 50. Neither pairing is 145/145.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: 184 / 165, A2: 76 / 50, A3: 125 / 171 · No rule reproduces 145/145 — whole roots 184/165, nouns 76/50, surface families 125/171.

**Locations (239 verses; verses per surah — 2: 26, 3: 17, 4: 9, 5: 4, 6: 13, 7: 8, 8: 3, 9: 5, 10: 9, 11: 2, 13: 3, 14: 5, 15: 1, 16: 6, 17: 1, 18: 4, 19: 5, 20: 6, 21: 3, 22: 3, 23: 7, 24: 2, 25: 4, 26: 1, 27: 1, 28: 5, 29: 4, 30: 6, 31: 2, 32: 1, 33: 5, 34: 1, 35: 4, 36: 5, 37: 4, 39: 3, 40: 6, 41: 3, 42: 2, 43: 3, 44: 3, 45: 5, 46: 2, 47: 3, 49: 1, 50: 4, 53: 2, 56: 2, 57: 3, 58: 1, 62: 2, 63: 1, 67: 1, 75: 1, 77: 1, 79: 1, 80: 1, 87: 2, 89: 1):** first 20: 2:19, 2:26, 2:28, 2:49, 2:56, 2:73, 2:85, 2:86, 2:94, 2:96, 2:132, 2:133, 2:154, 2:161, 2:164, 2:173, 2:179, 2:180, 2:204, 2:212 … (full list in data/locations.json)

### sun-moon-33-27

**Claim:** Harun Yahya pairs 'sun' (shams) and 'light' (nur), each 33 times, counting simple forms only; separately, 'moon' (qamar) occurs 27 times.

**Arabic:** الشمس / النور (and القمر 27, separate claim)

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Yahya's rule for sun/light: 'only the simple forms of the word were included'. Moon 27 is a separate widely-circulated claim (WikiIslam), not paired with sun by Yahya — Yahya's page contains no 'moon' at all.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Sun: شمس substring 33 exact. Moon: قمر substring 27 exact. Light: نور substring 46; lemma nuwr 43; the claimed 33 is reproduced only by a narrow selection of simple forms — نور 8 + النور 10 + نورا 9 + والنور 3 + بنور 1 + نورهم 2 = 33 — excluding نورنا/نوركم and منير ('shining') forms. So the sun+light 33/33 pair is confirmed under that stated selection, and moon 27 stands on its own. An earlier draft of this finding conflated the two claims into one sun/moon pair.

**Scholar's method (stated):** Yahya's page states for light: 'In counting the word "light" only the simple forms of the word were included.' Sun and moon carry no method statement on the page; the moon 27 is a separate claim (WikiIslam), not paired with sun by Yahya -- his page contains no 'moon' at all. Units: simple surface forms.

**Exceptions:** Light simple forms counted: نور 8 + النور 10 + نورا 9 + والنور 3 + بنور 1 + نورهم 2 = 33. Excluded: نورنا/نوركم (suffixed) and منير 'shining' forms (6). Sun: شمس substring 33, all sun-sense, no look-alikes. Moon: قمر substring 27, all moon-sense.

**Verification — scholar's rule:** 33 / 33 / 27 — Stated rule verified: sun شمس substring = 33; light simple forms = 33 (selection above); moon قمر substring = 27. The pair is really sun/light 33/33 plus a separate moon 27.

**Verification — root rule:** 33 / 27 / 43 — QAC: ROOT $ms (sun) = 33; ROOT qmr (moon) = 27; LEM nuwr (light) = 43, or 49 counting LEM m~uniyr ('shining', 6). Sun and moon agree under both rules; light is 33 only under Yahya's stated simple-forms selection.

**Assumptions:** scholar set A5 · our set A1 · reconciles under: A3, A5 · numbers by set: A1: 33 / 43 / 27, A2: 33 / 43 / 27, A3: 33 / 33 / 27, A5: 33 / 33 / 27 · 33/33/27 reproduces under Yahya's stated simple-forms rule and the surface rule; the root/lemma rule gives light 43 (49 with منير).

**Locations (71 verses; verses per surah — 2: 3, 4: 1, 5: 4, 6: 6, 7: 2, 9: 1, 10: 1, 12: 1, 13: 2, 14: 3, 16: 1, 17: 1, 18: 3, 20: 1, 21: 1, 22: 1, 24: 2, 25: 2, 27: 1, 29: 1, 31: 1, 33: 1, 35: 2, 36: 3, 39: 3, 41: 1, 42: 1, 50: 1, 54: 1, 55: 1, 57: 5, 61: 1, 64: 1, 65: 1, 66: 1, 71: 1, 74: 1, 75: 2, 76: 1, 81: 1, 84: 1, 91: 2):** first 20: 2:17, 2:257, 2:258, 4:174, 5:15, 5:16, 5:44, 5:46, 6:1, 6:77, 6:78, 6:91, 6:96, 6:122, 7:54, 7:157, 9:32, 10:5, 12:4, 13:2 … (full list in data/locations.json)
**Locations — scholar's rule (67 verses):** 2:257, 2:258, 4:174, 5:15, 5:16, 6:1, 6:77, 6:78, 6:91, 6:96, 6:122, 7:54, 7:157, 9:32, 10:5, 12:4, 13:2, 13:16, 14:1, 14:5, 14:33, 16:12, 17:78, 18:17, 18:86, 18:90, 20:130, 21:33, 22:18, 24:35, 24:40, 25:45, 25:61, 27:24, 29:61, 31:29, 33:43, 35:13, 35:20, 36:38, 36:39, 36:40, 39:5, 39:22, 39:69, 41:37, 42:52, 50:39, 54:1, 55:5, 57:9, 57:12, 57:13, 57:28, 61:8, 64:8, 65:11, 66:8, 71:16, 74:32 …

### muhammad-4

**Claim:** The name 'Muhammad' occurs 4 times in the Quran.

**Arabic:** محمد

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** محمد substring = 4. Attribution note: we could not locate 'Muhammad 4' verbatim on the fetched Yahya article page, so the attribution to Yahya's list rests on the wider list tradition, not on a line seen on that page; the figure itself is verified by our recount.

**Scholar's method (reconstructed):** plain surface count محمد = 4.

**Exceptions:** The name occurs at 3:144, 33:40, 47:2, 48:29. Excluded: أحمد (Ahmad, 61:6) -- a different name for the same person, not counted. The attribution to Yahya's list rests on the wider list tradition: the fetched Yahya article page does not contain 'Muhammad 4' verbatim.

**Verification — scholar's rule:** 4 — Reconstructed: plain surface count محمد = 4. The source states no method; this is the selection that reproduces the claim.

**Verification — root rule:** 4 — QAC: LEM muHam~ad = 4. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A3, A6 · numbers by set: A1: 4, A2: 4, A3: 4, A6: 4 · 4 under every rule tried (surface, lemma and root-narrowed).

**Locations (4 verses):** 3:144, 33:40, 47:2, 48:29
**Locations — scholar's rule (4 verses):** 3:144, 33:40, 47:2, 48:29

### iman-kufr-25

**Claim:** The words 'belief' (iman) and 'disbelief' (kufr) each occur 25 times.

**Arabic:** إيمان / كفر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Naive substring counts: ايمان 86, كفر 343 — far from 25/25. Yahya's wording is 'faith (iman) (without genitive) is repeated 25 times… as is also the word infidelity (kufr)' — the 25 figure must rest on a very narrow form selection (excluding genitive constructions) that the source does not state in countable detail, so it does not reproduce under any clean rule we could state. The circulating quranic-miracles.com list gives iman/kufr as 17, not 25.

Methods pass (2026-11-08): differs→confirmed: bare (unsuffixed) noun forms reproduce exactly — bare إيمان 25, bare كفر 25 (QAC). Yahya's '(without genitive)' = no possessive suffix.

**Scholar's method (stated):** Yahya's page states the qualifier: 'The word faith (iman) (without genitive) is repeated 25 times throughout the Qur'an as is also the word infidelity (kufr).' Units: the nouns إيمان / كفر, with the genitive excluded. What '(without genitive)' means in practice is reconstructed below (see verification note); the qualifier itself is verbatim from the source.

**Exceptions:** Genitive in Arabic covers the possessive pronoun suffixes (إيمانهم/إيمانكم/كفرهم -- the suffix is a genitive pronoun). Bare (unsuffixed) tokens: iman 25 (GEN-case 12 + ACC-case 11 + NOM-case 2); kufr 25 (ACC-case 14 + GEN-case 10 + NOM-case 1). Suffixed tokens excluded: iman 20, kufr 12. The alternative reading -- excluding all GEN-case tokens -- gives 21 (iman) and 20 (kufr) and does NOT reproduce 25. The circulating list (quranic-miracles.com) gives iman/kufr as 17, not 25.

**Verification — scholar's rule:** 25 / 25 — Reconstructed implementation of the stated qualifier: bare (unsuffixed) noun forms give exactly 25/25 (QAC LEM <iyma`n bare 25; LEM kufor bare 25). Both words occur together in several of the same verses (2:108, 3:167, 3:177, 9:23, 16:106, 49:7).

**Verification — root rule:** 45 / 37 — QAC noun-only (root narrowed by lemma to the intended sense): LEM <iyma`n = 45, LEM kufor = 37. The 25/25 is the bare-noun subset. Broader sense-level families: belief (verb آمن 537 + مؤمن 202 + إيمان 45 + مؤمنات 22 + مؤمنة 6) = 812; disbelief (ROOT kfr minus كفّارة 'expiation') = 507.

**Assumptions:** scholar set A5 · our set A1 · reconciles under: A3, A5 · numbers by set: A1: 45 / 37, A2: 45 / 37, A3: 25 / 25, A5: 25 / 25 · 25/25 is the bare (unsuffixed) noun selection — Yahya's stated '(without genitive)'; lemma totals are 45/37.

**Locations (67 verses; verses per surah — 2: 6, 3: 11, 4: 5, 5: 5, 6: 2, 8: 1, 9: 9, 10: 2, 14: 1, 16: 1, 18: 1, 30: 2, 31: 1, 32: 1, 33: 1, 35: 1, 39: 2, 40: 3, 42: 1, 48: 1, 49: 4, 52: 1, 58: 1, 59: 2, 60: 1, 74: 1):** first 20: 2:88, 2:93, 2:108, 2:109, 2:143, 2:217, 3:52, 3:80, 3:86, 3:90, 3:100, 3:106, 3:167, 3:173, 3:176, 3:177, 3:193, 4:25, 4:46, 4:137 … (full list in data/locations.json)
**Locations — scholar's rule (43 verses):** 2:108, 2:217, 3:52, 3:80, 3:90, 3:167, 3:173, 3:176, 3:177, 3:193, 4:137, 5:5, 5:41, 5:61, 5:64, 5:68, 8:2, 9:12, 9:17, 9:23, 9:37, 9:74, 9:97, 9:107, 9:124, 14:28, 16:106, 18:80, 30:56, 33:22, 39:7, 40:10, 42:52, 48:4, 49:7, 49:11, 49:14, 49:17, 52:21, 58:22, 59:9, 59:10, 74:31

### zakah-blessing-32

**Claim:** The words 'charity' (zakah) and 'blessing' (barakah) each occur 32 times.

**Arabic:** الزكاة / البركة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** زك substring 67 (incl. الزكاة, زكاة, يزكي and derived verb forms); برك substring 5. Neither side is near 32 under a simple substring count.

Methods pass (2026-11-08): differs→confirmed: by lemma/root, zakah (LEM zakaw`p) is exactly 32 and blessing (ROOT brk) is exactly 32. The old substring test was the wrong unit.

**Scholar's method (reconstructed):** zakah noun (LEM zakaw`p) = 32; blessing by ROOT brk = 32.

**Exceptions:** Zakah: noun الزكاة (LEM zakaw`p) 32; excluded are the same-root purify verbs (زكّى 12, تزكّى 8, أزكى 4, زكيّ 2 -- ROOT zkw total 59). Blessing: ROOT brk 32, all blessing-sense lemmas (مبارك 8, تبارك 9, بركة 3, بارك 8, مباركة 4). The برك substring (5) misses بارك/تبارك because of the alif; the زك substring (67) catches the purify verbs.

**Verification — scholar's rule:** 32 / 32 — Reconstructed: zakah noun (LEM zakaw`p) = 32; blessing by ROOT brk = 32. The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 32 / 32 — QAC: LEM zakaw`p = 32; ROOT brk = 32. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 32 / 32, A2: 32 / 32, A3: 67 / 5, A6: 32 / 32 · 32/32 reproduces under the root and lemma rules; plain substrings give 67/5.

**Locations (63 verses; verses per surah — 2: 5, 3: 1, 4: 2, 5: 2, 6: 2, 7: 4, 9: 4, 11: 2, 17: 1, 18: 1, 19: 3, 21: 4, 22: 2, 23: 3, 24: 4, 25: 3, 27: 2, 28: 1, 30: 1, 31: 1, 33: 1, 34: 1, 37: 1, 38: 1, 40: 1, 41: 2, 43: 1, 44: 1, 50: 1, 55: 1, 58: 1, 67: 1, 73: 1, 98: 1):** first 20: 2:43, 2:83, 2:110, 2:177, 2:277, 3:96, 4:77, 4:162, 5:12, 5:55, 6:92, 6:155, 7:54, 7:96, 7:137, 7:156, 9:5, 9:11, 9:18, 9:71 … (full list in data/locations.json)

### say-they-said-332

**Claim:** The word 'say' (qul) occurs 332 times and 'they said' (qalu) 332 times.

**Arabic:** قل / قالوا

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 'They said' (قالوا substring) = 332 exactly. 'Say' (قل, imperative, exact-form count after stripping prefixes) = 333 — one more than the claimed 332. The قال family as a whole (substring) is 932.

Methods pass (2026-11-08): differs→confirmed: singular imperative قل is 332 exactly (293 + 18 + 21 by prefix, QAC LEM qaAla IMPV 2MS) and قالوا is 332 (QAC PERF 3MP).

**Scholar's method (reconstructed):** singular imperative قل (QAC LEM qaAla, IMPV, 2MS) = 332; قالوا = 332 (surface and QAC PERF 3MP agree).

**Exceptions:** "Say" is the 2nd-person masculine singular imperative قُلْ: قُلْ 293 (قُلْ 218 + قُل 45 + قُلِ 30) + فَقُلْ 18 + وَقُلْ 21 = 332. Excluded from 'say': plural/dual/feminine imperatives قولوا (17 tokens: وقولوا 8, قولوا 2, فقولوا 2, فقولا 3, فقولي 1, وقلن 1) and the jussive وَلْيَقُولُوا (1) -- 350 imperatives in all. 'They said' is the perfect 3rd-person masculine plural قالوا (332: قالوا/وقالوا/فقالوا/لقالوا); the imperfect يقولون ('they say') is a different form and is excluded.

**Verification — scholar's rule:** 332 / 332 — Reconstructed: singular imperative قل (QAC LEM qaAla, IMPV, 2MS) = 332; قالوا = 332 (surface and QAC PERF 3MP agree). The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 332 / 332 — QAC: LEM qaAla IMPV 2MS = 332; LEM qaAla PERF 3MP قالوا = 332. Whole ROOT qwl = 1722 (all 'say/said' forms). Both rules agree on 332/332.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 332 / 332, A2: 332 / 332, A3: 333 / 332, A6: 332 / 332 · 332/332 reproduces under the lemma/POS rule; the plain surface count of قل gives 333 (one non-imperative token).

**Locations (603 verses; verses per surah — 2: 40, 3: 28, 4: 9, 5: 23, 6: 46, 7: 34, 8: 6, 9: 15, 10: 24, 11: 13, 12: 22, 13: 6, 14: 5, 15: 9, 16: 5, 17: 24, 18: 14, 19: 4, 20: 12, 21: 16, 22: 3, 23: 16, 24: 5, 25: 9, 26: 15, 27: 12, 28: 9, 29: 9, 30: 1, 31: 2, 32: 3, 33: 8, 34: 20, 35: 2, 36: 7, 37: 6, 38: 8, 39: 16, 40: 7, 41: 11, 42: 2, 43: 9, 44: 1, 45: 4, 46: 10, 47: 2, 48: 3, 49: 3, 51: 5, 52: 2, 54: 2, 56: 1, 57: 1, 58: 1, 60: 1, 61: 1, 62: 3, 63: 1, 64: 2, 67: 8, 68: 3, 71: 1, 72: 5, 74: 1, 79: 2, 83: 1, 109: 1, 112: 1, 113: 1, 114: 1):** first 20: 2:11, 2:13, 2:14, 2:25, 2:30, 2:32, 2:67, 2:68, 2:69, 2:70, 2:71, 2:76, 2:80, 2:88, 2:91, 2:93, 2:94, 2:97, 2:111, 2:116 … (full list in data/locations.json)
**Locations — scholar's rule (603 verses):** 2:11, 2:13, 2:14, 2:25, 2:30, 2:32, 2:67, 2:68, 2:69, 2:70, 2:71, 2:76, 2:80, 2:88, 2:91, 2:93, 2:94, 2:97, 2:111, 2:116, 2:120, 2:133, 2:135, 2:139, 2:140, 2:142, 2:156, 2:170, 2:189, 2:215, 2:217, 2:219, 2:220, 2:222, 2:246, 2:247, 2:249, 2:250, 2:275, 2:285, 3:12, 3:15, 3:20, 3:24, 3:26, 3:29, 3:31, 3:32, 3:61, 3:64, 3:73, 3:75, 3:81, 3:84, 3:93, 3:95, 3:98, 3:99, 3:119, 3:147 …

### plant-tree-26

**Claim:** The words 'plant' and 'tree' each occur 26 times.

**Arabic:** نبات / شجر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** نبات substring 11; شجر substring 27. Plant is far from 26; tree is one over.

Methods pass (2026-11-08): differs→confirmed: by root, plant (nbt) is exactly 26 and tree ($jr) is 27 of which one token (شَجَرَ, 4:65) is the verb 'to dispute', leaving 26.

**Scholar's method (reconstructed):** plant by ROOT nbt = 26; tree by ROOT $jr minus the dispute verb = 26.

**Exceptions:** Plant: ROOT nbt 26 (أنبت verbs 16 + نبات nouns 9 + تنبت 1). Tree: ROOT $jr 27, of which 1 is the dispute verb شَجَرَ (4:65, LEM $ajara, 'what has arisen/disputed between them') -- not a tree. Tree-sense = 26 (شجرة 19 + شجر 7).

**Verification — scholar's rule:** 26 / 26 — Reconstructed: plant by ROOT nbt = 26; tree by ROOT $jr minus the dispute verb = 26. The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 26 / 26 — QAC: ROOT nbt = 26; ROOT $jr tree-sense = 26 (whole root 27 incl. the 4:65 dispute verb). Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 26 / 26, A2: 26 / 26, A3: 11 / 27, A6: 26 / 26 · 26/26 reproduces under the root rule (tree minus the 4:65 dispute verb); substrings give 11/27.

**Locations (45 verses):** 2:35, 2:61, 2:261, 3:37, 6:99, 7:19, 7:20, 7:22, 7:58, 10:24, 14:24, 14:26, 15:19, 16:10, 16:11, 16:68, 17:60, 18:45, 20:53, 20:120, 22:5, 22:18, 23:20, 24:35, 26:7, 27:60, 28:30, 31:10, 31:27, 36:36, 36:80, 37:62, 37:64, 37:146, 44:43, 48:18, 50:7, 50:9, 55:6, 56:52, 56:72, 57:20, 71:17, 78:15, 80:27

### reward-forgiveness-117-234

**Claim:** The words 'reward' (al-jaza') and 'forgiveness' (maghfira) occur 117 and 234 times (forgiveness exactly double reward).

**Arabic:** الجزاء / المغفرة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The filed Arabic ثواب (thawab) was wrong — Yahya's word is الجزاء (al-jaza'), and the thawab substring is only 13. By root: QAC root j-z-y = 118 — one more than the claimed 117, so the reward side needs an unstated one-token exclusion. Forgiveness reproduces exactly as the QAC root gh-f-r = 234 (including غفور, يغفر, استغفار and مغفرة forms). So the pair as claimed differs by one on the reward side only. (مغفر substring alone is 28 — that counts only the مغفر- stem, not the whole root.)

Methods pass (2026-11-08): differs→confirmed: reward (ROOT jzy) is 118 minus the jizya tax token (9:29) = 117; forgiveness (ROOT gfr) is 234 exactly.

**Scholar's method (reconstructed):** reward by ROOT jzy minus the jizya tax token = 117; forgiveness by ROOT gfr = 234.

**Exceptions:** Reward: ROOT jzy 118 = جزى verbs (jazaY` 73) + جزاء nouns (jazaA^' 42) + جازٍ 'one who avails' (31:33) + نجازي 'We recompense' (34:17) + الجزية 'jizya tax' (9:29). Only the jizya (1 token) is not reward. Forgiveness: ROOT gfr 234 = غفور 91 + غفر 65 + استغفر 40 + مغفرة 28 + غفّار 5 + غافر 2 + غفران 1 + مستغفرين 1 + استغفار 1 -- all forgiveness-sense.

**Verification — scholar's rule:** 117 / 234 — Reconstructed: reward by ROOT jzy minus the jizya tax token = 117; forgiveness by ROOT gfr = 234. The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 117 / 234 — QAC: ROOT jzy reward-sense = 117 (whole root 118 incl. jizya 9:29); ROOT gfr = 234. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 117 / 234, A2: 117 / 234, A3: 48 / 28, A6: 117 / 234 · 117/234 reproduces under the root rule (reward minus the jizya tax token); substrings give 48/28.

**Locations (306 verses; verses per surah — 2: 20, 3: 16, 4: 17, 5: 15, 6: 11, 7: 13, 8: 7, 9: 12, 10: 5, 11: 7, 12: 10, 13: 1, 14: 4, 15: 1, 16: 7, 17: 4, 18: 4, 19: 1, 20: 5, 21: 1, 22: 2, 23: 3, 24: 6, 25: 4, 26: 3, 27: 3, 28: 4, 29: 1, 30: 1, 31: 1, 32: 1, 33: 7, 34: 6, 35: 6, 36: 3, 37: 6, 38: 4, 39: 4, 40: 6, 41: 5, 42: 5, 45: 3, 46: 5, 47: 3, 48: 4, 49: 3, 51: 1, 52: 1, 53: 3, 54: 2, 55: 1, 56: 1, 57: 3, 58: 2, 59: 2, 60: 4, 61: 1, 63: 2, 64: 2, 66: 3, 67: 2, 71: 4, 73: 1, 74: 1, 76: 3, 77: 1, 78: 2, 85: 1, 92: 1, 98: 1, 110: 1):** first 20: 2:48, 2:58, 2:85, 2:123, 2:173, 2:175, 2:182, 2:191, 2:192, 2:199, 2:218, 2:221, 2:225, 2:226, 2:235, 2:263, 2:268, 2:284, 2:285, 2:286 … (full list in data/locations.json)

### guidance-mercy-79

**Claim:** The words 'guidance' (huda) and 'mercy' (rahma) each occur 79 times.

**Arabic:** هدى / رحمة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** هد substring 432; رحم substring 318 — polluted by الرحمن 169 and الرحيم 227, which share the root. The 79 figure must use a narrow selection the source does not state.

Methods pass (2026-11-08): differs→confirmed: bare (unsuffixed) nouns reproduce exactly — hudFY 79 (85−6 suffixed), raHomap 79 (114−35 suffixed); same bare-form rule as iman/kufr.

**Scholar's method (reconstructed):** bare (unsuffixed) noun forms give exactly 79/79 (QAC LEM hudFY bare 79; LEM raHomap bare 79).

**Exceptions:** Guidance: noun هدى (LEM hudFY) 85 total, of which 79 are bare (unsuffixed) -- QAC stem forms hudFY 43 + hudaY` 24 + hudaY 7 + hudaY`^ 5; the 6 suffixed tokens (هداه/هداهم...) are excluded. Mercy: noun رحمة (LEM raHomap) 114 total, of which 79 are bare (unsuffixed) -- stem forms raHomapF 34 + raHomapN 12 + raHomapK 11 + r~aHomapi 5 + raHomata 3 + raHomapi 3 and 11 further bare forms; the 35 suffixed tokens (رحمته/رحمتهم/رحمتك...) are excluded. Whole roots: hdy 316, rHm 339. This is the same bare-form (unsuffixed noun) rule that reproduces iman/kufr 25/25 -- Yahya's '(without genitive)' for iman is the same idea (no possessive/genitive suffix).

**Verification — scholar's rule:** 79 / 79 — Reconstructed: bare (unsuffixed) noun forms give exactly 79/79 (QAC LEM hudFY bare 79; LEM raHomap bare 79). The source states no method; this is the selection that reproduces the claim.

**Verification — root rule:** 79 / 79 — QAC: bare nouns hudFY 79 / raHomap 79. Noun totals 85/114; whole-root 316/339. The 79/79 is the bare-noun subset on both sides.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A3, A6 · numbers by set: A1: 79 / 79, A2: 85 / 114, A3: 79 / 79, A6: 79 / 79 · 79/79 is the bare-noun selection (same rule as iman/kufr); lemma totals are 85/114, whole roots 316/339.

**Locations (138 verses; verses per surah — 2: 12, 3: 8, 4: 3, 5: 2, 6: 10, 7: 8, 9: 3, 10: 2, 11: 8, 12: 1, 15: 1, 16: 3, 17: 7, 18: 8, 19: 3, 20: 3, 21: 2, 22: 2, 27: 2, 28: 7, 29: 1, 30: 4, 31: 3, 32: 1, 33: 1, 34: 2, 35: 1, 36: 1, 38: 2, 39: 4, 40: 3, 41: 3, 42: 1, 43: 1, 44: 1, 45: 2, 46: 1, 47: 3, 48: 1, 53: 1, 57: 2, 61: 1, 72: 1, 92: 1, 96: 1):** first 20: 2:2, 2:5, 2:16, 2:38, 2:97, 2:120, 2:157, 2:159, 2:175, 2:178, 2:185, 2:218, 3:4, 3:8, 3:73, 3:96, 3:107, 3:138, 3:157, 3:159 … (full list in data/locations.json)

### tongue-sermon-25

**Claim:** The words 'tongue' (lisan) and 'sermon' (maw'iza) each occur 25 times.

**Arabic:** لسان / موعظة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** لسان substring 15; موعظ substring 9. Both below 25. Note: WikiIslam points out the counted word is 'admonition', not 'sermon' — 'sermon' as such does not appear in the Quran.

Methods pass (2026-11-08): differs→confirmed: by root, tongue (lsn) is exactly 25 and admonition (wEZ) is exactly 25. 'Sermon' mistranslates موعظة (admonition).

**Scholar's method (reconstructed):** tongue by ROOT lsn = 25; admonition by ROOT wEZ = 25.

**Exceptions:** Tongue: ROOT lsn 25, all LEM lisaAn -- singular لسان plus plural ألسنة (the substring لسان 15 misses the plurals). Sermon: the counted word is موعظة 'admonition', not 'sermon' (WikiIslam: 'sermon' as such does not appear in the Quran). ROOT wEZ 25 = وعظ verbs 15 + موعظة 9 + واعظين 1 (the substring موعظ 9 misses the verbs).

**Verification — scholar's rule:** 25 / 25 — Reconstructed: tongue by ROOT lsn = 25; admonition by ROOT wEZ = 25. The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 25 / 25 — QAC: ROOT lsn = 25; ROOT wEZ = 25. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 25 / 25, A2: 25 / 25, A3: 15 / 9, A6: 25 / 25 · 25/25 reproduces under the root and lemma rules; substrings give 15/9.

**Locations (48 verses):** 2:66, 2:231, 2:232, 2:275, 3:78, 3:138, 4:34, 4:46, 4:58, 4:63, 4:66, 5:46, 5:78, 7:145, 7:164, 10:57, 11:46, 11:120, 14:4, 16:62, 16:90, 16:103, 16:116, 16:125, 19:50, 19:97, 20:27, 24:15, 24:17, 24:24, 24:34, 26:13, 26:84, 26:136, 26:195, 28:34, 30:22, 31:13, 33:19, 34:46, 44:58, 46:12, 48:11, 58:3, 60:2, 65:2, 75:16, 90:9

### wine-intoxication-6

**Claim:** The words 'wine' (khamr) and 'intoxication' (sakara) each occur 6 times.

**Arabic:** خمر / سكر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** خمر substring 7 (claimed 6); سكر substring 4 (claimed 6). The سكر family totals 7: the 4 are سكرت (15:15), سكرتهم (15:72), سكرا (16:67) and سكرة (50:19) — سكرة was already inside the 4, so it cannot be added again — plus سكارى, 3 tokens (4:43 ×1, 22:2 ×2, the verse containing it twice). An earlier draft of this note added سكرة on top of the 4 and counted سكارى as 2 — two compensating errors; the family total 7 is right either way. The two sides do not match as claimed (7 vs 7 by root would match, but the claimed figure is 6/6).

**Scholar's method (unstated):** method not stated by the source

**Exceptions:** Wine: noun خمر (LEM xamor) 6; the 7th ROOT xmr token is خمرهن 'their veils' (24:31, LEM xumur) -- not wine. Intoxication: ROOT skr 7, all intoxication-sense -- سكرت 15:15, سكرتهم 15:72, سكرا 16:67, سكرة الموت 50:19, سكارى x3 (4:43, 22:2 x2). No token can be excluded on sense grounds; intoxication is 7, not 6.

**Verification — scholar's rule:** 6 / None — Wine 6 reproduces as the noun (LEM xamor). Intoxication does not reproduce as 6: ROOT skr = 7, all intoxication-sense. No stated or reconstructable rule gives 6/6.

**Verification — root rule:** 6 / 7 — QAC: LEM xamor (wine noun) = 6 (whole ROOT xmr 7 incl. veils 24:31); ROOT skr (intoxication) = 7. The pair differs by one on the intoxication side.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: 6 / 7, A2: 6 / 7, A3: 7 / 4 · Wine 6 reproduces as the noun; intoxication is 7 under every rule tried — no rule gives 6/6.

**Locations (12 verses):** 2:219, 4:43, 5:90, 5:91, 12:36, 12:41, 15:15, 15:72, 16:67, 22:2, 47:15, 50:19

### mind-light-49

**Claim:** The words 'mind' ('aql) and 'light' (nur) each occur 49 times.

**Arabic:** عقل / نور

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** عقل substring 49 exactly; نور substring 46 — three short of 49. The pair matches on one side only. WikiIslam notes the 49 can be reached as nur 43 (lemma) + muneer 6 — but that mixes the noun 'light' with the adjective 'shining', so we do not accept it as the same word.

**Scholar's method (unstated):** method not stated by the source

**Exceptions:** Mind: ROOT Eql 49 -- all verb forms (تعقلون 'you use reason' etc.); there is no noun عقل in the Quran, so the 'mind' count is already a root count over verbs. Light: LEM nuwr 43; LEM m~uniyr ('shining, illuminating', adjective) 6; nuwr + muniyr = 49. ROOT nwr as a whole is 194 because it includes نار 'fire' (145) -- not light. The 49 for light therefore requires counting منير as 'light', which mixes the noun with the adjective (WikiIslam's route to 49).

**Verification — scholar's rule:** 49 / None — Mind 49 reproduces by ROOT Eql. Light 49 reproduces ONLY as nuwr 43 + muniyr 6; the noun alone is 43. No stated method; the light side needs the adjective included.

**Verification — root rule:** 49 / 43 — QAC: ROOT Eql = 49; LEM nuwr = 43 (49 with m~uniyr). Under the plain lemma rule the pair is 49/43; under a root rule that counts منير as light it is 49/49. NOT proposed as a correction: the prior team explicitly rejected mixing the noun with the adjective, and the choice is a judgement call for the coordinator/MK.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: 49 / 43, A2: 49 / 43, A3: 49 / 46 · Mind 49 reproduces by root; light is 43 as the noun (49 only if the adjective منير is counted as 'light' — left undecided).

**Locations (82 verses; verses per surah — 2: 10, 3: 2, 4: 1, 5: 6, 6: 5, 7: 2, 8: 1, 9: 1, 10: 4, 11: 1, 12: 2, 13: 2, 14: 2, 16: 2, 21: 2, 22: 1, 23: 1, 24: 3, 25: 1, 26: 1, 28: 1, 29: 3, 30: 2, 33: 1, 35: 1, 36: 2, 37: 1, 39: 3, 40: 1, 42: 1, 43: 1, 45: 1, 49: 1, 57: 6, 59: 1, 61: 1, 64: 1, 65: 1, 66: 1, 67: 1, 71: 1):** first 20: 2:17, 2:44, 2:73, 2:75, 2:76, 2:164, 2:170, 2:171, 2:242, 2:257, 3:65, 3:118, 4:174, 5:15, 5:16, 5:44, 5:46, 5:58, 5:103, 6:1 … (full list in data/locations.json)

### benefit-corrupt-50

**Claim:** The words 'benefit' (naf') and 'corrupt' (fasad) each occur 50 times.

**Arabic:** نفع / فساد

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** نفع substring 45; فساد substring 11. Corrupt is far from 50.

**Scholar's method (reconstructed):** both sides are exactly 50 under the QAC root rule (nfE 50, fsd 50).

**Exceptions:** Benefit: ROOT nfE 50 (نفع verb 31 + نفع noun 11 + منافع 8). Corrupt: ROOT fsd 50 (مفسد 21 + أفسد 15 + فساد 11 + فسدت 3). The old differs rested on substrings (نفع 45, فساد 11).

**Verification — scholar's rule:** 50 / 50 — Reconstructed: both sides are exactly 50 under the QAC root rule (nfE 50, fsd 50).

**Verification — root rule:** 50 / 50 — QAC: ROOT nfE = 50; ROOT fsd = 50. Both rules agree. NOTE: this is the same result as the benefit-corrupt-50 flip proposed in PASTED_PAGE_CHECK.md, which is still UNAPPROVED by MK -- so NO correction is recorded here, per the task instructions. The numbers are reported; the status change is left to the coordinator/MK.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 50 / 50, A2: 50 / 50, A3: 45 / 11, A6: 50 / 50 · Both sides are exactly 50 under the root and lemma rules; the status flip is still unapproved by MK, so the finding stays 'differs'.

**Locations (96 verses; verses per surah — 2: 12, 3: 1, 4: 1, 5: 5, 6: 2, 7: 8, 8: 1, 10: 7, 11: 3, 12: 2, 13: 3, 16: 2, 17: 1, 18: 1, 20: 2, 21: 2, 22: 4, 23: 2, 25: 2, 26: 4, 27: 3, 28: 4, 29: 2, 30: 2, 32: 1, 33: 1, 34: 2, 36: 1, 38: 1, 40: 4, 43: 1, 47: 1, 48: 1, 51: 1, 57: 1, 60: 1, 74: 1, 80: 1, 87: 1, 89: 1):** first 20: 2:11, 2:12, 2:27, 2:30, 2:60, 2:102, 2:123, 2:164, 2:205, 2:219, 2:220, 2:251, 3:63, 4:11, 5:32, 5:33, 5:64, 5:76, 5:119, 6:71 … (full list in data/locations.json)

### love-obedience-83

**Claim:** The words 'love' (hubb) and 'obedience' (ta'a) each occur 83 times.

**Arabic:** حب / طاعة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** حب substring 153; طاع substring 16. Neither is near 83.

**Scholar's method (unstated):** method not stated by the source

**Exceptions:** Love: ROOT Hbb 95, minus grain (حبّ 'grain/seed' 7 + حبّة 5 = 12) = 83 love-sense (أحبّ verbs 64 + حبّ noun 9 + استحبّ 4 + أحبّ 3 + أحبّاء 1 + محبّة 1 + حبّب 1). Obedience: ROOT TwE 129, minus استطاع 'to be able' (LEM {sotaTaAEa, 42) = 87 obedience-sense (أطاع 72 + طوع 4 + طاعة 3 + تطوّع 2 + يطاع 2 + طواعية 1 + مطوّعين 1 + طائعين 1 + مطاع 1). Love reproduces (83); obedience is 87, four over.

**Verification — scholar's rule:** 83 / None — Love 83 reproduces under root-minus-grain. Obedience does not reproduce as 83: obedience-sense root = 87, whole root = 129. No stated or reconstructable rule gives 83/83.

**Verification — root rule:** 83 / 87 — QAC: ROOT Hbb love-sense = 83 (whole root 95 incl. grain 12); ROOT TwE obedience-sense = 87 (whole root 129 incl. 'to be able' 42). The pair differs by four on the obedience side.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: 83 / 87, A2: 83 / 87, A3: 153 / 16 · Love 83 reproduces (root minus grain); obedience is 87 sense-correct (129 whole root) — no rule gives 83.

**Locations (150 verses; verses per surah — 2: 11, 3: 20, 4: 11, 5: 10, 6: 4, 7: 3, 8: 4, 9: 8, 12: 3, 13: 1, 14: 1, 16: 2, 18: 1, 20: 2, 22: 1, 23: 1, 24: 8, 25: 1, 26: 9, 28: 3, 29: 1, 30: 1, 31: 2, 33: 6, 38: 1, 40: 1, 41: 2, 42: 1, 43: 2, 47: 3, 48: 2, 49: 4, 57: 1, 58: 1, 59: 2, 60: 1, 61: 2, 64: 2, 68: 2, 71: 1, 75: 1, 76: 3, 81: 1, 89: 1, 96: 1, 100: 1):** first 20: 2:158, 2:165, 2:177, 2:184, 2:190, 2:195, 2:205, 2:216, 2:222, 2:276, 2:285, 3:14, 3:31, 3:32, 3:50, 3:57, 3:76, 3:83, 3:92, 3:100 … (full list in data/locations.json)

### refuge-forever-28

**Claim:** The words 'destination/return' (al-maseer) and 'forever' (abadan) each occur 28 times.

**Arabic:** المصير / أبدا

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The filed Arabic ملجأ (malja', 'refuge') was wrong — Yahya's word is المصير (al-maseer, 'destination/return'), and the ملجا substring is only 3. With the correct word: مصير substring = 28 exactly (المصير 23 + مصيرا/ومصيرا/مصيركم). Forever: ابدا substring 29 — one over 28. So the pair differs by one on the 'forever' side only; the 'refuge' side was never the problem, the filed word was.

Methods pass (2026-11-08): differs→confirmed: refuge (LEM maSiyr) is 28 and forever (LEM >abadFA) is 28. The old '29' was a substring false positive: عابدات (66:5) contains ابدا in its skeleton but is not أبدا.

**Scholar's method (reconstructed):** maseer (LEM maSiyr) = 28; forever (LEM >abadFA, exact form) = 28.

**Exceptions:** The filed Arabic ملجأ (malja', 'refuge') was wrong -- Yahya's page says 'refuge (maseer)', i.e. المصير 'destination/return'. مصير substring = 28 (المصير 23 + مصيرا/ومصيرا/مصيركم forms); LEM maSiyr = 28. Forever: ابدا = 28 by exact surface form and by QAC lemma >abadFA (28 verses). The earlier '29' was a substring false positive: the ابدا substring also catches عابدات 'devout [women]' (66:5, LEM Ea`bida`t, ROOT Ebd), which is not أبدا at all.

**Verification — scholar's rule:** 28 / 28 — Reconstructed: maseer (LEM maSiyr) = 28; forever (LEM >abadFA, exact form) = 28. The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 28 / 28 — QAC: LEM maSiyr = 28; LEM >abadFA = 28. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 28 / 28, A2: 28 / 28, A3: 28 / 29, A6: 28 / 28 · 28/28 reproduces under the root and lemma rules; the ابدا substring gives 29 (the 66:5 عابدات false positive).

**Locations (55 verses):** 2:95, 2:126, 2:285, 3:28, 3:162, 4:57, 4:97, 4:115, 4:122, 4:169, 5:18, 5:24, 5:119, 8:16, 9:22, 9:73, 9:83, 9:84, 9:100, 9:108, 14:30, 18:3, 18:20, 18:35, 18:57, 22:48, 22:72, 24:4, 24:17, 24:21, 24:42, 24:57, 25:15, 31:14, 33:53, 33:65, 35:18, 40:3, 42:15, 48:6, 48:12, 50:43, 57:15, 58:8, 59:11, 60:4, 62:7, 64:3, 64:9, 64:10, 65:11, 66:9, 67:6, 72:23, 98:8

### disaster-thanks-75

**Claim:** The words 'disaster' (musiba) and 'thanks' (shukr) each occur 75 times.

**Arabic:** مصيبة / شكر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** مصيب substring 11; شكر substring 47. Both below 75.

Methods pass (2026-11-08): differs→confirmed: by root, thanks ($kr) is exactly 75 and disaster-sense (Swb) is 75, excluding صيّب (rainstorm, 2:19) and صواب ('right', 78:38).

**Scholar's method (reconstructed):** disaster by ROOT Swb minus the two non-disaster lemmas (صيّب, صواب) = 75; thanks by ROOT $kr = 75.

**Exceptions:** Disaster: ROOT Swb 77 = أصاب 'befall/afflict' verbs 64 + مصيبة 10 + مصيب 'one who is struck' (11:81) 1 + صيّب 'rainstorm' (2:19) 1 + صواب 'what is right' (78:38) 1. The last two are not disaster-sense; excluding them gives 75. Thanks: ROOT $kr 75, all thanks-sense (شكر 46 + شاكر 14 + شكور 10 + مشكور 2 + شكور 2 + شكر 1).

**Verification — scholar's rule:** 75 / 75 — Reconstructed: disaster by ROOT Swb minus the two non-disaster lemmas (صيّب, صواب) = 75; thanks by ROOT $kr = 75. The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 75 / 75 — QAC: ROOT Swb disaster-sense = 75 (whole root 77); ROOT $kr = 75. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 75 / 75, A2: 75 / 75, A3: 11 / 47, A6: 75 / 75 · 75/75 reproduces under the root and lemma rules (disaster minus the two non-disaster lemmas); substrings give 11/47.

**Locations (123 verses; verses per surah — 2: 11, 3: 10, 4: 6, 5: 5, 6: 3, 7: 8, 8: 2, 9: 5, 10: 3, 11: 2, 12: 2, 13: 2, 14: 3, 16: 5, 17: 2, 21: 1, 22: 3, 23: 1, 24: 2, 25: 1, 27: 3, 28: 2, 29: 1, 30: 3, 31: 4, 32: 1, 34: 3, 35: 3, 36: 2, 38: 1, 39: 3, 40: 2, 42: 5, 45: 1, 46: 1, 48: 1, 49: 1, 54: 1, 56: 1, 57: 1, 64: 2, 67: 1, 76: 3):** first 20: 2:52, 2:56, 2:152, 2:156, 2:158, 2:172, 2:185, 2:243, 2:264, 2:265, 2:266, 3:117, 3:120, 3:123, 3:144, 3:145, 3:146, 3:153, 3:165, 3:166 … (full list in data/locations.json)

### trouble-peace-13

**Claim:** The words 'distress' (al-dayq) and 'tranquillity' (al-tuma'nina) each occur 13 times.

**Arabic:** الضيق / الطمأنينة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The filed Arabic ضر/سلام was wrong — the counted words are الضيق (distress) and الطمأنينة (tranquillity). By QAC root: D-y-q = 13 exactly and T-m-n = 13 exactly. Plain substrings give ضيق 7 and طمان 3, so the 13/13 pair needs root counting, not substrings. Confirmed under the root rule.

**Scholar's method (reconstructed):** ROOT Dyq = 13 and ROOT Tmn = 13.

**Exceptions:** The counted words are الضيق (distress) and الطمأنينة (tranquillity) -- the filed Arabic ضر/سلام was wrong. Yahya's English page just says 'trouble' and 'peace' with no Arabic, so the word identification is itself reconstructed from the root counts. Distress: ROOT Dyq 13 (ضاق verbs 7 + ضيق 2 + ضيق 2 + ضائق 1 + تضيق 1). Tranquillity: ROOT Tmn 13 (اطمأنّ 9 + مطمئن 2 + مطمئنة 2). Plain substrings give ضيق 7 and طمأن 3 -- the 13/13 needs root counting, not substrings.

**Verification — scholar's rule:** 13 / 13 — Reconstructed: ROOT Dyq = 13 and ROOT Tmn = 13. The source states no method and gives no Arabic; this is the selection that reproduces the claim.

**Verification — root rule:** 13 / 13 — QAC: ROOT Dyq = 13; ROOT Tmn = 13. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 13 / 13, A2: 13 / 13, A3: 7 / 3, A6: 13 / 13 · 13/13 reproduces under the root and lemma rules; substrings give 7/3.

**Locations (24 verses):** 2:260, 3:126, 4:103, 5:113, 6:125, 8:10, 9:25, 9:118, 10:7, 11:12, 11:77, 13:28, 15:97, 16:106, 16:112, 16:127, 17:95, 22:11, 25:13, 26:13, 27:70, 29:33, 65:6, 89:27

### treachery-foul-16

**Claim:** The words 'treachery' (khiyana) and 'foul' (khabith) each occur 16 times.

**Arabic:** خيانة / خبيث

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** خيان substring 2; خبيث substring 13. Both below 16.

Methods pass (2026-11-08): differs→confirmed: by root, treachery (xwn) is exactly 16 and foul (xbv) is exactly 16.

**Scholar's method (reconstructed):** treachery by ROOT xwn = 16; foul by ROOT xbv = 16.

**Exceptions:** Treachery: ROOT xwn 16 (خان 5 + خائنين 3 + يختانون 2 + خوّان 2 + خائنة 2 + خيانة 2). Foul: ROOT xbv 16 (خبيث 9 + خبيثة 4 + خبيثات 2 + خبث 1). The substrings (خيان 2, خبيث 13) miss the verb forms.

**Verification — scholar's rule:** 16 / 16 — Reconstructed: treachery by ROOT xwn = 16; foul by ROOT xbv = 16. The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 16 / 16 — QAC: ROOT xwn = 16; ROOT xbv = 16. Both rules agree.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A2, A6 · numbers by set: A1: 16 / 16, A2: 16 / 16, A3: 2 / 13, A6: 16 / 16 · 16/16 reproduces under the root and lemma rules; substrings give 2/13.

**Locations (21 verses):** 2:187, 2:267, 3:179, 4:2, 4:105, 4:107, 5:13, 5:100, 7:58, 7:157, 8:27, 8:37, 8:58, 8:71, 12:52, 14:26, 21:74, 22:38, 24:26, 40:19, 66:10

### righteous-wicked-6-3

**Claim:** The words 'the righteous' (al-abrar) and 'the wicked' (al-fujjar) occur 6 and 3 times.

**Arabic:** الأبرار / الفجار

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The filed Arabic صالح/طالح was wrong — Yahya's words are الأبرار and الفجار. With the correct words: أبرار substring 6 (الأبرار 5 + للأبرار 1) and فجار substring 3 (الفجار 2 + كالفجار 1) — exact. (The filed words give صلح 37 and طلح 1, and WikiIslam's literal-form recount of those gives 5 vs 2 — all beside the point once the words are right.)

**Scholar's method (reconstructed):** surface forms أبرار 6 / فجار 3.

**Exceptions:** The filed Arabic صالح/طالح was wrong -- Yahya's words are الأبرار (the righteous) and الفجار (the wicked). أبرار substring 6 (الأبرار 5 + للأبرار 1); فجار substring 3 (الفجار 2 + كالفجار 1). Under the lemma rule the wicked side is 4, not 3: LEM fuj~aAr also covers الفجرة (80:42, a different plural pattern of the same lemma). The righteous side is 6 under both rules (LEM bar~ does not separate الأبرار from البرّ, so the surface form is the identifier).

**Verification — scholar's rule:** 6 / 3 — Reconstructed: surface forms أبرار 6 / فجار 3. The source states no method; this is the selection that reproduces the claim.

**Verification — root rule:** 6 / 4 — QAC: righteous (surface الأبرار) = 6; wicked by LEM fuj~aAr = 4 (الفجار 3 + الفجرة 80:42). The two rules differ by the one 80:42 token; the finding stands confirmed on the surface-form rule.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A3, A6 · numbers by set: A1: 6 / 4, A3: 6 / 3, A6: 6 / 3 · 6/3 reproduces as exact surface forms; under the lemma rule the wicked side is 4 (الفجرة 80:42).

**Locations (10 verses):** 3:193, 3:198, 38:28, 76:5, 80:42, 82:13, 82:14, 83:7, 83:18, 83:22
**Locations — scholar's rule (9 verses):** 3:193, 3:198, 38:28, 76:5, 82:13, 82:14, 83:7, 83:18, 83:22

### summer-winter-5

**Claim:** The words 'summer-hot' and 'winter-cold' each occur 5 times.

**Arabic:** صيف / شتاء

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** صيف (summer) substring 1; شتاء (winter) substring 3. The words 'summer' and 'winter' barely occur as such; WikiIslam notes heat 4 and cold 3 (our برد substring is 4). The 5/5 pair does not reproduce.

**Scholar's method (unstated):** method not stated by the source

**Exceptions:** Summer: ROOT Syf = 1 (الصيف, 106:2 only). Winter: ROOT $tw = 1 (الشتاء, 106:2 only -- Uthmani spelling الشتآء, which is why a raw search for شتاء finds nothing) -- both words occur in a single verse. The nearest neighbours do not give 5/5 either: heat ROOT Hrr = 15 (حرور, حرّ, تحرير...), cold ROOT brd = 5 (برد 2 + بارد 2 + برد 1). Cold alone is 5; heat is 15 and summer/winter are 1 each.

**Verification — scholar's rule:** None / None — No rule reproduces 5/5. Summer/winter by root = 1/1 (each occurs once, both in 106:2); heat/cold by root = 15/5.

**Verification — root rule:** 1 / 1 — QAC: ROOT Syf = 1; ROOT $tw = 1; ROOT Hrr (heat) = 15; ROOT brd (cold) = 5. Locations are the single verse 106:2, which contains both words.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: 1 / 1, A2: 1 / 1, A3: 1 / 3 · Summer/winter occur once each (both 106:2); heat 15 / cold 5 — no rule gives 5/5.

**Locations (1 verses):** 106:2

### human-being-65

**Claim:** The word 'human being' (insan) occurs 65 times.

**Arabic:** إنسان

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** انسان substring = 65 exactly. The creation-stage reading (the stages of human creation summing to 65) reproduces under lemma/form rules: soil (turaAb) 17 + drop (n~uTofap) 12 + clot (Ealaqap 5 + Ealaq 96:2) 6 + lump (muDogap) 3 + bone (عظام 13 + عظم 6:146, 19:4) 15 + flesh (laHom) 12 = 65. (An earlier draft of this note gave علقة as 7 — the 7th is the bare word علق in 96:2, which has no ة; علقة itself is 6: علقة 4 + العلقة 1 + كالمعلقة 1.) Yahya's own stage table (soil 17, drop 12, embryo 6, lump 3, bone 15, flesh 12 = 65) matches the lemma/form recount exactly — the 65 total for 'human being' is confirmed, and the stage arithmetic now is too.

**Scholar's method (reconstructed):** انسان surface count = 65; the stage table reproduces exactly under lemma/form rules (see exceptions).

**Exceptions:** Human being: انسان substring 65; QAC LEM <insa`n = 71, of which 65 are انسان (الانسان 58 + للانسان 6 + انسان 1) and 6 are أناس/أناسيّ (people/mankind collective: أناس 5 + وأناسيّ 1) -- a different word, excluded. Creation stages (Yahya's table, verified here by lemma/form): soil تراب (LEM turaAb) 17 -- the substring 20 catches أتراب 'peers' (3 tokens); drop نطفة (LEM n~uTofap) 12; embryo علقة (LEM Ealaqap) 5 + علق (LEM Ealaq, 96:2) 1 = 6 -- كالمعلقة 'like one suspended' (4:129, LEM muEal~aqap) is NOT an embryo and is excluded; lump مضغة (LEM muDogap) 3; bone عظام 13 + عظم (6:146, 19:4) 2 = 15; flesh لحم (LEM laHom) 12 -- the substring 58 catches لحوم 'meats' and other forms. Stages sum: 17+12+6+3+15+12 = 65.

**Verification — scholar's rule:** 65 — Reconstructed: انسان surface count = 65; the stage table reproduces exactly under lemma/form rules (see exceptions). The source states no method; these are the selections that reproduce the claim.

**Verification — root rule:** 65 — QAC: LEM <insa`n = 71 (65 انسان + 6 أناس/أناسيّ collective); انسان on its own = 65. Both rules agree on 65 for the word as claimed.

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A1, A3, A6 · numbers by set: A1: 65, A2: 71, A3: 65, A6: 65 · 65 is the انسان surface count (and the انسان subset of the lemma); the whole lemma is 71 (6 collective أناس/أناسيّ).

**Locations (63 verses; verses per surah — 4: 1, 10: 1, 11: 1, 12: 1, 14: 1, 15: 1, 16: 1, 17: 6, 18: 1, 19: 2, 21: 1, 22: 1, 23: 1, 25: 1, 29: 1, 31: 1, 32: 1, 33: 1, 36: 1, 39: 2, 41: 2, 42: 1, 43: 1, 46: 1, 50: 1, 53: 2, 55: 2, 59: 1, 70: 1, 75: 6, 76: 2, 79: 1, 80: 2, 82: 1, 84: 1, 86: 1, 89: 2, 90: 1, 95: 1, 96: 3, 99: 1, 100: 1, 103: 1):** first 20: 4:28, 10:12, 11:9, 12:5, 14:34, 15:26, 16:4, 17:11, 17:13, 17:53, 17:67, 17:83, 17:100, 18:54, 19:66, 19:67, 21:37, 22:66, 23:12, 25:29 … (full list in data/locations.json)
**Locations — scholar's rule (63 verses):** 4:28, 10:12, 11:9, 12:5, 14:34, 15:26, 16:4, 17:11, 17:13, 17:53, 17:67, 17:83, 17:100, 18:54, 19:66, 19:67, 21:37, 22:66, 23:12, 25:29, 29:8, 31:14, 32:7, 33:72, 36:77, 39:8, 39:49, 41:49, 41:51, 42:48, 43:15, 46:15, 50:16, 53:24, 53:39, 55:3, 55:14, 59:16, 70:19, 75:3, 75:5, 75:10, 75:13, 75:14, 75:36, 76:1, 76:2, 79:35, 80:17, 80:24, 82:6, 84:6, 86:5, 89:15, 89:23, 90:4, 95:4, 96:2, 96:5, 96:6 …

### harun-yahya-populariser

**Claim:** Harun Yahya (Adnan Oktar) popularised the paired-count list in his book Miracles of the Qur'an.

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an — 'Word Repetitions in the Qur'an'* — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Literature fact; the full list is published at harunyahya.info (fetched 2026-11-06). Method not stated in the source.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** The list as published at harunyahya.info does not include life/death 145; that claim circulates on other sites (e.g. quranic-miracles.com). The book's imprint could not be confirmed: harunyahya.info's own book page cites 'Miracles of the Qur'an, Harun Yahya, Araştırma Press', and a circulating edition is Global Publishing, Istanbul — the 'Goodword Books, 2005' imprint previously given here is not asserted. The live list also contains one pair this file omits: 'reward' (ajr) and 'action' (fa'il), both 107 times.

**Scholar's method (unstated):** method not stated by the source

**Exceptions:** Not a word count: a literature fact (Yahya popularised the paired-count list in Miracles of the Qur'an). The full list is published at harunyahya.info (fetched 2026-11-07); it does not include life/death 145, which circulates on other sites. The list also contains one pair this file omits: 'reward' (ajr) and 'action' (fa'il), both 107 times -- side-check here: LEM >ajor (ajr noun) = 105, ROOT fEl = 108, LEM faAEil = 9; the 107/107 does not reproduce under the QAC rules tested.

**Verification — scholar's rule:** — — Not applicable -- no count is claimed.

**Verification — root rule:** — — Not applicable -- no count is claimed.

**Assumptions:** scholar set — · our set — · reconciles under: none · numbers by set: — · Not a word/letter count — a literature fact (Yahya popularised the paired-count list); no counting assumption applies.

**Locations:** not applicable — locations: not applicable -- this is a literature fact, not a word count.

## Letter counts and the disconnected letters (muqatta'at)

### qaf-57-57

**Claim:** The letter Qaf occurs 57 times in surah 50 (Qaf) and 57 times in surah 42 (Shura) — 57 + 57 = 114.

**Arabic:** ق

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Letter counting under our stated convention (see meta). Khalifa's headline finding.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** ق in surah 50 = 57 and in surah 42 = 57, confirmed by our recount.

**Scholar's method (stated):** Khalifa states it (Appendix 1, fetched 2026-11-07): 'The computer data showed that the text of the only Q-initialed suras, 42 and 50, contained the same number of Q's, 57 and 57.' Units: occurrences of the letter ق in the text of surahs 42 and 50. The unnumbered basmalahs contain no ق, so basmalah handling does not affect the count.

**Exceptions:** None. The letter ق occurs in surah 50 (57) and surah 42 (57); the initial ق of 50:1 itself counts. No textual variant is involved.

**Verification — scholar's rule:** 57 / 57 — Stated rule verified: letter ق in surah 50 = 57, in surah 42 = 57, under the project letter convention.

**Verification — root rule:** 57 / 57 — Same count -- this is a letter count, not a word count, so the 'root rule' is the project letter convention (base letters count; dagger alif/small waw/small yeh are marks). Both agree: 57/57.

**Assumptions:** scholar set A5 · our set A4 · reconciles under: A4, A5 · numbers by set: A4: 57 / 57, A5: 57 / 57 · 57/57 reproduces under the project letter convention and Khalifa's stated rule; the basmalahs contain no ق.

**Locations (65 verses; verses per surah — 42: 31, 50: 34):** first 20: 42:2, 42:3, 42:5, 42:7, 42:9, 42:12, 42:13, 42:14, 42:15, 42:17, 42:18, 42:19, 42:21, 42:22, 42:23, 42:24, 42:25, 42:27, 42:28, 42:29 … (full list in data/locations.json)

### nun-132-vs-133

**Claim:** The letter Nun occurs 133 times in surah 68 (Qalam).

**Arabic:** ن

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Letter counting under our stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** ن in surah 68 = 132 by our recount. Khalifa's 133 requires counting the spelled-out name 'Noon' (ن و ن) as 2 nuns; the orthodox written initial is a single ن.

**Scholar's method (stated):** Khalifa states it (Appendix 1, fetched 2026-11-07): the initial 'is unique; it occurs in one sura, 68, and the name of the letter is spelled out as three letters -- Noon Wow Noon -- in the original text, and is therefore counted as two N's. The total count of this letter in the N-initialed sura is 133.' Units: occurrences of the letter ن in surah 68, with the 68:1 initial counted as two.

**Exceptions:** The orthodox written initial is a single ن (68:1), counted once under the project convention. The unnumbered basmalah prepended to 68:1 contributes exactly one ن (in الرحمن): surah 68 has 132 ن including it, 131 without it. Khalifa's 133 = 132 + 1 for the spelled-out initial.

**Verification — scholar's rule:** 133 — Stated rule verified arithmetically: our count 132 + 1 for the spelled-out initial (ن و ن) = 133. The rule itself is Khalifa's, stated in the source.

**Verification — root rule:** 132 — Project letter convention: ن in surah 68 = 132 (131 in the surah text proper + 1 from the unnumbered basmalah in 68:1). Differs from Khalifa's 133 by exactly the spelled-out initial.

**Assumptions:** scholar set A5 · our set A4 · reconciles under: A5 · numbers by set: A4: 131, A5: 133, A7: 132 · 133 requires Khalifa's stated rule (the spelled-out initial ن و ن counts as two); the written text gives 132 with the basmalah, 131 without it.

**Locations (50 verses):** 68:1, 68:2, 68:3, 68:4, 68:5, 68:6, 68:7, 68:8, 68:9, 68:10, 68:11, 68:12, 68:13, 68:14, 68:15, 68:16, 68:17, 68:18, 68:19, 68:21, 68:22, 68:23, 68:24, 68:25, 68:26, 68:27, 68:28, 68:29, 68:30, 68:31, 68:32, 68:33, 68:34, 68:35, 68:36, 68:37, 68:38, 68:39, 68:41, 68:42, 68:43, 68:44, 68:45, 68:46, 68:47, 68:48, 68:49, 68:50, 68:51, 68:52

### sad-153-vs-152

**Claim:** The letter Sad occurs 152 times across surahs 7, 19 and 38 (97 + 26 + 29).

**Arabic:** ص

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Letter counting under our stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** ص: surah 38 = 29, surah 7 = 98, surah 19 = 26; total 153. Khalifa's 152 requires 97 in surah 7, which requires reading 7:69 as بسطة with س (Samarkand codex spelling); the Tanzil file reads بصطة with ص.

**Scholar's method (stated):** Khalifa states it (Appendix 1, Table 2, fetched 2026-11-07): S in sura 7 = 97, sura 19 = 26, sura 38 = 29, total 152. He also states the textual rule: in 7:69 'the word "Bastatan" is written in some printings with a "Saad," instead of "Seen." This is an erroneous distortion... By looking at the oldest available copy of the Quran, the Tashkent Copy, it was found that the word "Bastatan" is correctly written with a "Seen".' Units: occurrences of the letter ص in surahs 7, 19 and 38, with 7:69 read بسطة (Seen).

**Exceptions:** The Tanzil text reads 7:69 as بصطة (with ص, small seen above it) -- verified by script: the skeleton of 7:69 contains بصطة, not بسطة. That one ص is the whole difference: surah 7 has 98 ص under Tanzil against Khalifa's 97. Surahs 19 (26) and 38 (29) agree. The unnumbered basmalahs contain no ص.

**Verification — scholar's rule:** 97 / 26 / 29 — Stated rule verified arithmetically: 97+26+29 = 152 requires 7:69 read بسطة (Seen). Under the Tanzil reading (بصطة) the counts are 98/26/29 = 153.

**Verification — root rule:** 98 / 26 / 29 — Project letter convention on the Tanzil text: ص in surah 7 = 98, surah 19 = 26, surah 38 = 29; total 153. Differs from Khalifa's 152 by exactly the one ص in 7:69.

**Assumptions:** scholar set A5 · our set A4 · reconciles under: A5 · numbers by set: A4: 98 / 26 / 29, A5: 97 / 26 / 29 · 152 requires Khalifa's stated textual rule (7:69 read بسطة with س); the Tanzil text reads بصطة, giving 153.

**Locations (133 verses; verses per surah — 7: 81, 19: 25, 38: 27):** first 20: 7:1, 7:2, 7:7, 7:11, 7:13, 7:16, 7:21, 7:22, 7:29, 7:32, 7:35, 7:36, 7:37, 7:42, 7:43, 7:44, 7:45, 7:46, 7:47, 7:48 … (full list in data/locations.json)

### muqattaat-structure-29-14-78

**Claim:** 29 surahs open with disconnected letters (muqatta'at), using 14 distinct letters; 75 initial letters in the verse-1 openings (78 counting surah 42's second set, 'A.S.Q., separately).

**Arabic:** الم، المص، الر، المر، كهيعص، طه، طسم، طس، يس، ص، حم، حم عسق، ق، ن

**Source:** Halim Sayoud, *'Investigation on the Mystery of the Qur'an's Disjointed Letters', QURANICA 5(2), December 2013, University of Malaya* (2013) — <https://ijeas.um.edu.my/index.php/quranica/article/download/5185/2991/11903>

**Section:** Scholar findings

**Corpus and method:** First-verse check on the Tanzil file after stripping the merged unnumbered basmalah; structure per Sayoud (2013).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The expected initials match in 29/29 surahs from verse 1 (an earlier draft said 28/29 — all 29 match, including 42:1 حم; عسق is in 42:2). Distinct initial letters 14 (ا ل م ص ر ك ه ي ع ط س ح ق ن). Total: 75 letters in the verse-1 openings (3 monograms, 10 bigrams, 13 trigrams, 2 tetragrams, 1 pentagram = 75), or 78 counting surah 42's second set عسق (3 more letters) separately — the earlier draft's '78 (3/10/13/2/1)' mixed the two counts. Author: Halim Sayoud (not 'Khalifa Sayoud' as previously filed); the SeekersGuidance URL previously cited contains none of this structure and is dropped.

**Scholar's method (stated):** Sayoud states it (QURANICA 5(2), 2013, fetched 2026-11-07): 'there exist 29 Surahs that begin with... "muqattaat letters"... There are fourteen of such letters in total'; 'There are 3 Surahs that begin with 1 disjointed letter (character-monogram); 10 Surahs that begin with 2 disjointed letters (character-bigram); 13 Surahs that begin with 3 disjointed letters (character-trigram); 2 Surahs that begin with 4 disjointed letters (character-tetragram); 1 Surah that begins with 5 disjointed letters (character-pentagram).' Units: the opening letters of verse 1 of each initialed surah (surah 42's second set عسق is in 42:2, counted separately).

**Exceptions:** All 29 verse-1 openings match the expected initials (verified by script after stripping the merged unnumbered basmalah from verse 1). Breakdown: monograms ص (38), ق (50), ن (68); bigrams طه (20), طس (27), يس (36), حم (40-46); trigrams الم (2, 3, 29-32), الر (10-12, 14, 15), طسم (26, 28); tetragrams المص (7), المر (13); pentagram كهيعص (19). Distinct letters 14: ا ل م ص ر ك ه ي ع ط س ح ق ن. Total 75 letters in the verse-1 openings (3x1 + 10x2 + 13x3 + 2x4 + 1x5), or 78 counting 42:2 عسق separately.

**Verification — scholar's rule:** 29 / 14 / 75 — Stated structure verified: 29 surahs, 14 distinct letters, 75 letters in verse-1 openings (78 with 42:2).

**Verification — root rule:** 29 / 14 / 75 — Same -- this is a structural count of opening verses, not a word count; both rules are the same count. 78 counting 42:2 عسق separately.

**Assumptions:** scholar set A5 · our set A4 · reconciles under: A4, A5 · numbers by set: A4: 29 / 14 / 75, A5: 29 / 14 / 75 · 29 surahs, 14 letters, 75 opening letters (78 counting 42:2 عسق) — the stated structure reproduces exactly.

**Locations (30 verses):** 2:1, 3:1, 7:1, 10:1, 11:1, 12:1, 13:1, 14:1, 15:1, 19:1, 20:1, 26:1, 27:1, 28:1, 29:1, 30:1, 31:1, 32:1, 36:1, 38:1, 40:1, 41:1, 42:1, 42:2, 43:1, 44:1, 45:1, 46:1, 50:1, 68:1

### all-28-letters-verses

**Claim:** Two verses contain all 28 letters of the Arabic alphabet: 3:154 and 48:29.

**Source:** Classical/traditional observation, *Two verses containing all 28 letters of the Arabic alphabet (3:154, 48:29)*

**Section:** Scholar findings

**Corpus and method:** Distinct-letter count per verse on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 3:154 and 48:29 each have 28 distinct letters, none missing — confirmed by our recount. Previously cited to Khalifa's Appendix 1, which contains no such claim; re-cited as a classical/traditional observation, corroborated by multiple modern checks against the Uthmani text.

**Scholar's method (stated):** Classical/traditional observation; the claim itself states the method: a verse contains all 28 letters of the Arabic alphabet (distinct-letter count per verse). No source URL (previously cited to Khalifa's Appendix 1, which contains no such claim; re-cited as a traditional observation).

**Exceptions:** Distinct-letter count per verse on the Tanzil skeleton text (ة counted as ه, ى as ي, per the project convention). Only two verses in the whole Quran have 28 distinct letters: 3:154 and 48:29 (verified by script over all 6,236 verses; neither verse is a verse 1, so no basmalah is involved).

**Verification — scholar's rule:** 28 / 28 — Stated rule verified: 3:154 and 48:29 each have 28 distinct letters, none missing; no other verse does.

**Verification — root rule:** 28 / 28 — Same -- distinct-letter count per verse under the project letter convention. Both agree.

**Assumptions:** scholar set A5 · our set A4 · reconciles under: A4, A5 · numbers by set: A4: 28 / 28, A5: 28 / 28 · 3:154 and 48:29 each have 28 distinct letters and no other verse does.

**Locations (2 verses):** 3:154, 48:29

### longest-word-fasqaynakumuhu

**Claim:** The longest word in the Quran is fa'asqaynakumuhu (15:22).

**Arabic:** فَأَسْقَيْنَاكُمُوهُ

**Source:** Classical observation, repeated in modern Quran-statistics pages, *'How long is a Quran?' (calendar-uk FAQ, citing the classical claim)* — <https://www.calendar-uk.co.uk/frequently-asked-questions/how-long-is-a-quran>

**Section:** Scholar findings

**Corpus and method:** Letter counting under our stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** فأسقيناكموه (15:22) is 10 letters under our convention (the dagger alif is a mark, not a letter); the longest words are والمستغفرين (3:17) and والمستضعفين (4:75, 4:127) at 11 letters. Under a convention counting the dagger alif as a letter, فأسقيناكموه is 11 letters and tied for longest. The cited source (calendar-uk FAQ) confirms it as the longest word but gives no '11 letters' figure — the 11 is convention-dependent, not stated by the source.

**Scholar's method (stated):** Classical observation, repeated in modern Quran-statistics pages (calendar-uk FAQ, fetched 2026-11-07: 'The longest word in the Qur'an is: "fa'asqaynākumūhu" (فَأَسْقَيْنَاكُمُوهُ)'). The source states the word but gives no letter figure and no counting convention -- the '11 letters' figure is convention-dependent, not stated by the source. Units: the longest whitespace token in the Quran, by letter count.

**Exceptions:** فأسقيناكموه (15:22) is 10 letters under the project convention (the dagger alif is a mark, not a letter); it is 11 letters under a convention counting the dagger alif as a letter -- in which case it ties for longest with والمستغفرين (3:17) and والمستضعفين (4:75, 4:127), all 11 letters. Under the project convention the longest words are those three 11-letter tokens; the next tier is 10 letters (اقترفتموها 9:24, وبالمؤمنين 8:62, فسينفقونها 8:36, ...).

**Verification — scholar's rule:** 11 — Under a dagger-alif-counts convention, فأسقيناكموه is 11 letters and tied for longest (with 3:17, 4:75, 4:127). The source does not state this convention.

**Verification — root rule:** 11 — Project convention (dagger alif is a mark): فأسقيناكموه is 10 letters; the longest words are والمستغفرين (3:17) and والمستضعفين (4:75, 4:127) at 11 letters. The claim 'longest word' fails under this convention and ties under the other.

**Assumptions:** scholar set — · our set A4 · reconciles under: none · numbers by set: A4: 10 · فأسقيناكموه is 10 letters under the project convention; 11 only if the dagger alif counts as a letter, and then it merely ties for longest (3:17, 4:75, 4:127 also 11).

**Locations (4 verses):** 3:17, 4:75, 4:127, 15:22

### seven-heavens-7

**Claim:** The phrase 'seven heavens' (sab' samawat) occurs in 7 verses.

**Arabic:** سبع سماوات

**Source:** Harun Yahya (Adnan Oktar), with WikiIslam's verse-by-verse analysis, *Miracles of the Qur'an; WikiIslam, 'Word Count Miracles in the Qur'an'* — <https://wikiislam.net/index.php?title=Word_Count_Miracles_in_the_Qur%27an>

**Section:** Popular claims (Harun Yahya)

**Corpus and method:** Verse-level substring search on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 7 verses contain سبع + سماوات (2:29, 17:44, 23:86, 41:12, 65:12, 67:3, 71:15); plus 1 'seven paths' (23:17 طرائق) and 2 'seven strong' (12:48 seven hard years; 78:12 seven strong heavens) = 9 total سبع + heaven-ish verses, matching WikiIslam's analysis.

**Scholar's method (stated):** Phrase count, stated in the claim itself (Yahya's page: 'The statement of "seven heavens" is repeated seven times'): verses containing سبع ('seven') together with سماوات ('heavens'). WikiIslam's verse-by-verse analysis agrees on the 7 verses.

**Exceptions:** The 7 verses are 2:29, 17:44, 23:86, 41:12, 65:12, 67:3, 71:15. Further سبع + heaven-ish verses (WikiIslam's 9 total): 'seven paths' (طرائق, 23:17), 'seven hard years' (12:48, سنين) and 'seven strong' (شدادا, 78:12) -- these are سبع with a different second word, not سماوات, and are excluded from the 7.

**Verification — scholar's rule:** 7 — Stated rule verified: 7 verses contain سبع + سماوات.

**Verification — root rule:** 7 — QAC: verses containing both ROOT sbE and LEM samaA^' = 7 (same verses). Both rules agree.

**Assumptions:** scholar set A5 · our set A1 · reconciles under: A1, A2, A3, A5 · numbers by set: A1: 7, A2: 7, A3: 7, A5: 7 · 7 verses contain سبع + سماوات under every rule tried.

**Locations (7 verses):** 2:29, 17:44, 23:86, 41:12, 65:12, 67:3, 71:15

## Code 19 — Rashad Khalifa's 'mathematical miracle'

### basmalah-19-letters-114

**Claim:** The Basmalah consists of 19 letters, occurs 114 times in the Quran, and the Quran has 114 surahs = 19 x 6.

**Arabic:** بسم الله الرحمن الرحيم

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Letter counting under our stated convention (see meta); occurrence count on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Basmalah = 19 letters under our convention; occurs 114 times in the text (113 at surah starts + 27:30); 114 surahs = 19 x 6.

**Scholar's method (unstated):** method not stated by the source. Khalifa lists the basmalah facts among the 'Simple Facts' that 'do not require any tools to be verified' and 'refer to the original Arabic text' (Appendix 1, Part 1); he states no letter-counting rule — not which marks count as letters, not whether the alef wasla counts. Note: 19 requires counting the alef wasla in ٱلله (بسم 3 + الله 4 + الرحمن 6 + الرحيم 6 = 19); a rule that dropped the wasla would give 18.

**Exceptions:** The 112 unnumbered basmalahs (surah openings) are not QAC words — only 1:1 and the 27:30 basmalah are numbered-verse words. Surah 9 has no opening basmalah; surah 27 has two basmalahs (opening + 27:30).

**Verification — scholar's rule:** 19 — 19 letters under the project's stated letter convention (alef wasla counts; no dagger alif or small letters occur in the basmalah). The letter rule itself is unstated by Khalifa, so this is a reproduction under our convention, not his.

**Verification — root rule:** 19 — Same 19 letters (a letter count has no root rule); occurrences in the text = 114 (113 surah openings + 27:30).

**Assumptions:** scholar set — · our set A4 · reconciles under: A4 · numbers by set: A4: 19 / 114 · 19 letters and 114 occurrences reproduce under the project letter convention (alef wasla counts); Khalifa states no letter rule.

**Locations (114 verses; verses per surah — 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 2, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1, 86: 1, 87: 1, 88: 1, 89: 1, 90: 1, 91: 1, 92: 1, 93: 1, 94: 1, 95: 1, 96: 1, 97: 1, 98: 1, 99: 1, 100: 1, 101: 1, 102: 1, 103: 1, 104: 1, 105: 1, 106: 1, 107: 1, 108: 1, 109: 1, 110: 1, 111: 1, 112: 1, 113: 1, 114: 1):** first 20: 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 10:1, 11:1, 12:1, 13:1, 14:1, 15:1, 16:1, 17:1, 18:1, 19:1, 20:1, 21:1 … (full list in data/locations.json)

### allah-2699

**Claim:** The word 'Allah' (God) occurs 2,698 times in the Quran = 19 x 142.

**Arabic:** الله

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Lemma count (all forms of the name, incl. prefixed/clitic forms) on the Tanzil file, excluding the 112 unnumbered basmalahs (see note for the reconciliation).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Lemma count excl. 112 unnumbered basmalahs = 2,699 exactly (incl. basmalahs 2,801; strict surface الله 2,267). The 2,699 includes the oath forms تالله/وتالله (9) and interrogative أبالله (1). Dropping 9:129 (one of Khalifa's two rejected verses) gives his 2,698 = 19 x 142. (QuranCodex's 'strict surface 2,155' differs — method unstated.)

**Scholar's method (reconstructed):** Reconstructed. Khalifa states only the totals (2,698 occurrences; checksum 118,123) and no word-counting rule — nothing in Appendix 1 says whether prefixes, oath forms or the basmalahs count. The operative rule is stated in his Appendix 24: verses 9:128-129 are 'false injections' to be removed, and 'the count of the word "God" in the Quran was found to be 2699, which is not a multiple of 19, unless we remove one'. Reconstructed rule: (a) count every form of the name, including prefixed/clitic forms (lemma rule) — oath تالله/وتالله (9x) and interrogative أبالله (1x) included; (b) exclude the 112 unnumbered basmalahs (QAC convention); (c) drop 9:129.

**Exceptions:** 9:129 contains the one Allah dropped by Khalifa's rule (9:128 contains no Allah). The 112 unnumbered basmalahs are excluded (each contains one Allah; including them gives 2,811). Allahumma (5x, QAC lemma {ll~ahum~a) and generic ilah (147x, lemma <ila`h) are separate lemmas and are not counted.

**Verification — scholar's rule:** 2698 — Lemma count excl. unnumbered basmalahs (2,699) minus the Allah in 9:129 = 2,698 = 19 x 142. Test: 2,699 (Tanzil lemma) = 2,699 (QAC lemma {ll~ah).

**Verification — root rule:** 2699 — QAC lemma {ll~ah = 2,699 (standard text, basmalahs excluded by QAC construction). Tanzil lemma incl. basmalahs = 2,811; strict surface الله = 2267.

**Assumptions:** scholar set A6 · our set A2 · reconciles under: A6 · numbers by set: A1: 2851, A2: 2699, A3: 2155, A6: 2698, A7: 2811 · 2,698 reproduces only under Khalifa's reconstructed rule (lemma count, basmalahs out, 9:129 dropped); the standard text gives 2,699.

**Locations (1821 verses; verses per surah — 1: 2, 2: 172, 3: 131, 4: 135, 5: 88, 6: 65, 7: 45, 8: 52, 9: 101, 10: 49, 11: 33, 12: 34, 13: 23, 14: 28, 15: 2, 16: 64, 17: 10, 18: 14, 19: 8, 20: 6, 21: 5, 22: 50, 23: 12, 24: 50, 25: 6, 26: 13, 27: 25, 28: 21, 29: 30, 30: 21, 31: 21, 32: 1, 33: 51, 34: 8, 35: 27, 36: 2, 37: 15, 38: 2, 39: 43, 40: 37, 41: 11, 42: 24, 43: 3, 44: 3, 45: 15, 46: 14, 47: 21, 48: 25, 49: 14, 50: 1, 51: 3, 52: 2, 53: 6, 57: 22, 58: 22, 59: 17, 60: 11, 61: 10, 62: 8, 63: 9, 64: 14, 65: 9, 66: 8, 67: 3, 69: 1, 70: 1, 71: 7, 72: 8, 73: 1, 74: 2, 76: 4, 79: 1, 81: 1, 82: 1, 84: 1, 85: 3, 87: 1, 88: 1, 91: 1, 95: 1, 96: 1, 98: 3, 104: 1, 110: 2, 112: 2):** first 20: 1:1, 1:2, 2:7, 2:8, 2:9, 2:10, 2:15, 2:17, 2:19, 2:20, 2:22, 2:23, 2:26, 2:27, 2:28, 2:55, 2:60, 2:61, 2:62, 2:64 … (full list in data/locations.json)
**Locations — scholar's rule (1820 verses):** 1:1, 1:2, 2:7, 2:8, 2:9, 2:10, 2:15, 2:17, 2:19, 2:20, 2:22, 2:23, 2:26, 2:27, 2:28, 2:55, 2:60, 2:61, 2:62, 2:64, 2:67, 2:70, 2:72, 2:73, 2:74, 2:75, 2:76, 2:77, 2:79, 2:80, 2:83, 2:85, 2:88, 2:89, 2:90, 2:91, 2:94, 2:95, 2:96, 2:97, 2:98, 2:101, 2:102, 2:103, 2:105, 2:106, 2:107, 2:109, 2:110, 2:112, 2:113, 2:114, 2:115, 2:116, 2:118, 2:120, 2:126, 2:132, 2:136, 2:137 …

### rahman-57-rahim-115

**Claim:** The names 'Rahman' (Most Gracious) and 'Rahim' (Most Merciful) occur 57 (= 19 x 3) and 114 (= 19 x 6) times.

**Arabic:** الرحمن / الرحيم

**Source:** Rashad Khalifa, *Appendix 1, Part 2, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1_p2.html>

**Section:** Scholar findings

**Corpus and method:** Lemma count on the Tanzil file, excluding the 112 unnumbered basmalahs (see note).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Rahman lemma excl. unnumbered basmalahs = 57 = 19 x 3 (incl. basmalahs 169). Rahim lemma excl. basmalahs = 115; Khalifa's 114 = 115 minus the رحيم in 9:128, one of his two rejected verses. Citation note: this table is in Appendix 1 Part 2, not Part 1 (the citation previously pointed at Part 1).

**Scholar's method (reconstructed):** Reconstructed. Khalifa states only the totals (Rahman 57, Rahim 114) in Appendix 1, Part 2 ('A Strong Foundation'); no counting rule is stated. Reconstructed: Rahman 57 reproduces exactly under the lemma rule excl. unnumbered basmalahs with no further exclusion. Rahim 114 reproduces only as 115 minus the رحيم in 9:128 (one of the two verses Khalifa deletes; his surah 9 has 127 verses). Note the rule matters: the QAC lemma gives Rahim 116, not 115, because QAC lemmatises the plural رُحَمَاءُ at 48:29 ('merciful ones', describing the believers) as r~aHiym — so Khalifa's 114 reproduces only under the singular-form (Tanzil surface-lemma) rule, not under the QAC lemma rule.

**Exceptions:** 9:128 رحيم dropped under Khalifa's rule (Rahim 115 -> 114). 48:29 رحماء (plural) is counted by the QAC lemma but not by the singular-form rule. The 112 unnumbered basmalahs are excluded (each contains Rahman once and Rahim once; including them: Rahman 169, Rahim 227).

**Verification — scholar's rule:** 114 — Rahim: 115 (Tanzil surface-lemma, excl. basmalahs) minus 9:128 = 114 = 19 x 6. Rahman is 57 under the same rule with no exclusion needed (Tanzil 57 = QAC lemma r~aHoma`n 57).

**Verification — root rule:** 116 — Rahim under the QAC lemma rule (r~aHiym = 116, incl. the 48:29 plural); 115 under the Tanzil surface-lemma rule. Rahman 57 under both rules.

**Assumptions:** scholar set A6 · our set A2 · reconciles under: A6 · numbers by set: A1: 57 / 116, A2: 57 / 116, A3: 57 / 115, A6: 57 / 114, A7: 169 / 227 · 57 reproduces under the lemma rule; 114 needs the 9:128 رحيم dropped (115 on the standard text, 116 by QAC lemma incl. the 48:29 plural).

**Locations (166 verses; verses per surah — 1: 2, 2: 12, 3: 3, 4: 11, 5: 5, 6: 3, 7: 2, 8: 2, 9: 9, 10: 1, 11: 2, 12: 2, 13: 1, 14: 1, 15: 1, 16: 6, 17: 2, 19: 16, 20: 4, 21: 4, 22: 1, 24: 5, 25: 6, 26: 10, 27: 2, 28: 1, 30: 1, 32: 1, 33: 6, 34: 1, 36: 6, 39: 1, 41: 2, 42: 1, 43: 7, 44: 1, 46: 1, 48: 2, 49: 3, 50: 1, 52: 1, 55: 1, 57: 2, 58: 1, 59: 2, 60: 2, 64: 1, 66: 1, 67: 4, 73: 1, 78: 2):** first 20: 1:1, 1:3, 2:37, 2:54, 2:128, 2:143, 2:160, 2:163, 2:173, 2:182, 2:192, 2:199, 2:218, 2:226, 3:31, 3:89, 3:129, 4:16, 4:23, 4:25 … (full list in data/locations.json)
**Locations — scholar's rule (165 verses):** 1:1, 1:3, 2:37, 2:54, 2:128, 2:143, 2:160, 2:163, 2:173, 2:182, 2:192, 2:199, 2:218, 2:226, 3:31, 3:89, 3:129, 4:16, 4:23, 4:25, 4:29, 4:64, 4:96, 4:100, 4:106, 4:110, 4:129, 4:152, 5:3, 5:34, 5:39, 5:74, 5:98, 6:54, 6:145, 6:165, 7:153, 7:167, 8:69, 8:70, 9:5, 9:27, 9:91, 9:99, 9:102, 9:104, 9:117, 9:118, 10:107, 11:41, 11:90, 12:53, 12:98, 13:30, 14:36, 15:49, 16:7, 16:18, 16:47, 16:110 …

### ism-19

**Claim:** The word 'ism' (name) in its full spelling occurs 19 times.

**Arabic:** اسم

**Source:** Rashad Khalifa, *Appendix 1, Part 2, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1_p2.html>

**Section:** Scholar findings

**Corpus and method:** Exact-form count on the Tanzil file (plural أسماء excluded, per Khalifa's 'no plural forms' rule).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** اسم 14 + باسم 4 + الاسم 1 = 19; plural أسماء (skeletonised اسما, 4 occurrences) excluded. Contracted بسم = 115 (114 basmalahs + 11:41).

**Scholar's method (reconstructed):** Reconstructed. Khalifa states only 'Ism (Name) occurs 19 times' (Appendix 1, Part 2). No rule is stated anywhere in Appendix 1 about which forms count: the word 'plural' does not occur in Appendix 1 Part 2 and there is no 'no plural forms' rule in the source. Reconstructed: 19 reproduces only for the full spelling اسم with prefixes (اسم 14 + باسم 4 + الاسم 1), excluding the plural أسماء (12 prefixed/suffixed forms; 4 tokens strip to اسما on the Tanzil text) and the contracted بسم (115 occurrences: 114 basmalahs + 11:41).

**Exceptions:** Plural أسماء excluded (12 prefixed/suffixed forms in the text; the bare skeleton count is 4). Contracted بسم excluded (115x). Suffixed singular forms (اسمه, اسمهو, 5x) excluded by the full-spelling rule but counted by the QAC lemma.

**Verification — scholar's rule:** 19 — Full-spelling forms on the Tanzil text: اسم 14 + باسم 4 + الاسم 1 = 19.

**Verification — root rule:** 39 — QAC lemma {som} = 39: 19 full-spelling + 12 plural أسماء forms + 5 suffixed singular (اسمه/اسمهو) + 3 contracted بسم (1:1, 11:41, 27:30 — the only basmalahs in the QAC word list).

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A3, A6 · numbers by set: A1: 39, A2: 39, A3: 19, A6: 19 · 19 reproduces only for the full spelling اسم (plural أسماء and contracted بسم excluded); the lemma total is 39.

**Locations (19 verses):** 5:4, 6:118, 6:119, 6:121, 6:138, 22:28, 22:34, 22:36, 22:40, 49:11, 55:78, 56:74, 56:96, 69:52, 73:8, 76:25, 87:1, 87:15, 96:1

### first-revelation-words-19

**Claim:** The first revelation (96:1-5) consists of 19 words.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Whitespace token count on the Tanzil file, excluding the merged basmalah.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** 96:1-5 has 20 whitespace tokens excl. basmalah (اقرأ باسم ربك الذي خلق / خلق الإنسان من علق / اقرأ وربك الأكرم / الذي علم بالقلم / علم الإنسان ما لم يعلم); 24 incl. basmalah. Khalifa's 19 is one short.

**Scholar's method (unstated):** method not stated by the source. Khalifa states only 'The famous first revelation (96:1-5) consists of 19 words' (Simple Fact 8). No counting rule is stated — nothing says whether the merged basmalah counts, or whether a repeated or contracted word counts.

**Exceptions:** The basmalah merged into 96:1 in the Tanzil text (4 words) is not a QAC word. The 20 words are: اقرأ باسم ربك الذي خلق / خلق الإنسان من علق / اقرأ وربك الأكرم / الذي علم بالقلم / علم الإنسان ما لم يعلم.

**Verification — scholar's rule:** — — No rule reconstructs 19: 20 words excl. basmalah under every natural count (Tanzil whitespace tokens 20; QAC words 20), 24 incl. basmalah. 19 would require dropping exactly one word (e.g. the repeated اقرأ or the contracted باسم) — no such rule is stated, so none is asserted here.

**Verification — root rule:** 20 — QAC words in 96:1-5 = 20; Tanzil tokens excl. basmalah = 20.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: 20, A3: 20, A7: 24 · 20 words under every natural count (24 with the basmalah); 19 would require dropping exactly one word — no such rule is stated.

**Locations (5 verses):** 96:1, 96:2, 96:3, 96:4, 96:5

### first-revelation-letters-76

**Claim:** The first revelation (96:1-5) consists of 76 letters.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Letter counting under our stated convention (see meta), excluding the merged basmalah.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 96:1-5 = 76 letters excl. basmalah under our convention — confirmed.

**Scholar's method (unstated):** method not stated by the source. Khalifa states only 'This 19-worded first revelation consists of 76 letters' (Simple Fact 9). No letter-counting rule is stated.

**Exceptions:** Basmalah excluded (19 letters; including it the count is 95).

**Verification — scholar's rule:** 76 — 76 letters excl. basmalah under the project's stated letter convention (base letters; alef wasla counts; dagger alif/small waw/small yeh do not count). The letter rule itself is unstated by Khalifa.

**Verification — root rule:** 76 — Same 76 (a letter count has no root rule).

**Assumptions:** scholar set — · our set A4 · reconciles under: A4 · numbers by set: A4: 76, A7: 95 · 76 letters excl. the basmalah under the project convention; 95 with it — Khalifa states no letter rule.

**Locations (5 verses):** 96:1, 96:2, 96:3, 96:4, 96:5

### surah-96-19-verses-304-letters

**Claim:** Surah 96 has 19 verses and 304 letters in total.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Verse count (standard Hafs table) and letter counting under our stated convention (see meta).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Surah 96 has 19 verses (standard) and 304 letters by our recount — Khalifa's figures exactly.

**Scholar's method (unstated):** method not stated by the source for the letter total. Khalifa states 'Sura 96 consists of 304 Arabic letters' (Simple Fact 12) and 19 verses (Simple Fact 10, the standard Hafs count). No letter-counting rule is stated.

**Exceptions:** The 304 total REQUIRES the merged basmalah to be counted (285 letters excl. basmalah + 19 = 304). Note the inconsistency inside Khalifa's own figures: his 76 letters for 96:1-5 requires the basmalah EXCLUDED, while his 304 for the whole surah requires it INCLUDED.

**Verification — scholar's rule:** 304 — 304 letters incl. the merged basmalah under the project's letter convention; 19 verses (standard Hafs count; QAC max verse for surah 96 is 19).

**Verification — root rule:** 285 — 285 letters excl. the merged basmalah under the project's letter convention (QAC words in surah 96 = 102).

**Assumptions:** scholar set A6 · our set A4 · reconciles under: A6, A7 · numbers by set: A4: 19 / 285, A6: 19 / 304, A7: 19 / 304 · 19 verses and 304 letters reproduce only with the merged basmalah counted in (285 without it) — the opposite basmalah convention from the 76-letter count for 96:1–5.

**Locations (19 verses):** 96:1, 96:2, 96:3, 96:4, 96:5, 96:6, 96:7, 96:8, 96:9, 96:10, 96:11, 96:12, 96:13, 96:14, 96:15, 96:16, 96:17, 96:18, 96:19

### surah-110-19-words

**Claim:** Surah 110 consists of 19 words (excluding the Basmalah), and its first verse consists of 19 letters.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Whitespace token count and letter counting under our stated convention (see meta), excluding the merged basmalah.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Surah 110 = 19 words excl. basmalah; verse 110:1 = 19 letters excl. basmalah — confirmed.

**Scholar's method (unstated):** method not stated by the source. Khalifa states only 'The last revelation (Sura 110) consists of 19 words' (Simple Fact 13) and 'The first verse of the last revelation (110:1) consists of 19 letters' (Simple Fact 14). No counting rule is stated for either.

**Exceptions:** Basmalah merged into 110:1 excluded from both counts (4 words / 19 letters).

**Verification — scholar's rule:** 19 — 19 words excl. basmalah (Tanzil tokens 19; QAC words 19); verse 110:1 = 19 letters excl. basmalah under the project's letter convention.

**Verification — root rule:** 19 — Same 19 words (QAC words in surah 110 = 19).

**Assumptions:** scholar set — · our set A1 · reconciles under: A1, A4 · numbers by set: A1: 19 / —, A4: — / 19, A7: 23 / 38 · 19 words (A1) and 19 letters in 110:1 (A4) both reproduce excl. the basmalah; 23 words / 38 letters with it.

**Locations (3 verses):** 110:1, 110:2, 110:3

### verse-number-checksum-118123

**Claim:** The sum of the verse numbers of all verses containing the word 'Allah' is 118,123 = 19 x 6,217.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Verse-number sum over verses containing the Allah lemma, on the Tanzil file (see note for the two conditions required).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The sum is 118,123 exactly — but only under two conditions: excluding the 112 unnumbered basmalahs AND excluding Khalifa's two rejected verses 9:128-129 (only 9:129 contains Allah, verse number 129; 118,252 - 129 = 118,123). Without those exclusions the sum is 118,340. Khalifa's figure is therefore confirmed as a property of his edited text, not of the standard text.

**Scholar's method (reconstructed):** Reconstructed. Khalifa states only the total (118,123 = 19 x 6,217) and the Allah total (2,698). No rule is stated for which verses enter the sum. Reconstructed: the sum reproduces only if (a) each verse is counted once however many times Allah occurs in it, (b) the 112 unnumbered basmalahs are excluded (they would add the verse-1 numbers of 112 surahs), and (c) 9:128-129 are dropped (only 9:129 contains Allah: -129). 118,252 - 129 = 118,123.

**Exceptions:** 9:129 (verse number 129) dropped — the only effect of deleting 9:128-129 on this sum, since 9:128 contains no Allah. Unnumbered basmalahs excluded: including them adds 88 to the sum (verse-1 numbers of the surahs whose verse 1 does not otherwise contain Allah).

**Verification — scholar's rule:** 118123 — Sum of verse numbers of Allah-containing verses, excl. unnumbered basmalahs and excl. 9:128-129 = 118,123 exactly. Cross-check on QAC lemma verses gives the same 118,252 excl. basmalahs, minus 129 = 118,123.

**Verification — root rule:** 118340 — Same sum on the standard text incl. the unnumbered basmalahs = 118,340; excl. basmalahs only = 118,252. 1,821 verses contain Allah excl. basmalahs (1,909 incl.).

**Assumptions:** scholar set A6 · our set A1 · reconciles under: A6 · numbers by set: A1: 118252, A2: 118252, A6: 118123, A7: 118340 · 118,123 reproduces only excluding the basmalahs and Khalifa's two deleted verses (9:129 contributes 129); the standard text gives 118,252.

**Locations (1821 verses; verses per surah — 1: 2, 2: 172, 3: 131, 4: 135, 5: 88, 6: 65, 7: 45, 8: 52, 9: 101, 10: 49, 11: 33, 12: 34, 13: 23, 14: 28, 15: 2, 16: 64, 17: 10, 18: 14, 19: 8, 20: 6, 21: 5, 22: 50, 23: 12, 24: 50, 25: 6, 26: 13, 27: 25, 28: 21, 29: 30, 30: 21, 31: 21, 32: 1, 33: 51, 34: 8, 35: 27, 36: 2, 37: 15, 38: 2, 39: 43, 40: 37, 41: 11, 42: 24, 43: 3, 44: 3, 45: 15, 46: 14, 47: 21, 48: 25, 49: 14, 50: 1, 51: 3, 52: 2, 53: 6, 57: 22, 58: 22, 59: 17, 60: 11, 61: 10, 62: 8, 63: 9, 64: 14, 65: 9, 66: 8, 67: 3, 69: 1, 70: 1, 71: 7, 72: 8, 73: 1, 74: 2, 76: 4, 79: 1, 81: 1, 82: 1, 84: 1, 85: 3, 87: 1, 88: 1, 91: 1, 95: 1, 96: 1, 98: 3, 104: 1, 110: 2, 112: 2):** first 20: 1:1, 1:2, 2:7, 2:8, 2:9, 2:10, 2:15, 2:17, 2:19, 2:20, 2:22, 2:23, 2:26, 2:27, 2:28, 2:55, 2:60, 2:61, 2:62, 2:64 … (full list in data/locations.json)
**Locations — scholar's rule (1820 verses):** 1:1, 1:2, 2:7, 2:8, 2:9, 2:10, 2:15, 2:17, 2:19, 2:20, 2:22, 2:23, 2:26, 2:27, 2:28, 2:55, 2:60, 2:61, 2:62, 2:64, 2:67, 2:70, 2:72, 2:73, 2:74, 2:75, 2:76, 2:77, 2:79, 2:80, 2:83, 2:85, 2:88, 2:89, 2:90, 2:91, 2:94, 2:95, 2:96, 2:97, 2:98, 2:101, 2:102, 2:103, 2:105, 2:106, 2:107, 2:109, 2:110, 2:112, 2:113, 2:114, 2:115, 2:116, 2:118, 2:120, 2:126, 2:132, 2:136, 2:137 …

### khalifa-verse-total-6346

**Claim:** The total number of verses in the Quran is 6,346 = 19 x 334 (6,234 numbered verses + 112 unnumbered Basmalahs).

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Standard Hafs count is 6,236 verses; Khalifa's figure rests on counting basmalahs as verses and deleting 9:128-129.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** The arithmetic checks out (6,236 + 112 - 2 = 6,346) but the deletion of 9:128-129 is the contested step: with those verses the Allah count would be 2,699 not 2,698 and Rahim 115 not 114. The scholarly consensus rejects the deletion (see the reception finding).

**Scholar's method (stated):** Stated by Khalifa himself (Simple Fact 3): 'The total number of verses in the Quran is 6346, or 19 x 334. [6234 numbered verses & 112 un-numbered verses (Basmalahs) 6234+112 = 6346]'. His tables (Appendix 1, Part 2, Tables 22 and 25) give surah 9 as 127 verses, i.e. 6,234 = 6,236 - 2 (9:128-129 dropped).

**Exceptions:** 9:128-129 deleted from the numbered verses (surah 9 = 127 verses in his text, not 129). The 112 unnumbered basmalahs are counted as verses; surah 1's basmalah is a numbered verse (1:1) and is not double-counted.

**Verification — scholar's rule:** 6346 — Arithmetic checks: 6,234 + 112 = 6,346 = 19 x 334.

**Verification — root rule:** 6236 — Standard Hafs numbered verses = 6,236 (QAC file: 6,236 verses). Counting the 112 unnumbered basmalahs as verses WITHOUT dropping 9:128-129 gives 6,348 (Botani's figure).

**Assumptions:** scholar set A5 · our set A1 · reconciles under: A5 · numbers by set: A1: 6236, A5: 6346, A7: 6348 · 6,346 is arithmetic under Khalifa's stated rule (6,234 numbered + 112 basmalahs); the standard count is 6,236, or 6,348 with basmalahs counted and no verses deleted.

**Locations:** not applicable — verse total, not a word/letter count — no occurrences to locate; the two verses at issue are 9:128-129

### khalifa-reception

**Claim:** Khalifa's 19-based 'mathematical miracle' was published from 1973-1989 and drew both praise and sustained scholarly/skeptical criticism.

**Source:** Rashad Khalifa; Martin Gardner; Bilal Philips; Ziauddin Sardar; Edip Yüksel, *Quran: The Final Testament (1989); Scientific American (1980); The Qur'an's Numerical Miracle: Hoax and Heresy (1987)* (1989) — <https://submission.org/App1.html>

**Section:** Scholar findings

**Corpus and method:** Literature review (bibliographic sources, verified by web search 2026-11-06).

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Timeline: initials research from 1969; Miracle of the Quran: Significance of the Mysterious Alphabets (1973); the 19-code claimed January 1974; The Computer Speaks: God's Message to the World (1981); Quran: Visual Presentation of the Miracle (1982); Quran: The Final Testament translation (1989). Reception: Martin Gardner, Scientific American, September 1980, p. 22 ('ingenious study...'); critical review in Skeptical Inquirer 21(5), September-October 1997, pp. 16-17; Canadian Council on the Study of Religion, Quarterly Review, April 1983 (quoted by proponents as calling it 'an authenticating proof'); Bilal Philips, The Qur'an's Numerical Miracle: Hoax and Heresy (1987/1407 AH, 76 pp., 2nd ed. 2002). Submission.org's own 2002 recount confirmed Khalifa's initial counts 'except for a few counts' (submission.org/App1.html). The following were listed in an earlier draft of this note but were NOT individually verified in the 2026-11-07 re-check and are not asserted here: Gardner, Skeptical Inquirer p. 58; Ziauddin Sardar, Explorations in Islamic Science (1989); Edip Yüksel, Nineteen: God's Signature in Nature and Scripture (Brainbow Press, 2011); Abdullah Arik, Beyond Probability (2012); Matthew Stanley, A Miracle on Trial (2016).

**Scholar's method (not_a_count):** not a count — literature/provenance fact. No counting method applies; the items below were checked against the cited publications and against Khalifa's own Appendix 1 text.

**Exceptions:** None — the claim is a reception history, not a count. Note the Gardner date conflict: Philips' book (quoting the column) and this finding say September 1980, p. 22; Yuksel's 'Nineteen' material says September 1981, pp. 22-24. Philips is treated as the stronger witness here.

**Verification — scholar's rule:** — — Timeline verified: initials research from 1969 (Khalifa, App1; Wikipedia 'Quran code'); 'Miracle of the Quran: Significance of the Mysterious Alphabets' 1973 (Philips book, foreword/contents); 19-code claimed January 1974 (App1; Wikipedia); 'The Computer Speaks' 1981 and 'Visual Presentation of the Miracle' 1982 (Philips foreword); 'The Final Testament' 1989 (App1 itself). Gardner, Scientific American, September 1980, p. 22 ('ingenious study of the Koran') — confirmed via Philips' book, which quotes the passage and its context (a fictional 'Mathematical Games' story). Skeptical Inquirer 21(5), Sept-Oct 1997 — confirmed as the issue carrying Gardner's 'The Numerology of Dr Rashad Khalifa' (fetched PDF, pp. 16 and 58 visible; the finding's pp. 16-17 range is consistent with the fetched file). Bilal Philips, 'The Qur'an's Numerical Miracle: Hoax and Heresy', 1987/1407 AH, 76 pp., 2nd ed. 2002 — confirmed via the Scribd/pdf-archive copies. Submission.org's 2002 recount ('confirmed Khalifa's counts of all the Quranic initials except for a few counts in "A" and "L"') — confirmed verbatim on submission.org/App1.html itself.

**Verification — root rule:** — — Same verification (no corpus count applies). NOT verified: the Canadian Council on the Study of Religion, Quarterly Review, April 1983 quotation ('an authenticating proof') — no source for it was located in this pass; the finding's note already hedges it as 'quoted by proponents'. The items the finding's note lists as not individually verified (Gardner SI p. 58; Sardar 1989; Yuksel 2011; Arik 2012; Stanley 2016) remain unverified.

**Assumptions:** scholar set — · our set — · reconciles under: none · numbers by set: — · Not a word/letter count — a reception-history fact; no counting assumption applies.

**Locations:** not applicable — literature/reception fact — no occurrences to locate

## Modern corpus linguistics

### qac-word-count-77429

**Claim:** The Quran contains 77,429 words (Quranic Arabic Corpus FAQ and v0.4 release notes); 77,430 is the earlier v0.3 figure.

**Source:** Kais Dukes, University of Leeds, *Quranic Arabic Corpus — FAQ and release notes* (2009) — <https://corpus.quran.com/faq.jsp>

**Section:** Scholar findings

**Corpus and method:** QAC v0.4 morphological annotation; our recount on the Tanzil Uthmani text.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Our recount: 77,881 whitespace tokens incl. basmalahs; 77,433 excl. 112 unnumbered basmalahs — 4 above the published 77,429. The gap is fully explained by word-boundary conventions: exactly 4 verses differ by one token each — 2:181, 8:6, 13:37 (بعدما: two tokens in Tanzil vs one QAC word) and 37:130 (آل ياسين: two words in Tanzil vs one in QAC). An earlier draft of this note attributed the whole gap to 37:130 alone; that accounts for only 1 of the 4.

**Scholar's method (stated):** Stated by the QAC FAQ: 'The annotation for each of the 77,429 words in the Quran was then reviewed in stages by two annotators.' The word unit is the QAC morphological word (LOCATION surah:verse:word:segment); only the 1:1 basmalah is in the word list — the 112 unnumbered basmalahs prepended in Tanzil are NOT QAC words.

**Exceptions:** QAC word boundaries differ from Tanzil whitespace tokens in exactly 4 verses (2:181, 8:6, 13:37 — بعدما as one QAC word vs two Tanzil tokens — and 37:130 — آل ياسين as two Tanzil tokens vs one QAC word). Those 4 verses explain the whole gap between the QAC total (77,429) and the Tanzil token total excl. basmalahs (77,433).

**Verification — scholar's rule:** 77429 — Counted from the v0.4 file itself: 77,429 words, 128,219 segments, 6,236 verses — exactly the published figure.

**Verification — root rule:** 77429 — Same 77,429 QAC words. Tanzil whitespace tokens excl. unnumbered basmalahs = 77,433 (4 more; see exceptions).

**Assumptions:** scholar set A5 · our set A1 · reconciles under: A1, A5 · numbers by set: A1: 77429, A3: 77433, A5: 77429, A7: 77881 · 77,429 QAC words reproduces exactly; Tanzil whitespace tokens give 77,433 excl. basmalahs (77,881 incl.) — 4 verses differ by one token each.

**Locations:** not applicable — whole-corpus total, not a set of occurrences; per-surah QAC word counts are in data/methods_check_B_results.json (qac_words_per_surah)

### dukes-unique-words

**Claim:** The Quran has 18,994 unique surface forms, 12,183 unique stems, 1,685 unique roots and 3,382 unique lemmas (QAC annotation).

**Source:** Kais Dukes (figures as widely published), *'Number of unique words in the Quran' — circulating estimate (QAC figures)* — <https://www.calendar-uk.co.uk/frequently-asked-questions/how-long-is-a-quran>

**Section:** Scholar findings

**Corpus and method:** QAC v0.4 annotation (Dukes' 2013 primary-source answer); our recount on the Tanzil Uthmani text for the surface-form figure only.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Unique surface forms 18,994 — our raw unique count is 18,994 exactly. Skeletonised unique forms 14,881. Stem/root/lemma figures (12,183 / 1,685 / 3,382) were not recounted (they need the QAC annotation). The earlier draft attributed these figures to a Dukes blog post (quickestwaytoquran.blogspot.com, 2013) — that URL returns 404 and Dukes' authorship of that post could not be confirmed, so the figures are cited here as the widely published estimate, not as Dukes' blog post. The earlier note's 'Dukes' estimate: at most 7,000 unique words' was not verified and is dropped.

Methods pass (2026-11-08): confirmed→differs: recounted from QAC v0.4, only the 18,994 surface-form figure reproduces exactly. Stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832 (not 3,382).

**Scholar's method (unstated):** method not stated by the source. The estimate ('77,430 words, 18,994 unique words, 12,183 stems, 3,382 lemmas and 1,685 roots') is printed without author, method, version or counting unit on calendar-uk.co.uk; no rule is stated for what counts as a 'unique word', 'stem', 'lemma' or 'root'.

**Exceptions:** The four figures may come from an older QAC version (v0.3: 77,430 words, 128,076 morphemes) or a different lemmatisation — no natural QAC v0.4 rule reproduces 12,183 / 1,685 / 3,382 (POS subsets tried: nouns only 2,690 lemmas; nouns+adjectives+verbs 4,593; none is 3,382).

**Verification — scholar's rule:** 18994 — Unique surface forms (raw whitespace tokens) = 18,994 exactly — the one figure that reproduces. Stems/roots/lemmas do not reproduce (see root rule).

**Verification — root rule:** 4832 — From the QAC v0.4 annotation: unique stem lemmas 4,832 (not 3,382); unique stem forms 12,113 (not 12,183); unique roots 1,642 at both word and segment level (not 1,685); skeletonised unique surface forms 14,881.

**Assumptions:** scholar set — · our set A1 · reconciles under: none · numbers by set: A1: — / — / 1642 / —, A2: — / — / — / 4832, A3: 18994 / — / — / — · Only the 18,994 unique surface forms reproduce; stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832 (not 3,382).

**Locations:** not applicable — vocabulary inventory, not a set of occurrences

### qac-morphology

**Claim:** The Quranic Arabic Corpus provides manually verified morphological annotation of the whole Quran, about 99% accurate, reviewed in stages by two annotators.

**Source:** Kais Dukes, University of Leeds, *Quranic Arabic Corpus — release notes* (2011) — <https://corpus.quran.com/releasenotes.jsp>

**Section:** Scholar findings

**Corpus and method:** QAC v0.4 release notes; verifying needs the QAC data itself, not the plain text.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Treebank covered 40% by word count in v0.4. The 128,076-morpheme figure is from the QAC v0.3 announcement (12 March 2011) ... Not recounted here beyond that (the annotation layer is the sibling agents' and the data pipeline's work).

**Scholar's method (not_a_count):** not a count — literature/provenance fact about the corpus itself. No counting method applies; the factual items were checked against the QAC FAQ and release notes and against the v0.4 file.

**Exceptions:** The 128,076-morpheme figure is from the v0.3 announcement, not v0.4; the v0.4 file has 128,219 segments (143 more). The treebank coverage figure (40%) is a v0.4 release-notes figure, not a recount (the syntax layer is not in the morphology file).

**Verification — scholar's rule:** — — FAQ (fetched 2026-11-08): 'The annotation for each of the 77,429 words in the Quran was then reviewed in stages by two annotators. It is believed that the text is now 99% accurate in terms of morphological annotation.' Release notes v0.4 (1 May 2011, fetched): treebank 'covers 40% of the Quran by word count (30,895 out of 77,429 words)' for chapters 1-8 and 59-114. V0.3 announcement (Kais Dukes, Corpora-List, archived): 'Each of the 77,430 words in the Quran has been morphologically segmented, resulting in 128,076 individual morphemes' — confirmed verbatim. Our v0.4 file: 128,219 segments.

**Verification — root rule:** — — Same verification (no corpus count applies beyond the segment count above: 128,219).

**Assumptions:** scholar set — · our set — · reconciles under: none · numbers by set: — · Not a word/letter count — a provenance fact about the corpus; no counting assumption applies.

**Locations:** not applicable — provenance fact about the corpus — no occurrences to locate

### tanzil-provenance

**Claim:** The Tanzil Quran Text (Uthmani) is derived from the Medina Mushaf, Hafs narration, distributed under CC BY 3.0 with verbatim redistribution only.

**Source:** Tanzil Project, *Tanzil — Quran Text licence and Medina Mushaf documentation* — <https://tanzil.net/docs/text_license>

**Section:** Scholar findings

**Corpus and method:** Tanzil project documentation; the corpus file used for all recounts here is Tanzil Uthmani v1.1.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Tanzil's licence documentation (tanzil.net/docs/text_license) and Medina Mushaf documentation (tanzil.net/docs/Medina_Mushaf) confirm the provenance: Medina Mushaf, Hafs reading, CC BY 3.0, verbatim redistribution only. The previously cited download page (tanzil.net/download) does not display the licence or Mushaf details in its text, so the citation is re-pointed. This is the text all our spot-recounts ran against.

**Scholar's method (not_a_count):** not a count — literature/provenance fact. No counting method applies; checked against Tanzil's own documentation pages.

**Exceptions:** None. The file used for all recounts here is Tanzil Uthmani v1.1 (per the finding's note); the licence and Mushaf pages do not carry a version number, so the v1.1 label itself was not re-verified from those pages.

**Verification — scholar's rule:** — — Licence page (tanzil.net/docs/text_license, fetched): 'License: Creative Commons Attribution 3.0', 'Permission is granted to copy and distribute verbatim copies of this text, but CHANGING IT IS NOT ALLOWED' — confirms CC BY 3.0 with verbatim redistribution only. Medina Mushaf page (tanzil.net/docs/Medina_Mushaf, fetched): 'The Quran text provided by Tanzil is based on the Medina Mushaf, narration of Hafs.'

**Verification — root rule:** — — Same verification (no corpus count applies).

**Assumptions:** scholar set — · our set — · reconciles under: none · numbers by set: — · Not a word/letter count — a provenance fact; no counting assumption applies.

**Locations:** not applicable — provenance fact — no occurrences to locate

### text-fabric-quran

**Claim:** Text-Fabric Quran (Roorda & van Lit, 2019) re-expresses the Quranic Arabic Corpus morphology as linked open data.

**Source:** Dirk Roorda & Cornelis van Lit, *Text-Fabric Quran (2019)* (2019) — <https://github.com/q-ran/quran>

**Section:** Scholar findings

**Corpus and method:** GitHub q-ran/quran; Zenodo DOI 10.5281/zenodo.2532177; built from QAC 0.4 morphology + Tanzil Uthmani v1.0.2; CC-BY 4.0. Not used in our recounts.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Roorda (2018), 'Text-Fabric: Text representation for linguistic annotation', Research Data Journal for the Humanities and Social Sciences 3(1), 1-23. The dataset itself was not re-analysed here. (The Zenodo DOI 10.5281/zenodo.2532177 is now confirmed: doi.org resolves it to 'q-ran/quran: Initial release', published 5 January 2019, v0.1, Dirk Roorda.)

**Scholar's method (not_a_count):** not a count — literature/provenance fact. No counting method applies; checked against the GitHub repository and the Zenodo DOI record.

**Exceptions:** The Zenodo record for the v0.1 release lists Dirk Roorda alone as author; Cornelis van Lit is co-author of the repository (README lists both). The dataset was not re-analysed here.

**Verification — scholar's rule:** — — GitHub q-ran/quran (fetched): 'We have taken the source materials from Quranic Arabic Corpus 0.4 (2011) by Kais Dukes and Tanzil'; 'The data in TF format is licensed as CC-BY 4.0'; authors Cornelis van Lit and Dirk Roorda; released 2019-01-07; repo now archived. Zenodo DOI 10.5281/zenodo.2532177 (resolved via doi.org, fetched): 'q-ran/quran: Initial release', published 5 January 2019, Version v0.1, Dirk Roorda — the DOI is now confirmed, correcting the finding's note.

**Verification — root rule:** — — Same verification (no corpus count applies). Roorda (2018), 'Text-Fabric: Text representation for linguistic annotation', Research Data Journal for the Humanities and Social Sciences 3(1), 1-23, was not re-fetched in this pass.

**Assumptions:** scholar set — · our set — · reconciles under: none · numbers by set: — · Not a word/letter count — a provenance fact; no counting assumption applies.

**Locations:** not applicable — provenance fact — no occurrences to locate

### root-frequency-studies

**Claim:** Root-frequency studies of the Quran (QAC 0.4) find about 1,650 roots; the most frequent root is Alh (Allah), about 2,851 occurrences.

**Arabic:** أ-ل-ه

**Source:** Abdul Baqi (QAC 0.4 data by Kais Dukes), *'Standing on the Shoulder of Giants' (abdulbaqi.io, 2019)* (2019) — <http://abdulbaqi.io/2019/01/15/quranic_roots/>

**Section:** Scholar findings

**Corpus and method:** Corpus-based root counts from QAC 0.4 morphology (abdulbaqi.io 2019; thequran.love 2026; Malkoç 2025). Root counting is the sibling agents' task; not recounted here.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** abdulbaqi.io (2019): 1,651 roots; top roots Alh 2,851, qwl 1,722, kwn 1,390, rbb 980 (data file quranic-corpus-morphology-0.4.txt, 128,276 lines). Our independent QAC recount reproduces Alh 2,851, qwl 1,722, kwn 1,390, rbb 980 and Ḥ-S-N 194, and 49,967 root-bearing tokens (64.5%) — but counts 1,642 distinct roots, not 1,651 (thequran.love gives 1,642 too) and not Dukes' 1,685: the root total depends on how rare/derived forms are grouped. Zia H Shah / thequran.love (2026): 1,642 roots, verbal-only counts (qwl 1,618, kwn 1,358). Muzaffer Malkoç, Beauty as Method (Zenodo, 2025): root concordance via Tanzil + Abd al-Baqi's al-Mu'jam al-Mufahras, e.g. Ḥ-S-N 194. Note the Alh root count (2,851) is a different unit from the Allah lemma count (2,699). The earlier draft's file URL returned 404; the live page is /2019/01/15/quranic_roots/. The post is Abdul Baqi's; Dukes is the data source, not a co-author.

**Scholar's method (stated):** Stated in the post itself (abdulbaqi.io, 2019): the pipeline greps ROOT: from the FEATURES column of the QAC v0.4 morphology file and counts occurrences per SEGMENT line (sort | uniq -c), i.e. a segment-level count, not a per-word count. The post's file is the same 128,276-line v0.4 file used here. Note the post counts every ROOT: occurrence including repeated roots inside one word; in this file that makes no difference (see exceptions).

**Exceptions:** Segment-level and word-level root counting give identical results for every root in this file: no root's segment count exceeds its word count (exactly one word carries two root-bearing segments — 20:94:2, يابنُمَّ 'O son of my mother', stems bona [ROOT bny] + &um~a [ROOT Amm] — giving 49,968 segment ROOT occurrences vs 49,967 root-bearing words). Abdulbaqi's published pipeline re-run on this file gives 1,641 unique roots, not his printed 1,651: it loses the root wAd (81:8:2, الموءودة 'the baby girl buried alive') because that word's FORM 'mawo'u,dapu' contains a comma, shifting cut -d',' -f4. His printed 1,651 reproduces under no rule constructed here (word level 1,642; segment level 1,642; his pipeline 1,641). The thequran.love figure (1,642) matches the word/segment count.

**Verification — scholar's rule:** 1641 — Abdulbaqi's own published pipeline re-run on this file: 1,641 unique roots, 49,960 segment ROOT occurrences. His printed 1,651 does not reproduce from this file by his own method.

**Verification — root rule:** 1642 — Unique roots 1,642 (word level = segment level). Top roots reproduce exactly at both levels: Alh 2,851, qwl 1,722, kwn 1,390, rbb 980; Ḥ-S-N 194 reproduces (word level). Alh root count (2,851) is a different unit from the Allah lemma count (2,699): the root also covers allahumma (5) and generic ilah (147).

**Assumptions:** scholar set A5 · our set A1 · reconciles under: none · numbers by set: A1: 1642 / 2851, A5: 1641 / 2851 · Alh 2,851 reproduces exactly; the 1,651 root total reproduces under no rule (1,642 by word/segment count, 1,641 by the post's own pipeline).

**Locations (1879 verses; verses per surah — 1: 2, 2: 174, 3: 133, 4: 135, 5: 89, 6: 67, 7: 47, 8: 53, 9: 101, 10: 50, 11: 34, 12: 34, 13: 24, 14: 29, 15: 2, 16: 66, 17: 11, 18: 16, 19: 9, 20: 8, 21: 17, 22: 50, 23: 12, 24: 50, 25: 9, 26: 14, 27: 25, 28: 22, 29: 31, 30: 21, 31: 21, 32: 1, 33: 51, 34: 8, 35: 27, 36: 3, 37: 18, 38: 4, 39: 44, 40: 39, 41: 12, 42: 24, 43: 6, 44: 4, 45: 15, 46: 15, 47: 21, 48: 25, 49: 14, 50: 1, 51: 3, 52: 2, 53: 6, 57: 22, 58: 22, 59: 17, 60: 11, 61: 10, 62: 8, 63: 9, 64: 14, 65: 9, 66: 8, 67: 3, 69: 1, 70: 1, 71: 8, 72: 8, 73: 2, 74: 2, 76: 4, 79: 1, 81: 1, 82: 1, 84: 1, 85: 3, 87: 1, 88: 1, 91: 1, 95: 1, 96: 1, 98: 3, 104: 1, 110: 2, 112: 2, 114: 1):** first 20: 1:1, 1:2, 2:7, 2:8, 2:9, 2:10, 2:15, 2:17, 2:19, 2:20, 2:22, 2:23, 2:26, 2:27, 2:28, 2:55, 2:60, 2:61, 2:62, 2:64 … (full list in data/locations.json)

### most-frequent-min-3226

**Claim:** The most frequent word in the Quran is 'min' (from), 3,226 times, followed by 'Allah' 2,699 and 'ma' 2,565.

**Arabic:** من / الله / ما

**Source:** Words of Quran (QAC v0.4 data), *wordsofquran.com — most frequent words* — <https://wordsofquran.com/>

**Section:** Scholar findings

**Corpus and method:** wordsofquran.com, from QAC v0.4; our recount on the Tanzil file for the min lemma.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Our min lemma recount = 3,314 (من 2,763 + ومن 342 + لمن 94 + فمن 90 + بمن 10 + كمن 9 + ولمن 5 + وبمن 1) — 88 above the published 3,226, method unclear. (wordsofquran.com also gives 4,832 unique lemmas of ~77,797 total words — figures that differ from Dukes' own, definitional.)

Methods pass (2026-11-08): differs→confirmed: QAC lemma min (preposition) is 3,226 exactly; ma 2,565 and Allah 2,699 also reproduce exactly under the same lemma rule. The old 'differs' rested on a Tanzil skeleton count (3,314) that conflates مِن with مَن.

**Scholar's method (unstated):** method not stated by the source. wordsofquran.com states its data come from QAC v0.4 but gives no counting rule for 'min' — nothing says whether the relative pronoun مَن counts, whether suffixed forms (منها, مما) count, or what a 'word' is. The method is identified by reproduction (see verification): the QAC lemma rule reproduces all three of the site's figures exactly.

**Exceptions:** Tanzil skeleton matching conflates مِن (preposition, QAC lemma min) with مَن (relative pronoun, QAC lemma man) once diacritics are stripped. Of the 3,314 Tanzil bare-من tokens, 2,499 are QAC min, 806 are QAC man, 6 are the verb man~a ('he bestowed'), and 3 are alignment artifacts at 13:37 (the بعدما verse). The QAC min total (3,226) = 2,499 bare tokens + 727 suffixed/contracted forms (مما, منها, مني ...). The site also gives 4,832 unique lemmas of ~77,797 total words — the lemma total matches QAC (4,832); the 77,797 word total matches no count here (QAC 77,429; Tanzil excl. basmalahs 77,433; incl. 77,881).

**Verification — scholar's rule:** 3226 — QAC lemma min (preposition) = 3,226 exactly. The site's other two figures also reproduce exactly under the same rule: lemma maA = 2,565, lemma {ll~ah = 2,699. All three figures identify the method as QAC v0.4 lemma counts.

**Verification — root rule:** 3226 — Same 3,226 under the QAC lemma rule. The Tanzil skeleton-lemma count is 3,314 — a different unit (it merges min and man); the earlier note's '88 above' is arithmetic coincidence, not an explanation (3,314 - 3,226 = 88, but the man tokens inside the 3,314 number 806, not 88).

**Assumptions:** scholar set — · our set A2 · reconciles under: A1, A2 · numbers by set: A1: 3226 / 2699 / 2565, A2: 3226 / 2699 / 2565, A3: 3314 / — / — · All three figures reproduce exactly under the QAC lemma rule; the Tanzil skeleton count for من is 3,314 because it conflates مِن with مَن.

**Locations (2230 verses; verses per surah — 2: 159, 3: 103, 4: 105, 5: 74, 6: 67, 7: 108, 8: 30, 9: 66, 10: 53, 11: 58, 12: 52, 13: 27, 14: 27, 15: 34, 16: 58, 17: 35, 18: 46, 19: 34, 20: 40, 21: 46, 22: 37, 23: 28, 24: 29, 25: 17, 26: 44, 27: 35, 28: 48, 29: 32, 30: 30, 31: 12, 32: 17, 33: 35, 34: 25, 35: 25, 36: 28, 37: 31, 38: 28, 39: 35, 40: 30, 41: 25, 42: 33, 43: 30, 44: 10, 45: 16, 46: 21, 47: 14, 48: 11, 49: 8, 50: 15, 51: 14, 52: 9, 53: 11, 54: 12, 55: 8, 56: 19, 57: 15, 58: 10, 59: 13, 60: 7, 61: 6, 62: 7, 63: 2, 64: 5, 65: 9, 66: 5, 67: 7, 68: 6, 69: 8, 70: 7, 71: 6, 72: 8, 73: 2, 74: 4, 75: 2, 76: 10, 77: 3, 78: 3, 79: 2, 80: 4, 81: 1, 83: 4, 85: 3, 86: 4, 88: 3, 90: 1, 92: 1, 93: 1, 96: 1, 97: 2, 98: 5, 105: 1, 106: 1, 111: 1, 113: 4, 114: 2):** first 20: 2:3, 2:4, 2:5, 2:8, 2:19, 2:21, 2:22, 2:23, 2:25, 2:26, 2:27, 2:34, 2:35, 2:36, 2:37, 2:38, 2:48, 2:49, 2:51, 2:52 … (full list in data/locations.json)

### classical-word-totals

**Claim:** Classical authorities give the Quran's word total as 77,439 (with variants 77,430 / 77,437 / 77,797 / 77,934).

**Source:** al-Suyuti (via SeekersGuidance, Shaykh Anas al-Musa), *al-Itqan fi 'Ulum al-Qur'an — classical word and letter totals* — <https://seekersguidance.org/answers/quran/what-is-the-total-number-of-words-verses-and-letters-in-the-quran/>

**Section:** Scholar findings

**Corpus and method:** Classical counts (al-Suyuti, al-Itqan; Basra reciters; Ata' bin Yasar); our recount on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Our 77,433 (excl. unnumbered basmalahs) is 6 below the lowest classical figure (77,439) — within the spread of counting conventions. Kufan reciters recorded 77,430, Basran 77,437 (arabiantongue.com). The 77,430 / 77,797 / 77,934 variants are not on the SeekersGuidance page (which gives 77,439 and 77,437); they are al-Suyuti variants reported by other witnesses (Kufan 77,430 per arabiantongue.com; al-Suyuti collecting 77,934, 77,437, 77,277 per answeringislam.net; eaalim.com lists 77,439, 77,797 and 77,934).

**Scholar's method (stated):** Stated on the SeekersGuidance page (Shaykh Anas al-Musa, summarising al-Suyuti's al-Itqan and classical sources): the variation comes from word-boundary rules — 'they counted (في السماء) and (في الأرض) and (في خلق) and the like as two words, while some counted them as one word'. The Basra reciters' figure is 77,439 words; Kufan 77,430; Ata' b. Yasar 77,437. The 77,430 / 77,797 / 77,934 variants are al-Suyuti variants reported by other witnesses, not on that page.

**Exceptions:** The classical counts are hand counts (the Basra count was made with barley over four months, per the page). Word-boundary conventions for prepositional phrases are the stated cause of the spread (77,430-77,439).

**Verification — scholar's rule:** 77439 — Headline Basra figure 77,439 as stated on the page; variants 77,430 (Kufan) and 77,437 (Ata' b. Yasar) stated on the same page.

**Verification — root rule:** 77433 — Tanzil whitespace tokens excl. unnumbered basmalahs = 77,433 — 6 below the lowest classical figure (77,439) and 3 above the Kufan 77,430; within the spread of counting conventions. QAC words = 77,429.

**Assumptions:** scholar set A5 · our set A1 · reconciles under: none · numbers by set: A1: 77429, A3: 77433, A7: 77881 · No modern recount reproduces 77,439 exactly; closest is Tanzil tokens 77,433 (6 below) — within the spread of the classical word-boundary conventions.

**Locations:** not applicable — whole-Quran total, not a set of occurrences

### classical-letter-totals

**Claim:** Classical authorities give the Quran's letter total as 323,671 (with variants 323,015 / 330,733).

**Source:** al-Suyuti (via SeekersGuidance, Shaykh Anas al-Musa), *al-Itqan fi 'Ulum al-Qur'an — classical word and letter totals* — <https://seekersguidance.org/answers/quran/what-is-the-total-number-of-words-verses-and-letters-in-the-quran/>

**Section:** Scholar findings

**Corpus and method:** Classical counts (al-Suyuti via Yahya ibn al-Harith and others); our recount on the Tanzil file under a stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Our 325,386 (excl. unnumbered basmalahs) matches none of the classical figures exactly; the classical sources disagree among themselves by up to 7,718 (323,015 vs 330,733), and further variants exist (Mujahid 321,000; Ibn Mas'ud 300,670; Salam Abu Muhammad 340,740), so no single letter total is settled. The variation is partly definitional (e.g. whether a doubled letter counts as one or two). The 323,671 and 330,733 variants are not on the SeekersGuidance page (which gives 323,015); they are genuine al-Suyuti variants corroborated elsewhere (eaalim.com lists 323,015, 323,671 and 330,733; riwaqalquran.com cites 323,671 from al-Suyuti's al-Itqan).

**Scholar's method (stated):** Stated on the same SeekersGuidance page: the variation comes from whether 'the emphasized letter' (shaddah) is counted as two letters or one — 'those who counted the emphasized letter as two had a higher count of Quranic letters'. Basra reciters: 323,015 letters; Mujahid 321,000; Ibn Mas'ud 300,670; Salam Abu Muhammad 340,740; Abu Mu'adh 321,200. The 323,671 and 330,733 variants are al-Suyuti variants reported elsewhere (eaalim.com, riwaqalquran.com), not on that page.

**Exceptions:** The classical sources disagree among themselves by up to 7,718 letters (323,015 vs 330,733) and further variants exist, so no single letter total is settled. Doubled-letter handling is the stated definitional cause; the Uthmani spelling (omitted alifs, variant readings) is also cited on the page as a cause.

**Verification — scholar's rule:** 323015 — Headline Basra figure 323,015 as stated on the page.

**Verification — root rule:** 325386 — 325,386 letters excl. unnumbered basmalahs under the project's letter convention (327,514 incl.) — matches none of the classical figures. Counting shaddah as doubled would give 348,402, far above all of them, so the classical counters were not simply doubling shaddah.

**Assumptions:** scholar set A5 · our set A4 · reconciles under: none · numbers by set: A4: 325386, A7: 327514 · Headline 323,671 (Basra 323,015; variants to 330,733) reproduces under no modern rule — project convention gives 325,386 excl. basmalahs, 327,514 incl.

**Locations:** not applicable — whole-Quran total, not a set of occurrences

### rdsq-words-77430

**Claim:** A Tanzil-based reproducible count (RDS-Q No. 4, Mulyana 2020) gives 77,430 words for the Quran.

**Source:** Eueung Mulyana, *RDS-Q No. 4 — Quran Statistical Overview and Analysis (2020)* (2020) — <https://www.scribd.com/document/550406160/RDS-Q-004>

**Section:** Scholar findings

**Corpus and method:** Tanzil Uthmani text, unnumbered basmalahs excluded; our recount on the same text.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Ours 77,433 — differs by 3 (word-boundary conventions; the 4 verses that differ by one token each are 2:181, 8:6, 13:37 and 37:130 — see the qac-word-count finding). The odd/even verse-group totals 38,716 / 38,714 DO reproduce under the document's own stated criterion, odd/even C+V parity (chapter + verse number): on QAC data exactly 38,715 / 38,714 (the document's own Dukes-data figures, p. 20), and on Tanzil 38,717 / 38,716 — within the same 3-word gap as the headline total. The earlier draft's groupings (ayah-number, verse-index, surah-number parity) were not the document's criterion.

**Scholar's method (stated):** Stated in RDS-Q No. 4 (Mulyana 2020) itself, fetched from Scribd: 'the Quran text is based on the Uthmani version published by Tanzil project... the Quran is composed of 77430 words and 325666 letters (note: unnumbered Basmallah at the beginning of 112 chapters is not counted)'. Word unit = Tanzil whitespace token. The document also gives odd/even splits by C+V parity (chapter + verse number), per RDS-Q #1/#2.

**Exceptions:** RDS-Q attributes the QAC-vs-Tanzil word gap to 37:130 alone (QAC one word, Tanzil two); the full gap is 4 verses (2:181, 8:6, 13:37, 37:130). The 3-word gap between our Tanzil count (77,433) and RDS-Q's (77,430) on the same text is not explained by the document.

**Verification — scholar's rule:** 77430 — RDS-Q's headline total, 77,430 words (6236 verses, Tanzil Uthmani, unnumbered basmalahs excluded).

**Verification — root rule:** 77433 — Our Tanzil token count on the same text and rule = 77,433 — 3 above RDS-Q (unexplained at token level). QAC words = 77,429 (4 below ours; the 4 boundary verses).

**Assumptions:** scholar set A5 · our set A1 · reconciles under: none · numbers by set: A1: 77429, A3: 77433, A5: 77433, A7: 77881 · RDS-Q's stated rule (Tanzil tokens, basmalahs out) gives 77,433 on this file, not 77,430 — a 3-word gap the document does not explain; QAC words 77,429.

**Locations:** not applicable — whole-Quran total, not a set of occurrences

### rdsq-letters-325666

**Claim:** A Tanzil-based reproducible count (RDS-Q No. 4, Mulyana 2020) gives 325,666 letters for the Quran (unnumbered basmalahs excluded).

**Source:** Eueung Mulyana, *RDS-Q No. 4 — Quran Statistical Overview and Analysis (2020)* (2020) — <https://www.scribd.com/document/550406160/RDS-Q-004>

**Section:** Scholar findings

**Corpus and method:** Tanzil Uthmani text, unnumbered basmalahs excluded; our recount on the same text under a stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Ours 325,386 — 280 fewer under our letter convention (dagger alif/small waw/small yeh not counted as letters; alef wasla counted). The exact cause of the 280 gap is unidentified. RDS-Q notes Dukes' figure of 623,638 counts 'join letters and diacritics/harakah' — a different unit.

**Scholar's method (stated):** Stated in RDS-Q No. 4 itself (same passage as the word total): 325,666 letters on the Tanzil Uthmani text, unnumbered basmalahs excluded. The document states NO letter-counting convention — nothing says which marks count as letters — so the 280 gap below cannot be attributed to a stated rule.

**Exceptions:** RDS-Q notes Dukes' figure of 623,638 counts 'join letters and diacritics/harakah' — a different unit (all characters including diacritics), not comparable. The 280-letter gap to our count is still unexplained after testing variants (see verification).

**Verification — scholar's rule:** 325666 — RDS-Q's headline total, 325,666 letters (same text and rule as the word total).

**Verification — root rule:** 325386 — Our letter count = 325,386 — 280 fewer. Variants tested, none gives +280: counting dagger alif as a letter gives 335,224 (+9,838); dagger alif + small waw/yeh gives 337,438; doubling shaddah gives 348,402. The exact cause of the 280 gap remains unidentified.

**Assumptions:** scholar set A5 · our set A4 · reconciles under: none · numbers by set: A4: 325386, A7: 327514 · 325,666 reproduces under no letter convention tried (project convention 325,386 excl. basmalahs; 327,514 incl.) — a 280-letter gap with no stated rule to explain it.

**Locations:** not applicable — whole-Quran total, not a set of occurrences

### botani-2012-distributions

**Claim:** The Quran's verse/word/letter distributions can be fitted statistically (Botani 2012, using QuranCode software): 6,348 verses, 77,878 words, 327,792 letters.

**Source:** Delshad Shaker Ismael Botani, Salahaddin University-Hawler, *'Probability Distributions of the Verses, Words, and Letters of the Holy Quran', IJMCAR 2(3), 27-34* (2012) — <https://www.academia.edu/13913774/Probability_Distributions_of_the_Verses_Words_and_Letters_of_the_Holy_Quran>

**Section:** Scholar findings

**Corpus and method:** QuranCode software (Adams 2011), counting basmalahs as verses; distributions fitted as Exponential/Gamma. Not recounted.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Botani (2012), 'Probability Distributions of the Verses, Words, and Letters of the Holy Quran', International Journal of Mathematical and Computational Applications Research 2(3), 27-34. The higher totals come from counting basmalahs as verses and a different word/letter convention.

**Scholar's method (stated):** Stated in the paper (Botani 2012, IJMCAR 2(3), 27-34, fetched from Academia): 'All the data which is used in this paper are obtained from QuranCode software created by Adams (2011)'; '29 Arabic letters take into consideration (with accounting Hamza as a letter)'; 'the starting verse of each chapter (Basmalah) considered as a verse in whole Quran' — hence 6,348 verses, 77,878 words, 327,792 letters. Distributions fitted with Excel, Statgraphics Centurion XV and EasyFit 5.5: verses Exponential (lambda = 0.01795), words Gamma (alpha = 0.538, beta = 1269.9).

**Exceptions:** Counting the basmalah as a verse is the whole reason the verse total is 6,348 rather than 6,236 ('In most of literatures, the number of verses is equal to 6236 verses because of non-accounting 112 starting verses as a Quranic verse'). The word/letter totals are QuranCode-software counts, not hand counts; no tokenisation rule beyond the software is stated.

**Verification — scholar's rule:** 6348 — Verse arithmetic checks: 6,236 + 112 = 6,348. Words 77,878 and letters 327,792 are the paper's QuranCode figures (see root rule for the comparison).

**Verification — root rule:** 6236 — Numbered verses 6,236. On the same Tanzil text incl. basmalahs: words 77,881 (3 above Botani's 77,878) and letters 327,514 (278 below Botani's 327,792) under the project's letter convention. Both gaps are unexplained; the letter gap is in the same family as the 280 RDS-Q gap (278 vs 280 — they differ by 2, so the same unknown convention difference cannot explain both exactly).

**Assumptions:** scholar set A5 · our set A1 · reconciles under: none · numbers by set: A1: 6236 / 77429 / 325386, A7: 6348 / 77881 / 327514 · Verses 6,348 reproduce (6,236 + 112 basmalahs); words 77,878 vs our 77,881 and letters 327,792 vs our 327,514 do not — both gaps unexplained.

**Locations:** not applicable — whole-Quran totals plus fitted distributions, not a set of occurrences

### quran-word-57-khalifa

**Claim:** The word 'Quran' occurs 57 times in the Quran — 'this Quran', after excluding 10:15's 'another Quran' from a raw 58.

**Arabic:** القرآن

**Source:** Rashad Khalifa, *Appendix 1, Part 2, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1_p2.html>

**Section:** Scholar findings

**Corpus and method:** Substring and narrow-selection counts on the Tanzil file.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Full substring count of قرآن = 71; narrow selection القرآن + والقرآن + بالقرآن + قرآنا = 59 under our skeleton. Khalifa's own table (Appendix 1, Part 2, Table 21) is explicit: 'The word 'Quran' occurs in the Quran 58 times, with one of them, in 10:15, referring to 'another Quran'… must be excluded. Thus, the frequency of 'this Quran' is 57, or 19x3.' Our recount gives 59 for the narrow selection, not 57 — the claimed 57 does not reproduce even under Khalifa's own stated rule. The citation previously pointed at Part 1; the table is in Part 2.

**Scholar's method (stated):** Stated by Khalifa (Appendix 1, Part 2, Table 21 and text): 'The word "Quran" occurs in the Quran 58 times, with one of them, in 10:15, referring to "another Quran"... must be excluded. Thus, the frequency of occurrence of "this Quran" in the Quran is 57, or 19x3.' Table 21 lists the suras and verses 'where the word "Quran," in all its grammatical forms, occurs'. Two other grammatical forms ('Quranun' and 'Quranahu') 'occur in 12 verses'; 13:31 ('another Quran' that crumbles mountains) and 41:44 ('a non-Arabic Quran') are excluded.

**Exceptions:** Table 21 as printed has 66 rows, not 58. It excludes all three semantically-excluded verses (10:15, 13:31, 41:44) — the full all-forms verse set is 69 verses. 9 Table-21 verses contain only non-narrow forms (10:61, 15:1, 17:78, 17:106, 36:69, 56:77, 75:17, 75:18, 85:21 — 11 tokens); with 10:15 that is 10 verses containing a non-narrow form, not the 12 Khalifa states. No verse contains both a narrow and a non-narrow form. The substring count (71 tokens) catches one verb: قَرَأْنَاهُ ('We recited it', 75:18:2, QAC lemma qara>a), which is not the noun 'Quran'.

**Verification — scholar's rule:** 59 — Under Khalifa's own stated rule (the narrow forms القرآن / والقرآن / بالقرآن / قرآنا, minus 10:15): 59, not 57. 10:15's token is بقرآن (indefinite, outside the narrow set), so the stated exclusion changes nothing. His 57 = the 57 narrow-form verses in his table; the table silently also excludes 13:31 and 41:44 (both قرآنا, in the narrow set) on semantic grounds. His headline 58 = 57 + 10:15 — i.e. it counts 10:15 in the total while his table excludes it. Either way the claimed 57 does not reproduce under his own stated rule.

**Verification — root rule:** 70 — QAC lemma quro'aAn (the noun 'Quran') = 70 words in 69 verses. Tanzil substring قران = 71 tokens — the extra token is the verb at 75:18:2.

**Assumptions:** scholar set A5 · our set A1 · reconciles under: none · numbers by set: A1: 70, A2: 70, A3: 59, A5: 59 · Khalifa's own stated rule gives 59, not 57 (his table silently also excludes 13:31 and 41:44 on semantic grounds); the lemma total is 70.

**Locations (69 verses; verses per surah — 2: 1, 4: 1, 5: 1, 6: 1, 7: 1, 9: 1, 10: 3, 12: 2, 13: 1, 15: 3, 16: 1, 17: 10, 18: 1, 20: 3, 25: 2, 27: 4, 28: 1, 30: 1, 34: 1, 36: 2, 38: 1, 39: 2, 41: 3, 42: 1, 43: 2, 46: 1, 47: 1, 50: 2, 54: 4, 55: 1, 56: 1, 59: 1, 72: 1, 73: 2, 75: 2, 76: 1, 84: 1, 85: 1):** first 20: 2:185, 4:82, 5:101, 6:19, 7:204, 9:111, 10:15, 10:37, 10:61, 12:2, 12:3, 13:31, 15:1, 15:87, 15:91, 16:98, 17:9, 17:41, 17:45, 17:46 … (full list in data/locations.json)
**Locations — scholar's rule (57 verses):** 2:185, 4:82, 5:101, 6:19, 7:204, 9:111, 10:37, 12:2, 12:3, 15:87, 15:91, 16:98, 17:9, 17:41, 17:45, 17:46, 17:60, 17:82, 17:88, 17:89, 18:54, 20:2, 20:113, 20:114, 25:30, 25:32, 27:1, 27:6, 27:76, 27:92, 28:85, 30:58, 34:31, 36:2, 38:1, 39:27, 39:28, 41:3, 41:26, 42:7, 43:3, 43:31, 46:29, 47:24, 50:1, 50:45, 54:17, 54:22, 54:32, 54:40, 55:2, 59:21, 72:1, 73:4, 73:20, 76:23, 84:21

### wikiislam-critique

**Claim:** WikiIslam's 'Word Count Miracles in the Qur'an' documents, verse by verse, the selective counting tactics behind the paired-count claims.

**Source:** WikiIslam, *'Word Count Miracles in the Qur'an'* — <https://wikiislam.net/index.php?title=Word_Count_Miracles_in_the_Qur%27an>

**Section:** Scholar findings

**Corpus and method:** Corpus-based critique using actual verse counts (fetched 2026-11-06).

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Sub-articles cover 365 days, month 12, dunya/akhira 115, paradise/hell 77, iman/kufr 25, land/water ratio, tongue/sermon 25, shaytan/angel 88, life/death 145, zakah/blessing 32, sun/light 33. Documents selective tactics (prefix/suffix inclusion, plural/singular mixing, sense conflation, cherry-picking). Quoted scholarly refutations: Dr. Zahid Aziz ('no rule or principle for determining which word... must always occur a special number of times'); Dr. Ashraf 'Abd al-Razzaaq Qatanah ('the numerical miracle as presented in these books is not real at all'); Dr. Fahd al-Roomi (on the 365-day count excluding يومكم / يومهم / يومئذ). Dr. Fahd al-Roomi's point on the 365-day count was not separately located in the fetched WikiIslam text, so it is not asserted here.

**Scholar's method (not_a_count):** not a count — literature/critique fact. No counting method applies; the page itself was fetched and its claims checked against it. WikiIslam's own method is corpus-based critique using actual verse counts.

**Exceptions:** Dr. Fahd al-Roomi's point on the 365-day count was not separately located in the fetched WikiIslam text, so it is not asserted here (already noted in the finding).

**Verification — scholar's rule:** — — Page fetched (wikiislam.net, 'Word Count Miracles in the Qur'an', 1,195 lines): documents the selective tactics — selective choice of words, adding counts of similar words, phrase counts instead of word counts, selective choice of grammatical forms (singular/plural/dual, prefixes/suffixes), calling the selected form 'the simple form', ignoring other meanings, mistranslations, cherry-picking. Sub-articles linked from the page include the zakah/blessing 32-times item (confirmed at line 908). Quoted scholarly refutations: Dr. Zahid Aziz — confirmed quoted at lines 1132-1139 ('A conclusion of Dr. Zahid Aziz after he refuted several "miracles"'). The lead's figures agree with our recounts (day total 475, night 92).

**Verification — root rule:** — — Same verification (no corpus count applies). The finding's sub-article list (365 days, month 12, dunya/akhira 115, paradise/hell 77, iman/kufr 25, land/water ratio, tongue/sermon 25, shaytan/angel 88, life/death 145, zakah/blessing 32, sun/light 33) was not exhaustively re-checked link by link in this pass — only the zakah/blessing link and the Zahid Aziz quotation were individually located.

**Assumptions:** scholar set — · our set — · reconciles under: none · numbers by set: — · Not a word/letter count — a critique of counting tactics; no counting assumption applies.

**Locations:** not applicable — critique of counting methods — no occurrences to locate

### dukes-atwell-2012

**Claim:** The Quranic Arabic Corpus is an annotated linguistic resource for Classical Arabic (Dukes & Atwell 2012; Dukes PhD 2013).

**Source:** Kais Dukes & Eric Atwell, *'The Quranic Arabic Corpus: An annotated linguistic resource', Language Resources and Evaluation 46(3), 475-489* (2012)

**Section:** Scholar findings

**Corpus and method:** Peer-reviewed papers; the treebank itself was not re-analysed here.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Dukes & Atwell (2012), 'The Quranic Arabic Corpus: An annotated linguistic resource', Language Resources and Evaluation 46(3), 475-489, DOI 10.1007/s10579-012-9205-0; Dukes & Habash (2010), 'Morphological Annotation of Quranic Arabic', LREC 2010; Dukes, Atwell & Sharaf (2010), syntactic annotation guidelines, LREC 2010; Dukes & Atwell (2012), LAMP platform, LREC'12; Dukes PhD thesis (2013), Statistical Parsing by Machine Learning from a Classical Arabic Treebank, University of Leeds. The corpus and its annotation are the primary source for the app's morphology work.

Methods pass (2026-11-08): the DOI formerly cited here (10.1007/s10579-012-9205-0) is wrong — it resolves to 'Evaluating Word Sense Induction and Disambiguation Methods' (Klapaftis & Manandhar, 2013), a different paper. The real items are Dukes & Atwell (2012), 'LAMP', Proc. LREC'12, pp. 3268–3275, and Dukes, Atwell & Habash (2013), Language Resources and Evaluation 47(1), 33–62, DOI 10.1007/s10579-011-9167-7 (verified via Crossref).

**Scholar's method (not_a_count):** not a count — bibliographic fact. No counting method applies; the citation itself was checked by resolving the DOI and searching for the cited paper.

**Exceptions:** None beyond the citation error itself.

**Verification — scholar's rule:** — — The cited DOI 10.1007/s10579-012-9205-0 is WRONG: doi.org resolves it to 'Evaluating Word Sense Induction and Disambiguation Methods' (Manandhar et al., Language Resources and Evaluation, published 2013-03-02) — a different paper by different authors. The cited journal article ('The Quranic Arabic Corpus: An annotated linguistic resource', Language Resources and Evaluation 46(3), 475-489) could not be located in this pass. The real items are: (a) Dukes & Atwell (2012), 'LAMP: A Multimodal Web Platform for Collaborative Linguistic Analysis', Proc. LREC'12, Istanbul, pp. 3268-3275 (conference paper, no Springer DOI); (b) Dukes, Atwell & Habash (2013), 'Supervised Collaboration for Syntactic Annotation of Quranic Arabic', Language Resources and Evaluation 47(1), 33-62, DOI 10.1007/s10579-011-9167-7. The exact title 'The Quranic Arabic Corpus: An annotated linguistic resource for the Holy Quran' belongs to a different paper: Dukhovny & Atwell, Proc. LREC 2009.

**Verification — root rule:** — — Same verification (no corpus count applies). The corpus and its annotation are genuinely the primary source for the app's morphology work — only this finding's citation is wrong, not the underlying claim that the corpus exists and is Dukes' work.

**Assumptions:** scholar set — · our set — · reconciles under: none · numbers by set: — · Not a word/letter count — a bibliographic fact; no counting assumption applies.

**Locations:** not applicable — bibliographic fact — no occurrences to locate

### hapax-legomena

**Claim:** About 1,620 words occur only once in the Quran (hapax legomena).

**Source:** arabiantongue.com, *'How Many Words Are in the Quran?'* (2026) — <https://arabiantongue.com/blog/how-many-words-are-in-the-quran/>

**Section:** Scholar findings

**Corpus and method:** Lemma-based count (arabiantongue.com); our surface-form hapax is a different unit and is not comparable.

**Our status:** ❓ cannot_verify · **confidence:** reported, method unclear

**Our note:** Our surface-form hapax (raw whitespace tokens occurring once) = 12,005 — a different unit from the lemma-based ~1,620, so the two figures cannot be compared directly. The lemma-based figure has now been recounted from the QAC v0.4 annotation: 1,994 stem lemmas occur exactly once (in 1,528 verses) — which does not match ~1,620 under any POS subset tried (nouns only 1,249; nouns+adjectives+verbs 1,943).

**Scholar's method (unstated):** method not stated by the source. arabiantongue.com states 'nearly 1,620 hapax legomena (words that appear only once in the entire text)' with no counting unit — nothing says whether the unit is a lemma, a surface form, or a root, or which text/edition was counted.

**Exceptions:** The page's own figures are internally inconsistent in unit: it also gives '~14,800 unique words' and '~1,720 roots', while the QAC v0.4 annotation gives 14,881 skeletonised unique surface forms, 4,832 unique lemmas and 1,642 unique roots.

**Verification — scholar's rule:** — — No unit stated, so no scholar-rule count can be constructed. No rule tried reproduces ~1,620 (see root rule).

**Verification — root rule:** 1994 — QAC stem-lemma hapax = 1,994 lemmas occurring exactly once (in 1,528 verses). Surface-form hapax (raw whitespace tokens) = 12,005 — a different unit, confirmed. Skeletonised surface hapax = 8,709. Hapax by POS subsets: nouns only 1,249; nouns+adjectives+verbs 1,943; excl. proper nouns 1,954; roots occurring once 395. None is ~1,620.

**Assumptions:** scholar set — · our set A2 · reconciles under: none · numbers by set: A1: 395, A2: 1994, A3: 12005 · No unit gives ~1,620 — lemma hapax 1,994, surface-form hapax 12,005, roots occurring once 395.

**Locations (1528 verses; verses per surah — 1: 1, 2: 78, 3: 45, 4: 45, 5: 33, 6: 32, 7: 32, 8: 20, 9: 48, 10: 11, 11: 32, 12: 30, 13: 12, 14: 14, 15: 16, 16: 30, 17: 40, 18: 41, 19: 33, 20: 38, 21: 28, 22: 24, 23: 15, 24: 22, 25: 20, 26: 26, 27: 21, 28: 22, 29: 6, 30: 13, 31: 5, 32: 2, 33: 26, 34: 15, 35: 10, 36: 13, 37: 29, 38: 27, 39: 11, 40: 12, 41: 9, 42: 7, 43: 17, 44: 8, 45: 5, 46: 5, 47: 13, 48: 7, 49: 6, 50: 14, 51: 10, 52: 11, 53: 18, 54: 17, 55: 16, 56: 30, 57: 8, 58: 4, 59: 10, 60: 3, 61: 3, 62: 1, 63: 2, 64: 1, 65: 4, 66: 3, 67: 7, 68: 16, 69: 19, 70: 10, 71: 9, 72: 8, 73: 10, 74: 17, 75: 17, 76: 11, 77: 13, 78: 10, 79: 18, 80: 16, 81: 13, 82: 3, 83: 10, 84: 6, 85: 3, 86: 6, 87: 3, 88: 11, 89: 11, 90: 10, 91: 7, 92: 4, 93: 4, 94: 1, 95: 3, 96: 4, 97: 1, 98: 1, 99: 1, 100: 7, 101: 3, 102: 1, 103: 1, 104: 4, 105: 4, 106: 2, 107: 1, 108: 3, 111: 2, 112: 2, 113: 4, 114: 1):** first 20: 1:7, 2:16, 2:17, 2:19, 2:20, 2:25, 2:26, 2:30, 2:36, 2:54, 2:60, 2:61, 2:68, 2:69, 2:71, 2:72, 2:74, 2:85, 2:93, 2:96 … (full list in data/locations.json)

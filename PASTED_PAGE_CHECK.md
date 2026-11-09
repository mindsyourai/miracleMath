# Pasted-page claims check — Mizan

**Source:** pasted article text supplied by MK (no URL or site name given), treated as
**"pasted article text, source unidentified"**. Sections checked: Exceptional Knowledge;
The Divine Balance of Numbers; Miracle 1: The Middle Nation; Miracle 2: Iron in the
Earth's Core; Miracle 3: The Structure of the Quran; Miracle 4: Sleepers of the Cave;
Miracle 5: Surah Al-Mulk Symmetry; Miracle 6: The Moon and Surah Al-Qamar; Code 7;
Code 19; Mathematical Precision in Word Frequency and Opposites; Understanding the
Revelation; Conclusion.

**Corpus:** Quranic Arabic Corpus v0.4 morphology
(`corpus/quranic-corpus-morphology-0.4.txt`, 77,429 words) + Tanzil Uthmani text
(`corpus/quran-uthmani.txt`). Counting rules reused from
`data/root_counts_script.py`, `data/names_script.py` and `data/scholar_spotcheck.py`
— no new rules invented silently; where a claim needs a different rule to reproduce,
that rule is stated. No live file or data file was changed in this pass — this is a
check, not a publish. The Harun Yahya framing is decided (2026-11-09): his
21 confirmed counts are now the site's own script-verified counts, the 7
unconfirmed ones are circulating popular claims, and his name is no longer
used as a source on the site.

**Date:** 2026-11-07/08. Checkers: A (word counts) and B (structural/arithmetic).

## Tally — 40 verdict-bearing rows

- **Confirmed: 20** · **Differs: 17** · **Cannot verify as stated: 3**
- Out of scope (doctrinal/background, listed only, not tallied): 6 items (section K).
- One existing finding needs correction: `benefit-corrupt-50` (differs → confirmed).

## Verdict table

| # | Claim as stated | Our recount | Verdict | Existing finding |
|---|---|---|---|---|
| A1 | "Salawat" 5 | 5 plural forms (2:157, 2:238, 9:99, 22:40, 23:9) | Confirmed | `salawat-5` — covers it, no correction (Yahya) |
| A2 | "Shahr" (month) 12 | 12 under selective simple+prefixed rule; whole ROOT `$hr` = 21 | Confirmed (selective rule) | `month-12` — no correction (Yahya) |
| A3 | "Yawm" (day) 365 | 365 under selective rule; singular alone 378; ROOT `ywm` 405; +`yawma'idhin` → 475 | Confirmed (selective rule) | `day-365` — no correction (Yahya) |
| A4 | "Ayyam" (days, plural) 30 | 27 (QAC ROOT `ywm` plural stems); no clean rule gives 30 | Differs | None — proposed new finding |
| A5 | "Al-Hayat" 145 | Noun 76; ROOT `Hyy` 184; no rule gives 145 | Differs | `life-death-145` — already differs, no correction |
| A6 | "Al-Mawt" 145 | Noun 50; ROOT `mwt` 165; no rule gives 145 | Differs | `life-death-145` — already differs, no correction |
| A7 | "Al-Dunya" 115 | 115 (QAC LEM + Tanzil substring agree) | Confirmed | `dunya-akhira-115` — no correction (Yahya) |
| A8 | "Al-Akhira" 115 | 115 (1 of them 29:20 "latter creation"; strict Hereafter sense 114) | Confirmed | `dunya-akhira-115` — no correction (Yahya) |
| A9 | "Malaika" 88 | 88 (QAC LEM `malak`: 73 plural + 13 singular + 2 duals) | Confirmed | `shaytan-angels-88` — no correction (Yahya) |
| A10 | "Shayatin" 88 | 88 (QAC ROOT `$Tn`) | Confirmed | `shaytan-angels-88` — no correction (Yahya) |
| A11 | "Ar-Rajul" 24 | 24 singular forms only; with plurals root total 57 | Confirmed (singular rule) | `man-woman-24-24` — no correction (24/24 is Al-Suwaidan/Elias; Yahya gives 23/23) |
| A12 | "Al-Mar'a" 24 | 24 singular forms only (LEM 26 incl. 2 duals); with plural نساء total 85 | Confirmed (singular rule) | `man-woman-24-24` — no correction |
| G-count | Surah Al-Qamar (54) mentions the moon 27 times | Surah 54: **1** (54:1 only). Whole Quran: 27 | Differs | `sun-moon-33-27` (whole-Quran 27) correct — no correction; error is the article's surah attribution |
| H1 | Verses mentioning "seven heavens" appear 7 times | 7 verses: 2:29, 17:44, 23:86, 41:12, 65:12, 67:3, 71:15 | Confirmed | `seven-heavens-7` — no correction (Yahya) |
| H2 | "Hell" has seven gates; the word appears 77 times | 77 (QAC LEM `jahan~am`, Tanzil substring جهنم). "Seven gates" is a reference to 15:44, reported only | Confirmed (count) | `jannah-jahannam-77` — no correction |
| H3 | Surah Al-Fatiha has 7 verses | 7 verses (standard Hafs count) | Confirmed | None — trivial, leave out |
| H4 | Fatiha's total letter count "is built on prime numbers, many relating back to 7" | No specific numbers/primes/relation stated. Context: 139 letters, 29 words under the spotcheck convention (139 and 29 prime; 12 and 18 in the per-verse counts are not) | Cannot verify as stated | None — leave out (no falsifiable content) |
| J1 | Reward 117 | QAC ROOT `j-z-y` = **118** (noun 42 + verb 73 + jizya 1 + 2 minor) | Differs (by one) | `reward-forgiveness-117-234` — already differs, no correction (Yahya) |
| J2 | Forgiveness 234 | QAC ROOT `gh-f-r` = **234** exactly | Confirmed | `reward-forgiveness-117-234` — no correction (Yahya) |
| J3 | "Forgiveness is mentioned exactly twice as much as punishment" (giving reward/forgiveness numbers) | **Internal mismatch.** 234 = 2 × 117 (twice the *reward* figure just given). Punishment is ROOT `E*b` 373 (noun عذاب alone 322); 234 is twice neither | Differs (false as stated) | Covered by `reward-forgiveness-117-234` (differs) — no new finding needed |
| J4 | Good deeds ("birr") 20 | LEM `bir~` 8; surface البر 19; ROOT `b-r-r` 32. No clean rule gives 20 | Differs | None — proposed new finding |
| J5 | Reward ("jazaa") 20 | Noun جزاء 42; whole ROOT `j-z-y` 118; bare surface tokens 29. No clean rule gives 20 | Differs | None — proposed new finding (or fold into reward-forgiveness note; see actions) |
| J6 | Benefit 50 | QAC ROOT `n-f-ʿ` = **50** exactly | Confirmed | `benefit-corrupt-50` — **NEEDS CORRECTION** (currently "differs") |
| J7 | Corruption 50 | QAC ROOT `f-s-d` = **50** exactly | Confirmed | `benefit-corrupt-50` — **NEEDS CORRECTION** (currently "differs") |
| B | 2:143 "middle nation" is exactly in the middle of Al-Baqara (286 verses) | 286 verses confirmed. But 143 has 142 verses before it and 143 after it — first verse of the second half, not the exact centre; with an even count there is no single middle verse (centre falls between 143 and 144) | Differs (as literally stated) | None — proposed new finding |
| C | Al-Hadid is the 57th surah, exactly in the middle of the 114; iron at the centre of the Earth's core, ~5,100 km deep; 5,100 verses up to the mention of iron (57:25) | Surah 57: 56 before, 57 after — not exactly the middle (middle pair 57/58). Verse count to 57:25: **5,075 + 25 = 5,100 exactly, confirmed** (57:25 contains الحديد). Depth: inner-core boundary ≈ 5,150 km; Earth's centre 6,371 km — "about 5,100 km" is ~50 km off the boundary but 1,271 km off the centre | Differs (verse count confirmed; middle-surah and centre-depth parts fail as stated) | None — proposed new finding |
| D | 1+2+…+114 = 6,555; total verses 6,236; odd/even "perfectly splits 50/50" | 6,555 confirmed (114×115/2); 6,236 confirmed. (i) odd vs even surah numbers: **57 vs 57 — exactly 50/50**. (ii) surahs with odd vs even verse counts: **54 vs 60 — NOT 50/50**. (iii) same-parity vs different-parity (surah no., verse count): **57 vs 57 — exactly 50/50** (27 odd/odd, 30 odd/even, 27 even/odd, 30 even/even). By verse-sum also not 50/50 (odd-numbered surahs 3,031 verses vs even-numbered 3,205) | Confirmed for readings (i) and (iii); reading (ii) differs | None — proposed new finding |
| E | 300 solar years = 109,500 days; 309 lunar years ≈ 109,499.43 days | 300 × 365 = 109,500 confirmed (assumes a 365-day year, ignoring leap days; at 365.25 d it would be 109,575). 309 × 354.367056 d (12 × 29.530588) = **109,499.42** — page's figure matches to rounding (implies lunar year 354.36709 d, the standard mean). Gap: **0.58 days (~14 hours)** over 300 years | Confirmed (near-equality, not exact; leap-day caveat) | None — proposed new finding |
| F | Surah Al-Mulk (67) has 30 verses, split into two halves of 140 words each | 30 verses confirmed. Words (whitespace tokens, Uthmani, basmalah excluded): **vv. 1–15 = 161, vv. 16–30 = 172; total 333** (incl. basmalah 165 vs 172, total 337). QAC cross-check: 333 words, identical. Claimed 280; actual total is 53 words higher, neither half is 140 | Differs | None — proposed new finding |
| G-comp | Moon mentioned 27 times in Al-Qamar "mirrors the lunar cycle of about 29.5 days" | 27 vs 29.5 is 2.5 days off (~8.5%) — does not match the synodic month (~29.53 d). 27 matches the **sidereal month (~27.3 d)** far better (0.3 d off) | Differs (as a match to a 29.5-day cycle) | Fold into proposed moon-in-surah-54 finding |
| I-1 | Bismillah has 19 letters | **19 letters confirmed** under the spotcheck letter convention (no dagger alif/small waw/yeh in the basmalah, so that choice does not affect this count) | Confirmed | `basmalah-19-letters-114` — no correction |
| I-2n | The Quran mentions 19 different whole numbers | **31 distinct values** named (1–12, 19, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100, 200, 300, 1000, 2000, 3000, 5000, 50000, 100000 — each verified with verse refs; e.g. 11 in 12:4, 19 in 74:30, 100000 in 37:147). **33** counting compositional values (950 = "a thousand years less fifty", 29:14; 309 = "three hundred years and add nine", 18:25). No 13–18 found. 19 is reachable only by an unstated narrow selection (e.g. 1–10 + tens 20–80 + 100 + 1000) | Differs | None — proposed new finding |
| I-2f | …and 19 fractions | **8 distinct values** — 1/2, 1/3, 2/3, 1/4, 1/5, 1/6, 1/8, 1/10 (e.g. 1/10 in 34:45, معشار). No route to 19 | Differs | Fold into proposed I-2n finding |
| I-3 | Surah Al-Muddaththir (74) has word counts in multiples of 19 | Surah total: **255 words** excl. basmalah (259 incl.) — 255 = 19×13 + 8, **not divisible by 19** (QAC cross-check: 255, identical). True multiples exist inside: **v. 31 alone = 57 words (19×3); vv. 1–30 = 95 (19×5); vv. 1–31 = 152 (19×8)** | Differs (surah total as stated; sub-counts noted) | None — proposed new finding |
| I-4a | Surah Al-Alaq (96, first revelation) has 19 verses | 19 verses confirmed | Confirmed | `surah-96-19-verses-304-letters` — no correction |
| I-4b | 76 letters in the first command (96:1 "iqra bismi rabbik alladhi khalaq"); 76 = 19×4 | 96:1 letters = **18** (اقرأ 4 + باسم 4 + ربك 3 + الذي 4 + خلق 3), not 76. The 76-letter figure belongs to **96:1–5 as a whole (confirmed: 76 letters, 20 words)**, not to 96:1 alone. 76 = 19×4 is true arithmetic, attached to the wrong span | Differs (as stated; 76 confirmed only for 96:1–5) | `first-revelation-letters-76` (96:1–5) already correct — no correction |
| I-5a | The last revealed surah (An-Nasr, 110) contains 19 words | **19 words confirmed** excl. basmalah (5 + 7 + 7; QAC cross-check: 19; 110:1 = 19 letters also confirmed) | Confirmed | `surah-110-19-words` — no correction |
| I-5b | …(An-Nasr is) the last revealed surah | Revelation order is not in the corpus — a traditional view, not a corpus fact | Cannot verify | None — leave out |
| I-6a | "19 + Surah 74 = 1974" | **19 + 74 = 93, not 1,974** — false as addition. "19"+"74" = "1974" is concatenation wordplay, not arithmetic | Differs (arithmetic) | None — proposed new finding |
| I-6b | The code was discovered in 1974 | Historical claim, not corpus-checkable | Cannot verify | Fold into proposed I-6a finding |

## K. Out of scope (doctrinal/background — listed only, not verified or disputed)

Revealed over 23 years; 3:96 "guidance for the worlds"; 4:174 "manifest light"; the
Prophet could neither read nor write; revelation in three ways (Gabriel, dreams,
directly into memory); "seven layers of the Earth / seven colours in the light
spectrum / seven heavens / seven rounds of Tawaf".

## Most important corrections

1. **The moon claim is wrong in the way it is stated.** Surah Al-Qamar mentions the
   moon once (54:1). The 27 is the whole-Quran count, and 27 does not mirror a
   29.5-day cycle anyway (2.5 days off); it matches the sidereal month (~27.3 d).
2. **Surah Al-Mulk is not 140 + 140 words.** The halves are 161 and 172 words
   (total 333, confirmed by QAC). The claimed total, 280, is 53 words short.
3. **"19 + 74 = 1974" is false arithmetic.** The sum is 93; 1974 is concatenation,
   not addition.
4. **76 letters belong to 96:1–5, not to the first command (96:1).** Verse 96:1
   alone has 18 letters.
5. **The 19-numbers / 19-fractions claim does not survive a count.** 31 distinct
   whole numbers (33 counting compositional values) and 8 fractions are actually
   named — no route to 19/19.
6. **"Forgiveness is twice as much as punishment" mislabels its own numbers.**
   234 is twice the *reward* figure (117) just given, not punishment (373 by
   root `E*b`; noun عذاب alone 322).
7. **"Exactly in the middle" fails twice** (2:143 of 286; surah 57 of 114): with
   even totals there is no single middle verse or surah — 2:143 is the first verse
   of the second half, and surah 57 has 56 before it and 57 after it.
8. **The iron 5,100s do not line up the way the page implies.** The verse count to
   57:25 really is 5,100 — but 5,100 km is (approximately) the inner-core boundary
   (~5,150 km), not the centre of the core (6,371 km).
9. **One existing finding was wrong and flips to confirmed:** `benefit-corrupt-50`.
   By the project's own QAC root rule both sides are exactly 50 (ROOT `nfE` 50,
   ROOT `fsd` 50); the old "differs" rested on substrings (45 / 11), the wrong rule.
10. **"Confirmed" for yawm-365, shahr-12, man/woman-24 and salawat-5 means confirmed
    under a stated selective rule** (simple/prefixed or singular-only forms); the
    whole-root totals differ (405, 21, 57/85, 83). The numbers are not wrong, but
    they are rule-dependent, and the page does not state the rule.

## Proposed actions (for MK to decide — NOT applied)

### Updates to existing findings (1)

- `benefit-corrupt-50`: status differs → **confirmed**; confidence "confirmed by our
  recount". Rewrite `our_note` to cite ROOT `nfE` = 50 (نفع verb 31 + noun 11 +
  منافع 8) and ROOT `fsd` = 50 (مفسد 21 + أفسد 15 + فساد 11 + فسدت 3), noting
  substring counts (45 / 11) are not the right rule for these words. Tallies would
  become 29 confirmed / 24 differ / 11 cannot verify (from 28 / 25 / 11).

### Proposed new findings (JSON-ready records in the appendix below)

1. `ayyam-30` — differs (A4).
2. `moon-in-surah-54` — differs (G-count + G-comp combined).
3. `middle-nation-2-143` — differs (B).
4. `iron-5100` — differs, with the 5,100 verse count confirmed inside the note (C).
5. `surah-parity-6555-6236` — confirmed (D).
6. `sleepers-300-309` — confirmed, with the leap-day caveat (E).
7. `mulk-140-140` — differs (F).
8. `code19-numbers-fractions` — differs (I-2n + I-2f).
9. `muddathir-multiples-19` — differs, noting the true sub-multiples (I-3).
10. `alaq-76-letters-command` — differs as stated (I-4b; existing
    `first-revelation-letters-76` already covers 96:1–5 correctly, so this record
    exists to correct the article's attribution).
11. `code19-discovery-1974` — differs (arithmetic, I-6a) with the discovery year
    marked not corpus-checkable (I-6b).

### Leave out, and why

- **Fatiha letter-primes claim (H4):** no falsifiable content as stated — cannot be
  turned into a checkable finding.
- **Fatiha 7 verses (H3):** undisputed structural fact, not a miracle claim worth a
  finding.
- **An-Nasr "last revealed" (I-5b):** word count already covered by
  `surah-110-19-words`; last-revealed status is not corpus-checkable.
- **J3 "twice as much as punishment" sentence:** covered by
  `reward-forgiveness-117-234` (already "differs"); no separate finding needed.
- **J5 reward ("jazaa") 20:** fold into the `reward-forgiveness-117-234` note rather
  than a standalone finding (same root, same correction).
- **K doctrinal/background items:** out of scope for a corpus-count app.
- **Yahya framing:** untouched in this pass (decision still open with MK). Note: of
  the claims checked here, Yahya's list covers A1, A2, A3, A7, A8, A9, A10, J1, J2,
  J6, J7 and H1; it does NOT cover life/death-145, man/woman-24/24 (Al-Suwaidan/
  Elias; Yahya gives 23/23), moon-27, ayyam-30, or the Code 19 items (Khalifa's).

## Appendix — JSON-ready proposed finding records (not yet applied)

Source for all records below: `{"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}`.

```json
[
  {
    "id": "ayyam-30",
    "category": "paired_counts",
    "claim": "The word 'ayyam' (days, plural) occurs 30 times in the Quran, matching the typical number of days in a month.",
    "claim_arabic_or_terms": "أيام",
    "confidence": "contested",
    "corpus_and_method": "QAC v0.4 ROOT ywm plural stems; Tanzil Uthmani cross-check.",
    "our_note": "QAC ROOT ywm plural stems give 27 occurrences; exact أيام surface forms 25, substring أيام 28 (the extra 2 are possessive أيامكم and a spelling variant). No clean rule gives 30.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "moon-in-surah-54",
    "category": "paired_counts",
    "claim": "Surah Al-Qamar (54) mentions the moon 27 times, mirroring the lunar cycle of about 29.5 days.",
    "claim_arabic_or_terms": "القمر",
    "confidence": "contested",
    "corpus_and_method": "QAC v0.4 ROOT qmr / LEM qamar within surah 54 and whole-Quran; Tanzil substring قمر.",
    "our_note": "Surah 54 mentions the moon once (54:1, 'the moon has split'). The 27 is the whole-Quran count (ROOT qmr 27, LEM qamar 27, substring 27). And 27 vs a 29.5-day cycle is 2.5 days off (~8.5%); 27 matches the sidereal month (~27.3 d) far better.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "middle-nation-2-143",
    "category": "structure",
    "claim": "Verse 2:143 ('middle nation') sits exactly in the middle of Surah Al-Baqara, which has 286 verses.",
    "claim_arabic_or_terms": "أمة وسطا",
    "confidence": "contested",
    "corpus_and_method": "Standard Hafs verse table; QAC max verse 2:286; verse text verified.",
    "our_note": "286 verses confirmed, and 2:143 does contain 'أمة وسطا'. But 143 has 142 verses before it and 143 after it: it is the first verse of the second half, not the exact centre. With an even count there is no single middle verse; the centre falls between 143 and 144.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "iron-5100",
    "category": "structure",
    "claim": "Surah Al-Hadid (Iron) is the 57th surah, exactly in the middle of the 114 surahs; iron is at the centre of the Earth's core, about 5,100 km deep; there are 5,100 verses in the Quran up to the mention of iron (57:25).",
    "claim_arabic_or_terms": "الحديد",
    "confidence": "contested",
    "corpus_and_method": "Standard Hafs verse table; verse count to 57:25 computed from surah verse counts.",
    "our_note": "The verse count is exact: 5,075 verses in surahs 1-56 plus 25 = 5,100, and 57:25 contains الحديد. But surah 57 has 56 surahs before it and 57 after it, so it is not exactly the middle of 114 (the middle pair is 57/58). And 5,100 km is approximately the inner-core boundary (~5,150 km), not the centre of the core (6,371 km).",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "surah-parity-6555-6236",
    "category": "structure",
    "claim": "The sum of surah numbers 1+2+...+114 is 6555 and the total verses are 6236; dividing into odd and even numbers splits them 50/50.",
    "claim_arabic_or_terms": null,
    "confidence": "confirmed by our recount",
    "corpus_and_method": "Direct computation; standard Hafs verse table (sums to 6236).",
    "our_note": "6555 confirmed (114x115/2); 6236 confirmed. Odd vs even surah numbers: 57 vs 57, exactly 50/50. Same-parity vs different-parity (surah number, verse count) pairs: 57 vs 57, exactly 50/50. Caveat: surahs with odd vs even verse counts are 54 vs 60, not 50/50; and by verse-sum, odd-numbered surahs total 3,031 verses vs 3,205 for even-numbered.",
    "our_status": "confirmed",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "sleepers-300-309",
    "category": "structure",
    "claim": "300 solar years equal 109,500 days and 309 lunar years equal roughly 109,499.43 days (Quran 18:25: 'three hundred years, adding nine').",
    "claim_arabic_or_terms": null,
    "confidence": "confirmed by our recount",
    "corpus_and_method": "Arithmetic on standard year lengths (solar 365 d; lunar year 12 x 29.530588 d = 354.367056 d).",
    "our_note": "300 x 365 = 109,500 confirmed; 309 x 354.367056 = 109,499.42, matching the page's 109,499.43 to rounding. The gap is 0.58 days (~14 hours) over 300 years. Caveat: the solar side assumes a 365-day year with no leap days; at 365.25 d it would be 109,575.",
    "our_status": "confirmed",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "mulk-140-140",
    "category": "structure",
    "claim": "Surah Al-Mulk (67) has 30 verses, split into two halves of 140 words each.",
    "claim_arabic_or_terms": null,
    "confidence": "contested",
    "corpus_and_method": "Whitespace-token word count on Tanzil Uthmani text, basmalah excluded; QAC cross-check.",
    "our_note": "30 verses confirmed. But verses 1-15 have 161 words and verses 16-30 have 172 (total 333; QAC cross-check: 333 words, identical). The claimed 140 + 140 = 280 is 53 words short, and neither half is 140.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "code19-numbers-fractions",
    "category": "code19",
    "claim": "The Quran mentions 19 different whole numbers and 19 fractions.",
    "claim_arabic_or_terms": null,
    "confidence": "contested",
    "corpus_and_method": "Enumeration of number-words named in the Quran (QAC v0.4 + Tanzil text, each value verified with verse references).",
    "our_note": "Whole numbers actually named: 31 distinct values (1-12, 19, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100, 200, 300, 1000, 2000, 3000, 5000, 50000, 100000); 33 counting compositional values (950 in 29:14, 309 in 18:25). No 13-18 found. 19 is reachable only by an unstated narrow selection. Fractions actually named: 8 distinct values (1/2, 1/3, 2/3, 1/4, 1/5, 1/6, 1/8, 1/10). No route to 19/19.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "muddathir-multiples-19",
    "category": "code19",
    "claim": "Surah Al-Muddaththir (74) has word counts in multiples of 19.",
    "claim_arabic_or_terms": null,
    "confidence": "contested",
    "corpus_and_method": "Whitespace-token word count on Tanzil Uthmani text, basmalah excluded; QAC cross-check.",
    "our_note": "Surah total is 255 words (259 including the basmalah); 255 = 19x13 + 8, not divisible by 19 (QAC cross-check: 255, identical). True multiples exist inside the surah: verse 31 alone is 57 words (19x3), verses 1-30 are 95 (19x5), verses 1-31 are 152 (19x8) — but the surah total is not one.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "alaq-76-letters-command",
    "category": "code19",
    "claim": "Surah Al-Alaq (96) has 19 verses and 76 letters in the first command (96:1); 76 = 19x4.",
    "claim_arabic_or_terms": null,
    "confidence": "contested",
    "corpus_and_method": "Letter count under the scholar_spotcheck.py convention (base letters count; diacritics and shadda add none; dagger alif / small waw / small yeh do not count).",
    "our_note": "19 verses confirmed. But 96:1 has 18 letters (اقرأ 4 + باسم 4 + ربك 3 + الذي 4 + خلق 3), not 76. The 76-letter figure belongs to 96:1-5 as a whole (confirmed: 76 letters, 20 words). 76 = 19x4 is true arithmetic, attached to the wrong span. The existing finding first-revelation-letters-76 already covers 96:1-5 correctly.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  },
  {
    "id": "code19-discovery-1974",
    "category": "code19",
    "claim": "The Code 19 was discovered in 1974, and 19 + Surah 74 = 1974.",
    "claim_arabic_or_terms": null,
    "confidence": "contested",
    "corpus_and_method": "Arithmetic; the discovery year is a historical claim, not corpus-checkable.",
    "our_note": "19 + 74 = 93, not 1,974. '19' + '74' = '1974' is concatenation wordplay, not arithmetic. The discovery year 1974 itself is a historical claim and cannot be verified from the corpus.",
    "our_status": "differs",
    "source": {"author": "Pasted article text, source unidentified", "title": "Popular article on Quranic numerical miracles (text supplied by MK; no URL)", "url": null, "year": null}
  }
]
```

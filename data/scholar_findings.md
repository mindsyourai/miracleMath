# Scholar findings on the Quran corpus — miracleMath

Date: 2026-11-06. Corpus: Tanzil Quran Text, Uthmani script (corpus/quran-uthmani.txt), 6,236 verses, downloaded 2026-11-06 from tanzil.net.

> **Read this first:** disputed numerology is presented here as *reported findings* — each with a source and a status — never as settled fact. “Confirmed” means our own scripted recount on the Tanzil file reproduces the claimed figure under a stated method; “differs” means it does not; “cannot verify” means no recount was possible or the claim needs sense disambiguation. The Nursi strand (Isaratul-I'jaz) is parked by MK's decision and is **not** covered here.

## Tally

- **Total findings: 64** — ✅ confirmed 29 · ❌ differs 28 · ❓ cannot verify 7

- Paired-count claims: 30 (confirmed 10, differs 19, cannot verify 1)
- Letter counts and the disconnected letters (muqatta'at): 7 (confirmed 4, differs 3, cannot verify 0)
- Code 19 — Rashad Khalifa's 'mathematical miracle': 11 (confirmed 9, differs 2, cannot verify 0)
- Modern corpus linguistics: 16 (confirmed 6, differs 4, cannot verify 6)

## Recount method

Whitespace tokens. Skeleton normalisation for matching: diacritics/tatweel removed; hamza variants normalised (أ إ آ ٱ → ا, ؤ → و, ئ → ي, ء dropped); dagger alif ٰ → ا, small waw ۥ → و, small yeh ۦ → ي are kept as letters for matching. Letter-counting convention: base letters count, including alef wasla ٱ as ا; dagger alif, small waw and small yeh are marks and do NOT count; standalone hamza ء counts. This convention reproduces the anchors: basmalah = 19 letters, 96:1-5 = 76 letters, 110:1 = 19 letters. 'Excl. unnumbered basmalahs' means excluding the 112 basmalahs merged into verse 1 of surahs 2-8 and 10-114 (the 2 numbered basmalahs, 1:1 and 27:30, are kept). Surah boundaries use the standard Hafs verse-count table (sums to 6,236).

Spot-recount script: [`scholar_spotcheck.py`](scholar_spotcheck.py) (corpus totals, Code 19 anchors, paired counts, letter counts, muqatta'at). The remaining Harun Yahya pairs were checked with a one-off substring batch (not kept as a deliverable; its numbers are quoted in the notes below).

## Paired-count claims

### dunya-akhira-115

**Claim:** The words 'world' (dunya) and 'hereafter' (akhira) each occur 115 times in the Quran.

**Arabic:** الدنيا / الآخرة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Our substring recount on the Tanzil Uthmani text: دنيا 115, اخرة 115 — exact match.

### jannah-jahannam-77

**Claim:** The words 'paradise' (jannah) and 'hell' (jahannam) each occur 77 times.

**Arabic:** الجنة / جهنم

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Strict forms الجنة/جنة with prefixes: 77; جهنم substring 77. (جنة substring alone is 78 — one extra is a construct form.)

### shaytan-angels-88

**Claim:** The words 'devil' (shaytan) and 'angel' each occur 88 times.

**Arabic:** الشيطان / الملائكة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Devil: شيط 70 + شياطين 18 = 88 confirmed (the plural needs the شياط pattern because the dagger alif breaks the شيط substring). Angels: ملائكة 73 confirmed; singular malak-as-angel is about 11-12 by verse inspection (6:8, 6:9, 6:50, 11:12, 11:31, 12:31, 25:7, 32:11, 53:26, 69:17, 89:22, plus dual الملكين 2:102), giving a total of about 85 — three short of 88. The form ملك/الملك totals 63 and mostly means king/sovereignty, so sense disambiguation is required.

### day-365

**Claim:** The word 'day' (yawm) occurs 365 times, matching the days of a (Gregorian) year.

**Arabic:** يوم

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source; our recount reproduces 365 only under a stated selective method (see note).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Simple forms يوم/اليوم/يوما = 274; plus prefixed ويوم 44, واليوم 23, ليوم 8, فاليوم 8, بيوم 5, باليوم 2, وباليوم 1 = 365 exactly. Caveat: suffixed forms (يومكم, يومهم, يومئذ 65+), dual يومين and plural أيام are excluded by this method; all tokens containing يوم = 590, polluted by belief verbs (يؤمنون). The Islamic calendar has 354/355 days, so the Gregorian-365 framing is itself a critique point (WikiIslam).

### month-12

**Claim:** The word 'month' (shahr) occurs 12 times, matching the months of a year.

**Arabic:** شهر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source; our recount reproduces 12 only under a stated selective method (see note).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Simple شهر/الشهر/شهرا = 10; plus بالشهر 1, والشهر 1 = 12 exactly. Dual شهرين (2) and plural أشهر (5) + الأشهر (1) are excluded by this method.

### salawat-5

**Claim:** The word for the (five daily) prayers (salawat) occurs 5 times.

**Arabic:** صلوات

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 7 tokens match صلوات, at 2:157, 2:238, 9:99, 9:103, 11:87, 22:40, 23:9. The 5 plural صلوات are 2:157, 2:238, 9:99, 22:40, 23:9; 9:103 and 11:87 are singular صلاة written صلوة in Uthmani. Only 3 of the 5 mean 'prayers' (2:157 = blessings, 22:40 = synagogues) — WikiIslam's sense critique.

### sea-land-32-13

**Claim:** The word 'sea' occurs 32 times and 'land' 13 times (the ratio 13/45 = 29% land, 71% sea, matching the Earth's surface).

**Arabic:** البحر / البر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❓ cannot verify · **confidence:** reported, method unclear

**Our note:** Sea: البحر 23 + والبحر 9 = 32 confirmed (all بحر tokens 40, incl. dual البحرين 4). Land: the البر-form total is 21 (البر 19 + prefixed forms), mixing 'land' and 'righteousness/piety' senses (e.g. 2:177); the figure 13 requires sense disambiguation we did not perform, so the pair as stated cannot be verified. The 29:71 land/sea ratio claim therefore cannot be verified as stated.

### man-woman-24-24

**Claim:** The words 'man' and 'woman' (singular) each occur 24 times.

**Arabic:** رجل / امرأة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Man singular (رجل family): رجل 13 + رجلا 7 + لرجل 2 + فرجل 1 + ورجلا 1 = 24. Woman singular (امرأة family): امرات 6 + امراتهي 5 + امراة 3 + وامراتهي 2 + امراتك 2 + امراتى 2 + وامراتى 1 + لامراتهو 1 + وامراة 1 + وامرات 1 = 24. Harun Yahya's own list gives 23/23 — one short on each side. With duals/plurals: man 30 (excl. feet), woman 26. Naive substrings both give 45/45 only by coincidence (رجل mixes in 13-15 foot/feet forms; امرا mixes in امرأ 'man' 19 and السامري 1).

### life-death-145

**Claim:** The words 'life' (hayat) and 'death' (mawt) each occur 145 times.

**Arabic:** الحياة / الموت

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source. (Note: Harun Yahya's published list does not include this pair; it circulates on other sites, e.g. quranic-miracles.com.)

**Our status:** ❌ differs · **confidence:** contested

**Our note:** حياة family (حيو/حيي/حيا) = 125; الحياة noun = 67. موت family = 171 (موت/ميت/مات, after removing the 22 الظلمات/ظلمات and 14 كلمات-forms false positives caught by the مات substring); الموت noun = 35; موت substring = 91. No straightforward form/root count reproduces 145/145.

### sun-moon-33-27

**Claim:** The words 'sun' (shams) and 'moon' (qamar) occur 33 and 27 times.

**Arabic:** الشمس / القمر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** شمس substring 33, قمر substring 27 — both exact.

### muhammad-4

**Claim:** The name 'Muhammad' occurs 4 times in the Quran.

**Arabic:** محمد

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** محمد substring = 4.

### iman-kufr-25

**Claim:** The words 'belief' (iman) and 'disbelief' (kufr) each occur 25 times.

**Arabic:** إيمان / كفر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Naive substring counts: ايمان 86, كفر 343 — far from 25/25. The 25 figure must rest on a very narrow form selection that the source does not state.

### zakah-blessing-32

**Claim:** The words 'charity' (zakah) and 'blessing' (barakah) each occur 32 times.

**Arabic:** الزكاة / البركة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** زك substring 67 (incl. الزكاة, زكاة, يزكي and derived verb forms); برك substring 5. Neither side is near 32 under a simple substring count.

### say-they-said-332

**Claim:** The word 'say' (qul) occurs 332 times and 'they said' (qalu) 332 times.

**Arabic:** قل / قالوا

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** 'They said' (قالوا substring) = 332 exactly. 'Say' (قل, imperative, exact-form count after stripping prefixes) = 333 — one more than the claimed 332. The قال family as a whole (substring) is 932.

### plant-tree-26

**Claim:** The words 'plant' and 'tree' each occur 26 times.

**Arabic:** نبات / شجر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** نبات substring 11; شجر substring 27. Plant is far from 26; tree is one over.

### reward-forgiveness-117-234

**Claim:** The words 'reward' (thawab) and 'forgiveness' (maghfira) occur 117 and 234 times (forgiveness exactly double reward).

**Arabic:** ثواب / مغفرة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** ثواب substring 13; مغفر substring 28. Both far from 117/234.

### guidance-mercy-79

**Claim:** The words 'guidance' (huda) and 'mercy' (rahma) each occur 79 times.

**Arabic:** هدى / رحمة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** هد substring 432; رحم substring 318 — polluted by الرحمن 169 and الرحيم 227, which share the root. The 79 figure must use a narrow selection the source does not state.

### tongue-sermon-25

**Claim:** The words 'tongue' (lisan) and 'sermon' (maw'iza) each occur 25 times.

**Arabic:** لسان / موعظة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** لسان substring 15; موعظ substring 9. Both below 25.

### wine-intoxication-6

**Claim:** The words 'wine' (khamr) and 'intoxication' (sakara) each occur 6 times.

**Arabic:** خمر / سكر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** خمر substring 7 (claimed 6); سكر substring 4 (claimed 6), rising to 7 with the سكارى (4:43, 22:2) and سكرة (50:19) forms — the root count WikiIslam cites. The two sides do not match as claimed.

### mind-light-49

**Claim:** The words 'mind' ('aql) and 'light' (nur) each occur 49 times.

**Arabic:** عقل / نور

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** عقل substring 49 exactly; نور substring 46 — three short of 49. The pair matches on one side only.

### benefit-corrupt-50

**Claim:** The words 'benefit' (naf') and 'corrupt' (fasad) each occur 50 times.

**Arabic:** نفع / فساد

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** نفع substring 45; فساد substring 11. Corrupt is far from 50.

### love-obedience-83

**Claim:** The words 'love' (hubb) and 'obedience' (ta'a) each occur 83 times.

**Arabic:** حب / طاعة

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** حب substring 153; طاع substring 16. Neither is near 83.

### refuge-forever-28

**Claim:** The words 'refuge' (malja') and 'forever' (abadan) each occur 28 times.

**Arabic:** ملجأ / أبدا

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** ملجا substring 3; ابدا substring 29 (one over 28). Refuge is far from 28.

### disaster-thanks-75

**Claim:** The words 'disaster' (musiba) and 'thanks' (shukr) each occur 75 times.

**Arabic:** مصيبة / شكر

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** مصيب substring 11; شكر substring 47. Both below 75.

### trouble-peace-13

**Claim:** The words 'trouble' (durr) and 'peace' (salam) each occur 13 times.

**Arabic:** ضر / سلام

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** ضر substring 162 (incl. الضرر, يضر and derived forms); سلم substring 84 (incl. السلام, مسلم and derived forms). The 13 figure must use a narrow selection the source does not state.

### treachery-foul-16

**Claim:** The words 'treachery' (khiyana) and 'foul' (khabith) each occur 16 times.

**Arabic:** خيانة / خبيث

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** خيان substring 2; خبيث substring 13. Both below 16.

### righteous-wicked-6-3

**Claim:** The words 'righteous' (salih) and 'wicked' (talih) occur 6 and 3 times.

**Arabic:** صالح / طالح

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** صلح substring 37; طلح substring 1 (56:29). WikiIslam's literal-form recount gives 5 vs 2, not 6 vs 3.

### summer-winter-5

**Claim:** The words 'summer-hot' and 'winter-cold' each occur 5 times.

**Arabic:** صيف / شتاء

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** صيف (summer) substring 1; شتاء (winter) substring 3. The words 'summer' and 'winter' barely occur as such; WikiIslam notes heat 4 and cold 3 (our برد substring is 4). The 5/5 pair does not reproduce.

### human-being-65

**Claim:** The word 'human being' (insan) occurs 65 times.

**Arabic:** إنسان

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Method not stated by the source.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** انسان substring = 65 exactly. The creation-stage reading (the stages of human creation summing to 65) does not reproduce: تراب 20 + نطفة 12 + علقة 7 + مضغة 3 + عظام 13 + لحم 58 = 113 by substring.

### harun-yahya-populariser

**Claim:** Harun Yahya (Adnan Oktar) popularised the paired-count list in his book Miracles of the Qur'an.

**Source:** Harun Yahya (Adnan Oktar), *Miracles of the Qur'an (Goodword Books, 2005) — 'Word Repetitions in the Qur'an'* (2005) — <https://www.harunyahya.info/en/articles/word-repetitions-in-the-quran>

**Corpus and method:** Literature fact; the full list is published at harunyahya.info (fetched 2026-11-06). Method not stated in the source.

**Our status:** ✅ confirmed · **confidence:** reported, method unclear

**Our note:** The list as published at harunyahya.info does not include life/death 145; that claim circulates on other sites (e.g. quranic-miracles.com).

## Letter counts and the disconnected letters (muqatta'at)

### qaf-57-57

**Claim:** The letter Qaf occurs 57 times in surah 50 (Qaf) and 57 times in surah 42 (Shura) — 57 + 57 = 114.

**Arabic:** ق

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Letter counting under our stated convention (see meta). Khalifa's headline finding.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** ق in surah 50 = 57 and in surah 42 = 57, confirmed by our recount.

### nun-132-vs-133

**Claim:** The letter Nun occurs 133 times in surah 68 (Qalam).

**Arabic:** ن

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Letter counting under our stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** ن in surah 68 = 132 by our recount. Khalifa's 133 requires counting the spelled-out name 'Noon' (ن و ن) as 2 nuns; the orthodox written initial is a single ن.

### sad-153-vs-152

**Claim:** The letter Sad occurs 152 times across surahs 7, 19 and 38 (97 + 26 + 29).

**Arabic:** ص

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Letter counting under our stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** ص: surah 38 = 29, surah 7 = 98, surah 19 = 26; total 153. Khalifa's 152 requires 97 in surah 7, which requires reading 7:69 as بسطة with س (Samarkand codex spelling); the Tanzil file reads بصطة with ص.

### muqattaat-structure-29-14-78

**Claim:** 29 surahs open with disconnected letters (muqatta'at), using 14 distinct letters, 78 initial letters in total.

**Arabic:** الم، المص، الر، المر، كهيعص، طه، طسم، طس، يس، ص، حم، حم عسق، ق، ن

**Source:** Khalifa Sayoud (and SeekersGuidance, Shaykh Anas al-Musa), *'Quranic Descriptors' / 'What is the total number of words, verses, and letters in the Quran?'* (2013) — <https://seekersguidance.org/answers/quran/what-is-the-total-number-of-words-verses-and-letters-in-the-quran/>

**Corpus and method:** First-verse check on the Tanzil file after stripping the merged unnumbered basmalah; structure per Sayoud (2013) and SeekersGuidance.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The expected initials match in 28/29 surahs from verse 1; surah 42's عسق is in verse 2 (42:1 is حم, 42:2 is عسق). Distinct initial letters 14 (ا ل م ص ر ك ه ي ع ط س ح ق ن); total initial letters 78 (3 monograms, 10 bigrams, 13 trigrams, 2 tetragrams, 1 pentagram).

### all-28-letters-verses

**Claim:** Two verses contain all 28 letters of the Arabic alphabet: 3:154 and 48:29.

**Source:** Classical observation, cited in Sayoud (2013) and Quran-code literature, *Quranic letter-count literature* — <https://submission.org/App1.html>

**Corpus and method:** Distinct-letter count per verse on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 3:154 and 48:29 each have 28 distinct letters, none missing — confirmed by our recount.

### longest-word-fasqaynakumuhu

**Claim:** The longest word in the Quran is fa'asqaynakumuhu (15:22), with 11 letters.

**Arabic:** فَأَسْقَيْنَاكُمُوهُ

**Source:** Classical observation, repeated in modern Quran-statistics pages, *'How long is a Quran?' (calendar-uk FAQ, citing the classical claim)* — <https://www.calendar-uk.co.uk/frequently-asked-questions/how-long-is-a-quran>

**Corpus and method:** Letter counting under our stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** فأسقيناكموه (15:22) is 10 letters under our convention (the dagger alif is a mark, not a letter); the longest words are والمستغفرين (3:17) and والمستضعفين (4:75, 4:127) at 11 letters. Under a convention counting the dagger alif as a letter, فأسقيناكموه is 11 letters and tied for longest. Convention-dependent.

### seven-heavens-7

**Claim:** The phrase 'seven heavens' (sab' samawat) occurs in 7 verses.

**Arabic:** سبع سماوات

**Source:** Harun Yahya (Adnan Oktar), with WikiIslam's verse-by-verse analysis, *Miracles of the Qur'an; WikiIslam, 'Word Count Miracles in the Qur'an'* (2005) — <https://wikiislam.net/index.php?title=Word_Count_Miracles_in_the_Qur%27an>

**Corpus and method:** Verse-level substring search on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 7 verses contain سبع + سماوات (2:29, 17:44, 23:86, 41:12, 65:12, 67:3, 71:15); plus 1 'seven paths' (23:17 طرائق) and 2 'seven strong' (12:48 seven hard years; 78:12 seven strong heavens) = 9 total سبع + heaven-ish verses, matching WikiIslam's analysis.

## Code 19 — Rashad Khalifa's 'mathematical miracle'

### basmalah-19-letters-114

**Claim:** The Basmalah consists of 19 letters, occurs 114 times in the Quran, and the Quran has 114 surahs = 19 x 6.

**Arabic:** بسم الله الرحمن الرحيم

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Letter counting under our stated convention (see meta); occurrence count on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Basmalah = 19 letters under our convention; occurs 114 times in the text (113 at surah starts + 27:30); 114 surahs = 19 x 6.

### allah-2699

**Claim:** The word 'Allah' (God) occurs 2,698 times in the Quran = 19 x 142.

**Arabic:** الله

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Lemma count (all forms of the name, incl. prefixed/clitic forms) on the Tanzil file, excluding the 112 unnumbered basmalahs (see note for the reconciliation).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Lemma count excl. 112 unnumbered basmalahs = 2,699 exactly (incl. basmalahs 2,801; strict surface الله 2,267). The 2,699 includes the oath forms تالله/وتالله (9) and interrogative أبالله (1). Dropping 9:129 (one of Khalifa's two rejected verses) gives his 2,698 = 19 x 142. (QuranCodex's 'strict surface 2,155' differs — method unstated.)

### rahman-57-rahim-115

**Claim:** The names 'Rahman' (Most Gracious) and 'Rahim' (Most Merciful) occur 57 (= 19 x 3) and 114 (= 19 x 6) times.

**Arabic:** الرحمن / الرحيم

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Lemma count on the Tanzil file, excluding the 112 unnumbered basmalahs (see note).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Rahman lemma excl. unnumbered basmalahs = 57 = 19 x 3 (incl. basmalahs 169). Rahim lemma excl. basmalahs = 115; Khalifa's 114 = 115 minus the رحيم in 9:128, one of his two rejected verses.

### ism-19

**Claim:** The word 'ism' (name) in its full spelling occurs 19 times.

**Arabic:** اسم

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Exact-form count on the Tanzil file (plural أسماء excluded, per Khalifa's 'no plural forms' rule).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** اسم 14 + باسم 4 + الاسم 1 = 19; plural أسماء (skeletonised اسما, 4 occurrences) excluded. Contracted بسم = 115 (114 basmalahs + 11:41).

### first-revelation-words-19

**Claim:** The first revelation (96:1-5) consists of 19 words.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Whitespace token count on the Tanzil file, excluding the merged basmalah.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** 96:1-5 has 20 whitespace tokens excl. basmalah (اقرأ باسم ربك الذي خلق / خلق الإنسان من علق / اقرأ وربك الأكرم / الذي علم بالقلم / علم الإنسان ما لم يعلم); 24 incl. basmalah. Khalifa's 19 is one short.

### first-revelation-letters-76

**Claim:** The first revelation (96:1-5) consists of 76 letters.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Letter counting under our stated convention (see meta), excluding the merged basmalah.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** 96:1-5 = 76 letters excl. basmalah under our convention — confirmed.

### surah-96-19-verses-304-letters

**Claim:** Surah 96 has 19 verses and 304 letters in total.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Verse count (standard Hafs table) and letter counting under our stated convention (see meta).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Surah 96 has 19 verses (standard) and 304 letters by our recount — Khalifa's figures exactly.

### surah-110-19-words

**Claim:** Surah 110 consists of 19 words (excluding the Basmalah), and its first verse consists of 19 letters.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Whitespace token count and letter counting under our stated convention (see meta), excluding the merged basmalah.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Surah 110 = 19 words excl. basmalah; verse 110:1 = 19 letters excl. basmalah — confirmed.

### verse-number-checksum-118123

**Claim:** The sum of the verse numbers of all verses containing the word 'Allah' is 118,123 = 19 x 6,217.

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Verse-number sum over verses containing the Allah lemma, on the Tanzil file (see note for the two conditions required).

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** The sum is 118,123 exactly — but only under two conditions: excluding the 112 unnumbered basmalahs AND excluding Khalifa's two rejected verses 9:128-129 (only 9:129 contains Allah, verse number 129; 118,252 - 129 = 118,123). Without those exclusions the sum is 118,340. Khalifa's figure is therefore confirmed as a property of his edited text, not of the standard text.

### khalifa-verse-total-6346

**Claim:** The total number of verses in the Quran is 6,346 = 19 x 334 (6,234 numbered verses + 112 unnumbered Basmalahs).

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Standard Hafs count is 6,236 verses; Khalifa's figure rests on counting basmalahs as verses and deleting 9:128-129.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** The arithmetic checks out (6,236 + 112 - 2 = 6,346) but the deletion of 9:128-129 is the contested step: with those verses the Allah count would be 2,699 not 2,698 and Rahim 115 not 114. The scholarly consensus rejects the deletion (see the reception finding).

### khalifa-reception

**Claim:** Khalifa's 19-based 'mathematical miracle' was published from 1973-1989 and drew both praise and sustained scholarly/skeptical criticism.

**Source:** Rashad Khalifa; Martin Gardner; Bilal Philips; Ziauddin Sardar; Edip Yüksel, *Quran: The Final Testament (1989); Scientific American (1980); The Qur'an's Numerical Miracle: Hoax and Heresy (1987)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Literature review (bibliographic sources, verified by web search 2026-11-06).

**Our status:** ✅ confirmed · **confidence:** reported, method unclear

**Our note:** Timeline: initials research from 1969; Miracle of the Quran: Significance of the Mysterious Alphabets (1973); the 19-code claimed January 1974; The Computer Speaks: God's Message to the World (1981); Quran: Visual Presentation of the Miracle (1982); Quran: The Final Testament translation (1989). Reception: Martin Gardner, Scientific American, September 1980, p. 22 ('ingenious study...'); critical review in Skeptical Inquirer 21(5), September-October 1997, pp. 16-17, 58; Canadian Council on the Study of Religion, Quarterly Review, April 1983 (quoted by proponents as calling it 'an authenticating proof'); Bilal Philips, The Qur'an's Numerical Miracle: Hoax and Heresy (1987); Ziauddin Sardar, Explorations in Islamic Science (1989) on the Nun spelling and letter-count selectivity; Edip Yüksel (proponent), Nineteen: God's Signature in Nature and Scripture (Brainbow Press, 2011); Abdullah Arik, Beyond Probability (2012); Matthew Stanley, A Miracle on Trial (2016). Submission.org's own 2002 recount confirmed Khalifa's initial counts 'except for a few counts' (submission.org/App1.html).

## Modern corpus linguistics

### qac-word-count-77429

**Claim:** The Quran contains 77,429 words (Quranic Arabic Corpus FAQ) / 77,430 words (release notes).

**Source:** Kais Dukes, University of Leeds, *Quranic Arabic Corpus — FAQ and release notes* (2009) — <https://corpus.quran.com/faq.jsp>

**Corpus and method:** QAC v0.4 morphological annotation; our recount on the Tanzil Uthmani text.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Our recount: 77,881 whitespace tokens incl. basmalahs; 77,433 excl. 112 unnumbered basmalahs — 3-4 above the published figures, attributed to word-boundary conventions (known cause: 37:130 آل ياسين is 2 words in Tanzil Uthmani vs 1 in QAC).

### dukes-unique-words

**Claim:** The Quran has 18,994 unique surface forms, 12,183 unique stems, 1,685 unique roots and 3,382 unique lemmas (QAC annotation).

**Source:** Kais Dukes, *'Number of Unique Words in the Quran' (primary-source answer, Quickest Way to the Quran blog)* (2013) — <https://quickestwaytoquran.blogspot.com/2013/08/number-of-unique-words-in-the-quran.html>

**Corpus and method:** QAC v0.4 annotation (Dukes' 2013 primary-source answer); our recount on the Tanzil Uthmani text for the surface-form figure only.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Dukes: unique surface forms 18,994 — our raw unique count is 18,994 exactly. Skeletonised unique forms 14,881. His stem/root/lemma figures (12,183 / 1,685 / 3,382) were not recounted (they need the QAC annotation). Dukes' estimate: 'at most 7,000 unique words'.

### qac-morphology

**Claim:** The Quranic Arabic Corpus provides manually verified morphological annotation of the whole Quran (128,076 morphemes), about 99% accurate, reviewed in stages by two annotators.

**Source:** Kais Dukes, University of Leeds, *Quranic Arabic Corpus — release notes* (2011) — <https://corpus.quran.com/releasenotes.jsp>

**Corpus and method:** QAC v0.4 release notes; verifying needs the QAC data itself, not the plain text.

**Our status:** ❓ cannot verify · **confidence:** reported, method unclear

**Our note:** Treebank covered 40% by word count in v0.4. Not recounted here (the annotation layer is the sibling agents' and the data pipeline's work).

### tanzil-provenance

**Claim:** The Tanzil Quran Text (Uthmani) is derived from the Medina Mushaf, Hafs narration, distributed under CC BY 3.0 with verbatim redistribution only.

**Source:** Tanzil Project, *Tanzil — Quran Text (Uthmani), download and FAQ* — <https://tanzil.net/download>

**Corpus and method:** Tanzil project documentation; the corpus file used for all recounts here is Tanzil Uthmani v1.1.

**Our status:** ✅ confirmed · **confidence:** reported, method unclear

**Our note:** File header and tanzil.net/download confirm the provenance. This is the text all our spot-recounts ran against.

### text-fabric-quran

**Claim:** Text-Fabric Quran (Roorda & van Lit, 2019) re-expresses the Quranic Arabic Corpus morphology as linked open data.

**Source:** Dirk Roorda & Cornelis van Lit, *Text-Fabric Quran (2019)* (2019) — <https://github.com/q-ran/quran>

**Corpus and method:** GitHub q-ran/quran; Zenodo DOI 10.5281/zenodo.2532177; built from QAC 0.4 morphology + Tanzil Uthmani v1.0.2; CC-BY 4.0. Not used in our recounts.

**Our status:** ❓ cannot verify · **confidence:** reported, method unclear

**Our note:** Roorda (2018), 'Text-Fabric: Text representation for linguistic annotation', Research Data Journal for the Humanities and Social Sciences 3(1), 1-23. The dataset itself was not re-analysed here.

### root-frequency-studies

**Claim:** Root-frequency studies of the Quran (QAC 0.4) find about 1,650 roots; the most frequent root is Alh (Allah), about 2,851 occurrences.

**Arabic:** أ-ل-ه

**Source:** Abdul Baqi / Kais Dukes (QAC 0.4 data), *'Standing on the shoulder of Giants' (abdulbaqi.io, 2019)* (2019) — <https://abdulbaqi.io/2019/01/01/standing-on-the-shoulder-of-giants/>

**Corpus and method:** Corpus-based root counts from QAC 0.4 morphology (abdulbaqi.io 2019; thequran.love 2026; Malkoç 2025). Root counting is the sibling agents' task; not recounted here.

**Our status:** ❓ cannot verify · **confidence:** reported, method unclear

**Our note:** abdulbaqi.io (2019): 1,651 roots; top roots Alh 2,851, qwl 1,722, kwn 1,390, rbb 980 (data file quranic-corpus-morphology-0.4.txt, 128,276 lines). Zia H Shah / thequran.love (2026): 1,642 roots, verbal-only counts (qwl 1,618, kwn 1,358), 49,967 root-bearing tokens (64.5%). Muzaffer Malkoç, Beauty as Method (Zenodo, 2025): root concordance via Tanzil + Abd al-Baqi's al-Mu'jam al-Mufahras, e.g. Ḥ-S-N 194. Note the Alh root count (2,851) is a different unit from the Allah lemma count (2,699).

### most-frequent-min-3226

**Claim:** The most frequent word in the Quran is 'min' (from), 3,226 times, followed by 'Allah' 2,699 and 'ma' 2,565.

**Arabic:** من / الله / ما

**Source:** Words of Quran (QAC v0.4 data), *wordsofquran.com — most frequent words* — <https://wordsofquran.com/>

**Corpus and method:** wordsofquran.com, from QAC v0.4; our recount on the Tanzil file for the min lemma.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Our min lemma recount = 3,314 (من 2,763 + ومن 342 + لمن 94 + فمن 90 + بمن 10 + كمن 9 + ولمن 5 + وبمن 1) — 88 above the published 3,226, method unclear. (wordsofquran.com also gives 4,832 unique lemmas of ~77,797 total words — figures that differ from Dukes' own, definitional.)

### classical-word-totals

**Claim:** Classical authorities give the Quran's word total as 77,439 (with variants 77,430 / 77,437 / 77,797 / 77,934).

**Source:** al-Suyuti (via SeekersGuidance, Shaykh Anas al-Musa), *al-Itqan fi 'Ulum al-Qur'an — classical word and letter totals* — <https://seekersguidance.org/answers/quran/what-is-the-total-number-of-words-verses-and-letters-in-the-quran/>

**Corpus and method:** Classical counts (al-Suyuti, al-Itqan; Basra reciters; Ata' bin Yasar); our recount on the Tanzil file.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Our 77,433 (excl. unnumbered basmalahs) is 6 below the lowest classical figure (77,439) — within the spread of counting conventions. Kufan reciters recorded 77,430, Basran 77,437 (arabiantongue.com).

### classical-letter-totals

**Claim:** Classical authorities give the Quran's letter total as 323,671 (with variants 323,015 / 330,733).

**Source:** al-Suyuti (via SeekersGuidance, Shaykh Anas al-Musa), *al-Itqan fi 'Ulum al-Qur'an — classical word and letter totals* — <https://seekersguidance.org/answers/quran/what-is-the-total-number-of-words-verses-and-letters-in-the-quran/>

**Corpus and method:** Classical counts (al-Suyuti via Yahya ibn al-Harith and others); our recount on the Tanzil file under a stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Our 325,386 (excl. unnumbered basmalahs) matches none of the classical figures exactly; the classical sources disagree among themselves by up to 7,718 (323,015 vs 330,733), and further variants exist (Mujahid 321,000; Ibn Mas'ud 300,670; Salam Abu Muhammad 340,740), so no single letter total is settled. The variation is partly definitional (e.g. whether a doubled letter counts as one or two).

### rdsq-words-77430

**Claim:** A Tanzil-based reproducible count (RDS-Q No. 4, Mulyana 2020) gives 77,430 words for the Quran.

**Source:** Eueung Mulyana, *RDS-Q No. 4 — Quran Statistical Overview and Analysis (2020)* (2020) — <https://www.scribd.com/document/550406160/RDS-Q-004>

**Corpus and method:** Tanzil Uthmani text, unnumbered basmalahs excluded; our recount on the same text.

**Our status:** ✅ confirmed · **confidence:** confirmed by our recount

**Our note:** Ours 77,433 — differs by 3 (word-boundary conventions; known cause: 37:130 آل ياسين is 2 words in Tanzil Uthmani vs 1 in QAC). RDS-Q also notes odd/even verse-group word totals 38,716 / 38,714.

### rdsq-letters-325666

**Claim:** A Tanzil-based reproducible count (RDS-Q No. 4, Mulyana 2020) gives 325,666 letters for the Quran (unnumbered basmalahs excluded).

**Source:** Eueung Mulyana, *RDS-Q No. 4 — Quran Statistical Overview and Analysis (2020)* (2020) — <https://www.scribd.com/document/550406160/RDS-Q-004>

**Corpus and method:** Tanzil Uthmani text, unnumbered basmalahs excluded; our recount on the same text under a stated convention (see meta).

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Ours 325,386 — 280 fewer under our letter convention (dagger alif/small waw/small yeh not counted as letters; alef wasla counted). The exact cause of the 280 gap is unidentified. RDS-Q notes Dukes' figure of 623,638 counts 'join letters and diacritics/harakah' — a different unit.

### botani-2012-distributions

**Claim:** The Quran's verse/word/letter distributions can be fitted statistically (Botani 2012, using QuranCode software): 6,348 verses, 77,878 words, 327,792 letters.

**Source:** Delshad Shaker Ismael Botani, Salahaddin University-Hawler, *'Probability Distributions of the Verses, Words, and Letters of the Holy Quran', IJMCAR 2(3), 27-34* (2012) — <https://www.academia.edu/13913774/Probability_Distributions_of_the_Verses_Words_and_Letters_of_the_Holy_Quran>

**Corpus and method:** QuranCode software (Adams 2011), counting basmalahs as verses; distributions fitted as Exponential/Gamma. Not recounted.

**Our status:** ❓ cannot verify · **confidence:** reported, method unclear

**Our note:** Botani (2012), 'Probability Distributions of the Verses, Words, and Letters of the Holy Quran', International Journal of Mathematical and Computational Applications Research 2(3), 27-34. The higher totals come from counting basmalahs as verses and a different word/letter convention.

### quran-word-57-khalifa

**Claim:** The word 'Quran' itself occurs 57 times in the Quran.

**Arabic:** القرآن

**Source:** Rashad Khalifa, *Appendix 1, Quran: The Final Testament (Authorized English Version)* (1989) — <https://submission.org/App1.html>

**Corpus and method:** Substring and narrow-selection counts on the Tanzil file.

**Our status:** ❌ differs · **confidence:** contested

**Our note:** Full substring count of قرآن = 71; narrow selection القرآن + والقرآن + بالقرآن + قرآنا = 59 under our skeleton (57 under an earlier normalisation, because قرانا went 7 to 9). The claimed 57 does not reproduce under either selection; the method behind it is unclear.

### wikiislam-critique

**Claim:** WikiIslam's 'Word Count Miracles in the Qur'an' documents, verse by verse, the selective counting tactics behind the paired-count claims.

**Source:** WikiIslam, *'Word Count Miracles in the Qur'an'* — <https://wikiislam.net/index.php?title=Word_Count_Miracles_in_the_Qur%27an>

**Corpus and method:** Corpus-based critique using actual verse counts (fetched 2026-11-06).

**Our status:** ✅ confirmed · **confidence:** reported, method unclear

**Our note:** Sub-articles cover 365 days, month 12, dunya/akhira 115, paradise/hell 77, iman/kufr 25, land/water ratio, tongue/sermon 25, shaytan/angel 88, life/death 145, zakah/blessing 32, sun/light 33. Documents selective tactics (prefix/suffix inclusion, plural/singular mixing, sense conflation, cherry-picking). Quoted scholarly refutations: Dr. Zahid Aziz ('no rule or principle for determining which word... must always occur a special number of times'); Dr. Ashraf 'Abd al-Razzaaq Qatanah ('the numerical miracle as presented in these books is not real at all'); Dr. Fahd al-Roomi (on the 365-day count excluding يومكم / يومهم / يومئذ).

### dukes-atwell-2012

**Claim:** The Quranic Arabic Corpus is an annotated linguistic resource for Classical Arabic (Dukes & Atwell 2012; Dukes PhD 2013).

**Source:** Kais Dukes & Eric Atwell, *'The Quranic Arabic Corpus: An annotated linguistic resource', Language Resources and Evaluation 46(3), 475-489* (2012) — <https://doi.org/10.1007/s10579-012-9205-0>

**Corpus and method:** Peer-reviewed papers; the treebank itself was not re-analysed here.

**Our status:** ❓ cannot verify · **confidence:** reported, method unclear

**Our note:** Dukes & Atwell (2012), 'The Quranic Arabic Corpus: An annotated linguistic resource', Language Resources and Evaluation 46(3), 475-489, DOI 10.1007/s10579-012-9205-0; Dukes & Habash (2010), 'Morphological Annotation of Quranic Arabic', LREC 2010; Dukes, Atwell & Sharaf (2010), syntactic annotation guidelines, LREC 2010; Dukes & Atwell (2012), LAMP platform, LREC'12; Dukes PhD thesis (2013), Statistical Parsing by Machine Learning from a Classical Arabic Treebank, University of Leeds. The corpus and its annotation are the primary source for the app's morphology work.

### hapax-legomena

**Claim:** About 1,620 words occur only once in the Quran (hapax legomena).

**Source:** arabiantongue.com, *'How Many Words Are in the Quran?'* (2026) — <https://arabiantongue.com/blog/how-many-words-are-in-the-quran/>

**Corpus and method:** Lemma-based count (arabiantongue.com); our surface-form hapax is a different unit and is not comparable.

**Our status:** ❓ cannot verify · **confidence:** reported, method unclear

**Our note:** Our surface-form hapax (raw whitespace tokens occurring once) = 12,005 — a different unit from the lemma-based ~1,620, so the two figures cannot be compared directly. The lemma-based figure was not recounted (it needs the QAC annotation).

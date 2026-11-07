#!/usr/bin/env python3
"""Reconcile miracleMath scholar findings (2026-11-07).

Applies Checker A (our numbers re-counted) and Checker B (scholar accuracy)
corrections to data/scholar_findings.json, recomputes tallies, regenerates
data/scholar_findings.md from the JSON, and prints a before->after change
log (used for RECONCILIATION.md).

Every number in the new our_note texts was verified by script against the
corpus files in this working copy (see /tmp/merge_verify*.py runs).
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

f = json.load(open(DATA / "scholar_findings.json", encoding="utf-8"))
findings = {x["id"]: x for x in f["findings"]}
changes = []  # (id, field, before, after)


def setf(fid, field, value):
    old = findings[fid].get(field)
    if old != value:
        changes.append((fid, field, old, value))
        findings[fid][field] = value


# ---- Global: drop the unconfirmed "Goodword Books, 2005" imprint ----
for x in f["findings"]:
    s = x.get("source") or {}
    if "Goodword" in (s.get("title") or ""):
        setf(x["id"], "source", {**s,
             "title": "Miracles of the Qur'an — 'Word Repetitions in the Qur'an'",
             "year": None})
# seven-heavens source also carries the 2005 year on the Yahya half
s = findings["seven-heavens-7"]["source"]
setf("seven-heavens-7", "source", {**s, "year": None})

# ---- jannah-jahannam-77: extra token is ajinnah (fetuses), plus 147 explanation ----
setf("jannah-jahannam-77", "our_note",
     "Strict singular forms (الجنة/جنة with prefixes: الجنة 56 + جنة 18 + وجنة 2 + بالجنة 1) = 77; "
     "جهنم substring 77. The جنة substring alone is 78 — the one extra token is أَجِنَّةٌ (ajinnah, 'fetuses', 53:32), "
     "not a form of 'garden' (an earlier draft of this note called it a construct form). The popular 77/77 claim counts "
     "singular 'garden' only. Counting every garden by root/lemma (QAC lemma jan~ap: singular 71 + plural جنات 69 + dual 7) "
     "gives 147 — that is the 147 in Agent 1's heaven/hell pair (147:77), while hell (jahannam) is 77 under both rules. "
     "Both numbers are true under different stated rules: singular garden vs all gardens.")

# ---- shaytan-angels-88: differs -> confirmed (angels 88 by LEM malak) ----
setf("shaytan-angels-88", "our_status", "confirmed")
setf("shaytan-angels-88", "confidence", "confirmed by our recount")
setf("shaytan-angels-88", "our_note",
     "Devils: شيط 70 + شياطين 18 = 88. Angels: QAC lemma malak = 88 — plural ملائكة 73 + 13 singular + 2 duals "
     "(الملكين 2:102, ملكين 7:20). The singulars: 6:8 ×2 (ملك and ملكا — two tokens in one verse), 6:9, 6:50, 11:12, 11:31, "
     "12:31, 17:95, 25:7, 32:11 (ملك الموت, Angel of Death), 53:26, 69:17, 89:22. Our earlier note counted only 12 non-plural "
     "forms (missing the second 6:8 token, the 7:20 dual and 17:95) and so stopped three short at about 85. The pair 88:88 is "
     "confirmed. Note: the bare surface form ملك/الملك totals 63 and mostly means 'king/sovereignty' — sense disambiguation is "
     "required, which the lemma count provides.")

# ---- man-woman-24-24: re-attribute 24/24 to Al-Suwaidan; fix note errors ----
setf("man-woman-24-24", "source",
     {"author": "Tariq Al-Suwaidan (circulating list; also Mufti Afzal Hoosen Elias, 'Astonishing Facts about the Qur'aan')",
      "title": "'Mathematical Miracles of the Holy Quran' (circulating list)",
      "url": "https://www.scribd.com/document/45864275/Mathematical-Miracles-of-the-Holy-Quran",
      "year": None})
setf("man-woman-24-24", "corpus_and_method",
     "Method not stated by the source. (Note: Harun Yahya's published list gives 23/23; the 24/24 figure is from the "
     "circulating Al-Suwaidan/Elias list.)")
setf("man-woman-24-24", "our_note",
     "Man singular (رجل family): رجل 13 + رجلا 7 + لرجل 2 + فرجل 1 + ورجلا 1 = 24. Woman singular (امرأة family): امرات 6 + "
     "امراتهو 5 + امراة 3 + وامراتهو 2 + امراتك 2 + امراتى 2 + وامراتى 1 + لامراتهي 1 + وامراة 1 + وامرات 1 = 24. (An earlier draft "
     "of this note mislabelled the -hu/-hi suffixes as امراتهي/لامراتهو — corrected here.) Harun Yahya's own list gives 23/23 — "
     "one short on each side — so the 24/24 figure belongs to the circulating Al-Suwaidan/Elias list, not to Yahya. With duals "
     "(plurals excluded): man 30, woman 26; with plurals (رجال 27, نساء 59) the root totals are 57/85. Naive substrings: رجل 45, "
     "امرا 46 — the امرا count includes امرأ 'man' 19 and the extra token سَامِرًا (23:67, 'chatting by night'), not السامري as an "
     "earlier draft said (السامري contains no امرا substring).")

# ---- life-death-145: not Yahya; fix 22 -> 23 ----
setf("life-death-145", "source",
     {"author": "Circulating list (quranic-miracles.com; Tariq Al-Suwaidan; Mufti Afzal Hoosen Elias)",
      "title": "'Word repetitions' — circulating mathematical-miracle list",
      "url": "https://www.quranic-miracles.com/miracles/mathematical/word-repetitions",
      "year": None})
setf("life-death-145", "our_note",
     "حياة family (حيو/حيي/حيا) = 125; الحياة noun = 67. موت family = 171 (موت/ميت/مات, after removing the 23 ظلم-forms "
     "(الظلمات 14 + ظلمات 8 + كظلمات 1) and 14 كلمات-forms false positives caught by the مات substring — an earlier draft of "
     "this note said 22 ظلم-forms, omitting كظلمات); الموت noun = 35; موت substring = 91. No straightforward form/root count "
     "reproduces 145/145. This pair is not in Harun Yahya's published list; it circulates on other sites.")

# ---- sun-moon-33-27: Yahya pairs sun+LIGHT; moon 27 is separate ----
setf("sun-moon-33-27", "claim",
     "Harun Yahya pairs 'sun' (shams) and 'light' (nur), each 33 times, counting simple forms only; separately, "
     "'moon' (qamar) occurs 27 times.")
setf("sun-moon-33-27", "claim_arabic_or_terms", "الشمس / النور (and القمر 27, separate claim)")
setf("sun-moon-33-27", "corpus_and_method",
     "Yahya's rule for sun/light: 'only the simple forms of the word were included'. Moon 27 is a separate "
     "widely-circulated claim (WikiIslam), not paired with sun by Yahya — Yahya's page contains no 'moon' at all.")
setf("sun-moon-33-27", "our_note",
     "Sun: شمس substring 33 exact. Moon: قمر substring 27 exact. Light: نور substring 46; lemma nuwr 43; the claimed 33 is "
     "reproduced only by a narrow selection of simple forms — نور 8 + النور 10 + نورا 9 + والنور 3 + بنور 1 + نورهم 2 = 33 — "
     "excluding نورنا/نوركم and منير ('shining') forms. So the sun+light 33/33 pair is confirmed under that stated selection, "
     "and moon 27 stands on its own. An earlier draft of this finding conflated the two claims into one sun/moon pair.")

# ---- muhammad-4: attribution caveat ----
setf("muhammad-4", "our_note",
     "محمد substring = 4. Attribution note: we could not locate 'Muhammad 4' verbatim on the fetched Yahya article page, so "
     "the attribution to Yahya's list rests on the wider list tradition, not on a line seen on that page; the figure itself is "
     "verified by our recount.")

# ---- iman-kufr-25: keep Yahya's qualifier; note the 17 variant ----
setf("iman-kufr-25", "our_note",
     "Naive substring counts: ايمان 86, كفر 343 — far from 25/25. Yahya's wording is 'faith (iman) (without genitive) is "
     "repeated 25 times… as is also the word infidelity (kufr)' — the 25 figure must rest on a very narrow form selection "
     "(excluding genitive constructions) that the source does not state in countable detail, so it does not reproduce under any "
     "clean rule we could state. The circulating quranic-miracles.com list gives iman/kufr as 17, not 25.")

# ---- reward-forgiveness-117-234: Yahya's word is الجزاء, not ثواب ----
setf("reward-forgiveness-117-234", "claim",
     "The words 'reward' (al-jaza') and 'forgiveness' (maghfira) occur 117 and 234 times (forgiveness exactly double reward).")
setf("reward-forgiveness-117-234", "claim_arabic_or_terms", "الجزاء / المغفرة")
setf("reward-forgiveness-117-234", "our_note",
     "The filed Arabic ثواب (thawab) was wrong — Yahya's word is الجزاء (al-jaza'), and the thawab substring is only 13. "
     "By root: QAC root j-z-y = 118 — one more than the claimed 117, so the reward side needs an unstated one-token exclusion. "
     "Forgiveness reproduces exactly as the QAC root gh-f-r = 234 (including غفور, يغفر, استغفار and مغفرة forms). So the pair "
     "as claimed differs by one on the reward side only. (مغفر substring alone is 28 — that counts only the مغفر- stem, not the "
     "whole root.)")

# ---- tongue-sermon-25: counted word is 'admonition' ----
setf("tongue-sermon-25", "our_note",
     "لسان substring 15; موعظ substring 9. Both below 25. Note: WikiIslam points out the counted word is 'admonition', not "
     "'sermon' — 'sermon' as such does not appear in the Quran.")

# ---- wine-intoxication-6: fix the سكر derivation (two compensating errors) ----
setf("wine-intoxication-6", "our_note",
     "خمر substring 7 (claimed 6); سكر substring 4 (claimed 6). The سكر family totals 7: the 4 are سكرت (15:15), سكرتهم (15:72), "
     "سكرا (16:67) and سكرة (50:19) — سكرة was already inside the 4, so it cannot be added again — plus سكارى, 3 tokens "
     "(4:43 ×1, 22:2 ×2, the verse containing it twice). An earlier draft of this note added سكرة on top of the 4 and counted "
     "سكارى as 2 — two compensating errors; the family total 7 is right either way. The two sides do not match as claimed (7 vs 7 "
     "by root would match, but the claimed figure is 6/6).")

# ---- mind-light-49: note the nur 43 + muneer 6 route ----
setf("mind-light-49", "our_note",
     "عقل substring 49 exactly; نور substring 46 — three short of 49. The pair matches on one side only. WikiIslam notes the 49 "
     "can be reached as nur 43 (lemma) + muneer 6 — but that mixes the noun 'light' with the adjective 'shining', so we do not "
     "accept it as the same word.")

# ---- refuge-forever-28: Yahya's word is المصير, not ملجأ ----
setf("refuge-forever-28", "claim",
     "The words 'destination/return' (al-maseer) and 'forever' (abadan) each occur 28 times.")
setf("refuge-forever-28", "claim_arabic_or_terms", "المصير / أبدا")
setf("refuge-forever-28", "our_note",
     "The filed Arabic ملجأ (malja', 'refuge') was wrong — Yahya's word is المصير (al-maseer, 'destination/return'), and the "
     "ملجا substring is only 3. With the correct word: مصير substring = 28 exactly (المصير 23 + مصيرا/ومصيرا/مصيركم). Forever: "
     "ابدا substring 29 — one over 28. So the pair differs by one on the 'forever' side only; the 'refuge' side was never the "
     "problem, the filed word was.")

# ---- trouble-peace-13: correct words; root counts give 13/13 -> confirmed ----
setf("trouble-peace-13", "claim",
     "The words 'distress' (al-dayq) and 'tranquillity' (al-tuma'nina) each occur 13 times.")
setf("trouble-peace-13", "claim_arabic_or_terms", "الضيق / الطمأنينة")
setf("trouble-peace-13", "our_note",
     "The filed Arabic ضر/سلام was wrong — the counted words are الضيق (distress) and الطمأنينة (tranquillity). By QAC root: "
     "D-y-q = 13 exactly and T-m-n = 13 exactly. Plain substrings give ضيق 7 and طمان 3, so the 13/13 pair needs root counting, "
     "not substrings. Confirmed under the root rule.")
setf("trouble-peace-13", "our_status", "confirmed")
setf("trouble-peace-13", "confidence", "confirmed by our recount")

# ---- righteous-wicked-6-3: correct words; 6/3 exact -> confirmed ----
setf("righteous-wicked-6-3", "claim",
     "The words 'the righteous' (al-abrar) and 'the wicked' (al-fujjar) occur 6 and 3 times.")
setf("righteous-wicked-6-3", "claim_arabic_or_terms", "الأبرار / الفجار")
setf("righteous-wicked-6-3", "our_note",
     "The filed Arabic صالح/طالح was wrong — Yahya's words are الأبرار and الفجار. With the correct words: أبرار substring 6 "
     "(الأبرار 5 + للأبرار 1) and فجار substring 3 (الفجار 2 + كالفجار 1) — exact. (The filed words give صلح 37 and طلح 1, and "
     "WikiIslam's literal-form recount of those gives 5 vs 2 — all beside the point once the words are right.)")
setf("righteous-wicked-6-3", "our_status", "confirmed")
setf("righteous-wicked-6-3", "confidence", "confirmed by our recount")

# ---- human-being-65: علقة is 6, not 7 ----
setf("human-being-65", "our_note",
     "انسان substring = 65 exactly. The creation-stage reading (the stages of human creation summing to 65) does not reproduce: "
     "تراب 20 + نطفة 12 + علقة 6 + مضغة 3 + عظام 13 + لحم 58 = 112 by substring. (An earlier draft of this note gave علقة as 7 — "
     "the 7th is the bare word علق in 96:2, which has no ة; علقة itself is 6: علقة 4 + العلقة 1 + كالمعلقة 1.) Yahya's own stage "
     "table gives different numbers again (soil 17, drop 12, embryo 6, lump 3, bone 15, flesh 12 = 65) — his stages are a "
     "different selection from the substring counts, so the 65 total for 'human being' is confirmed but the stage arithmetic is not.")

# ---- harun-yahya-populariser: confirmed -> cannot_verify; drop Goodword imprint ----
setf("harun-yahya-populariser", "our_status", "cannot_verify")
setf("harun-yahya-populariser", "our_note",
     "The list as published at harunyahya.info does not include life/death 145; that claim circulates on other sites (e.g. "
     "quranic-miracles.com). The book's imprint could not be confirmed: harunyahya.info's own book page cites 'Miracles of the "
     "Qur'an, Harun Yahya, Araştırma Press', and a circulating edition is Global Publishing, Istanbul — the 'Goodword Books, 2005' "
     "imprint previously given here is not asserted. The live list also contains one pair this file omits: 'reward' (ajr) and "
     "'action' (fa'il), both 107 times.")

# ---- muqattaat: author Halim Sayoud; 75 vs 78; 29/29 ----
setf("muqattaat-structure-29-14-78", "claim",
     "29 surahs open with disconnected letters (muqatta'at), using 14 distinct letters; 75 initial letters in the verse-1 "
     "openings (78 counting surah 42's second set, 'A.S.Q., separately).")
setf("muqattaat-structure-29-14-78", "corpus_and_method",
     "First-verse check on the Tanzil file after stripping the merged unnumbered basmalah; structure per Sayoud (2013).")
setf("muqattaat-structure-29-14-78", "our_note",
     "The expected initials match in 29/29 surahs from verse 1 (an earlier draft said 28/29 — all 29 match, including 42:1 حم; "
     "عسق is in 42:2). Distinct initial letters 14 (ا ل م ص ر ك ه ي ع ط س ح ق ن). Total: 75 letters in the verse-1 openings "
     "(3 monograms, 10 bigrams, 13 trigrams, 2 tetragrams, 1 pentagram = 75), or 78 counting surah 42's second set عسق "
     "(3 more letters) separately — the earlier draft's '78 (3/10/13/2/1)' mixed the two counts. Author: Halim Sayoud (not "
     "'Khalifa Sayoud' as previously filed); the SeekersGuidance URL previously cited contains none of this structure and is dropped.")
setf("muqattaat-structure-29-14-78", "source",
     {"author": "Halim Sayoud",
      "title": "'Investigation on the Mystery of the Qur'an's Disjointed Letters', QURANICA 5(2), December 2013, University of Malaya",
      "url": "https://ijeas.um.edu.my/index.php/quranica/article/download/5185/2991/11903",
      "year": 2013})

# ---- all-28-letters: re-cite as classical/traditional observation ----
setf("all-28-letters-verses", "source",
     {"author": "Classical/traditional observation",
      "title": "Two verses containing all 28 letters of the Arabic alphabet (3:154, 48:29)",
      "url": None, "year": None})
setf("all-28-letters-verses", "our_note",
     "3:154 and 48:29 each have 28 distinct letters, none missing — confirmed by our recount. Previously cited to Khalifa's "
     "Appendix 1, which contains no such claim; re-cited as a classical/traditional observation, corroborated by multiple modern "
     "checks against the Uthmani text.")

# ---- longest-word: '11 letters' is convention-dependent, not in the source ----
setf("longest-word-fasqaynakumuhu", "claim",
     "The longest word in the Quran is fa'asqaynakumuhu (15:22).")
setf("longest-word-fasqaynakumuhu", "our_note",
     "فأسقيناكموه (15:22) is 10 letters under our convention (the dagger alif is a mark, not a letter); the longest words are "
     "والمستغفرين (3:17) and والمستضعفين (4:75, 4:127) at 11 letters. Under a convention counting the dagger alif as a letter, "
     "فأسقيناكموه is 11 letters and tied for longest. The cited source (calendar-uk FAQ) confirms it as the longest word but "
     "gives no '11 letters' figure — the 11 is convention-dependent, not stated by the source.")

# ---- rahman-57-rahim-115 + ism-19: table is in Appendix 1 Part 2 ----
for fid in ("rahman-57-rahim-115", "ism-19"):
    s = findings[fid]["source"]
    setf(fid, "source", {**s,
         "title": "Appendix 1, Part 2, Quran: The Final Testament (Authorized English Version)",
         "url": "https://submission.org/App1_p2.html"})
setf("rahman-57-rahim-115", "our_note",
     findings["rahman-57-rahim-115"]["our_note"] +
     " Citation note: this table is in Appendix 1 Part 2, not Part 1 (the citation previously pointed at Part 1).")

# ---- khalifa-reception: confirmed -> cannot_verify; soften unverified items ----
setf("khalifa-reception", "our_status", "cannot_verify")
setf("khalifa-reception", "our_note",
     "Timeline: initials research from 1969; Miracle of the Quran: Significance of the Mysterious Alphabets (1973); the 19-code "
     "claimed January 1974; The Computer Speaks: God's Message to the World (1981); Quran: Visual Presentation of the Miracle "
     "(1982); Quran: The Final Testament translation (1989). Reception: Martin Gardner, Scientific American, September 1980, "
     "p. 22 ('ingenious study...'); critical review in Skeptical Inquirer 21(5), September-October 1997, pp. 16-17; Canadian "
     "Council on the Study of Religion, Quarterly Review, April 1983 (quoted by proponents as calling it 'an authenticating "
     "proof'); Bilal Philips, The Qur'an's Numerical Miracle: Hoax and Heresy (1987/1407 AH, 76 pp., 2nd ed. 2002). "
     "Submission.org's own 2002 recount confirmed Khalifa's initial counts 'except for a few counts' (submission.org/App1.html). "
     "The following were listed in an earlier draft of this note but were NOT individually verified in the 2026-11-07 re-check and "
     "are not asserted here: Gardner, Skeptical Inquirer p. 58; Ziauddin Sardar, Explorations in Islamic Science (1989); Edip "
     "Yüksel, Nineteen: God's Signature in Nature and Scripture (Brainbow Press, 2011); Abdullah Arik, Beyond Probability (2012); "
     "Matthew Stanley, A Miracle on Trial (2016).")

# ---- qac-word-count-77429: 77,430 is the v0.3 figure; gap fully explained ----
setf("qac-word-count-77429", "claim",
     "The Quran contains 77,429 words (Quranic Arabic Corpus FAQ and v0.4 release notes); 77,430 is the earlier v0.3 figure.")
setf("qac-word-count-77429", "our_note",
     "Our recount: 77,881 whitespace tokens incl. basmalahs; 77,433 excl. 112 unnumbered basmalahs — 4 above the published 77,429. "
     "The gap is fully explained by word-boundary conventions: exactly 4 verses differ by one token each — 2:181, 8:6, 13:37 "
     "(بعدما: two tokens in Tanzil vs one QAC word) and 37:130 (آل ياسين: two words in Tanzil vs one in QAC). An earlier draft of "
     "this note attributed the whole gap to 37:130 alone; that accounts for only 1 of the 4.")

# ---- dukes-unique-words: blogspot 404; re-cite as widely published estimate ----
setf("dukes-unique-words", "source",
     {"author": "Kais Dukes (figures as widely published)",
      "title": "'Number of unique words in the Quran' — circulating estimate (QAC figures)",
      "url": "https://www.calendar-uk.co.uk/frequently-asked-questions/how-long-is-a-quran",
      "year": None})
setf("dukes-unique-words", "our_note",
     "Unique surface forms 18,994 — our raw unique count is 18,994 exactly. Skeletonised unique forms 14,881. Stem/root/lemma "
     "figures (12,183 / 1,685 / 3,382) were not recounted (they need the QAC annotation). The earlier draft attributed these "
     "figures to a Dukes blog post (quickestwaytoquran.blogspot.com, 2013) — that URL returns 404 and Dukes' authorship of that "
     "post could not be confirmed, so the figures are cited here as the widely published estimate, not as Dukes' blog post. The "
     "earlier note's 'Dukes' estimate: at most 7,000 unique words' was not verified and is dropped.")

# ---- qac-morphology: 128,076 is v0.3, not v0.4 ----
setf("qac-morphology", "claim",
     "The Quranic Arabic Corpus provides manually verified morphological annotation of the whole Quran, about 99% accurate, "
     "reviewed in stages by two annotators.")
setf("qac-morphology", "our_note",
     "Treebank covered 40% by word count in v0.4. The 128,076-morpheme figure is from the QAC v0.3 announcement (14 March 2011), "
     "not the v0.4 release notes as previously cited; our own count of the v0.4 file is 128,219 segments — 143 more. Not recounted "
     "here beyond that (the annotation layer is the sibling agents' and the data pipeline's work).")

# ---- tanzil-provenance: confirmed -> cannot_verify; re-point citation ----
setf("tanzil-provenance", "our_status", "cannot_verify")
setf("tanzil-provenance", "source",
     {"author": "Tanzil Project",
      "title": "Tanzil — Quran Text licence and Medina Mushaf documentation",
      "url": "https://tanzil.net/docs/text_license",
      "year": None})
setf("tanzil-provenance", "our_note",
     "Tanzil's licence documentation (tanzil.net/docs/text_license) and Medina Mushaf documentation "
     "(tanzil.net/docs/Medina_Mushaf) confirm the provenance: Medina Mushaf, Hafs reading, CC BY 3.0, verbatim redistribution "
     "only. The previously cited download page (tanzil.net/download) does not display the licence or Mushaf details in its text, "
     "so the citation is re-pointed. This is the text all our spot-recounts ran against.")

# ---- text-fabric-quran: DOI not legibly confirmed ----
setf("text-fabric-quran", "our_note",
     findings["text-fabric-quran"]["our_note"] +
     " (The Zenodo DOI 10.5281/zenodo.2532177 appears only as a badge image on the fetched repo page, so the DOI number itself "
     "was not legibly confirmed from that page.)")

# ---- root-frequency-studies: fix URL, authorship, add roots 1,642 ----
setf("root-frequency-studies", "source",
     {"author": "Abdul Baqi (QAC 0.4 data by Kais Dukes)",
      "title": "'Standing on the Shoulder of Giants' (abdulbaqi.io, 2019)",
      "url": "http://abdulbaqi.io/2019/01/15/quranic_roots/",
      "year": 2019})
setf("root-frequency-studies", "our_note",
     "abdulbaqi.io (2019): 1,651 roots; top roots Alh 2,851, qwl 1,722, kwn 1,390, rbb 980 (data file "
     "quranic-corpus-morphology-0.4.txt, 128,276 lines). Our independent QAC recount reproduces Alh 2,851, qwl 1,722, kwn 1,390, "
     "rbb 980 and Ḥ-S-N 194, and 49,967 root-bearing tokens (64.5%) — but counts 1,642 distinct roots, not 1,651 (thequran.love "
     "gives 1,642 too) and not Dukes' 1,685: the root total depends on how rare/derived forms are grouped. Zia H Shah / "
     "thequran.love (2026): 1,642 roots, verbal-only counts (qwl 1,618, kwn 1,358). Muzaffer Malkoç, Beauty as Method (Zenodo, "
     "2025): root concordance via Tanzil + Abd al-Baqi's al-Mu'jam al-Mufahras, e.g. Ḥ-S-N 194. Note the Alh root count (2,851) is "
     "a different unit from the Allah lemma count (2,699). The earlier draft's file URL returned 404; the live page is "
     "/2019/01/15/quranic_roots/. The post is Abdul Baqi's; Dukes is the data source, not a co-author.")

# ---- classical totals: variants are al-Suyuti's, not all on the cited page ----
setf("classical-word-totals", "our_note",
     findings["classical-word-totals"]["our_note"] +
     " The 77,430 / 77,797 / 77,934 variants are not on the SeekersGuidance page (which gives 77,439 and 77,437); they are "
     "al-Suyuti variants reported by other witnesses (Kufan 77,430 per arabiantongue.com; al-Suyuti collecting 77,934, 77,437, "
     "77,277 per answeringislam.net; eaalim.com lists 77,439, 77,797 and 77,934).")
setf("classical-letter-totals", "our_note",
     findings["classical-letter-totals"]["our_note"] +
     " The 323,671 and 330,733 variants are not on the SeekersGuidance page (which gives 323,015); they are genuine al-Suyuti "
     "variants corroborated elsewhere (eaalim.com lists 323,015, 323,671 and 330,733; riwaqalquran.com cites 323,671 from "
     "al-Suyuti's al-Itqan).")

# ---- rdsq-words-77430: drop the unreproduced odd/even split ----
setf("rdsq-words-77430", "our_note",
     "Ours 77,433 — differs by 3 (word-boundary conventions; the 4 verses that differ by one token each are 2:181, 8:6, 13:37 and "
     "37:130 — see the qac-word-count finding). The odd/even verse-group totals 38,716 / 38,714 quoted in an earlier draft of this "
     "note did not reproduce under any natural grouping (ayah-number parity 39,647/38,234; global verse-index parity 38,433/39,000; "
     "surah-number parity 36,446/41,435) and are dropped.")

# ---- quran-word-57-khalifa: Khalifa's own 58-minus-10:15 rule; Part 2 ----
setf("quran-word-57-khalifa", "claim",
     "The word 'Quran' occurs 57 times in the Quran — 'this Quran', after excluding 10:15's 'another Quran' from a raw 58.")
setf("quran-word-57-khalifa", "source",
     {"author": "Rashad Khalifa",
      "title": "Appendix 1, Part 2, Quran: The Final Testament (Authorized English Version)",
      "url": "https://submission.org/App1_p2.html",
      "year": 1989})
setf("quran-word-57-khalifa", "our_note",
     "Full substring count of قرآن = 71; narrow selection القرآن + والقرآن + بالقرآن + قرآنا = 59 under our skeleton. Khalifa's own "
     "table (Appendix 1, Part 2, Table 21) is explicit: 'The word 'Quran' occurs in the Quran 58 times, with one of them, in 10:15, "
     "referring to 'another Quran'… must be excluded. Thus, the frequency of 'this Quran' is 57, or 19x3.' Our recount gives 59 for "
     "the narrow selection, not 57 — the claimed 57 does not reproduce even under Khalifa's own stated rule. The citation previously "
     "pointed at Part 1; the table is in Part 2.")

# ---- wikiislam-critique: confirmed -> cannot_verify; al-Roomi not located ----
setf("wikiislam-critique", "our_status", "cannot_verify")
setf("wikiislam-critique", "our_note",
     findings["wikiislam-critique"]["our_note"] +
     " Dr. Fahd al-Roomi's point on the 365-day count was not separately located in the fetched WikiIslam text, so it is not "
     "asserted here.")

# ---- recompute tallies; status/confidence must agree everywhere ----
status = Counter(x["our_status"] for x in f["findings"])
conf = Counter(x["confidence"] for x in f["findings"])
assert status["confirmed"] == conf["confirmed by our recount"], (status, conf)
assert status["differs"] == conf["contested"], (status, conf)
assert status["cannot_verify"] == conf["reported, method unclear"], (status, conf)
cat_tally = {}
for cat in ("paired_counts", "letter_counts", "code19", "corpus_linguistics"):
    c = Counter(x["our_status"] for x in f["findings"] if x["category"] == cat)
    cat_tally[cat] = {"confirmed": c["confirmed"], "differs": c["differs"],
                      "cannot_verify": c["cannot_verify"], "total": sum(c.values())}
f["meta"]["tally"] = {"confirmed": status["confirmed"], "differs": status["differs"],
                      "cannot_verify": status["cannot_verify"], "total": 64}
f["meta"]["reconciled"] = (
    "2026-11-07: scholar-vs-recount reconciliation (Checker A re-counted our numbers; Checker B verified every scholar "
    "claim against its source). Tallies now confirmed %d / differs %d / cannot_verify %d; our_status and confidence agree "
    "on all 64 findings. See RECONCILIATION.md." % (status["confirmed"], status["differs"], status["cannot_verify"]))
f["meta"]["category_tally"] = cat_tally

json.dump(f, open(DATA / "scholar_findings.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("tallies:", dict(status))
print("confidence:", dict(conf))
print("category tally:", json.dumps(cat_tally, ensure_ascii=False))
print("changed fields:", len(changes))
json.dump(changes, open("/tmp/reconcile_changes.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
for fid, field, old, new in changes:
    print(f"\n--- {fid} [{field}] ---")
    print("BEFORE:", json.dumps(old, ensure_ascii=False)[:300])
    print("AFTER: ", json.dumps(new, ensure_ascii=False)[:300])

#!/usr/bin/env python3
"""Build data/scholar_findings_enriched_B.json from methods_check_B results.

Also computes three small extras: strict-surface Allah count, the
Rahman/Rahim union verse list, and the one word with two root-bearing
segments. All numbers come from the corpus files, not from memory.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from methods_check_B import (parse_qac, load_tanzil, skeleton,
                             strip_prefixes, QAC, TANZIL)

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "methods_check_B_results.json"))
words, _n_seg, _sr, _sl = parse_qac(QAC)
verses, bounds = load_tanzil(TANZIL)
skel_tokens = [skeleton(t) for ln in verses for t in ln.split()]

# strict surface Allah (exact token الله after skeletonisation)
strict_allah = sum(1 for t in skel_tokens if t == "الله")
print("strict surface Allah =", strict_allah)

# Rahman/Rahim union verses
union = sorted(set(R["rahman_qac_lemma_verses"]) |
               set(R["rahim_qac_lemma_verses"]),
               key=lambda r: (int(r.split(":")[0]), int(r.split(":")[1])))
union_scholar = [v for v in union if v != "9:128"]
print("rahman/rahim union verses:", len(union),
      "scholar-rule:", len(union_scholar))
union_per = Counter(int(v.split(":")[0]) for v in union)
union_per = {str(s): union_per[s] for s in sorted(union_per)}

# the one word with two root-bearing segments
for loc, rec in sorted(words.items()):
    n_root_seg = sum(1 for _f, fe in rec["segments"] if "ROOT:" in fe)
    if n_root_seg > 1:
        print("two-root-segment word:", loc,
              [(f, fe) for f, fe in rec["segments"]])

# basmalah per-surah verse counts
b_per = Counter(int(v.split(":")[0]) for v in R["basmalah_verses"])
b_per = {str(s): b_per[s] for s in sorted(b_per)}

NA = lambda reason: {"not_applicable": reason}


def locs(verses_list, per_surah, scholar_verses=None):
    d = {"verses": verses_list, "per_surah": per_surah}
    if scholar_verses is not None:
        d["verses_scholar_rule"] = scholar_verses
    return d


def corr(field, was, now, why):
    return {"field": field, "was": was, "now": now, "why": why}


E = {}

E["basmalah-19-letters-114"] = {
    "id": "basmalah-19-letters-114",
    "scholar_method": "method not stated by the source. Khalifa lists the basmalah facts among the 'Simple Facts' that 'do not require any tools to be verified' and 'refer to the original Arabic text' (Appendix 1, Part 1); he states no letter-counting rule — not which marks count as letters, not whether the alef wasla counts. Note: 19 requires counting the alef wasla in \u0671\u0644\u0644\u0647 (بسم 3 + الله 4 + الرحمن 6 + الرحيم 6 = 19); a rule that dropped the wasla would give 18.",
    "method_status": "unstated",
    "exceptions": "The 112 unnumbered basmalahs (surah openings) are not QAC words — only 1:1 and the 27:30 basmalah are numbered-verse words. Surah 9 has no opening basmalah; surah 27 has two basmalahs (opening + 27:30).",
    "verification_scholar_rule": {"count": 19, "note": "19 letters under the project's stated letter convention (alef wasla counts; no dagger alif or small letters occur in the basmalah). The letter rule itself is unstated by Khalifa, so this is a reproduction under our convention, not his."},
    "verification_root_rule": {"count": 19, "note": "Same 19 letters (a letter count has no root rule); occurrences in the text = 114 (113 surah openings + 27:30)."},
    "locations": locs(R["basmalah_verses"], b_per),
    "correction": None,
}

E["allah-2699"] = {
    "id": "allah-2699",
    "scholar_method": "Reconstructed. Khalifa states only the totals (2,698 occurrences; checksum 118,123) and no word-counting rule — nothing in Appendix 1 says whether prefixes, oath forms or the basmalahs count. The operative rule is stated in his Appendix 24: verses 9:128-129 are 'false injections' to be removed, and 'the count of the word \"God\" in the Quran was found to be 2699, which is not a multiple of 19, unless we remove one'. Reconstructed rule: (a) count every form of the name, including prefixed/clitic forms (lemma rule) — oath \u062a\u0627\u0644\u0644\u0647/\u0648\u062a\u0627\u0644\u0644\u0647 (9x) and interrogative \u0623\u0628\u0627\u0644\u0644\u0647 (1x) included; (b) exclude the 112 unnumbered basmalahs (QAC convention); (c) drop 9:129.",
    "method_status": "reconstructed",
    "exceptions": "9:129 contains the one Allah dropped by Khalifa's rule (9:128 contains no Allah). The 112 unnumbered basmalahs are excluded (each contains one Allah; including them gives 2,811). Allahumma (5x, QAC lemma {ll~ahum~a) and generic ilah (147x, lemma <ila`h) are separate lemmas and are not counted.",
    "verification_scholar_rule": {"count": 2698, "note": "Lemma count excl. unnumbered basmalahs (2,699) minus the Allah in 9:129 = 2,698 = 19 x 142. Test: 2,699 (Tanzil lemma) = 2,699 (QAC lemma {ll~ah)."},
    "verification_root_rule": {"count": 2699, "note": "QAC lemma {ll~ah = 2,699 (standard text, basmalahs excluded by QAC construction). Tanzil lemma incl. basmalahs = 2,811; strict surface \u0627\u0644\u0644\u0647 = %d." % strict_allah},
    "locations": locs(R["allah_qac_lemma_verses"],
                      R["allah_qac_lemma_per_surah"],
                      R["allah_qac_lemma_verses_scholar_rule"]),
    "correction": None,
}

E["rahman-57-rahim-115"] = {
    "id": "rahman-57-rahim-115",
    "scholar_method": "Reconstructed. Khalifa states only the totals (Rahman 57, Rahim 114) in Appendix 1, Part 2 ('A Strong Foundation'); no counting rule is stated. Reconstructed: Rahman 57 reproduces exactly under the lemma rule excl. unnumbered basmalahs with no further exclusion. Rahim 114 reproduces only as 115 minus the \u0631\u062d\u064a\u0645 in 9:128 (one of the two verses Khalifa deletes; his surah 9 has 127 verses). Note the rule matters: the QAC lemma gives Rahim 116, not 115, because QAC lemmatises the plural \u0631\u064f\u062d\u064e\u0645\u064e\u0627\u0621\u064f at 48:29 ('merciful ones', describing the believers) as r~aHiym — so Khalifa's 114 reproduces only under the singular-form (Tanzil surface-lemma) rule, not under the QAC lemma rule.",
    "method_status": "reconstructed",
    "exceptions": "9:128 \u0631\u062d\u064a\u0645 dropped under Khalifa's rule (Rahim 115 -> 114). 48:29 \u0631\u062d\u0645\u0627\u0621 (plural) is counted by the QAC lemma but not by the singular-form rule. The 112 unnumbered basmalahs are excluded (each contains Rahman once and Rahim once; including them: Rahman 169, Rahim 227).",
    "verification_scholar_rule": {"count": 114, "note": "Rahim: 115 (Tanzil surface-lemma, excl. basmalahs) minus 9:128 = 114 = 19 x 6. Rahman is 57 under the same rule with no exclusion needed (Tanzil 57 = QAC lemma r~aHoma`n 57)."},
    "verification_root_rule": {"count": 116, "note": "Rahim under the QAC lemma rule (r~aHiym = 116, incl. the 48:29 plural); 115 under the Tanzil surface-lemma rule. Rahman 57 under both rules."},
    "locations": locs(union, union_per, union_scholar),
    "correction": None,
}

E["ism-19"] = {
    "id": "ism-19",
    "scholar_method": "Reconstructed. Khalifa states only 'Ism (Name) occurs 19 times' (Appendix 1, Part 2). No rule is stated anywhere in Appendix 1 about which forms count: the word 'plural' does not occur in Appendix 1 Part 2 and there is no 'no plural forms' rule in the source. Reconstructed: 19 reproduces only for the full spelling \u0627\u0633\u0645 with prefixes (\u0627\u0633\u0645 14 + \u0628\u0627\u0633\u0645 4 + \u0627\u0644\u0627\u0633\u0645 1), excluding the plural \u0623\u0633\u0645\u0627\u0621 (12 prefixed/suffixed forms; 4 tokens strip to \u0627\u0633\u0645\u0627 on the Tanzil text) and the contracted \u0628\u0633\u0645 (115 occurrences: 114 basmalahs + 11:41).",
    "method_status": "reconstructed",
    "exceptions": "Plural \u0623\u0633\u0645\u0627\u0621 excluded (12 prefixed/suffixed forms in the text; the bare skeleton count is 4). Contracted \u0628\u0633\u0645 excluded (115x). Suffixed singular forms (\u0627\u0633\u0645\u0647, \u0627\u0633\u0645\u0647\u0648, 5x) excluded by the full-spelling rule but counted by the QAC lemma.",
    "verification_scholar_rule": {"count": 19, "note": "Full-spelling forms on the Tanzil text: \u0627\u0633\u0645 14 + \u0628\u0627\u0633\u0645 4 + \u0627\u0644\u0627\u0633\u0645 1 = 19."},
    "verification_root_rule": {"count": 39, "note": "QAC lemma {som} = 39: 19 full-spelling + 12 plural \u0623\u0633\u0645\u0627\u0621 forms + 5 suffixed singular (\u0627\u0633\u0645\u0647/\u0627\u0633\u0645\u0647\u0648) + 3 contracted \u0628\u0633\u0645 (1:1, 11:41, 27:30 — the only basmalahs in the QAC word list)."},
    "locations": locs(R["ism_full_spelling_verses"],
                      R["ism_full_spelling_per_surah"]),
    "correction": None,
}

E["first-revelation-words-19"] = {
    "id": "first-revelation-words-19",
    "scholar_method": "method not stated by the source. Khalifa states only 'The famous first revelation (96:1-5) consists of 19 words' (Simple Fact 8). No counting rule is stated — nothing says whether the merged basmalah counts, or whether a repeated or contracted word counts.",
    "method_status": "unstated",
    "exceptions": "The basmalah merged into 96:1 in the Tanzil text (4 words) is not a QAC word. The 20 words are: \u0627\u0642\u0631\u0623 \u0628\u0627\u0633\u0645 \u0631\u0628\u0643 \u0627\u0644\u0630\u064a \u062e\u0644\u0642 / \u062e\u0644\u0642 \u0627\u0644\u0625\u0646\u0633\u0627\u0646 \u0645\u0646 \u0639\u0644\u0642 / \u0627\u0642\u0631\u0623 \u0648\u0631\u0628\u0643 \u0627\u0644\u0623\u0643\u0631\u0645 / \u0627\u0644\u0630\u064a \u0639\u0644\u0645 \u0628\u0627\u0644\u0642\u0644\u0645 / \u0639\u0644\u0645 \u0627\u0644\u0625\u0646\u0633\u0627\u0646 \u0645\u0627 \u0644\u0645 \u064a\u0639\u0644\u0645.",
    "verification_scholar_rule": {"count": None, "note": "No rule reconstructs 19: 20 words excl. basmalah under every natural count (Tanzil whitespace tokens 20; QAC words 20), 24 incl. basmalah. 19 would require dropping exactly one word (e.g. the repeated \u0627\u0642\u0631\u0623 or the contracted \u0628\u0627\u0633\u0645) — no such rule is stated, so none is asserted here."},
    "verification_root_rule": {"count": 20, "note": "QAC words in 96:1-5 = 20; Tanzil tokens excl. basmalah = 20."},
    "locations": locs(["96:1", "96:2", "96:3", "96:4", "96:5"], {"96": 5}),
    "correction": None,
}

E["first-revelation-letters-76"] = {
    "id": "first-revelation-letters-76",
    "scholar_method": "method not stated by the source. Khalifa states only 'This 19-worded first revelation consists of 76 letters' (Simple Fact 9). No letter-counting rule is stated.",
    "method_status": "unstated",
    "exceptions": "Basmalah excluded (19 letters; including it the count is 95).",
    "verification_scholar_rule": {"count": 76, "note": "76 letters excl. basmalah under the project's stated letter convention (base letters; alef wasla counts; dagger alif/small waw/small yeh do not count). The letter rule itself is unstated by Khalifa."},
    "verification_root_rule": {"count": 76, "note": "Same 76 (a letter count has no root rule)."},
    "locations": locs(["96:1", "96:2", "96:3", "96:4", "96:5"], {"96": 5}),
    "correction": None,
}

E["surah-96-19-verses-304-letters"] = {
    "id": "surah-96-19-verses-304-letters",
    "scholar_method": "method not stated by the source for the letter total. Khalifa states 'Sura 96 consists of 304 Arabic letters' (Simple Fact 12) and 19 verses (Simple Fact 10, the standard Hafs count). No letter-counting rule is stated.",
    "method_status": "unstated",
    "exceptions": "The 304 total REQUIRES the merged basmalah to be counted (285 letters excl. basmalah + 19 = 304). Note the inconsistency inside Khalifa's own figures: his 76 letters for 96:1-5 requires the basmalah EXCLUDED, while his 304 for the whole surah requires it INCLUDED.",
    "verification_scholar_rule": {"count": 304, "note": "304 letters incl. the merged basmalah under the project's letter convention; 19 verses (standard Hafs count; QAC max verse for surah 96 is 19)."},
    "verification_root_rule": {"count": 285, "note": "285 letters excl. the merged basmalah under the project's letter convention (QAC words in surah 96 = 102)."},
    "locations": locs([f"96:{v}" for v in range(1, 20)], {"96": 19}),
    "correction": None,
}

E["surah-110-19-words"] = {
    "id": "surah-110-19-words",
    "scholar_method": "method not stated by the source. Khalifa states only 'The last revelation (Sura 110) consists of 19 words' (Simple Fact 13) and 'The first verse of the last revelation (110:1) consists of 19 letters' (Simple Fact 14). No counting rule is stated for either.",
    "method_status": "unstated",
    "exceptions": "Basmalah merged into 110:1 excluded from both counts (4 words / 19 letters).",
    "verification_scholar_rule": {"count": 19, "note": "19 words excl. basmalah (Tanzil tokens 19; QAC words 19); verse 110:1 = 19 letters excl. basmalah under the project's letter convention."},
    "verification_root_rule": {"count": 19, "note": "Same 19 words (QAC words in surah 110 = 19)."},
    "locations": locs(["110:1", "110:2", "110:3"], {"110": 3}),
    "correction": None,
}

E["verse-number-checksum-118123"] = {
    "id": "verse-number-checksum-118123",
    "scholar_method": "Reconstructed. Khalifa states only the total (118,123 = 19 x 6,217) and the Allah total (2,698). No rule is stated for which verses enter the sum. Reconstructed: the sum reproduces only if (a) each verse is counted once however many times Allah occurs in it, (b) the 112 unnumbered basmalahs are excluded (they would add the verse-1 numbers of 112 surahs), and (c) 9:128-129 are dropped (only 9:129 contains Allah: -129). 118,252 - 129 = 118,123.",
    "method_status": "reconstructed",
    "exceptions": "9:129 (verse number 129) dropped — the only effect of deleting 9:128-129 on this sum, since 9:128 contains no Allah. Unnumbered basmalahs excluded: including them adds 88 to the sum (verse-1 numbers of the surahs whose verse 1 does not otherwise contain Allah).",
    "verification_scholar_rule": {"count": 118123, "note": "Sum of verse numbers of Allah-containing verses, excl. unnumbered basmalahs and excl. 9:128-129 = 118,123 exactly. Cross-check on QAC lemma verses gives the same 118,252 excl. basmalahs, minus 129 = 118,123."},
    "verification_root_rule": {"count": 118340, "note": "Same sum on the standard text incl. the unnumbered basmalahs = 118,340; excl. basmalahs only = 118,252. 1,821 verses contain Allah excl. basmalahs (1,909 incl.)."},
    "locations": locs(R["allah_qac_lemma_verses"],
                      R["allah_qac_lemma_per_surah"],
                      R["allah_qac_lemma_verses_scholar_rule"]),
    "correction": None,
}

E["khalifa-verse-total-6346"] = {
    "id": "khalifa-verse-total-6346",
    "scholar_method": "Stated by Khalifa himself (Simple Fact 3): 'The total number of verses in the Quran is 6346, or 19 x 334. [6234 numbered verses & 112 un-numbered verses (Basmalahs) 6234+112 = 6346]'. His tables (Appendix 1, Part 2, Tables 22 and 25) give surah 9 as 127 verses, i.e. 6,234 = 6,236 - 2 (9:128-129 dropped).",
    "method_status": "stated",
    "exceptions": "9:128-129 deleted from the numbered verses (surah 9 = 127 verses in his text, not 129). The 112 unnumbered basmalahs are counted as verses; surah 1's basmalah is a numbered verse (1:1) and is not double-counted.",
    "verification_scholar_rule": {"count": 6346, "note": "Arithmetic checks: 6,234 + 112 = 6,346 = 19 x 334."},
    "verification_root_rule": {"count": 6236, "note": "Standard Hafs numbered verses = 6,236 (QAC file: 6,236 verses). Counting the 112 unnumbered basmalahs as verses WITHOUT dropping 9:128-129 gives 6,348 (Botani's figure)."},
    "locations": NA("verse total, not a word/letter count — no occurrences to locate; the two verses at issue are 9:128-129"),
    "correction": None,
}

E["khalifa-reception"] = {
    "id": "khalifa-reception",
    "scholar_method": "not a count — literature/provenance fact. No counting method applies; the items below were checked against the cited publications and against Khalifa's own Appendix 1 text.",
    "method_status": "not_a_count",
    "exceptions": "None — the claim is a reception history, not a count. Note the Gardner date conflict: Philips' book (quoting the column) and this finding say September 1980, p. 22; Yuksel's 'Nineteen' material says September 1981, pp. 22-24. Philips is treated as the stronger witness here.",
    "verification_scholar_rule": {"count": None, "note": "Timeline verified: initials research from 1969 (Khalifa, App1; Wikipedia 'Quran code'); 'Miracle of the Quran: Significance of the Mysterious Alphabets' 1973 (Philips book, foreword/contents); 19-code claimed January 1974 (App1; Wikipedia); 'The Computer Speaks' 1981 and 'Visual Presentation of the Miracle' 1982 (Philips foreword); 'The Final Testament' 1989 (App1 itself). Gardner, Scientific American, September 1980, p. 22 ('ingenious study of the Koran') — confirmed via Philips' book, which quotes the passage and its context (a fictional 'Mathematical Games' story). Skeptical Inquirer 21(5), Sept-Oct 1997 — confirmed as the issue carrying Gardner's 'The Numerology of Dr Rashad Khalifa' (fetched PDF, pp. 16 and 58 visible; the finding's pp. 16-17 range is consistent with the fetched file). Bilal Philips, 'The Qur'an's Numerical Miracle: Hoax and Heresy', 1987/1407 AH, 76 pp., 2nd ed. 2002 — confirmed via the Scribd/pdf-archive copies. Submission.org's 2002 recount ('confirmed Khalifa's counts of all the Quranic initials except for a few counts in \"A\" and \"L\"') — confirmed verbatim on submission.org/App1.html itself."},
    "verification_root_rule": {"count": None, "note": "Same verification (no corpus count applies). NOT verified: the Canadian Council on the Study of Religion, Quarterly Review, April 1983 quotation ('an authenticating proof') — no source for it was located in this pass; the finding's note already hedges it as 'quoted by proponents'. The items the finding's note lists as not individually verified (Gardner SI p. 58; Sardar 1989; Yuksel 2011; Arik 2012; Stanley 2016) remain unverified."},
    "locations": NA("literature/reception fact — no occurrences to locate"),
    "correction": None,
}

E["qac-word-count-77429"] = {
    "id": "qac-word-count-77429",
    "scholar_method": "Stated by the QAC FAQ: 'The annotation for each of the 77,429 words in the Quran was then reviewed in stages by two annotators.' The word unit is the QAC morphological word (LOCATION surah:verse:word:segment); only the 1:1 basmalah is in the word list — the 112 unnumbered basmalahs prepended in Tanzil are NOT QAC words.",
    "method_status": "stated",
    "exceptions": "QAC word boundaries differ from Tanzil whitespace tokens in exactly 4 verses (2:181, 8:6, 13:37 — \u0628\u0639\u062f\u0645\u0627 as one QAC word vs two Tanzil tokens — and 37:130 — \u0622\u0644 \u064a\u0627\u0633\u064a\u0646 as two Tanzil tokens vs one QAC word). Those 4 verses explain the whole gap between the QAC total (77,429) and the Tanzil token total excl. basmalahs (77,433).",
    "verification_scholar_rule": {"count": 77429, "note": "Counted from the v0.4 file itself: 77,429 words, 128,219 segments, 6,236 verses — exactly the published figure."},
    "verification_root_rule": {"count": 77429, "note": "Same 77,429 QAC words. Tanzil whitespace tokens excl. unnumbered basmalahs = 77,433 (4 more; see exceptions)."},
    "locations": NA("whole-corpus total, not a set of occurrences; per-surah QAC word counts are in data/methods_check_B_results.json (qac_words_per_surah)"),
    "correction": None,
}

E["dukes-unique-words"] = {
    "id": "dukes-unique-words",
    "scholar_method": "method not stated by the source. The estimate ('77,430 words, 18,994 unique words, 12,183 stems, 3,382 lemmas and 1,685 roots') is printed without author, method, version or counting unit on calendar-uk.co.uk; no rule is stated for what counts as a 'unique word', 'stem', 'lemma' or 'root'.",
    "method_status": "unstated",
    "exceptions": "The four figures may come from an older QAC version (v0.3: 77,430 words, 128,076 morphemes) or a different lemmatisation — no natural QAC v0.4 rule reproduces 12,183 / 1,685 / 3,382 (POS subsets tried: nouns only 2,690 lemmas; nouns+adjectives+verbs 4,593; none is 3,382).",
    "verification_scholar_rule": {"count": 18994, "note": "Unique surface forms (raw whitespace tokens) = 18,994 exactly — the one figure that reproduces. Stems/roots/lemmas do not reproduce (see root rule)."},
    "verification_root_rule": {"count": 4832, "note": "From the QAC v0.4 annotation: unique stem lemmas 4,832 (not 3,382); unique stem forms 12,113 (not 12,183); unique roots 1,642 at both word and segment level (not 1,685); skeletonised unique surface forms 14,881."},
    "locations": NA("vocabulary inventory, not a set of occurrences"),
    "correction": corr("our_status", "confirmed", "differs",
                       "Recounted from the QAC v0.4 annotation (this pass): only the 18,994 surface-form figure reproduces exactly. Stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832 (not 3,382). The finding's 'confirmed' rested on the surface figure only — its note says the other three 'were not recounted'. They now are, and three of four do not reproduce."),
}

E["qac-morphology"] = {
    "id": "qac-morphology",
    "scholar_method": "not a count — literature/provenance fact about the corpus itself. No counting method applies; the factual items were checked against the QAC FAQ and release notes and against the v0.4 file.",
    "method_status": "not_a_count",
    "exceptions": "The 128,076-morpheme figure is from the v0.3 announcement, not v0.4; the v0.4 file has 128,219 segments (143 more). The treebank coverage figure (40%) is a v0.4 release-notes figure, not a recount (the syntax layer is not in the morphology file).",
    "verification_scholar_rule": {"count": None, "note": "FAQ (fetched 2026-11-08): 'The annotation for each of the 77,429 words in the Quran was then reviewed in stages by two annotators. It is believed that the text is now 99% accurate in terms of morphological annotation.' Release notes v0.4 (1 May 2011, fetched): treebank 'covers 40% of the Quran by word count (30,895 out of 77,429 words)' for chapters 1-8 and 59-114. V0.3 announcement (Kais Dukes, Corpora-List, archived): 'Each of the 77,430 words in the Quran has been morphologically segmented, resulting in 128,076 individual morphemes' — confirmed verbatim. Our v0.4 file: 128,219 segments."},
    "verification_root_rule": {"count": None, "note": "Same verification (no corpus count applies beyond the segment count above: 128,219)."},
    "locations": NA("provenance fact about the corpus — no occurrences to locate"),
    "correction": corr("our_note", "The 128,076-morpheme figure is from the QAC v0.3 announcement (14 March 2011) ...",
                       "The 128,076-morpheme figure is from the QAC v0.3 announcement (12 March 2011) ...",
                       "The archived announcement (Corpora-List, listserv.linguistlist.org, 'Sat Mar 12 17:23:42 UTC 2011') is dated 12 March 2011, not 14 March."),
}

E["tanzil-provenance"] = {
    "id": "tanzil-provenance",
    "scholar_method": "not a count — literature/provenance fact. No counting method applies; checked against Tanzil's own documentation pages.",
    "method_status": "not_a_count",
    "exceptions": "None. The file used for all recounts here is Tanzil Uthmani v1.1 (per the finding's note); the licence and Mushaf pages do not carry a version number, so the v1.1 label itself was not re-verified from those pages.",
    "verification_scholar_rule": {"count": None, "note": "Licence page (tanzil.net/docs/text_license, fetched): 'License: Creative Commons Attribution 3.0', 'Permission is granted to copy and distribute verbatim copies of this text, but CHANGING IT IS NOT ALLOWED' — confirms CC BY 3.0 with verbatim redistribution only. Medina Mushaf page (tanzil.net/docs/Medina_Mushaf, fetched): 'The Quran text provided by Tanzil is based on the Medina Mushaf, narration of Hafs.'"},
    "verification_root_rule": {"count": None, "note": "Same verification (no corpus count applies)."},
    "locations": NA("provenance fact — no occurrences to locate"),
    "correction": None,
}

E["text-fabric-quran"] = {
    "id": "text-fabric-quran",
    "scholar_method": "not a count — literature/provenance fact. No counting method applies; checked against the GitHub repository and the Zenodo DOI record.",
    "method_status": "not_a_count",
    "exceptions": "The Zenodo record for the v0.1 release lists Dirk Roorda alone as author; Cornelis van Lit is co-author of the repository (README lists both). The dataset was not re-analysed here.",
    "verification_scholar_rule": {"count": None, "note": "GitHub q-ran/quran (fetched): 'We have taken the source materials from Quranic Arabic Corpus 0.4 (2011) by Kais Dukes and Tanzil'; 'The data in TF format is licensed as CC-BY 4.0'; authors Cornelis van Lit and Dirk Roorda; released 2019-01-07; repo now archived. Zenodo DOI 10.5281/zenodo.2532177 (resolved via doi.org, fetched): 'q-ran/quran: Initial release', published 5 January 2019, Version v0.1, Dirk Roorda — the DOI is now confirmed, correcting the finding's note."},
    "verification_root_rule": {"count": None, "note": "Same verification (no corpus count applies). Roorda (2018), 'Text-Fabric: Text representation for linguistic annotation', Research Data Journal for the Humanities and Social Sciences 3(1), 1-23, was not re-fetched in this pass."},
    "locations": NA("provenance fact — no occurrences to locate"),
    "correction": corr("our_note", "(The Zenodo DOI 10.5281/zenodo.2532177 appears only as a badge image on the fetched repo page, so the DOI number itself was not legibly confirmed from that page.)",
                       "(The Zenodo DOI 10.5281/zenodo.2532177 is now confirmed: doi.org resolves it to 'q-ran/quran: Initial release', published 5 January 2019, v0.1, Dirk Roorda.)",
                       "DOI resolved and fetched in this pass (2026-11-08); it is the v0.1 initial release, 5 January 2019."),
}

E["root-frequency-studies"] = {
    "id": "root-frequency-studies",
    "scholar_method": "Stated in the post itself (abdulbaqi.io, 2019): the pipeline greps ROOT: from the FEATURES column of the QAC v0.4 morphology file and counts occurrences per SEGMENT line (sort | uniq -c), i.e. a segment-level count, not a per-word count. The post's file is the same 128,276-line v0.4 file used here. Note the post counts every ROOT: occurrence including repeated roots inside one word; in this file that makes no difference (see exceptions).",
    "method_status": "stated",
    "exceptions": "Segment-level and word-level root counting give identical results for every root in this file: no root's segment count exceeds its word count (exactly one word carries two root-bearing segments — 20:94:2, \u064a\u0627\u0628\u0646\u064f\u0645\u064e\u0651 'O son of my mother', stems bona [ROOT bny] + &um~a [ROOT Amm] — giving 49,968 segment ROOT occurrences vs 49,967 root-bearing words). Abdulbaqi's published pipeline re-run on this file gives 1,641 unique roots, not his printed 1,651: it loses the root wAd (81:8:2, \u0627\u0644\u0645\u0648\u0621\u0648\u062f\u0629 'the baby girl buried alive') because that word's FORM 'mawo'u,dapu' contains a comma, shifting cut -d',' -f4. His printed 1,651 reproduces under no rule constructed here (word level 1,642; segment level 1,642; his pipeline 1,641). The thequran.love figure (1,642) matches the word/segment count.",
    "verification_scholar_rule": {"count": 1641, "note": "Abdulbaqi's own published pipeline re-run on this file: 1,641 unique roots, 49,960 segment ROOT occurrences. His printed 1,651 does not reproduce from this file by his own method."},
    "verification_root_rule": {"count": 1642, "note": "Unique roots 1,642 (word level = segment level). Top roots reproduce exactly at both levels: Alh 2,851, qwl 1,722, kwn 1,390, rbb 980; \u1e24-S-N 194 reproduces (word level). Alh root count (2,851) is a different unit from the Allah lemma count (2,699): the root also covers allahumma (5) and generic ilah (147)."},
    "locations": locs(R["root_Alh_verses"], R["root_Alh_per_surah"]),
    "correction": None,
}

E["most-frequent-min-3226"] = {
    "id": "most-frequent-min-3226",
    "scholar_method": "method not stated by the source. wordsofquran.com states its data come from QAC v0.4 but gives no counting rule for 'min' — nothing says whether the relative pronoun \u0645\u064e\u0646 counts, whether suffixed forms (\u0645\u0646\u0647\u0627, \u0645\u0645\u0627) count, or what a 'word' is. The method is identified by reproduction (see verification): the QAC lemma rule reproduces all three of the site's figures exactly.",
    "method_status": "unstated",
    "exceptions": "Tanzil skeleton matching conflates \u0645\u0650\u0646 (preposition, QAC lemma min) with \u0645\u064e\u0646 (relative pronoun, QAC lemma man) once diacritics are stripped. Of the 3,314 Tanzil bare-\u0645\u0646 tokens, 2,499 are QAC min, 806 are QAC man, 6 are the verb man~a ('he bestowed'), and 3 are alignment artifacts at 13:37 (the \u0628\u0639\u062f\u0645\u0627 verse). The QAC min total (3,226) = 2,499 bare tokens + 727 suffixed/contracted forms (\u0645\u0645\u0627, \u0645\u0646\u0647\u0627, \u0645\u0646\u064a ...). The site also gives 4,832 unique lemmas of ~77,797 total words — the lemma total matches QAC (4,832); the 77,797 word total matches no count here (QAC 77,429; Tanzil excl. basmalahs 77,433; incl. 77,881).",
    "verification_scholar_rule": {"count": 3226, "note": "QAC lemma min (preposition) = 3,226 exactly. The site's other two figures also reproduce exactly under the same rule: lemma maA = 2,565, lemma {ll~ah = 2,699. All three figures identify the method as QAC v0.4 lemma counts."},
    "verification_root_rule": {"count": 3226, "note": "Same 3,226 under the QAC lemma rule. The Tanzil skeleton-lemma count is 3,314 — a different unit (it merges min and man); the earlier note's '88 above' is arithmetic coincidence, not an explanation (3,314 - 3,226 = 88, but the man tokens inside the 3,314 number 806, not 88)."},
    "locations": locs(R["min_qac_lemma_verses"], R["min_qac_lemma_per_surah"]),
    "correction": corr("our_status", "differs", "confirmed",
                       "Re-verification proves the published figure: QAC lemma min = 3,226 exactly, and the site's other two figures (ma 2,565, Allah 2,699) also reproduce exactly under the same QAC lemma rule. The 'differs' verdict rested on the Tanzil skeleton-lemma count (3,314), which is a different unit — it conflates the preposition \u0645\u0650\u0646 with the relative pronoun \u0645\u064e\u0646 after diacritic stripping."),
}

E["classical-word-totals"] = {
    "id": "classical-word-totals",
    "scholar_method": "Stated on the SeekersGuidance page (Shaykh Anas al-Musa, summarising al-Suyuti's al-Itqan and classical sources): the variation comes from word-boundary rules — 'they counted (\u0641\u064a \u0627\u0644\u0633\u0645\u0627\u0621) and (\u0641\u064a \u0627\u0644\u0623\u0631\u0636) and (\u0641\u064a \u062e\u0644\u0642) and the like as two words, while some counted them as one word'. The Basra reciters' figure is 77,439 words; Kufan 77,430; Ata' b. Yasar 77,437. The 77,430 / 77,797 / 77,934 variants are al-Suyuti variants reported by other witnesses, not on that page.",
    "method_status": "stated",
    "exceptions": "The classical counts are hand counts (the Basra count was made with barley over four months, per the page). Word-boundary conventions for prepositional phrases are the stated cause of the spread (77,430-77,439).",
    "verification_scholar_rule": {"count": 77439, "note": "Headline Basra figure 77,439 as stated on the page; variants 77,430 (Kufan) and 77,437 (Ata' b. Yasar) stated on the same page."},
    "verification_root_rule": {"count": 77433, "note": "Tanzil whitespace tokens excl. unnumbered basmalahs = 77,433 — 6 below the lowest classical figure (77,439) and 3 above the Kufan 77,430; within the spread of counting conventions. QAC words = 77,429."},
    "locations": NA("whole-Quran total, not a set of occurrences"),
    "correction": None,
}

E["classical-letter-totals"] = {
    "id": "classical-letter-totals",
    "scholar_method": "Stated on the same SeekersGuidance page: the variation comes from whether 'the emphasized letter' (shaddah) is counted as two letters or one — 'those who counted the emphasized letter as two had a higher count of Quranic letters'. Basra reciters: 323,015 letters; Mujahid 321,000; Ibn Mas'ud 300,670; Salam Abu Muhammad 340,740; Abu Mu'adh 321,200. The 323,671 and 330,733 variants are al-Suyuti variants reported elsewhere (eaalim.com, riwaqalquran.com), not on that page.",
    "method_status": "stated",
    "exceptions": "The classical sources disagree among themselves by up to 7,718 letters (323,015 vs 330,733) and further variants exist, so no single letter total is settled. Doubled-letter handling is the stated definitional cause; the Uthmani spelling (omitted alifs, variant readings) is also cited on the page as a cause.",
    "verification_scholar_rule": {"count": 323015, "note": "Headline Basra figure 323,015 as stated on the page."},
    "verification_root_rule": {"count": 325386, "note": "325,386 letters excl. unnumbered basmalahs under the project's letter convention (327,514 incl.) — matches none of the classical figures. Counting shaddah as doubled would give 348,402, far above all of them, so the classical counters were not simply doubling shaddah."},
    "locations": NA("whole-Quran total, not a set of occurrences"),
    "correction": None,
}

E["rdsq-words-77430"] = {
    "id": "rdsq-words-77430",
    "scholar_method": "Stated in RDS-Q No. 4 (Mulyana 2020) itself, fetched from Scribd: 'the Quran text is based on the Uthmani version published by Tanzil project... the Quran is composed of 77430 words and 325666 letters (note: unnumbered Basmallah at the beginning of 112 chapters is not counted)'. Word unit = Tanzil whitespace token. The document also gives odd/even splits by C+V parity (chapter + verse number), per RDS-Q #1/#2.",
    "method_status": "stated",
    "exceptions": "RDS-Q attributes the QAC-vs-Tanzil word gap to 37:130 alone (QAC one word, Tanzil two); the full gap is 4 verses (2:181, 8:6, 13:37, 37:130). The 3-word gap between our Tanzil count (77,433) and RDS-Q's (77,430) on the same text is not explained by the document.",
    "verification_scholar_rule": {"count": 77430, "note": "RDS-Q's headline total, 77,430 words (6236 verses, Tanzil Uthmani, unnumbered basmalahs excluded)."},
    "verification_root_rule": {"count": 77433, "note": "Our Tanzil token count on the same text and rule = 77,433 — 3 above RDS-Q (unexplained at token level). QAC words = 77,429 (4 below ours; the 4 boundary verses)."},
    "locations": NA("whole-Quran total, not a set of occurrences"),
    "correction": corr("our_note", "Ours 77,433 — differs by 3 (word-boundary conventions; the 4 verses that differ by one token each are 2:181, 8:6, 13:37 and 37:130 — see the qac-word-count finding). The odd/even verse-group totals 38,716 / 38,714 quoted in an earlier draft of this note did not reproduce under any natural grouping (ayah-number parity 39,647/38,234; global verse-index parity 38,433/39,000; surah-number parity 36,446/41,435) and are dropped.",
                       "Ours 77,433 — differs by 3 (word-boundary conventions; the 4 verses that differ by one token each are 2:181, 8:6, 13:37 and 37:130 — see the qac-word-count finding). The odd/even verse-group totals 38,716 / 38,714 DO reproduce under the document's own stated criterion, odd/even C+V parity (chapter + verse number): on QAC data exactly 38,715 / 38,714 (the document's own Dukes-data figures, p. 20), and on Tanzil 38,717 / 38,716 — within the same 3-word gap as the headline total. The earlier draft's groupings (ayah-number, verse-index, surah-number parity) were not the document's criterion.",
                       "Recomputed in this pass: C+V parity (the criterion RDS-Q #4 states, p. 18, citing RDS-Q #1/#2) gives 38,715/38,714 on QAC data — exactly the document's Dukes-data figures — and 38,717/38,716 on Tanzil. The earlier 'did not reproduce under any natural grouping' claim never tried C+V parity."),
}

E["rdsq-letters-325666"] = {
    "id": "rdsq-letters-325666",
    "scholar_method": "Stated in RDS-Q No. 4 itself (same passage as the word total): 325,666 letters on the Tanzil Uthmani text, unnumbered basmalahs excluded. The document states NO letter-counting convention — nothing says which marks count as letters — so the 280 gap below cannot be attributed to a stated rule.",
    "method_status": "stated",
    "exceptions": "RDS-Q notes Dukes' figure of 623,638 counts 'join letters and diacritics/harakah' — a different unit (all characters including diacritics), not comparable. The 280-letter gap to our count is still unexplained after testing variants (see verification).",
    "verification_scholar_rule": {"count": 325666, "note": "RDS-Q's headline total, 325,666 letters (same text and rule as the word total)."},
    "verification_root_rule": {"count": 325386, "note": "Our letter count = 325,386 — 280 fewer. Variants tested, none gives +280: counting dagger alif as a letter gives 335,224 (+9,838); dagger alif + small waw/yeh gives 337,438; doubling shaddah gives 348,402. The exact cause of the 280 gap remains unidentified."},
    "locations": NA("whole-Quran total, not a set of occurrences"),
    "correction": None,
}

E["botani-2012-distributions"] = {
    "id": "botani-2012-distributions",
    "scholar_method": "Stated in the paper (Botani 2012, IJMCAR 2(3), 27-34, fetched from Academia): 'All the data which is used in this paper are obtained from QuranCode software created by Adams (2011)'; '29 Arabic letters take into consideration (with accounting Hamza as a letter)'; 'the starting verse of each chapter (Basmalah) considered as a verse in whole Quran' — hence 6,348 verses, 77,878 words, 327,792 letters. Distributions fitted with Excel, Statgraphics Centurion XV and EasyFit 5.5: verses Exponential (lambda = 0.01795), words Gamma (alpha = 0.538, beta = 1269.9).",
    "method_status": "stated",
    "exceptions": "Counting the basmalah as a verse is the whole reason the verse total is 6,348 rather than 6,236 ('In most of literatures, the number of verses is equal to 6236 verses because of non-accounting 112 starting verses as a Quranic verse'). The word/letter totals are QuranCode-software counts, not hand counts; no tokenisation rule beyond the software is stated.",
    "verification_scholar_rule": {"count": 6348, "note": "Verse arithmetic checks: 6,236 + 112 = 6,348. Words 77,878 and letters 327,792 are the paper's QuranCode figures (see root rule for the comparison)."},
    "verification_root_rule": {"count": 6236, "note": "Numbered verses 6,236. On the same Tanzil text incl. basmalahs: words 77,881 (3 above Botani's 77,878) and letters 327,514 (278 below Botani's 327,792) under the project's letter convention. Both gaps are unexplained; the letter gap is in the same family as the 280 RDS-Q gap (278 vs 280 — they differ by 2, so the same unknown convention difference cannot explain both exactly)."},
    "locations": NA("whole-Quran totals plus fitted distributions, not a set of occurrences"),
    "correction": None,
}

E["quran-word-57-khalifa"] = {
    "id": "quran-word-57-khalifa",
    "scholar_method": "Stated by Khalifa (Appendix 1, Part 2, Table 21 and text): 'The word \"Quran\" occurs in the Quran 58 times, with one of them, in 10:15, referring to \"another Quran\"... must be excluded. Thus, the frequency of occurrence of \"this Quran\" in the Quran is 57, or 19x3.' Table 21 lists the suras and verses 'where the word \"Quran,\" in all its grammatical forms, occurs'. Two other grammatical forms ('Quranun' and 'Quranahu') 'occur in 12 verses'; 13:31 ('another Quran' that crumbles mountains) and 41:44 ('a non-Arabic Quran') are excluded.",
    "method_status": "stated",
    "exceptions": "Table 21 as printed has 66 rows, not 58. It excludes all three semantically-excluded verses (10:15, 13:31, 41:44) — the full all-forms verse set is 69 verses. 9 Table-21 verses contain only non-narrow forms (10:61, 15:1, 17:78, 17:106, 36:69, 56:77, 75:17, 75:18, 85:21 — 11 tokens); with 10:15 that is 10 verses containing a non-narrow form, not the 12 Khalifa states. No verse contains both a narrow and a non-narrow form. The substring count (71 tokens) catches one verb: \u0642\u064e\u0631\u064e\u0623\u0652\u0646\u064e\u0627\u0647\u064f ('We recited it', 75:18:2, QAC lemma qara>a), which is not the noun 'Quran'.",
    "verification_scholar_rule": {"count": 59, "note": "Under Khalifa's own stated rule (the narrow forms \u0627\u0644\u0642\u0631\u0622\u0646 / \u0648\u0627\u0644\u0642\u0631\u0622\u0646 / \u0628\u0627\u0644\u0642\u0631\u0622\u0646 / \u0642\u0631\u0622\u0646\u0627, minus 10:15): 59, not 57. 10:15's token is \u0628\u0642\u0631\u0622\u0646 (indefinite, outside the narrow set), so the stated exclusion changes nothing. His 57 = the 57 narrow-form verses in his table; the table silently also excludes 13:31 and 41:44 (both \u0642\u0631\u0622\u0646\u0627, in the narrow set) on semantic grounds. His headline 58 = 57 + 10:15 — i.e. it counts 10:15 in the total while his table excludes it. Either way the claimed 57 does not reproduce under his own stated rule."},
    "verification_root_rule": {"count": 70, "note": "QAC lemma quro'aAn (the noun 'Quran') = 70 words in 69 verses. Tanzil substring \u0642\u0631\u0627\u0646 = 71 tokens — the extra token is the verb at 75:18:2."},
    "locations": locs(R["quran_qac_lemma_verses"],
                      R["quran_qac_lemma_per_surah"],
                      R["quran_narrow_in_table21"]),
    "correction": None,
}

E["wikiislam-critique"] = {
    "id": "wikiislam-critique",
    "scholar_method": "not a count — literature/critique fact. No counting method applies; the page itself was fetched and its claims checked against it. WikiIslam's own method is corpus-based critique using actual verse counts.",
    "method_status": "not_a_count",
    "exceptions": "Dr. Fahd al-Roomi's point on the 365-day count was not separately located in the fetched WikiIslam text, so it is not asserted here (already noted in the finding).",
    "verification_scholar_rule": {"count": None, "note": "Page fetched (wikiislam.net, 'Word Count Miracles in the Qur'an', 1,195 lines): documents the selective tactics — selective choice of words, adding counts of similar words, phrase counts instead of word counts, selective choice of grammatical forms (singular/plural/dual, prefixes/suffixes), calling the selected form 'the simple form', ignoring other meanings, mistranslations, cherry-picking. Sub-articles linked from the page include the zakah/blessing 32-times item (confirmed at line 908). Quoted scholarly refutations: Dr. Zahid Aziz — confirmed quoted at lines 1132-1139 ('A conclusion of Dr. Zahid Aziz after he refuted several \"miracles\"'). The lead's figures agree with our recounts (day total 475, night 92)."},
    "verification_root_rule": {"count": None, "note": "Same verification (no corpus count applies). The finding's sub-article list (365 days, month 12, dunya/akhira 115, paradise/hell 77, iman/kufr 25, land/water ratio, tongue/sermon 25, shaytan/angel 88, life/death 145, zakah/blessing 32, sun/light 33) was not exhaustively re-checked link by link in this pass — only the zakah/blessing link and the Zahid Aziz quotation were individually located."},
    "locations": NA("critique of counting methods — no occurrences to locate"),
    "correction": None,
}

E["dukes-atwell-2012"] = {
    "id": "dukes-atwell-2012",
    "scholar_method": "not a count — bibliographic fact. No counting method applies; the citation itself was checked by resolving the DOI and searching for the cited paper.",
    "method_status": "not_a_count",
    "exceptions": "None beyond the citation error itself.",
    "verification_scholar_rule": {"count": None, "note": "The cited DOI 10.1007/s10579-012-9205-0 is WRONG: doi.org resolves it to 'Evaluating Word Sense Induction and Disambiguation Methods' (Manandhar et al., Language Resources and Evaluation, published 2013-03-02) — a different paper by different authors. The cited journal article ('The Quranic Arabic Corpus: An annotated linguistic resource', Language Resources and Evaluation 46(3), 475-489) could not be located in this pass. The real items are: (a) Dukes & Atwell (2012), 'LAMP: A Multimodal Web Platform for Collaborative Linguistic Analysis', Proc. LREC'12, Istanbul, pp. 3268-3275 (conference paper, no Springer DOI); (b) Dukes, Atwell & Habash (2013), 'Supervised Collaboration for Syntactic Annotation of Quranic Arabic', Language Resources and Evaluation 47(1), 33-62, DOI 10.1007/s10579-011-9167-7. The exact title 'The Quranic Arabic Corpus: An annotated linguistic resource for the Holy Quran' belongs to a different paper: Dukhovny & Atwell, Proc. LREC 2009."},
    "verification_root_rule": {"count": None, "note": "Same verification (no corpus count applies). The corpus and its annotation are genuinely the primary source for the app's morphology work — only this finding's citation is wrong, not the underlying claim that the corpus exists and is Dukes' work."},
    "locations": NA("bibliographic fact — no occurrences to locate"),
    "correction": corr("source.url", "https://doi.org/10.1007/s10579-012-9205-0",
                       "Remove the DOI link; cite the LREC'12 proceedings paper (Dukes & Atwell 2012, 'LAMP', pp. 3268-3275) instead.",
                       "The DOI resolves (fetched 2026-11-08) to 'Evaluating Word Sense Induction and Disambiguation Methods', a different paper by different authors (Manandhar et al., 2013). It cannot be the Dukes & Atwell 2012 reference."),
}

E["hapax-legomena"] = {
    "id": "hapax-legomena",
    "scholar_method": "method not stated by the source. arabiantongue.com states 'nearly 1,620 hapax legomena (words that appear only once in the entire text)' with no counting unit — nothing says whether the unit is a lemma, a surface form, or a root, or which text/edition was counted.",
    "method_status": "unstated",
    "exceptions": "The page's own figures are internally inconsistent in unit: it also gives '~14,800 unique words' and '~1,720 roots', while the QAC v0.4 annotation gives 14,881 skeletonised unique surface forms, 4,832 unique lemmas and 1,642 unique roots.",
    "verification_scholar_rule": {"count": None, "note": "No unit stated, so no scholar-rule count can be constructed. No rule tried reproduces ~1,620 (see root rule)."},
    "verification_root_rule": {"count": 1994, "note": "QAC stem-lemma hapax = 1,994 lemmas occurring exactly once (in 1,528 verses). Surface-form hapax (raw whitespace tokens) = 12,005 — a different unit, confirmed. Skeletonised surface hapax = 8,709. Hapax by POS subsets: nouns only 1,249; nouns+adjectives+verbs 1,943; excl. proper nouns 1,954; roots occurring once 395. None is ~1,620."},
    "locations": locs(R["hapax_stem_lemma_verses"],
                      R["hapax_stem_lemma_per_surah"]),
    "correction": corr("our_note", "Our surface-form hapax (raw whitespace tokens occurring once) = 12,005 — a different unit from the lemma-based ~1,620, so the two figures cannot be compared directly. The lemma-based figure was not recounted (it needs the QAC annotation).",
                       "Our surface-form hapax (raw whitespace tokens occurring once) = 12,005 — a different unit from the lemma-based ~1,620, so the two figures cannot be compared directly. The lemma-based figure has now been recounted from the QAC v0.4 annotation: 1,994 stem lemmas occur exactly once (in 1,528 verses) — which does not match ~1,620 under any POS subset tried (nouns only 1,249; nouns+adjectives+verbs 1,943).",
                       "Recounted in this pass from QAC v0.4 (stem-lemma level): 1,994 hapax lemmas. The ~1,620 figure remains unreproduced."),
}

# sanity: all 27 ids present, sections preserved
IDS = ["basmalah-19-letters-114", "allah-2699", "rahman-57-rahim-115",
       "ism-19", "first-revelation-words-19", "first-revelation-letters-76",
       "surah-96-19-verses-304-letters", "surah-110-19-words",
       "verse-number-checksum-118123", "khalifa-verse-total-6346",
       "khalifa-reception", "qac-word-count-77429", "dukes-unique-words",
       "qac-morphology", "tanzil-provenance", "text-fabric-quran",
       "root-frequency-studies", "most-frequent-min-3226",
       "classical-word-totals", "classical-letter-totals",
       "rdsq-words-77430", "rdsq-letters-325666",
       "botani-2012-distributions", "quran-word-57-khalifa",
       "wikiislam-critique", "dukes-atwell-2012", "hapax-legomena"]
assert set(E) == set(IDS), set(IDS) ^ set(E)
src = json.load(open(HERE / "scholar_findings.json"))
by = {f["id"]: f for f in src["findings"]}
for i in IDS:
    assert by[i]["section"] == "scholarly", i
    assert E[i]["id"] == i

out = [E[i] for i in IDS]
with open(HERE / "scholar_findings_enriched_B.json", "w",
          encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")

from collections import Counter as C
print("entries:", len(out))
print("method_status:", dict(C(e["method_status"] for e in out)))
print("corrections:", sum(1 for e in out if e["correction"]))
print("with locations:", sum(1 for e in out
                             if "not_applicable" not in e["locations"]))
print("Wrote", HERE / "scholar_findings_enriched_B.json")

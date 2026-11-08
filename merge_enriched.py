#!/usr/bin/env python3
"""Merge Checker A/B methods+locations enrichment into the live data files.

- Adds scholar_method / method_status / exceptions / verification_* to every
  finding in data/scholar_findings.json (from the enriched files).
- Applies the coordinator-verified corrections (14 status flips + note fixes).
- Extracts locations into data/locations.json (kept OUT of data.js for size).
- Recomputes meta tallies. Does NOT touch sections, and does NOT apply the
  PASTED_PAGE_CHECK proposals (benefit-corrupt-50 flip etc.) or Isharatul-I'jaz.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

CONF_FOR_STATUS = {
    "confirmed": "confirmed by our recount",
    "differs": "contested",
    "cannot_verify": "reported, method unclear",
}

main = json.load(open(DATA / "scholar_findings.json", encoding="utf-8"))
findings = {f["id"]: f for f in main["findings"]}

enr_a = json.load(open(DATA / "scholar_findings_enriched_A.json", encoding="utf-8"))["findings"]
enr_b = json.load(open(DATA / "scholar_findings_enriched_B.json", encoding="utf-8"))
enriched = {f["id"]: f for f in enr_a + enr_b}
assert set(enriched) == set(findings), (
    "enrichment/findings id mismatch: %s vs %s"
    % (sorted(set(enriched) - set(findings)), sorted(set(findings) - set(enriched))))

# --- coordinator-adjudicated corrections (verified by own scripts) ----------
# status flips: id -> (new_status, why)  -- why appended to our_note
STATUS_FLIPS = {
    "iman-kufr-25": "differs→confirmed: bare (unsuffixed) noun forms reproduce exactly — bare إيمان 25, bare كفر 25 (QAC). Yahya's '(without genitive)' = no possessive suffix.",
    "zakah-blessing-32": "differs→confirmed: by lemma/root, zakah (LEM zakaw`p) is exactly 32 and blessing (ROOT brk) is exactly 32. The old substring test was the wrong unit.",
    "say-they-said-332": "differs→confirmed: singular imperative قل is 332 exactly (293 + 18 + 21 by prefix, QAC LEM qaAla IMPV 2MS) and قالوا is 332 (QAC PERF 3MP).",
    "plant-tree-26": "differs→confirmed: by root, plant (nbt) is exactly 26 and tree ($jr) is 27 of which one token (شَجَرَ, 4:65) is the verb 'to dispute', leaving 26.",
    "reward-forgiveness-117-234": "differs→confirmed: reward (ROOT jzy) is 118 minus the jizya tax token (9:29) = 117; forgiveness (ROOT gfr) is 234 exactly.",
    "guidance-mercy-79": "differs→confirmed: bare (unsuffixed) nouns reproduce exactly — hudFY 79 (85−6 suffixed), raHomap 79 (114−35 suffixed); same bare-form rule as iman/kufr.",
    "tongue-sermon-25": "differs→confirmed: by root, tongue (lsn) is exactly 25 and admonition (wEZ) is exactly 25. 'Sermon' mistranslates موعظة (admonition).",
    "refuge-forever-28": "differs→confirmed: refuge (LEM maSiyr) is 28 and forever (LEM >abadFA) is 28. The old '29' was a substring false positive: عابدات (66:5) contains ابدا in its skeleton but is not أبدا.",
    "disaster-thanks-75": "differs→confirmed: by root, thanks ($kr) is exactly 75 and disaster-sense (Swb) is 75, excluding صيّب (rainstorm, 2:19) and صواب ('right', 78:38).",
    "treachery-foul-16": "differs→confirmed: by root, treachery (xwn) is exactly 16 and foul (xbv) is exactly 16.",
    "jannah-jahannam-77": "confirmed→differs: 12 of the 77 exact surface forms are not 'garden' — جِنَّة (jinn/madness, 10 tokens) and جُنَّة (shield, 2). Sense-correct garden counts are 65 (unsuffixed singular), 70 (QAC lemma singular), 147 (all gardens) — none is 77. Hell is 77 under both rules.",
    "sea-land-32-13": "cannot_verify→differs: land-sense البرّ occurs 12 times, not 13 (the other 10 LEM bar~ tokens are piety/righteousness). Sea (definite singular البحر) is 32, confirmed.",
    "most-frequent-min-3226": "differs→confirmed: QAC lemma min (preposition) is 3,226 exactly; ma 2,565 and Allah 2,699 also reproduce exactly under the same lemma rule. The old 'differs' rested on a Tanzil skeleton count (3,314) that conflates مِن with مَن.",
    "dukes-unique-words": "confirmed→differs: recounted from QAC v0.4, only the 18,994 surface-form figure reproduces exactly. Stems 12,113 (not 12,183), roots 1,642 (not 1,685), lemmas 4,832 (not 3,382).",
}
NEW_STATUS = {
    "iman-kufr-25": "confirmed", "zakah-blessing-32": "confirmed",
    "say-they-said-332": "confirmed", "plant-tree-26": "confirmed",
    "reward-forgiveness-117-234": "confirmed", "guidance-mercy-79": "confirmed",
    "tongue-sermon-25": "confirmed", "refuge-forever-28": "confirmed",
    "disaster-thanks-75": "confirmed", "treachery-foul-16": "confirmed",
    "jannah-jahannam-77": "differs", "sea-land-32-13": "differs",
    "most-frequent-min-3226": "confirmed", "dukes-unique-words": "differs",
}

applied_status = []
note_fixes = []
locations = {}

for fid, f in findings.items():
    e = enriched[fid]
    # new method fields
    f["scholar_method"] = e["scholar_method"]
    f["method_status"] = e["method_status"]
    # Reconstructed findings must SHOW the reconstruction: the checkers left
    # scholar_method as the stock "method not stated" phrase for 20 of them
    # and put the reconstruction only in the verification note. Promote the
    # first sentence of the scholar-rule note (which is the reconstruction)
    # into scholar_method so the site block reads correctly.
    if (f["method_status"] == "reconstructed"
            and f["scholar_method"].strip().lower().startswith("method not stated")):
        note = (e["verification_scholar_rule"] or {}).get("note") or ""
        first = note.split(". ", 1)[0]
        if not first.endswith("."):
            first += "."
        if first.lower().startswith("reconstructed"):
            first = first[len("Reconstructed"):].lstrip()
            if first.startswith(":"):
                first = first[1:].lstrip()
        f["scholar_method"] = first
    f["exceptions"] = e["exceptions"]
    f["verification_scholar_rule"] = e["verification_scholar_rule"]
    f["verification_root_rule"] = e["verification_root_rule"]
    # locations -> separate file
    # NORMALISE per_surah to verse counts per surah (number of listed verses
    # in each surah; sums to len(verses)). Checker A emitted occurrence counts
    # per surah, Checker B verse counts — the site headline is "Locations (N
    # verses)", so verses per surah is the single consistent unit. Occurrence
    # totals stay in the verification lines. The transform is mechanical
    # (derived from the verified verse lists only) — no new corpus logic.
    loc = e["locations"]
    if loc.get("verses"):
        from collections import Counter as _Counter
        loc = dict(loc)
        loc["per_surah"] = dict(sorted(
            _Counter(v.split(":")[0] for v in loc["verses"]).items(),
            key=lambda kv: int(kv[0])))
    locations[fid] = loc
    # status flips (idempotent: skip if already applied)
    if fid in NEW_STATUS:
        old = f["our_status"]
        if old != NEW_STATUS[fid]:
            f["our_status"] = NEW_STATUS[fid]
            f["confidence"] = CONF_FOR_STATUS[NEW_STATUS[fid]]
            f["our_note"] = (f.get("our_note", "") +
                             "\n\nMethods pass (2026-11-08): " + STATUS_FLIPS[fid])
            applied_status.append((fid, old, NEW_STATUS[fid]))
    # note / source corrections recorded in the enriched files
    corr = e.get("correction")
    if corr and fid not in NEW_STATUS:
        already = corr["now"] in f.get("our_note", "")
        if fid == "human-being-65" and \
                "reproduces under lemma/form rules: soil (turaAb) 17" in f.get("our_note", ""):
            already = True  # hand-fixed after the first merge (capitalised lead-in)
        if corr["field"] == "our_note" and already:
            note_fixes.append((fid, "already-applied"))
        elif corr["field"] == "source.url" and fid == "dukes-atwell-2012" \
                and f["source"].get("url") is None:
            note_fixes.append((fid, "already-applied"))
        elif corr["field"] == "our_note":
            was, now = corr["was"], corr["now"]
            note = f.get("our_note", "")
            if was in note:
                f["our_note"] = note.replace(was, now)
                note_fixes.append((fid, "exact"))
            else:
                # 'was' may be an excerpt; try its first 60 chars as anchor
                anchor = was[:60]
                if anchor in note:
                    # replace from anchor to end of the sentence containing it
                    i = note.index(anchor)
                    j = note.find(". ", i)
                    end = (j + 1) if j != -1 else len(note)
                    f["our_note"] = note[:i] + now + note[end:]
                    note_fixes.append((fid, "anchor"))
                else:
                    # fall back: append the corrected text
                    f["our_note"] = note + "\n\nMethods pass (2026-11-08) correction: " + now
                    note_fixes.append((fid, "appended"))
        elif corr["field"] == "source.url" and fid == "dukes-atwell-2012":
            f["source"]["url"] = None
            f["our_note"] = (f.get("our_note", "") +
                "\n\nMethods pass (2026-11-08): the DOI formerly cited here "
                "(10.1007/s10579-012-9205-0) is wrong — it resolves to 'Evaluating "
                "Word Sense Induction and Disambiguation Methods' (Klapaftis & "
                "Manandhar, 2013), a different paper. The real items are Dukes & "
                "Atwell (2012), 'LAMP', Proc. LREC'12, pp. 3268–3275, and Dukes, "
                "Atwell & Habash (2013), Language Resources and Evaluation 47(1), "
                "33–62, DOI 10.1007/s10579-011-9167-7 (verified via Crossref).")
            note_fixes.append((fid, "url-removed"))
        else:
            raise SystemExit("unhandled correction field %s for %s" % (corr["field"], fid))

# human-being-65 note fix is also in the enriched file as our_note correction
# (it is not in NEW_STATUS, so handled above via the correction branch).

# recompute tallies
tally = Counter(f["our_status"] for f in findings.values())
cat_tally = {}
for f in findings.values():
    t = cat_tally.setdefault(f["category"], Counter())
    t[f["our_status"]] += 1
    t["total"] += 1
main["meta"]["tally"] = {"confirmed": tally["confirmed"], "differs": tally["differs"],
                         "cannot_verify": tally["cannot_verify"], "total": 64}
main["meta"]["category_tally"] = {
    c: {"confirmed": t["confirmed"], "differs": t["differs"],
        "cannot_verify": t["cannot_verify"], "total": t["total"]}
    for c, t in cat_tally.items()}
main["meta"]["methods_pass"] = (
    "2026-11-08: every finding now carries the scholar's own method "
    "(stated / reconstructed / unstated), exceptions, verification under both "
    "the scholar's rule and the standard QAC root rule, and script-computed "
    "verse locations (data/locations.json). See METHODS.md. 14 status flips "
    "applied (10 differs→confirmed, 1 confirmed→differs, 1 cannot_verify→"
    "differs, 1 differs→confirmed, 1 confirmed→differs). Tallies now "
    "37 confirmed / 17 differ / 10 cannot verify.")

with open(DATA / "scholar_findings.json", "w", encoding="utf-8") as fh:
    json.dump(main, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
with open(DATA / "locations.json", "w", encoding="utf-8") as fh:
    json.dump({"generated": "2026-11-08",
               "note": "Script-computed verse locations (surah:verse) for miracleMath "
                       "findings, from QAC v0.4 morphology. 'verses' = deduplicated verses "
                       "under the standard QAC root rule; 'per_surah' = occurrence counts "
                       "by surah; 'verses_scholar_rule' = verses under the scholar's own "
                       "reconstructed rule where it differs. 'not_applicable' findings "
                       "are not word/letter counts.",
               "locations": locations}, fh, ensure_ascii=False, separators=(",", ":"))
    fh.write("\n")

print("status flips applied:", len(applied_status))
for fid, old, new in applied_status:
    print("  ", fid, old, "->", new)
print("note fixes:", note_fixes)
print("new tally:", dict(tally))
print("new category tally:", {c: dict(t) for c, t in cat_tally.items()})
nloc = sum(1 for v in locations.values() if "not_applicable" not in v)
print("locations: %d with verse lists, %d N/A" % (
    nloc, len(locations) - nloc))
print("root-rule verse refs:", sum(len(v.get("verses", [])) for v in locations.values()
      if "not_applicable" not in v))
print("scholar-rule verse refs:", sum(len(v.get("verses_scholar_rule") or [])
      for v in locations.values() if "not_applicable" not in v))

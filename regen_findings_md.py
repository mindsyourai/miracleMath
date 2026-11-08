#!/usr/bin/env python3
"""Regenerate data/scholar_findings.md from data/scholar_findings.json.

Keeps the .md in the same format as the original hand-written file so the
two cannot drift. Run after any edit to the JSON.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

f = json.load(open(DATA / "scholar_findings.json", encoding="utf-8"))
locs = json.load(open(DATA / "locations.json", encoding="utf-8"))["locations"]
meta = f["meta"]
findings = f["findings"]
tally = meta["tally"]
cat_tally = meta["category_tally"]

EMOJI = {"confirmed": "✅", "differs": "❌", "cannot_verify": "❓"}
CAT_HEADINGS = [
    ("paired_counts", "Paired-count claims"),
    ("letter_counts", "Letter counts and the disconnected letters (muqatta'at)"),
    ("code19", "Code 19 — Rashad Khalifa's 'mathematical miracle'"),
    ("corpus_linguistics", "Modern corpus linguistics"),
]

lines = []
lines.append("# Scholar findings on the Quran corpus — miracleMath")
lines.append("")
lines.append("Date: 2026-11-06. Corpus: Tanzil Quran Text, Uthmani script "
             "(corpus/quran-uthmani.txt), 6,236 verses, downloaded 2026-11-06 from tanzil.net.")
lines.append("")
lines.append("Reconciled 2026-11-07 — every finding now states the scholar claim as sourced, our recount number, "
             "and the reason for any difference (see RECONCILIATION.md).")
lines.append("")
lines.append("Methods pass 2026-11-08 — every finding now also carries the scholar's own method (stated / "
             "reconstructed / unstated / not a count), the exceptions to that method, verification under both "
             "the scholar's rule and our standard QAC root rule, and script-computed verse locations "
             "(see METHODS.md; full location lists in data/locations.json). Tallies after this pass: "
             "37 confirmed / 17 differ / 10 cannot verify.")
lines.append("")
lines.append("Assumptions pass 2026-11-08 — every finding now also carries named assumption sets (A1–A7) "
             "with per-set numbers and which sets reconcile the scholar's number with ours "
             "(see ASSUMPTIONS.md). Tallies unchanged: 37 confirmed / 17 differ / 10 cannot verify.")
lines.append("")
lines.append("> **Read this first:** disputed numerology is presented here as *reported findings* — each with a source "
             "and a status — never as settled fact. “Confirmed” means our own scripted recount on the Tanzil file "
             "reproduces the claimed figure under a stated method; “differs” means it does not; “cannot verify” means "
             "no recount was possible or the claim needs sense disambiguation. The Nursi strand (Isaratul-I'jaz) is "
             "parked by MK's decision and is **not** covered here.")
lines.append("")
lines.append("## Tally")
lines.append("")
lines.append("- **Total findings: %d** — ✅ confirmed %d · ❌ differs %d · ❓ cannot verify %d"
             % (tally["total"], tally["confirmed"], tally["differs"], tally["cannot_verify"]))
lines.append("")
for cat, heading in CAT_HEADINGS:
    ct = cat_tally[cat]
    lines.append("- %s: %d (confirmed %d, differs %d, cannot verify %d)"
                 % (heading, ct["total"], ct["confirmed"], ct["differs"], ct["cannot_verify"]))
lines.append("")
sec_tally = {}
for x in findings:
    sec = x.get("section", "scholarly")
    t = sec_tally.setdefault(sec, {"total": 0, "confirmed": 0, "differs": 0, "cannot_verify": 0})
    t["total"] += 1
    if x["our_status"] in t:
        t[x["our_status"]] += 1
lines.append("## Sections (split 2026-11-07)")
lines.append("")
lines.append("- Scholar findings: %d (confirmed %d, differs %d, cannot verify %d)"
             % (sec_tally["scholarly"]["total"], sec_tally["scholarly"]["confirmed"],
                sec_tally["scholarly"]["differs"], sec_tally["scholarly"]["cannot_verify"]))
lines.append("- Popular claims (Harun Yahya, Adnan Oktar): %d (confirmed %d, differs %d, cannot verify %d)"
             % (sec_tally["popular"]["total"], sec_tally["popular"]["confirmed"],
                sec_tally["popular"]["differs"], sec_tally["popular"]["cannot_verify"]))
lines.append("")
lines.append("Harun Yahya is the pen name of Adnan Oktar, a Turkish popular creationist author — not a "
             "scholarly source. He was convicted in Turkey in 2022 (8,658-year sentence, upheld 2024). "
             "His widely circulated claims are included so they can be tested against the corpus; "
             "inclusion is not endorsement. Each claim carries its recount label.")
lines.append("")
lines.append("## Recount method")
lines.append("")
lines.append(meta["recount_method"])
lines.append("")
lines.append("Spot-recount script: [`scholar_spotcheck.py`](scholar_spotcheck.py) (corpus totals, Code 19 anchors, "
             "paired counts, letter counts, muqatta'at). The remaining Harun Yahya pairs were checked with a one-off "
             "substring batch (not kept as a deliverable; its numbers are quoted in the notes below).")
lines.append("")
for cat, heading in CAT_HEADINGS:
    lines.append("## " + heading)
    lines.append("")
    for x in [y for y in findings if y["category"] == cat]:
        lines.append("### " + x["id"])
        lines.append("")
        lines.append("**Claim:** " + x["claim"])
        lines.append("")
        arabic = x.get("claim_arabic_or_terms")
        if arabic:
            lines.append("**Arabic:** " + arabic)
            lines.append("")
        s = x.get("source") or {}
        src = "**Source:** " + (s.get("author") or "") + ", *" + (s.get("title") or "") + "*"
        if s.get("year"):
            src += " (%s)" % s["year"]
        if s.get("url"):
            src += " — <%s>" % s["url"]
        lines.append(src)
        lines.append("")
        sec_label = ("Popular claims (Harun Yahya)" if x.get("section") == "popular"
                     else "Scholar findings")
        lines.append("**Section:** " + sec_label)
        lines.append("")
        lines.append("**Corpus and method:** " + x.get("corpus_and_method", ""))
        lines.append("")
        lines.append("**Our status:** %s %s · **confidence:** %s"
                     % (EMOJI[x["our_status"]], x["our_status"], x["confidence"]))
        lines.append("")
        lines.append("**Our note:** " + x.get("our_note", ""))
        lines.append("")
        # --- methods pass (2026-11-08) ---
        lines.append("**Scholar's method (%s):** %s"
                     % (x.get("method_status", "unstated"), x.get("scholar_method", "")))
        lines.append("")
        if x.get("exceptions"):
            lines.append("**Exceptions:** " + x["exceptions"])
            lines.append("")

        def fmt_ver(v):
            if not v:
                return "not applicable"
            c = v.get("count")
            cstr = (" / ".join(str(n) for n in c) if isinstance(c, list)
                    else (str(c) if c is not None else "—"))
            note = v.get("note", "")
            return cstr + ((" — " + note) if note else "")

        lines.append("**Verification — scholar's rule:** " + fmt_ver(x.get("verification_scholar_rule")))
        lines.append("")
        lines.append("**Verification — root rule:** " + fmt_ver(x.get("verification_root_rule")))
        lines.append("")
        a = x.get("assumptions") or {}
        if a:
            def fmt_nbs(v):
                if v is None:
                    return "—"
                if isinstance(v, list):
                    return " / ".join("—" if n is None else str(n) for n in v)
                return str(v)
            nbs_str = ", ".join("%s: %s" % (k, fmt_nbs(v)) for k, v in sorted((a.get("numbers_by_set") or {}).items()))
            lines.append("**Assumptions:** scholar set %s · our set %s · reconciles under: %s · numbers by set: %s · %s"
                         % (a.get("scholar_set") or "—", a.get("our_set") or "—",
                            (", ".join(a.get("reconciles_under") or []) or "none"),
                            (nbs_str or "—"), a.get("reason", "")))
            lines.append("")
        loc = locs.get(x["id"], {})
        if "not_applicable" in loc:
            lines.append("**Locations:** not applicable — " + loc["not_applicable"])
        elif not loc.get("verses"):
            lines.append("**Locations:** not applicable — " + loc.get("note", "no occurrences to locate."))
        else:
            verses = loc["verses"]
            per = loc.get("per_surah", {})
            ps = ", ".join("%s: %d" % (s, n) for s, n in sorted(per.items(), key=lambda kv: int(kv[0])))
            if len(verses) <= 60:
                lines.append("**Locations (%d verses):** %s" % (len(verses), ", ".join(verses)))
            else:
                lines.append("**Locations (%d verses; verses per surah — %s):** first 20: %s … (full list in data/locations.json)"
                             % (len(verses), ps, ", ".join(verses[:20])))
            if loc.get("verses_scholar_rule"):
                sv = loc["verses_scholar_rule"]
                lines.append("**Locations — scholar's rule (%d verses):** %s"
                             % (len(sv), ", ".join(sv[:60]) + (" …" if len(sv) > 60 else "")))
        lines.append("")

out = "\n".join(lines)
(DATA / "scholar_findings.md").write_text(out, encoding="utf-8")
print("wrote scholar_findings.md (%d bytes, %d findings)" % (len(out.encode("utf-8")), len(findings)))

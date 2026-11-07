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
        lines.append("**Corpus and method:** " + x.get("corpus_and_method", ""))
        lines.append("")
        lines.append("**Our status:** %s %s · **confidence:** %s"
                     % (EMOJI[x["our_status"]], x["our_status"], x["confidence"]))
        lines.append("")
        lines.append("**Our note:** " + x.get("our_note", ""))
        lines.append("")

out = "\n".join(lines)
(DATA / "scholar_findings.md").write_text(out, encoding="utf-8")
print("wrote scholar_findings.md (%d bytes, %d findings)" % (len(out.encode("utf-8")), len(findings)))

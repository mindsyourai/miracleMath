# DATA_SOURCES.md — miracleMath

Project: miracleMath — graphical / mathematical Quran web app (owner MK).
Repo target: mindsyourai/miracleMath — https://mindsyourai.github.io/miracleMath/
Last updated: 2026-11-06.

## Primary corpus — Quranic Arabic Corpus (corpus.quran.com)

- **Source:** The Quranic Arabic Corpus, https://corpus.quran.com — University of
  Leeds project, initiated by Kais Dukes. Morphological annotation of the Quran.
- **Version:** 0.4 (released 1 May 2011; release notes at
  https://corpus.quran.com/releasenotes.jsp).
- **Local file:** `corpus/quranic-corpus-morphology-0.4.txt`
  - SHA-256: `a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46`
  - 6,309,503 bytes; 128,276 lines; 128,219 data lines.
  - 77,429 words; 6,236 verses; 114 surahs — matches the corpus's own
    published figure of 77,429 words.
  - Format: tab-separated `LOCATION FORM TAG FEATURES`; LOCATION is
    `(surah:verse:word:segment)`. FORM is Buckwalter transliteration.
    FEATURES carry `LEM:` (lemma) and `ROOT:` (root) tags in Buckwalter.
  - Header copyright block verbatim: "Quranic Arabic Corpus (morphology,
    version 0.4), Copyright (C) 2011 Kais Dukes, License: GNU General
    Public License."
- **How obtained (stated honestly):** the official download page
  (https://corpus.quran.com/download/) serves v0.4 only behind an e-mail
  form (POST to `/download/default.jsp`) and publishes no direct file URL
  (direct-URL guesses redirect to `/`). The Java API (JQuranTree,
  https://corpus.quran.com/java/overview.jsp and
  https://corpus.quran.com/java/api/index.html) is a Java library, not a
  REST API — there is no live API endpoint to query from this environment.
  The file above was fetched 2026-11-06 from the textminingthequran.com
  mirror of the identical v0.4 file and verified against the corpus's own
  published figures (128,276 lines; 77,429 words; verbatim header block).
  It was NOT downloaded directly from corpus.quran.com.
- **Licence / attribution:** GNU GPL. Verbatim redistribution allowed,
  changes not allowed. Any use must name the Quranic Arabic Corpus and link
  to http://corpus.quran.com. The app's Sources page does this.
- **What it is used for:** all counts in the app are derived from this
  annotation — root counts (Agent 1, matched by `ROOT:`), Names of God
  (Agent 2, matched by `LEM:` with `ROOT:` cross-check), and the
  co-occurrence graph (verse membership from word locations).
  Display Arabic is NOT taken from this file (it stores Buckwalter
  transliteration); display Arabic comes from the Tanzil Uthmani text below.

## Cross-check corpus — Tanzil Quran Text, Uthmani script

- **Source:** Tanzil project, https://tanzil.net
  (download URL https://tanzil.net/pub/download/index.php?quranType=uthmani&outType=txt).
- **Local file:** `corpus/quran-uthmani.txt` — downloaded 2026-11-06.
  - SHA-256: `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`
  - 1,334,737 bytes; 6,266 lines (lines 0–6235 are the 6,236 verses, one per
    line; basmalah prepended to the first verse line of each surah except
    Surah 9; remainder is a Tanzil comment footer).
  - ~78,050 whitespace-separated tokens.
- **What it is used for:** (a) display Arabic in the app, copied
  byte-for-byte, never retyped; (b) cross-check of full-text totals.
- **Known counting difference (not an error):** QAC counts 77,429 segmented
  words; Tanzil counts ~78,050 space-delimited tokens. The QAC segments
  clitics (prefixes/suffixes) as separate segments but counts words once;
  Tanzil tokens include the basmalah lines as part of verse lines. The two
  totals are not expected to match; each agent's verification note states
  which total its counts are relative to.

## Counting rules (summary — per-agent detail in data/*_VERIFICATION.md)

- Agent 1 (root-word pairs): match by `ROOT:` in the QAC morphology file;
  surface-form fallback only where stated. Prefixes/suffixes handled at the
  segment level (a word counts once even if its root appears in a prefixed
  segment).
- Agent 2 (Names of God): match by `LEM:` with `ROOT:` cross-check; a Name
  counts once per word occurrence; co-occurrence = both Names in the same
  verse (QAC word locations), plus same-surah edges as a weaker link.
- Agent 3 (scholar findings): literature review only; any recount is a spot
  check against the QAC file above. Disputed numerology is labelled, never
  presented as settled fact.

## What is NOT a source

- MK's supplied Clear Quran PDF (Dr. Mustafa Khattab, 2022) is an English
  translation only and was NOT used as a counting source for any Arabic count.
- No corpus website other than corpus.quran.com / Tanzil was used. If MK
  names a different corpus site later, the corpus must be re-verified and
  this file updated; counts derived from the QAC file remain valid as stated.
- Said Nursi, İşârâtü'l-İ'câz (Signs of Miraculousness): PARKED entirely
  per MK 2026-11-06 — ignored for now, not included, PDF not awaited.

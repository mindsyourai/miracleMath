# miracleMath — The Mathematics of the Quran

A static web app showing word counts and mathematics of the Quran, computed by
script from the Quranic Arabic Corpus and cross-checked against the Tanzil
Uthmani text. Live at https://mindsyourai.github.io/miracleMath/

## What is inside

- **Paired word counts** — heaven/hell, this world/hereafter, life/death, angels/devils,
  belief/disbelief, day/night, sun/moon, man/woman and more, with ratios and verse references.
- **The 99 Names of God** — scripted occurrence counts per Name, a co-occurrence
  network graph (which Names appear together in a verse), and the 24 Names that do
  not occur in the Quran at all.
- **About the Quran** — accurate facts about the Quran (114 surahs, 6,236 verses,
  23 years of revelation, …), each cited to a proper Islamic source (Quran,
  Sahih al-Bukhari/Muslim, al-Suyuti's *al-Itqan*, Ibn Kathir); see
  `data/quran_facts.json` and `QURAN_FACTS.md`.
- **The corpus in numbers** — script-computed totals: 77,429 words, 128,219
  segments, 325,386 letters, 18,994 unique surface forms, 12,113 unique stems,
  1,642 unique roots, 4,832 unique lemmas (see `data/corpus_numbers.json`).
- **Verified counts** — ONE merged table of the 37 findings our recount confirms
  (16 scholarly + 21 popular), shown as claim | scholar's number | our number |
  assumption | verdict | source. Only verified counts appear on the main page.
- **Unverified claims** — the 27 findings that differ or cannot verify live on a
  separate page (`unverified.html`), clearly labelled as not verified, keeping
  the Scholar/Popular split. Nothing unverified appears on the main page.
- **Methodology & sources** — corpus, counting rules, and how to reproduce every number.

## Data

`data/` holds the machine-readable parsed data and the scripts that produced it:

| File | Contents |
|---|---|
| `data/root_counts.json` + `root_counts_script.py` | 13 word pairs + extras, QAC root/lemma counts |
| `data/names.json` + `name_edges.json` + `names_script.py` | 99 Names, co-occurrence graph |
| `data/scholar_findings.json` + `.md` + `scholar_spotcheck.py` | 64 findings with sources and labels |
| `data/quran_facts.json` + `QURAN_FACTS.md` | 10 sourced facts about the Quran |
| `data/corpus_numbers.json` + `corpus_numbers_check.py` + `letter_count.py` | 15 script-computed corpus numbers incl. the 325,386-letter count |
| `data/assumption_sets.json` + `assumption_recompute.py` + `ASSUMPTIONS.md` | 7 named assumption sets (A1–A7) + per-finding reconciliation |
| `data/locations.json` | Script-computed verse locations for the findings |
| `DATA_SOURCES.md` | Corpus provenance, file hashes, counting rules |

Re-running any `*_script.py` regenerates its JSON (root counts: byte-identical).

## Corpus

- **Primary:** Quranic Arabic Corpus v0.4 (Kais Dukes, University of Leeds, 2011),
  corpus.quran.com — 77,429 words, 6,236 verses, 114 surahs. GPL.
- **Cross-check / display Arabic:** Tanzil Quran Text, Uthmani script (tanzil.net).
- See `DATA_SOURCES.md` for the honest fetch note (official download is an e-mail
  form; the v0.4 file used here came via a mirror and was verified against the
  corpus's own published figures).

## The site

Static, no backend, no uploads: `index.html` + `unverified.html` + `styles.css` +
`app.js` + `data.js` (generated from `data/*.json` by `build.py` — re-run it
after any data update).

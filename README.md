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
- **Scholar findings** — 35 published claims about Quranic word-count
  mathematics, each labelled **confirmed by our recount**, **differs**, or **cannot verify**.
  Disputed numerology is presented as a reported finding with its status, never as settled fact.
- **Popular claims** — 29 widely circulated claims by Harun Yahya (Adnan Oktar), kept in a
  separate section with a source note; his list is popular, not scholarly, and each claim
  carries its recount label the same way.
- **Methodology & sources** — corpus, counting rules, and how to reproduce every number.

## Data

`data/` holds the machine-readable parsed data and the scripts that produced it:

| File | Contents |
|---|---|
| `data/root_counts.json` + `root_counts_script.py` | 13 word pairs + extras, QAC root/lemma counts |
| `data/names.json` + `name_edges.json` + `names_script.py` | 99 Names, co-occurrence graph |
| `data/scholar_findings.json` + `.md` + `scholar_spotcheck.py` | 64 findings with sources and labels |
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

Static, no backend, no uploads: `index.html` + `styles.css` + `app.js` + `data.js`
(generated from `data/*.json` by `build.py` — re-run it after any data update).

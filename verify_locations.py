#!/usr/bin/env python3
"""Independent spot-check: every verse listed in data/locations.json for the
sampled findings must actually contain a counted token in the QAC corpus,
parsed fresh here (not via the checkers' scripts)."""
import json, re
from collections import defaultdict

# verse -> set of (ROOT, LEM) from QAC v0.4 morphology
verse_tokens = defaultdict(set)
verse_root = defaultdict(set)
verse_lem = defaultdict(set)
with open('corpus/quranic-corpus-morphology-0.4.txt', encoding='utf-8') as fh:
    for line in fh:
        if line.startswith('LOCATION') or not line.strip():
            continue
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 4:
            continue
        loc, features = parts[0], parts[3]
        m = re.match(r'\(?(\d+):(\d+):', loc)
        if not m:
            continue
        v = '%s:%s' % (m.group(1), m.group(2))
        feats = dict(p.split(':', 1) for p in features.split('|') if ':' in p)
        if 'ROOT' in feats:
            verse_root[v].add(feats['ROOT'])
        if 'LEM' in feats:
            verse_lem[v].add(feats['LEM'])

locs = json.load(open('data/locations.json', encoding='utf-8'))['locations']
findings = {f['id']: f for f in
            json.load(open('data/scholar_findings.json', encoding='utf-8'))['findings']}

def check_verse_list(fid, roots=None, lems=None, exclude_verses=(), expect_per_surah_sum=None):
    loc = locs[fid]
    verses = loc['verses']
    bad = []
    for v in verses:
        ok = False
        if roots and verse_root[v] & set(roots):
            ok = True
        if lems and verse_lem[v] & set(lems):
            ok = True
        if not ok:
            bad.append(v)
    excl_bad = [v for v in exclude_verses if v in verses]
    psum = sum(loc['per_surah'].values())
    print('%s: %d verses, %d bad, excluded-present=%s, per_surah sum=%d%s' % (
        fid, len(verses), len(bad), excl_bad, psum,
        (' (occurrence total %d)' % expect_per_surah_sum) if expect_per_surah_sum else ''))
    if bad[:5]:
        print('   bad verses:', bad[:5])
    assert not bad, bad
    assert not excl_bad, excl_bad
    # per_surah is normalised to verses per surah (see merge_enriched.py)
    assert psum == len(verses), (fid, psum, len(verses))
    assert verses == sorted(set(verses), key=lambda s: (int(s.split(':')[0]), int(s.split(':')[1]))), 'not sorted/deduped'

# 1. Allah: every listed verse has ROOT Alh; 2,699 occurrences over 1,821 verses
check_verse_list('allah-2699', roots=['Alh'], expect_per_surah_sum=2699)
# 2. plant/tree: nbt + $jr roots; 4:65 (dispute verb) must NOT be listed; 26+26=52
check_verse_list('plant-tree-26', roots=['nbt', '$jr'], exclude_verses=['4:65'],
                 expect_per_surah_sum=52)
# 3. reward/forgiveness: jzy + gfr; 9:29 (jizya tax) must NOT be listed; 117+234=351
check_verse_list('reward-forgiveness-117-234', roots=['jzy', 'gfr'],
                 exclude_verses=['9:29'], expect_per_surah_sum=351)
# 4. tongue/admonition: lsn + wEZ; 25+25=50
check_verse_list('tongue-sermon-25', roots=['lsn', 'wEZ'], expect_per_surah_sum=50)
# 5. disaster/thanks: Swb + $kr; 2:19 (rainstorm) and 78:38 ('right') excluded; 75+75=150
check_verse_list('disaster-thanks-75', roots=['Swb', '$kr'],
                 exclude_verses=['2:19', '78:38'], expect_per_surah_sum=150)
# 6. treachery/foul: xwn + xbv; 16+16=32
check_verse_list('treachery-foul-16', roots=['xwn', 'xbv'], expect_per_surah_sum=32)
# 7. jannah/jahannam root rule: LEM jan~ap (147) + LEM jahan~am (77, a proper
#    noun with no QAC root) = 224
check_verse_list('jannah-jahannam-77', lems=['jan~ap', 'jahan~am'],
                 expect_per_surah_sum=224)
print('ALL LOCATION SPOT-CHECKS PASSED (7 findings, %d verse refs)' % sum(
    len(locs[f]['verses']) for f in
    ['allah-2699', 'plant-tree-26', 'reward-forgiveness-117-234', 'tongue-sermon-25',
     'disaster-thanks-75', 'treachery-foul-16', 'jannah-jahannam-77']))

/* Cold-load stub test for the miracleMath research redesign (2026-11-08):
   loads web/data.js + web/locations.js + web/app.js in a minimal fake DOM
   twice — once as the main page (index.html ids present) and once as the
   unverified page (unverified.html ids present) — and asserts the split:
   main page = 37 verified findings only, 0 unverified; unverified page =
   27 differs/cannot_verify rows only. Also checks the About-the-Quran
   facts table, the corpus-numbers table, pairs (13), Names (99) and graph.
   Supersedes verify_coldload.js, which asserted the old Scholar/Popular
   tab structure (35/29 rows). Usage: node verify_redesign.js */
const vm = require('vm');
const fs = require('fs');

const MAIN_IDS = new Set(['stats', 'tally-line', 'facts-table', 'corpus-table',
  'assumption-table', 'pair-search', 'pair-equal-only', 'pairs-list', 'extras-list',
  'name-search', 'name-filter', 'graph-scope', 'graph-edges', 'graph', 'graph-detail',
  'names-list', 'name-detail', 'verified-search', 'verified-cat', 'verified-tally',
  'verified-list']);
const UNV_IDS = new Set(['unverified-search', 'unverified-cat', 'unverified-status',
  'unverified-tally', 'unverified-list']);

class El {
  constructor(id) {
    this.id = id;
    this.innerHTML = '';
    this.textContent = '';
    this.value = /-search$/.test(id) ? '' : 'all';
    this.checked = false;
    this.classList = { add() {}, remove() {}, toggle() {} };
    this.style = {};
    this.width = 800;
    this.height = 600;
    this._listeners = {};
  }
  addEventListener(type, fn) { (this._listeners[type] = this._listeners[type] || []).push(fn); }
  _fire(type, ev) { (this._listeners[type] || []).forEach((fn) => fn(ev || {})); }
  getAttribute() { return ''; }
  getContext() {
    return new Proxy({}, {
      get: (t, k) => {
        if (k === 'measureText') return () => ({ width: 10 });
        if (k === 'canvas') return this;
        return () => {};
      },
      set: () => true,
    });
  }
  getBoundingClientRect() { return { left: 0, top: 0, width: 800, height: 600 }; }
  scrollIntoView() {}
}

function runPage(idSet) {
  const els = {};
  // Static HTML already carries the graph placeholder text; seed it like the
  // real page does so drawGraph() must not clobber it.
  if (idSet.has('graph-detail')) {
    els['graph-detail'] = new El('graph-detail');
    els['graph-detail'].textContent = 'Select a Name in the graph to see its strongest partners.';
  }
  const document = {
    getElementById: (id) => {
      if (!idSet.has(id)) return null;
      if (!els[id]) els[id] = new El(id);
      return els[id];
    },
    querySelectorAll: () => [],
  };
  const windowObj = {};
  const sandbox = { window: windowObj, document, console };
  vm.createContext(sandbox);
  const errors = [];
  try {
    for (const f of ['web/data.js', 'web/locations.js', 'web/app.js']) {
      vm.runInContext(fs.readFileSync(f, 'utf8'), sandbox, { filename: f });
    }
  } catch (e) { errors.push('LOAD ERROR: ' + e.stack); }
  return { els, data: windowObj.MIRACLE_DATA || {}, locs: windowObj.MIRACLE_LOCATIONS || {}, errors };
}

function count(re, s) { return (s.match(re) || []).length; }
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok, detail || '']);
  console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (detail ? '  (' + detail + ')' : ''));
}

const data = JSON.parse(fs.readFileSync('data/scholar_findings.json', 'utf8'));
const findings = data.findings;
const confirmed = findings.filter((f) => f.our_status === 'confirmed');
const unverified = findings.filter((f) => f.our_status !== 'confirmed');
console.log('source data: confirmed=' + confirmed.length + ' unverified=' + unverified.length +
  ' (scholarly confirmed ' + confirmed.filter((f) => f.section === 'scholarly').length +
  ', popular confirmed ' + confirmed.filter((f) => f.section === 'popular').length + ')');

/* ================= MAIN PAGE ================= */
console.log('\n--- main page (index.html) ---');
const main = runPage(MAIN_IDS);
const vHtml = () => (main.els['verified-list'] ? main.els['verified-list'].innerHTML : '');
check('main: no load errors', main.errors.length === 0, main.errors.join(' | '));
check('main: MIRACLE_DATA findings = 64', (main.data.findings || []).length === 64);
check('main: MIRACLE_LOCATIONS entries = 64', Object.keys(main.locs).length === 64);
check('main: data.js embeds quran_facts + corpus_numbers',
  Array.isArray(main.data.quran_facts) && Array.isArray(main.data.corpus_numbers),
  'facts=' + (main.data.quran_facts || []).length + ' numbers=' + (main.data.corpus_numbers || []).length);

// About the Quran facts table
const factsHtml = main.els['facts-table'] ? main.els['facts-table'].innerHTML : '';
const factsJson = JSON.parse(fs.readFileSync('data/quran_facts.json', 'utf8'));
const factsRows = factsJson.sample ? factsJson.facts : factsJson.facts || factsJson;
check('main: facts table renders one row per fact (' + factsRows.length + ')',
  count(/<tr><td>/g, factsHtml) === factsRows.length, 'got ' + count(/<tr><td>/g, factsHtml));
check('main: every fact row carries a source',
  factsRows.every((f) => factsHtml.includes(f.source.split('—')[0].trim()) || factsHtml.includes(f.source)),
  'checked ' + factsRows.length + ' sources');
check('main: facts table header is fact | value | source',
  factsHtml.includes('<th>Fact</th><th>Value</th><th>Source</th>'));
if (main.data.quran_facts_sample)
  check('main: SAMPLE facts flagged in-page (not silent)',
    factsHtml.includes('Sample data'), 'sample flag present in data.js');
else
  check('main: real (non-sample) facts — no sample flag', !factsHtml.includes('Sample data'));

// Corpus numbers table
const corpHtml = main.els['corpus-table'] ? main.els['corpus-table'].innerHTML : '';
const numsJson = JSON.parse(fs.readFileSync('data/corpus_numbers.json', 'utf8'));
const numsRows = numsJson.sample ? numsJson.numbers : numsJson.numbers || numsJson;
check('main: corpus table renders one row per number (' + numsRows.length + ')',
  count(/<tr><td>/g, corpHtml) === numsRows.length, 'got ' + count(/<tr><td>/g, corpHtml));
check('main: corpus table matches JSON values',
  numsRows.every((n) => corpHtml.includes(Number(n.value).toLocaleString('en-US'))),
  'checked ' + numsRows.length + ' values');
check('main: corpus table header is number | count | counting rule',
  corpHtml.includes('<th>Number</th><th>Count</th><th>Counting rule</th>'));
if (main.data.corpus_numbers_sample)
  check('main: SAMPLE corpus numbers flagged in-page (not silent)',
    corpHtml.includes('Sample data'), 'sample flag present in data.js');

// Verified counts table — the core guarantee
check('main: verified table renders exactly 37 rows', count(/<tr class="frow">/g, vHtml()) === 37,
  'got ' + count(/<tr class="frow">/g, vHtml()));
check('main: all 37 rows are Confirmed badges', count(/badge ok/g, vHtml()) === 37,
  'got ' + count(/badge ok/g, vHtml()));
check('main: ZERO differs rows', count(/badge bad/g, vHtml()) === 0, 'got ' + count(/badge bad/g, vHtml()));
check('main: ZERO cannot_verify rows', count(/badge warn/g, vHtml()) === 0, 'got ' + count(/badge warn/g, vHtml()));
const unvClaims = unverified.map((f) => f.claim);
check('main: no unverified claim text appears in verified table',
  !unvClaims.some((c) => vHtml().includes(c)), 'checked ' + unvClaims.length + ' claims');
check('main: verified tally 37 — 16 scholarly · 21 popular',
  (main.els['verified-tally'] || {}).textContent ===
  '37 verified findings — 16 scholarly · 21 popular. Showing 37.',
  (main.els['verified-tally'] || {}).textContent);
check('main: method block (collapsed) on all 37 verified rows',
  count(/Method &amp; where it occurs/g, vHtml()) === 37, 'got ' + count(/Method &amp; where it occurs/g, vHtml()));
check('main: allah locations render (1821 verses)', vHtml().includes('Locations (1821 verses)'));
check('main: no "location data not loaded" fallback', !vHtml().includes('location data not loaded'));
check('main: assumption labels render (A1–A7)', /A\d/.test(vHtml()) && vHtml().includes('assume-label'));
check('main: header tally line says verified-only + separate page',
  (main.els['tally-line'] || {}).textContent.includes('verified counts only') &&
  (main.els['tally-line'] || {}).textContent.includes('separate page'),
  (main.els['tally-line'] || {}).textContent);
check('main: hero stats show 37 verified counts',
  (main.els['stats'] || {}).innerHTML.includes('37') && (main.els['stats'] || {}).innerHTML.includes('verified counts'));
check('main: pairs render 13 pair cards', count(/<article class="pair">/g, main.els['pairs-list'].innerHTML) === 13,
  'got ' + count(/<article class="pair">/g, main.els['pairs-list'].innerHTML));
check('main: extras render 10 single counts', count(/class="extra"/g, main.els['extras-list'].innerHTML) === 10,
  'got ' + count(/class="extra"/g, main.els['extras-list'].innerHTML));
check('main: names render 99 name cards', count(/class="name-card/g, main.els['names-list'].innerHTML) === 99,
  'got ' + count(/class="name-card/g, main.els['names-list'].innerHTML));
check('main: graph detail placeholder intact',
  main.els['graph-detail'] && main.els['graph-detail'].textContent.includes('Select a Name'));
check('main: assumption sets table renders in methodology',
  main.els['assumption-table'] && main.els['assumption-table'].innerHTML.includes('<table'));

// Static HTML checks for the main page
const indexHtml = fs.readFileSync('web/index.html', 'utf8');
check('main html: link to unverified.html present', indexHtml.includes('href="unverified.html"'));
check('main html: sections in order About → Corpus → Verified → Pairs → Names → Method',
  ['id="about"', 'id="corpus"', 'id="verified"', 'id="pairs"', 'id="names"', 'id="method"']
    .every((s, i, a) => i === 0 || indexHtml.indexOf(s) > indexHtml.indexOf(a[i - 1])));
check('main html: old Scholar/Popular tabs gone',
  !indexHtml.includes('id="tab-findings"') && !indexHtml.includes('id="tab-popular"') &&
  !indexHtml.includes('finding-search') && !indexHtml.includes('popular-search'));
check('main html: no status filter on verified table',
  !indexHtml.includes('verified-status') && !indexHtml.includes('id="finding-status"'));

// Filter tests on the verified table
function resetMain() {
  main.els['verified-search'].value = ''; main.els['verified-cat'].value = 'all';
  main.els['verified-search']._fire('input');
}
resetMain();
main.els['verified-search'].value = 'dunya';
main.els['verified-search']._fire('input');
check('main filter: "dunya" narrows verified table',
  count(/<tr class="frow">/g, vHtml()) >= 1 && count(/<tr class="frow">/g, vHtml()) < 37,
  'got ' + count(/<tr class="frow">/g, vHtml()) + ' rows');
resetMain();
main.els['verified-cat'].value = 'code19';
main.els['verified-cat']._fire('change');
const code19Expected = confirmed.filter((f) => f.category === 'code19').length;
check('main filter: code19 shows ' + code19Expected + ' verified rows',
  count(/<tr class="frow">/g, vHtml()) === code19Expected, 'got ' + count(/<tr class="frow">/g, vHtml()));
resetMain();
check('main filter: reset restores 37 rows', count(/<tr class="frow">/g, vHtml()) === 37);

/* ================= UNVERIFIED PAGE ================= */
console.log('\n--- unverified page (unverified.html) ---');
const unv = runPage(UNV_IDS);
const uHtml = () => (unv.els['unverified-list'] ? unv.els['unverified-list'].innerHTML : '');
check('unverified: no load errors', unv.errors.length === 0, unv.errors.join(' | '));
check('unverified: renders exactly 27 rows', count(/<tr class="frow">/g, uHtml()) === 27,
  'got ' + count(/<tr class="frow">/g, uHtml()));
check('unverified: 17 differs badges', count(/badge bad/g, uHtml()) === 17, 'got ' + count(/badge bad/g, uHtml()));
check('unverified: 10 cannot_verify badges', count(/badge warn/g, uHtml()) === 10, 'got ' + count(/badge warn/g, uHtml()));
check('unverified: ZERO confirmed badges', count(/badge ok/g, uHtml()) === 0, 'got ' + count(/badge ok/g, uHtml()));
check('unverified: Scholar group header (19 unverified)',
  uHtml().includes('Scholar findings — 19 unverified'), 'header present');
check('unverified: Popular group header (8 unverified)',
  uHtml().includes('Popular claims — 8 unverified'), 'header present');
check('unverified: mind-light-49 present as differs',
  uHtml().includes('mind-light') || uHtml().includes('light') && uHtml().includes('49'));
check('unverified: benefit-corrupt-50 still differs (flip NOT applied)',
  (() => {
    const f = findings.find((x) => x.id === 'benefit-corrupt-50');
    return f && f.our_status === 'differs' && uHtml().includes(f.claim);
  })());
check('unverified: tally 27 — 17 differ · 10 cannot verify',
  (unv.els['unverified-tally'] || {}).textContent ===
  '27 unverified claims — 17 differ from our recount · 10 cannot verify. Showing 27.',
  (unv.els['unverified-tally'] || {}).textContent);
check('unverified: method block (collapsed) on all 27 rows',
  count(/Method &amp; where it occurs/g, uHtml()) === 27, 'got ' + count(/Method &amp; where it occurs/g, uHtml()));
check('unverified: no "location data not loaded" fallback', !uHtml().includes('location data not loaded'));
check('unverified: no confirmed claim text appears',
  !confirmed.some((f) => uHtml().includes(f.claim)), 'checked ' + confirmed.length + ' claims');

const unvHtml = fs.readFileSync('web/unverified.html', 'utf8');
check('unverified html: "Not verified" banner present', unvHtml.includes('Not verified'));
check('unverified html: back-link to index.html present', unvHtml.includes('href="index.html"'));
check('unverified html: loads same data.js + locations.js + app.js',
  unvHtml.includes('src="data.js"') && unvHtml.includes('src="locations.js"') && unvHtml.includes('src="app.js"'));
check('unverified html: status filter (differs vs cannot_verify) present',
  unvHtml.includes('id="unverified-status"') && unvHtml.includes('value="differs"') &&
  unvHtml.includes('value="cannot_verify"'));

// Filter tests on the unverified page
function resetUnv() {
  unv.els['unverified-search'].value = ''; unv.els['unverified-cat'].value = 'all';
  unv.els['unverified-status'].value = 'all';
  unv.els['unverified-search']._fire('input');
}
resetUnv();
unv.els['unverified-status'].value = 'differs';
unv.els['unverified-status']._fire('change');
check('unverified filter: status differs shows 17 rows',
  count(/<tr class="frow">/g, uHtml()) === 17, 'got ' + count(/<tr class="frow">/g, uHtml()));
resetUnv();
unv.els['unverified-status'].value = 'cannot_verify';
unv.els['unverified-status']._fire('change');
check('unverified filter: status cannot_verify shows 10 rows',
  count(/<tr class="frow">/g, uHtml()) === 10, 'got ' + count(/<tr class="frow">/g, uHtml()));
resetUnv();
unv.els['unverified-search'].value = 'sea';
unv.els['unverified-search']._fire('input');
check('unverified filter: "sea" narrows table',
  count(/<tr class="frow">/g, uHtml()) >= 1 && count(/<tr class="frow">/g, uHtml()) < 27,
  'got ' + count(/<tr class="frow">/g, uHtml()) + ' rows');
resetUnv();
check('unverified filter: reset restores 27 rows', count(/<tr class="frow">/g, uHtml()) === 27);

const failed = checks.filter((c) => !c[1]);
console.log('\n' + (failed.length === 0 ? 'ALL CHECKS PASSED (' + checks.length + ')' : 'FAILURES: ' + failed.length + ' of ' + checks.length));
if (main.data.quran_facts_sample || main.data.corpus_numbers_sample)
  console.log('NOTE: facts/corpus tables currently use SAMPLE data (Agent A files not landed) — replace data/quran_facts.json and data/corpus_numbers.json with Agent A\'s files and re-run build.py + this verifier before any push.');
process.exit(failed.length === 0 ? 0 : 1);

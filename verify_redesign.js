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
  'surah-search', 'surah-type', 'surahs-list', 'surahs-tally', 'surahs-totals',
  'assumption-table', 'pair-search', 'pair-equal-only', 'pairs-list', 'extras-list',
  'name-search', 'name-filter', 'graph-scope', 'graph-edges', 'graph', 'graph-detail',
  'names-list', 'name-detail', 'more-names', 'verified-search', 'verified-cat', 'verified-tally',
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

// Surahs section (2026-11-09): renders from data/surahs.json when present,
// degrades to a "list coming" note when absent — never a crash.
const surahsJsonPath = 'data/surahs.json';
const surahsExist = fs.existsSync(surahsJsonPath);
const surahsHtml = main.els['surahs-list'] ? main.els['surahs-list'].innerHTML : '';
if (surahsExist) {
  const sj = JSON.parse(fs.readFileSync(surahsJsonPath, 'utf8'));
  const sRows = Array.isArray(sj) ? sj : (sj.surahs || []);
  check('main: surahs payload = 114 rows', (main.data.surahs || []).length === 114,
    'got ' + (main.data.surahs || []).length);
  check('main: surah table renders 114 rows', count(/<tr><td><b>/g, surahsHtml) === 114,
    'got ' + count(/<tr><td><b>/g, surahsHtml));
  check('main: surah verse counts match data/surahs.json',
    sRows.every((s) => surahsHtml.includes('<b>' + s.verses + '</b>') || surahsHtml.includes('>' + s.verses + '<')),
    'checked ' + sRows.length + ' verse counts');
  check('main: every surah row has a Recite link to quran.com/<n>',
    count(/href="https:\/\/quran\.com\/\d+"/g, surahsHtml) === 114,
    'got ' + count(/href="https:\/\/quran\.com\/\d+"/g, surahsHtml));
  check('main: every surah row shows Meccan or Medinan tag',
    count(/type-tag/g, surahsHtml) === 114, 'got ' + count(/type-tag/g, surahsHtml));
  const facts604 = (JSON.parse(fs.readFileSync('data/quran_facts.json', 'utf8')).facts || [])
    .some((f) => /604/.test(String(f.value || '')));
  check('main: surah totals line shows 114 surahs · 30 juz' + (facts604 ? ' · 604 pages' : ''),
    (main.els['surahs-totals'] || {}).textContent ===
    (facts604 ? '114 surahs · 30 juz · 604 pages' : '114 surahs · 30 juz'),
    (main.els['surahs-totals'] || {}).textContent);
  check('main: surah tally says Showing 114 of 114 surahs',
    (main.els['surahs-tally'] || {}).textContent === 'Showing 114 of 114 surahs.',
    (main.els['surahs-tally'] || {}).textContent);
  // Search + filter behaviour on the surah table
  function resetSurahs() {
    main.els['surah-search'].value = ''; main.els['surah-type'].value = 'all';
    main.els['surah-search']._fire('input');
  }
  resetSurahs();
  main.els['surah-search'].value = 'yasin';
  main.els['surah-search']._fire('input');
  check('main surah filter: "yasin" narrows to 1 row',
    count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML) === 1,
    'got ' + count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML));
  resetSurahs();
  main.els['surah-search'].value = '36';
  main.els['surah-search']._fire('input');
  check('main surah filter: number "36" finds Yâsîn',
    main.els['surahs-list'].innerHTML.includes('Yâsîn') &&
    count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML) === 1,
    'got ' + count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML));
  resetSurahs();
  main.els['surah-type'].value = 'Meccan';
  main.els['surah-type']._fire('change');
  const meccanExpected = sRows.filter((s) => s.type === 'Meccan').length;
  check('main surah filter: Meccan shows ' + meccanExpected + ' rows',
    count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML) === meccanExpected,
    'got ' + count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML));
  resetSurahs();
  main.els['surah-type'].value = 'Medinan';
  main.els['surah-type']._fire('change');
  const medinanExpected = sRows.filter((s) => s.type === 'Medinan').length;
  check('main surah filter: Medinan shows ' + medinanExpected + ' rows',
    count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML) === medinanExpected,
    'got ' + count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML));
  resetSurahs();
  check('main surah filter: reset restores 114 rows',
    count(/<tr><td><b>/g, main.els['surahs-list'].innerHTML) === 114);
} else {
  check('main: surahs.json absent — payload falls back to empty array',
    Array.isArray(main.data.surahs) && main.data.surahs.length === 0);
  check('main: surahs.json absent — "list coming" note renders, no crash',
    surahsHtml.includes('being verified') && !surahsHtml.includes('<table'));
  console.log('NOTE: data/surahs.json not present — surah rows will appear after ' +
    "Agent A's file lands and build.py is re-run.");
}

// "More than 99" note (2026-11-09): renders only when data/more_names.json exists.
const moreJsonPath = 'data/more_names.json';
const moreExist = fs.existsSync(moreJsonPath);
const moreHtml = main.els['more-names'] ? main.els['more-names'].innerHTML : '';
if (moreExist) {
  const mj = JSON.parse(fs.readFileSync(moreJsonPath, 'utf8'));
  const mRows = Array.isArray(mj) ? mj : (mj.verified_additional || mj.more_names || mj.names || []);
  check('main: more_names payload = ' + mRows.length + ' rows',
    (main.data.more_names || []).length === mRows.length,
    'got ' + (main.data.more_names || []).length);
  check('main: "More than 99" note renders with Arabic + verse refs',
    moreHtml.includes('More than 99') &&
    mRows.every((m) => moreHtml.includes(m.arabic_printed || m.arabic || m.name_ar || m.name || '∅') ||
      moreHtml.includes(m.transliteration || '')),
    'checked ' + mRows.length + ' entries');
  check('main: "More than 99" note lists each entry\'s verse refs',
    mRows.every((m) => (m.verses || []).every((v) => moreHtml.includes(v))),
    'checked ' + mRows.length + ' entries');
} else {
  check('main: more_names.json absent — payload falls back to empty array, note hidden',
    Array.isArray(main.data.more_names) && main.data.more_names.length === 0 && moreHtml === '');
  console.log('NOTE: data/more_names.json not present — "More than 99" note will ' +
    "appear after Agent A's file lands and build.py is re-run.");
}

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
check('main html: humble intro above About the Quran (2–3 sentences)',
  indexHtml.indexOf('class="intro"') > indexHtml.indexOf('<main>') &&
  indexHtml.indexOf('class="intro"') < indexHtml.indexOf('id="about"') &&
  indexHtml.replace(/\s+/g, ' ').includes('humble attempt') &&
  indexHtml.replace(/\s+/g, ' ').includes('not a claim of authority'));
check('main html: surah section sits between corpus and verified',
  indexHtml.indexOf('id="surahs"') > indexHtml.indexOf('id="corpus"') &&
  indexHtml.indexOf('id="surahs"') < indexHtml.indexOf('id="verified"'));
check('main html: surah search + Meccan/Medinan filter present',
  indexHtml.includes('id="surah-search"') && indexHtml.includes('id="surah-type"') &&
  indexHtml.includes('value="Meccan"') && indexHtml.includes('value="Medinan"'));
check('main html: Names reframe — hadith cited, 99 not a ceiling',
  indexHtml.includes('Sahih al-Bukhari 7392') && indexHtml.includes('Sahih Muslim 2677') &&
  indexHtml.includes('not a ceiling') && indexHtml.includes('more names and attributes') &&
  indexHtml.includes('id="more-names"'));
check('mizan: title, logo + favicon, Why Mizan section before About',
  indexHtml.includes('<title>Mizan — The Quran in numbers</title>') &&
  indexHtml.includes('src="images/mizan-logo.png"') &&
  indexHtml.includes('href="images/mizan-favicon.png"') &&
  indexHtml.includes('id="why-mizan"') &&
  indexHtml.indexOf('id="why-mizan"') < indexHtml.indexOf('id="about"'));
check('mizan: 7 highlight rows with Tanzil Arabic + verse links',
  ['55:7–9', '57:25', '42:17', '21:47', '101:6–9', '17:35', '15:19']
    .every(r => indexHtml.includes('>' + r + '</a>')) &&
  indexHtml.includes('ٱلْمِيزَانَ') && indexHtml.includes('occurs in 9 verses') &&
  indexHtml.includes('quran.com/55/7') && indexHtml.includes('quran.com/101/6'));
check('mizan: no miracleMath display text left (repo URLs excepted)',
  !indexHtml.replace(/github\.com\/mindsyourai\/miracleMath/g, '').includes('miracleMath'));

// Recolor checks: light palette on both pages (shared styles.css), no dark-theme leftovers.
const css = fs.readFileSync('web/styles.css', 'utf8');
check('recolor: light beige background + gold-brown accents in palette',
  css.includes('--bg:#f7f2e8') && css.includes('--gold:#8a6d1f') && css.includes('--green:#166b2d'));
check('recolor: no leftover dark-theme background colors',
  !css.includes('#0b1220') && !css.includes('#0e1729') && !css.includes('#111c31') &&
  !css.includes('#0d1526') && !css.includes('#e8eef7') && !css.includes('#22d3ee'));
check('recolor: scroll-padding-top layout fix kept (124px, clears two-row sticky nav)',
  css.includes('scroll-padding-top:124px') && css.includes('scroll-margin-top:124px'));
check('recolor: .table-scroll overflow-x fix kept', css.includes('.table-scroll{overflow-x:auto}'));
const appJs = fs.readFileSync('web/app.js', 'utf8');
check('recolor: graph label colors are light-theme (dark ink on light canvas)',
  appJs.includes('"#2b2118"') && !appJs.includes('#e8eef7') && !appJs.includes('#22d3ee'));
check('recolor: graph geometry code untouched (radius + label clamping intact)',
  appJs.includes('Math.min(W, H) / 2 - 70 - maxR - 16') &&
  appJs.includes('Math.min(ox, W - tw - 6)') && appJs.includes('Math.max(ox, tw + 6)'));

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
const unvHtmlRaw = fs.readFileSync('web/unverified.html', 'utf8');
check('unverified: Mizan title + favicon, no miracleMath display text',
  unvHtmlRaw.includes('<title>Unverified claims — Mizan</title>') &&
  unvHtmlRaw.includes('href="images/mizan-favicon.png"') &&
  !unvHtmlRaw.replace(/github\.com\/mindsyourai\/miracleMath/g, '').includes('miracleMath'));
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

/* Cold-load stub test for miracleMath: loads web/data.js + web/locations.js +
   web/app.js in a minimal fake DOM and asserts the findings render correctly
   as data tables. Usage: node verify_coldload.js [data.js path] [locations.js path]
   Defaults: web/data.js, web/locations.js. Pass a mock data.js (with the
   "assumptions" field + assumption_sets) to test the assumptions rendering. */
const vm = require('vm');
const fs = require('fs');

const dataFile = process.argv[2] || 'web/data.js';
const locFile = process.argv[3] || 'web/locations.js';

class El {
  constructor(id) {
    this.id = id;
    this.innerHTML = '';
    this.textContent = '';
    // search inputs start empty; selects start on "all" (no filter)
    this.value = /-search$/.test(id) ? '' : 'all';
    this.classList = { add() {}, remove() {}, toggle() {} };
    this.style = {};
    this.width = 800;
    this.height = 600;
    this._listeners = {};
  }
  addEventListener(type, fn) {
    (this._listeners[type] = this._listeners[type] || []).push(fn);
  }
  _fire(type, ev) {
    (this._listeners[type] || []).forEach((fn) => fn(ev || {}));
  }
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
}
const els = {};
const document = {
  getElementById: (id) => { if (!els[id]) els[id] = new El(id); return els[id]; },
  querySelectorAll: () => [],
};
// Static HTML already carries the graph placeholder text; seed it like the
// real page does so drawGraph() must not clobber it.
els['graph-detail'] = new El('graph-detail');
els['graph-detail'].textContent = 'Select a Name in the graph to see its strongest partners.';
const windowObj = {};
const sandbox = { window: windowObj, document, console };
vm.createContext(sandbox);

const errors = [];
try {
  for (const f of [dataFile, locFile, 'web/app.js']) {
    vm.runInContext(fs.readFileSync(f, 'utf8'), sandbox, { filename: f });
  }
} catch (e) {
  errors.push('LOAD ERROR: ' + e.stack);
}

function count(re, s) { return (s.match(re) || []).length; }
function stripTags(s) { return s.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim(); }
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok, detail || '']);
  console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (detail ? '  (' + detail + ')' : ''));
}

const findingsHtml = () => els['findings-list'] ? els['findings-list'].innerHTML : '';
const popularHtml = () => els['popular-list'] ? els['popular-list'].innerHTML : '';
const data = windowObj.MIRACLE_DATA || {};
const hasAssumptions = (data.findings || []).some((f) => f.assumptions);
console.log('data file: ' + dataFile + ' | findings with assumptions field: ' +
  (data.findings || []).filter((f) => f.assumptions).length + ' | assumption_sets: ' +
  (data.assumption_sets || []).length);

check('no load errors', errors.length === 0, errors.join(' | '));
check('MIRACLE_DATA findings = 64', data.findings && data.findings.length === 64);
check('MIRACLE_LOCATIONS entries = 64',
  windowObj.MIRACLE_LOCATIONS && Object.keys(windowObj.MIRACLE_LOCATIONS).length === 64);
check('scholarly table renders 35 rows', count(/<tr class="frow">/g, findingsHtml()) === 35,
  'got ' + count(/<tr class="frow">/g, findingsHtml()));
check('popular table renders 29 rows', count(/<tr class="frow">/g, popularHtml()) === 29,
  'got ' + count(/<tr class="frow">/g, popularHtml()));
check('findings table has 6 columns',
  findingsHtml().includes("<th>Claim</th><th>Scholar's number</th><th>Our number</th><th>Assumption</th><th>Verdict</th><th>Source</th>"));
const st = els['finding-tally'] ? els['finding-tally'].textContent : '';
check('scholarly tally 16/10/9 + overall 37/17/10',
  st.includes('35 findings in this section — 16 confirmed by our recount · 10 differ from our recount · 9 cannot verify') &&
  st.includes('37 confirmed · 17 differ · 10 cannot verify'), st);
const pt = els['popular-tally'] ? els['popular-tally'].textContent : '';
check('popular tally 21/7/1',
  pt.includes('29 findings in this section — 21 confirmed by our recount · 7 differ from our recount · 1 cannot verify'), pt);
const methodBlocks = count(/Method &amp; where it occurs/g, findingsHtml() + popularHtml());
check('method block (collapsed) on all 64 findings', methodBlocks === 64, 'got ' + methodBlocks);
check('allah locations render (1821 verses)', findingsHtml().includes('Locations (1821 verses)'));
check('dunya-akhira locations render', findingsHtml().includes('Locations (') && findingsHtml().includes('2:25'));
check('sea-land scholar-rule verse 5:96 renders', popularHtml().includes('5:96'));
check('no "location data not loaded" fallback rendered',
  !(findingsHtml() + popularHtml()).includes('location data not loaded'));
check('hero stats show 64 findings reviewed',
  els['stats'] && els['stats'].innerHTML.includes('64') && els['stats'].innerHTML.includes('findings reviewed'));
check('header tally line shows 37/17/10',
  els['tally-line'] && els['tally-line'].textContent.includes('37 confirmed') &&
  els['tally-line'].textContent.includes('17 differ') &&
  els['tally-line'].textContent.includes('10 cannot verify'));
check('pairs render 13 pair cards', count(/<article class="pair">/g, els['pairs-list'].innerHTML) === 13,
  'got ' + count(/<article class="pair">/g, els['pairs-list'].innerHTML));
check('extras render 10 single counts', count(/class="extra"/g, els['extras-list'].innerHTML) === 10,
  'got ' + count(/class="extra"/g, els['extras-list'].innerHTML));
check('names render 99 name cards', count(/class="name-card/g, els['names-list'].innerHTML) === 99,
  'got ' + count(/class="name-card/g, els['names-list'].innerHTML));
check('graph detail placeholder set',
  els['graph-detail'] && els['graph-detail'].textContent.includes('Select a Name'));
if (hasAssumptions) {
  check('assumption labels render (with assumptions field)',
    findingsHtml().includes('assume-label') && /A\d/.test(findingsHtml() + popularHtml()));
  check('assumption reasons render',
    count(/class="reason"/g, findingsHtml() + popularHtml()) >= 60,
    'got ' + count(/class="reason"/g, findingsHtml() + popularHtml()));
  check('assumption sets table renders in methodology',
    els['assumption-table'] && els['assumption-table'].innerHTML.includes('<table'));
} else {
  check('fallback: method-status labels render (no assumptions field yet)',
    findingsHtml().includes('Method: reconstructed') || findingsHtml().includes('Method: stated'));
  check('fallback: shortened our_note reason lines render',
    count(/class="reason"/g, findingsHtml() + popularHtml()) >= 60,
    'got ' + count(/class="reason"/g, findingsHtml() + popularHtml()));
  check('fallback: assumption-table placeholder note renders',
    els['assumption-table'] && els['assumption-table'].innerHTML.includes('not yet in the data payload'));
}
// No full our_note prose on the page: the longest our_note is 1243 chars;
// no rendered reason line should exceed ~200 chars, and no finding's full
// our_note should appear verbatim.
const allText = stripTags(findingsHtml() + popularHtml());
const longestNote = (data.findings || []).reduce((m, f) => Math.max(m, (f.our_note || '').length), 0);
check('no full our_note prose on page (longest note ' + longestNote + ' chars, none verbatim)',
  !(data.findings || []).some((f) => f.our_note && f.our_note.length > 200 && allText.includes(f.our_note)));

/* ---------- filter tests (dispatch stub events) ---------- */
function resetFilters() {
  els['finding-search'].value = ''; els['finding-cat'].value = 'all'; els['finding-status'].value = 'all';
  els['popular-search'].value = ''; els['popular-cat'].value = 'all'; els['popular-status'].value = 'all';
  els['finding-search']._fire('input');
  els['popular-search']._fire('input');
}
resetFilters();
els['finding-search'].value = 'dunya';
els['finding-search']._fire('input');
check('search filter: "dunya" narrows scholarly tab',
  count(/<tr class="frow">/g, findingsHtml()) >= 1 &&
  count(/<tr class="frow">/g, findingsHtml()) < 35,
  'got ' + count(/<tr class="frow">/g, findingsHtml()) + ' rows');
resetFilters();
els['finding-status'].value = 'confirmed';
els['finding-status']._fire('change');
check('status filter: confirmed shows 16 scholarly rows',
  count(/<tr class="frow">/g, findingsHtml()) === 16,
  'got ' + count(/<tr class="frow">/g, findingsHtml()));
resetFilters();
els['finding-cat'].value = 'code19';
els['finding-cat']._fire('change');
const code19Rows = count(/<tr class="frow">/g, findingsHtml());
const code19Expected = (data.findings || []).filter((f) => f.section === 'scholarly' && f.category === 'code19').length;
check('category filter: code19 shows ' + code19Expected + ' scholarly rows',
  code19Rows === code19Expected, 'got ' + code19Rows);
resetFilters();
els['popular-search'].value = 'sea';
els['popular-search']._fire('input');
check('search filter works on popular tab too',
  count(/<tr class="frow">/g, popularHtml()) >= 1 &&
  count(/<tr class="frow">/g, popularHtml()) < 29,
  'got ' + count(/<tr class="frow">/g, popularHtml()) + ' rows');
resetFilters();
check('filters reset restores 35/29 rows',
  count(/<tr class="frow">/g, findingsHtml()) === 35 &&
  count(/<tr class="frow">/g, popularHtml()) === 29);

/* dump rendered output for spot-checking */
fs.writeFileSync('/tmp/mm-findings-rendered.html', findingsHtml());
fs.writeFileSync('/tmp/mm-popular-rendered.html', popularHtml());

const failed = checks.filter((c) => !c[1]);
console.log(failed.length === 0 && errors.length === 0 ? 'ALL CHECKS PASSED' : 'FAILURES: ' + failed.length);
process.exit(failed.length === 0 && errors.length === 0 ? 0 : 1);

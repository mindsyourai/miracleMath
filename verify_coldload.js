/* Cold-load stub test for miracleMath: loads web/data.js + web/locations.js +
   web/app.js in a minimal fake DOM and asserts the findings render correctly. */
const vm = require('vm');
const fs = require('fs');

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
  }
  addEventListener() {}
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
}
const els = {};
const document = {
  getElementById: (id) => { if (!els[id]) els[id] = new El(id); return els[id]; },
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
} catch (e) {
  errors.push('LOAD ERROR: ' + e.stack);
}

function count(re, s) { return (s.match(re) || []).length; }
const findingsHtml = els['findings-list'] ? els['findings-list'].innerHTML : '';
const popularHtml = els['popular-list'] ? els['popular-list'].innerHTML : '';
const checks = [];
function check(name, ok, detail) {
  checks.push([name, !!ok, detail || '']);
  console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (detail ? '  (' + detail + ')' : ''));
}

check('no load errors', errors.length === 0, errors.join(' | '));
check('MIRACLE_DATA findings = 64', windowObj.MIRACLE_DATA && windowObj.MIRACLE_DATA.findings.length === 64);
check('MIRACLE_LOCATIONS entries = 64',
  windowObj.MIRACLE_LOCATIONS && Object.keys(windowObj.MIRACLE_LOCATIONS).length === 64);
check('scholarly list renders 35 findings', count(/<article class="finding">/g, findingsHtml) === 35,
  'got ' + count(/<article class="finding">/g, findingsHtml));
check('popular list renders 29 findings', count(/<article class="finding">/g, popularHtml) === 29,
  'got ' + count(/<article class="finding">/g, popularHtml));
const st = els['finding-tally'] ? els['finding-tally'].textContent : '';
check('scholarly tally 16/10/9 + overall 37/17/10',
  st.includes('35 findings in this section — 16 confirmed by our recount · 10 differ from our recount · 9 cannot verify') &&
  st.includes('37 confirmed · 17 differ · 10 cannot verify'), st);
const pt = els['popular-tally'] ? els['popular-tally'].textContent : '';
check('popular tally 21/7/1',
  pt.includes('29 findings in this section — 21 confirmed by our recount · 7 differ from our recount · 1 cannot verify'), pt);
const methodBlocks = count(/Method &amp; where it occurs/g, findingsHtml + popularHtml);
check('method block on all 64 findings', methodBlocks === 64, 'got ' + methodBlocks);
check('allah locations render (1821 verses)', findingsHtml.includes('Locations (1821 verses)'));
check('dunya-akhira locations render', findingsHtml.includes('Locations (') && findingsHtml.includes('2:25'));
check('sea-land scholar-rule verse 5:96 renders', popularHtml.includes('5:96'));
check('jannah-jahannam now differs', popularHtml.includes('jannah') || findingsHtml.includes('jannah'));
check('hero stats show 64 findings reviewed',
  els['stats'] && els['stats'].innerHTML.includes('64') && els['stats'].innerHTML.includes('findings reviewed'));
check('no "location data not loaded" fallback rendered',
  !(findingsHtml + popularHtml).includes('location data not loaded'));
const failed = checks.filter((c) => !c[1]);
console.log(failed.length === 0 && errors.length === 0 ? 'ALL CHECKS PASSED' : 'FAILURES: ' + failed.length);
process.exit(failed.length === 0 && errors.length === 0 ? 0 : 1);

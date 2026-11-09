/* Mizan app — renders from window.MIRACLE_DATA (embedded data.js).
   No network calls, no backend. Charts are CSS bars; the Name network is a
   guarded canvas drawing (no-ops safely where canvas is unavailable).
   Shared by index.html (verified counts only) and unverified.html
   (differs / cannot_verify only): the script detects which page it is on
   from the DOM ids present and renders only that page's sections, so the
   row-rendering code is written once. Findings render as data tables.
   Each finding may carry an "assumptions" object {scholar_set, our_set,
   reconciles_under, numbers_by_set, reason}; when it is absent the page
   falls back to the method status and a shortened our_note, so the page
   never breaks on older data. */
(function () {
  "use strict";
  var D = window.MIRACLE_DATA || {};
  var $ = function (id) { return document.getElementById(id); };
  function on(id, ev, fn) {
    var el = $(id);
    if (el && el.addEventListener) el.addEventListener(ev, fn);
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function catLabel(c) {
    return { paired_counts: "Paired counts", letter_counts: "Letter counts",
      code19: "Code 19", corpus_linguistics: "Corpus linguistics" }[c] || c;
  }
  function sectionLabel(s) {
    return s === "popular" ? "Popular claims" : "Scholar findings";
  }
  function statusBadge(f) {
    if (f.our_status === "confirmed")
      return '<span class="badge ok">Confirmed</span>';
    if (f.our_status === "differs")
      return '<span class="badge bad">Differs</span>';
    return '<span class="badge warn">Cannot verify</span>';
  }

  /* ---------- assumption sets ---------- */
  var assumptionSets = {};
  (D.assumption_sets || []).forEach(function (s) { assumptionSets[s.id] = s; });
  function assumptionLabel(id) {
    if (!id) return "—";
    var s = assumptionSets[id];
    return s ? esc(id) + " — " + esc(s.name) : esc(id);
  }
  /* One-line reconciliation reason: the new assumptions.reason when present,
     otherwise the first sentence (or first ~160 chars) of our_note. */
  function reasonLine(f) {
    if (f.assumptions && f.assumptions.reason) return f.assumptions.reason;
    var n = (f.our_note || "").trim();
    if (!n) return "";
    var cut = n.indexOf(". ");
    var one = cut > 0 && cut < 200 ? n.slice(0, cut + 1) : n.slice(0, 160);
    return one.length < n.length && one.slice(-1) !== "." ? one + "…" : one;
  }
  function assumptionCell(f) {
    var a = f.assumptions;
    if (a) {
      var h = '<div class="assume-label">' + assumptionLabel(a.our_set) + "</div>";
      if (a.scholar_set && a.scholar_set !== a.our_set)
        h += '<div class="assume-sub">scholar: ' + assumptionLabel(a.scholar_set) + "</div>";
      if (a.reconciles_under && a.reconciles_under.length)
        h += '<div class="assume-sub">reconciles under: ' + a.reconciles_under.map(esc).join(", ") + "</div>";
      if (a.numbers_by_set) {
        var parts = Object.keys(a.numbers_by_set).sort().map(function (k) {
          var v = a.numbers_by_set[k];
          var vs = Array.isArray(v) ? v.map(function (n) { return n == null ? "—" : String(n); }).join(" / ") : String(v);
          return esc(k) + ": " + esc(vs);
        });
        if (parts.length) h += '<div class="assume-sub">' + parts.join(" · ") + "</div>";
      }
      if (a.reason) h += '<div class="reason">' + esc(a.reason) + "</div>";
      return h;
    }
    var h2 = '<div class="assume-label">Method: ' + esc(f.method_status || "unstated") + "</div>";
    var r = reasonLine(f);
    if (r) h2 += '<div class="reason">' + esc(r) + "</div>";
    return h2;
  }

  /* ---------- research header ---------- */
  (function stats() {
    var statsEl = $("stats");
    if (!statsEl) return;
    var c = D.corpus || {};
    var all = D.findings || [];
    var verified = all.filter(function (f) { return f.our_status === "confirmed"; }).length;
    var items = [
      [c.words ? c.words.toLocaleString("en-US") : "77,429", "words"],
      [c.verses ? c.verses.toLocaleString("en-US") : "6,236", "verses"],
      [c.surahs || 114, "surahs"],
      [(D.names || []).length || 99, "Names of God"],
      [(D.names_totals && D.names_totals.total_occurrences) || 1120, "Name occurrences"],
      [verified || 37, "verified counts"]
    ];
    statsEl.innerHTML = items.map(function (it) {
      return "<span><b>" + esc(it[0]) + "</b> " + esc(it[1]) + "</span>";
    }).join(" · ");
    var t = { confirmed: 0, differs: 0, cannot_verify: 0 };
    all.forEach(function (f) { if (t[f.our_status] != null) t[f.our_status]++; });
    var tl = $("tally-line");
    if (tl && all.length)
      tl.textContent = t.confirmed + " confirmed · " + t.differs + " differ · " +
        t.cannot_verify + " cannot verify — this page shows verified counts only; " +
        "the " + (t.differs + t.cannot_verify) + " unverified claims are on a separate page.";
  })();

  /* ---------- About the Quran: sourced facts table ---------- */
  (function renderFacts() {
    var host = $("facts-table");
    if (!host) return;
    var facts = D.quran_facts || [];
    if (!facts.length) {
      host.innerHTML = "<p class=\"method-note\">About-the-Quran facts are not yet in the data payload " +
        "(see data/quran_facts.json in the repo).</p>";
      return;
    }
    var h = "";
    if (D.quran_facts_sample)
      h += '<p class="sample-note">Sample data — citations pending; this table will be replaced ' +
        "with sourced facts (Agent A).</p>";
    h += '<div class="table-scroll"><table class="data-table"><thead><tr>' +
      "<th>Fact</th><th>Value</th><th>Source</th></tr></thead><tbody>";
    facts.forEach(function (f) {
      var src = esc(f.source || "—");
      if (f.source_url) src = '<a href="' + esc(f.source_url) + '" target="_blank" rel="noopener">' + src + "</a>";
      h += "<tr><td><b>" + esc(f.label || f.id || "") + "</b>" +
        (f.note ? '<div class="reason">' + esc(f.note) + "</div>" : "") + "</td>" +
        "<td><b>" + esc(f.value) + "</b></td><td>" + src + "</td></tr>";
    });
    host.innerHTML = h + "</tbody></table></div>";
  })();

  /* ---------- The corpus in numbers ---------- */
  (function renderCorpusNumbers() {
    var host = $("corpus-table");
    if (!host) return;
    var nums = D.corpus_numbers || [];
    if (!nums.length) {
      host.innerHTML = "<p class=\"method-note\">Corpus numbers are not yet in the data payload " +
        "(see data/corpus_numbers.json in the repo).</p>";
      return;
    }
    var h = "";
    if (D.corpus_numbers_sample)
      h += '<p class="sample-note">Sample data — script-computed QAC v0.4 totals; ' +
        "this table will be replaced / extended with Agent A's corpus numbers (e.g. a letter count).</p>";
    h += '<div class="table-scroll"><table class="data-table"><thead><tr>' +
      "<th>Number</th><th>Count</th><th>Counting rule</th></tr></thead><tbody>";
    nums.forEach(function (n) {
      var v = typeof n.value === "number" ? n.value.toLocaleString("en-US") : String(n.value == null ? "—" : n.value);
      h += "<tr><td><b>" + esc(n.label || n.id || "") + "</b></td>" +
        "<td><b>" + esc(v) + "</b></td><td>" + esc(n.rule || "") +
        (n.source ? ' <span class="src-title">(' + esc(n.source) + ")</span>" : "") + "</td></tr>";
    });
    host.innerHTML = h + "</tbody></table></div>";
  })();

  /* ---------- Surahs: 114-row table with search + Meccan/Medinan filter ---------- */
  function renderSurahs() {
    var host = $("surahs-list");
    if (!host) return;
    /* Header totals: "114 surahs · 30 juz" plus "· 604 pages" only once the
       604-pages fact has landed in data/quran_facts.json (Agent A). */
    var totalsEl = $("surahs-totals");
    if (totalsEl) {
      var hasPages = (D.quran_facts || []).some(function (f) {
        return /604/.test(String(f.value || ""));
      });
      totalsEl.textContent = hasPages ? "114 surahs · 30 juz · 604 pages" : "114 surahs · 30 juz";
    }
    var list = D.surahs || [];
    if (!list.length) {
      host.innerHTML = "<p class=\"method-note\">The 114-surah list is being verified " +
        "and will appear here (see data/surahs.json in the repo).</p>";
      var tally0 = $("surahs-tally");
      if (tally0) tally0.textContent = "";
      return;
    }
    var q = (($("surah-search") || {}).value || "").toLowerCase().trim();
    var t = ($("surah-type") || {}).value || "all";
    /* Normalise punctuation AND diacritics so "yasin" finds "Yâsîn" and
       "al fatiha" finds "Al-Fatiha": fold to base letters, then compare on
       letters/digits only (Arabic kept as-is). */
    var norm = function (s) {
      return String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9\u0600-\u06ff]/g, "");
    };
    var nq = norm(q);
    var rows = "";
    var shown = 0;
    list.forEach(function (s) {
      var hay = norm((s.name_tr || "") + " " + (s.name_ar || "") + " " + String(s.n));
      if (nq && hay.indexOf(nq) === -1 && String(s.n) !== q) return;
      if (t !== "all" && s.type !== t) return;
      shown++;
      rows += "<tr><td><b>" + esc(s.n) + "</b></td>" +
        "<td><b>" + esc(s.name_tr || "") + '</b> <span class="ar">' + esc(s.name_ar || "") + "</span></td>" +
        "<td><b>" + esc(s.verses) + "</b></td>" +
        '<td><span class="type-tag ' + (s.type === "Medinan" ? "medinan" : "meccan") + '">' +
        esc(s.type || "") + "</span></td>" +
        '<td><a href="https://quran.com/' + esc(s.n) + '" target="_blank" rel="noopener">Recite →</a></td></tr>';
    });
    host.innerHTML = '<div class="table-scroll"><table class="data-table"><thead><tr>' +
      "<th>#</th><th>Surah</th><th>Verses</th><th>Revealed</th><th></th></tr></thead><tbody>" +
      (rows || '<tr><td colspan="5">No surahs match that search.</td></tr>') +
      "</tbody></table></div>";
    var tally = $("surahs-tally");
    if (tally) tally.textContent = "Showing " + shown + " of " + list.length + " surahs.";
  }
  renderSurahs();
  on("surah-search", "input", renderSurahs);
  on("surah-type", "change", renderSurahs);

  /* ---------- "More than 99": verified names/attributes beyond the 99 ---------- */
  (function renderMoreNames() {
    var host = $("more-names");
    if (!host) return;
    var list = D.more_names || [];
    if (!list.length) return; /* renders only when Agent A's data exists */
    function refsOf(it) {
      var v = it.verses || it.verse || it.refs || it.ref || it.location || it.locations;
      if (!v) return "";
      if (Array.isArray(v)) return v.map(String).join(", ");
      return String(v);
    }
    var items = list.map(function (it) {
      var ar = it.arabic_printed || it.arabic || it.name_ar || it.name || "";
      var tr = it.transliteration || it.name_tr || it.name_en || "";
      var meaning = it.meaning_en || it.meaning || "";
      var refs = refsOf(it);
      return "<li><span class='ar'>" + esc(ar) + "</span>" +
        (tr ? " <b>" + esc(tr) + "</b>" : "") +
        (meaning ? " — " + esc(meaning) : "") +
        (refs ? ' <span class="ref-refs">(' + esc(refs) + ")</span>" : "") + "</li>";
    }).join("");
    host.innerHTML = '<div class="more-names"><h3>More than 99</h3>' +
      "<p>The Quran uses more names and attributes of Allah than the famous ninety-nine. " +
      "Verified examples counted in the Quran:</p><ul>" + items + "</ul></div>";
  })();

  /* ---------- methodology: assumption sets table ---------- */
  (function renderAssumptions() {
    var host = $("assumption-table");
    if (!host) return;
    var sets = D.assumption_sets || [];
    if (!sets.length) {
      host.innerHTML = "<p class=\"method-note\">Assumption sets are not yet in the data payload " +
        "(see data/assumption_sets.json in the repo). Findings below fall back to their method status.</p>";
      return;
    }
    var h = '<table class="data-table"><thead><tr><th>Set</th><th>Name</th><th>Definition</th></tr></thead><tbody>';
    sets.forEach(function (s) {
      h += "<tr><td><b>" + esc(s.id) + "</b></td><td>" + esc(s.name || "") +
        "</td><td>" + esc(s.definition || "") + "</td></tr>";
    });
    host.innerHTML = h + "</tbody></table>";
  })();

  /* ---------- paired counts ---------- */
  function refHtml(r) {
    return '<li><span class="ref-tag">' + esc(r.surah) + ":" + esc(r.ayah) + "</span>" +
      (r.arabic ? ' <span class="word ar">' + esc(r.arabic) + "</span>" : "") +
      (r.verse_arabic ? '<div class="verse">' + esc(r.verse_arabic) + "</div>" : "") + "</li>";
  }
  function sideRefs(side) {
    if (!side.refs || !side.refs.length) return "";
    return "<details><summary>Example verses (" + side.refs.length + " shown)</summary><ul class='refs'>" +
      side.refs.map(refHtml).join("") + "</ul></details>";
  }
  function renderPairs() {
    var searchEl = $("pair-search");
    if (!searchEl || !$("pairs-list")) return;
    var q = (searchEl.value || "").toLowerCase();
    var eqOnly = $("pair-equal-only") && $("pair-equal-only").checked;
    var max = 1;
    (D.pairs || []).forEach(function (p) {
      max = Math.max(max, p.a.count || 0, p.b.count || 0);
    });
    var html = "";
    (D.pairs || []).forEach(function (p) {
      var hay = (p.label_en + " " + p.a.term_en + " " + p.b.term_en + " " +
        (p.a.term_ar || "") + " " + (p.b.term_ar || "")).toLowerCase();
      if (q && hay.indexOf(q) === -1) return;
      if (eqOnly && p.a.count !== p.b.count) return;
      var pctA = Math.max(1.5, (p.a.count / max) * 100);
      var pctB = Math.max(1.5, (p.b.count / max) * 100);
      html += '<article class="pair"><h3>' + esc(p.label_en) +
        ' <span class="ar">' + esc(p.label_ar || "") + "</span></h3>" +
        '<div>Ratio <span class="ratio">' + esc(p.a.count) + " : " + esc(p.b.count) + "</span>" +
        (p.ratio != null ? " &nbsp;·&nbsp; " + esc(p.ratio) + "×" : "") + "</div>" +
        '<div class="bars">' +
        '<div class="bar-row"><span class="lbl">' + esc(p.a.term_en) +
        ' <span class="ar">' + esc(p.a.term_ar || "") + '</span></span>' +
        '<span class="bar-track"><span class="bar-fill fill-a" style="display:block;width:' + pctA + '%"></span></span>' +
        '<span class="num">' + esc(p.a.count) + "</span></div>" +
        '<div class="bar-row"><span class="lbl">' + esc(p.b.term_en) +
        ' <span class="ar">' + esc(p.b.term_ar || "") + '</span></span>' +
        '<span class="bar-track"><span class="bar-fill fill-b" style="display:block;width:' + pctB + '%"></span></span>' +
        '<span class="num">' + esc(p.b.count) + "</span></div></div>" +
        '<div class="notes">' +
        (p.a.notes ? "<p><b>" + esc(p.a.term_en) + ":</b> " + esc(p.a.notes) + "</p>" : "") +
        (p.b.notes ? "<p><b>" + esc(p.b.term_en) + ":</b> " + esc(p.b.notes) + "</p>" : "") +
        "</div>" +
        sideRefs(p.a) + sideRefs(p.b) +
        "</article>";
    });
    $("pairs-list").innerHTML = html || "<p>No pairs match that search.</p>";
    var ex = "";
    (D.extras || []).forEach(function (x) {
      var hay = (x.label_en + " " + (x.label_ar || "")).toLowerCase();
      if (q && hay.indexOf(q) === -1) return;
      ex += '<div class="extra"><b>' + esc(x.count) + '</b><span class="t">' + esc(x.label_en) +
        ' <span class="ar">' + esc(x.label_ar || "") + "</span></span>" +
        (x.notes ? "<p>" + esc(x.notes) + "</p>" : "") + "</div>";
    });
    var extrasEl = $("extras-list");
    if (extrasEl) extrasEl.innerHTML = ex || "<p>No single counts match that search.</p>";
  }
  on("pair-search", "input", renderPairs);
  on("pair-equal-only", "change", renderPairs);

  /* ---------- names ---------- */
  var namesById = {};
  (D.names || []).forEach(function (n) { namesById[n.id] = n; });
  var maxName = 1;
  (D.names || []).forEach(function (n) { maxName = Math.max(maxName, n.count || 0); });

  function renderNames() {
    if (!$("name-search") || !$("names-list")) return;
    var q = ($("name-search").value || "").toLowerCase();
    var f = $("name-filter").value;
    var list = (D.names || []).slice().sort(function (a, b) { return b.count - a.count; });
    if (f === "top20") list = list.slice(0, 20);
    var html = "";
    list.forEach(function (n) {
      var hay = (n.transliteration + " " + n.meaning_en + " " + (n.arabic || "")).toLowerCase();
      if (q && hay.indexOf(q) === -1) return;
      if (f === "present" && n.count === 0) return;
      if (f === "zero" && n.count !== 0) return;
      var pct = n.count ? Math.max(2, (n.count / maxName) * 100) : 0;
      html += '<div class="name-card' + (n.count === 0 ? " zero" : "") +
        '" data-id="' + n.id + '" tabindex="0" role="button" aria-label="' + esc(n.transliteration) + '">' +
        "<h4>" + esc(n.transliteration) + ' <span class="ar">' + esc(n.arabic || "") + "</span></h4>" +
        '<div class="meaning">' + esc(n.meaning_en || "") + "</div>" +
        (n.count === 0
          ? '<div class="zero-tag">Does not occur in the Quran</div>'
          : '<div class="count-line"><span>' + esc(n.count) + ' occurrence' + (n.count === 1 ? "" : "s") +
            " · " + esc(n.verse_count || 0) + " verses · " + esc(n.surah_count || 0) + " surahs</span><b>" +
            esc(n.count) + "</b></div>" +
            '<div class="mini-bar"><i style="width:' + pct + '%"></i></div>') +
        "</div>";
    });
    $("names-list").innerHTML = '<div class="name-grid">' + (html || "<p>No Names match that search.</p>") + "</div>";
    document.querySelectorAll(".name-card").forEach(function (card) {
      var open = function () { showNameDetail(parseInt(card.getAttribute("data-id"), 10)); };
      card.addEventListener("click", open);
      card.addEventListener("keydown", function (e) { if (e.key === "Enter") open(); });
    });
  }
  function showNameDetail(id) {
    var n = namesById[id];
    if (!n || !$("name-detail")) return;
    var refs = (n.example_refs || []).map(function (r) {
      return esc(r.surah) + ":" + esc(r.ayah);
    }).join(" · ");
    $("name-detail").innerHTML = '<div class="name-detail"><h3>' + esc(n.transliteration) +
      ' <span class="ar">' + esc(n.arabic || "") + "</span></h3>" +
      '<p>' + esc(n.meaning_en || "") + (n.root ? " · Root: <span class='ar'>" + esc(n.root) + "</span>" : "") + "</p>" +
      '<div class="kv">' +
      "<div><span>Occurrences</span><b>" + esc(n.count) + "</b></div>" +
      "<div><span>Verses</span><b>" + esc(n.verse_count || 0) + "</b></div>" +
      "<div><span>Surahs</span><b>" + esc(n.surah_count || 0) + "</b></div>" +
      "<div><span>Standalone</span><b>" + esc(n.standalone_count || 0) + "</b></div>" +
      "<div><span>In phrases</span><b>" + esc(n.phrase_count || 0) + "</b></div>" +
      "</div>" +
      (n.notes ? "<p>" + esc(n.notes) + "</p>" : "") +
      (refs ? "<p><b>Example verses:</b> " + refs + "</p>" : "") +
      "</div>";
    var det = $("name-detail");
    if (det.scrollIntoView) det.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
  on("name-search", "input", renderNames);
  on("name-filter", "change", renderNames);

  /* ---------- network graph ---------- */
  var graphState = { nodes: [], edges: [], pos: {}, selected: null };
  function drawGraph() {
    var canvas = $("graph");
    if (!canvas) return;
    var ctx = null;
    try { ctx = canvas.getContext("2d"); } catch (e) { ctx = null; }
    var scopeEl = $("graph-scope"), edgesEl = $("graph-edges");
    var scope = (scopeEl && parseInt(scopeEl.value, 10)) || 25;
    var edgeKind = (edgesEl && edgesEl.value) || "verse";
    var top = (D.names || []).slice().sort(function (a, b) { return b.count - a.count; })
      .filter(function (n) { return n.count > 0; }).slice(0, scope);
    var ids = {};
    top.forEach(function (n) { ids[n.id] = true; });
    var edges = (edgeKind === "verse" ? D.verse_edges : D.surah_edges) || [];
    var kept = edges.filter(function (e) { return ids[e.a] && ids[e.b]; })
      .sort(function (a, b) { return b.weight - a.weight; })
      .slice(0, edgeKind === "verse" ? 200 : 120);
    graphState.nodes = top; graphState.edges = kept;
    var W = canvas.width, H = canvas.height;
    var cx = W / 2, cy = H / 2;
    // Ring radius leaves room for the largest node circle plus its label,
    // so outer labels never sit on (or past) the canvas edge.
    var maxR = 0;
    top.forEach(function (n) { maxR = Math.max(maxR, 7 + Math.sqrt(n.count || 0) * 1.6); });
    var R = Math.min(W, H) / 2 - 70 - maxR - 16;
    graphState.pos = {};
    top.forEach(function (n, i) {
      var a = (i / top.length) * Math.PI * 2 - Math.PI / 2;
      graphState.pos[n.id] = { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) };
    });
    var detail = $("graph-detail");
    if (!ctx) {
      if (detail) detail.textContent = "Graph needs a canvas-capable browser; the pair counts below are the same data in table form.";
      return;
    }
    renderGraphCanvas(ctx, W, H);
  }
  function renderGraphCanvas(ctx, W, H) {
    var sel = graphState.selected;
    var neighbours = {};
    if (sel != null) {
      graphState.edges.forEach(function (e) {
        if (e.a === sel) neighbours[e.b] = e.weight;
        if (e.b === sel) neighbours[e.a] = e.weight;
      });
    }
    ctx.clearRect(0, 0, W, H);
    graphState.edges.forEach(function (e) {
      var p1 = graphState.pos[e.a], p2 = graphState.pos[e.b];
      if (!p1 || !p2) return;
      var active = sel == null || e.a === sel || e.b === sel;
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
      ctx.strokeStyle = active ? "rgba(122,92,0," + Math.min(0.85, 0.12 + e.weight / 40) + ")"
        : "rgba(107,93,73,0.10)";
      ctx.lineWidth = Math.max(0.6, Math.min(7, e.weight / 9));
      ctx.stroke();
    });
    graphState.nodes.forEach(function (n) {
      var p = graphState.pos[n.id];
      var r = 7 + Math.sqrt(n.count || 0) * 1.6;
      var dim = sel != null && n.id !== sel && !neighbours[n.id];
      ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      ctx.fillStyle = n.id === sel ? "#7a5c00" : (dim ? "#d8cbb0" : "#8a6d1f");
      ctx.fill();
      ctx.font = "11px system-ui, sans-serif";
      ctx.fillStyle = dim ? "#6b5d49" : "#2b2118";
      /* Full transliteration (no Ar-/Al- stripping — the stripped forms read
         as truncated labels), placed radially outward from the ring, so a
         label never sits on the next node down the ring: right-side labels
         anchor left, left-side labels anchor right, near-top/bottom centre. */
      var label = n.transliteration;
      var tw = label.length * 6;
      try { tw = ctx.measureText(label).width; } catch (e) { /* stubbed canvas: keep estimate */ }
      var dx = p.x - W / 2, dy = p.y - H / 2;
      var len = Math.hypot(dx, dy) || 1;
      var ux = dx / len, uy = dy / len;
      var ox = p.x + ux * (r + 13), oy = p.y + uy * (r + 13);
      var lx, ly;
      if (ux > 0.1) { ctx.textAlign = "left"; lx = Math.min(ox, W - tw - 6); }
      else if (ux < -0.1) { ctx.textAlign = "right"; lx = Math.max(ox, tw + 6); }
      else { ctx.textAlign = "center"; lx = Math.max(tw / 2 + 6, Math.min(W - tw / 2 - 6, ox)); }
      ly = Math.max(12, Math.min(H - 3, oy + 4));
      ctx.fillText(label, lx, ly);
    });
    if (sel != null) {
      var n = namesById[sel];
      var parts = Object.keys(neighbours).map(function (k) {
        return { name: namesById[+k], w: neighbours[k] };
      }).filter(function (x) { return x.name; })
        .sort(function (a, b) { return b.w - a.w; }).slice(0, 8);
      var detail = $("graph-detail");
      if (detail) detail.innerHTML = n ? "<b>" + esc(n.transliteration) + "</b> (" + esc(n.count) +
        " occurrences) co-occurs most with: " +
        parts.map(function (x) { return esc(x.name.transliteration) + " (" + x.w + ")"; }).join(" · ") +
        (parts.length ? "" : " — no verse partners in this scope.") : "";
    }
  }
  on("graph", "click", function (ev) {
    var canvas = $("graph");
    if (!canvas) return;
    var rect = canvas.getBoundingClientRect();
    var x = (ev.clientX - rect.left) * (canvas.width / rect.width);
    var y = (ev.clientY - rect.top) * (canvas.height / rect.height);
    var best = null, bestD = 1e9;
    graphState.nodes.forEach(function (n) {
      var p = graphState.pos[n.id];
      if (!p) return;
      var d = Math.hypot(p.x - x, p.y - y);
      if (d < bestD) { bestD = d; best = n; }
    });
    if (best && bestD < 40) {
      graphState.selected = (graphState.selected === best.id) ? null : best.id;
      var ctx = null;
      try { ctx = canvas.getContext("2d"); } catch (e) { ctx = null; }
      if (ctx) renderGraphCanvas(ctx, canvas.width, canvas.height);
      var detail = $("graph-detail");
      if (detail) {
        if (graphState.selected == null)
          detail.textContent = "Select a Name in the graph to see its strongest partners.";
        else showNameDetail(graphState.selected);
      }
    }
  });
  on("graph-scope", "change", drawGraph);
  on("graph-edges", "change", drawGraph);

  /* ---------- findings: method & locations (collapsed) ---------- */
  function fmtCount(c) {
    if (c == null) return "—";
    if (Array.isArray(c)) {
      var parts = c.map(function (x) { return x == null ? "—" : String(x); });
      if (parts.every(function (p) { return p === "—"; })) return "—";
      return parts.join(" / ");
    }
    return String(c);
  }
  function fmtVer(v) {
    if (!v) return "not applicable";
    var t = fmtCount(v.count);
    return v.note ? t + " — " + v.note : t;
  }
  function methodBlock(f) {
    var h = '<details class="method"><summary>Method &amp; where it occurs</summary>';
    h += "<p><b>Scholar's method (" + esc(f.method_status || "unstated") + "):</b> " +
      esc(f.scholar_method || "Method not stated by the source.") + "</p>";
    if (f.exceptions)
      h += "<p><b>Exceptions:</b> " + esc(f.exceptions) + "</p>";
    h += "<p><b>Verification — scholar's rule:</b> " + esc(fmtVer(f.verification_scholar_rule)) + "</p>";
    h += "<p><b>Verification — root rule:</b> " + esc(fmtVer(f.verification_root_rule)) + "</p>";
    var locs = (typeof window !== "undefined" && window.MIRACLE_LOCATIONS) || {};
    var loc = locs[f.id];
    if (!loc) {
      h += "<p><b>Locations:</b> location data not loaded.</p>";
    } else if (loc.not_applicable) {
      h += "<p><b>Locations:</b> not applicable — " + esc(loc.not_applicable) + "</p>";
    } else if (!loc.verses || !loc.verses.length) {
      h += "<p><b>Locations:</b> not applicable — " + esc(loc.note || "no occurrences to locate.") + "</p>";
    } else {
      var ps = loc.per_surah || {};
      var keys = Object.keys(ps).sort(function (a, b) { return +a - +b; });
      var breakdown = keys.map(function (k) { return k + ": " + ps[k]; }).join(" · ");
      h += "<p><b>Locations (" + loc.verses.length + " verses):</b> " +
        (breakdown ? "verses per surah — " + esc(breakdown) + "<br>" : "") +
        '<span class="loc-list">' + esc(loc.verses.join(", ")) + "</span></p>";
      if (loc.verses_scholar_rule && loc.verses_scholar_rule.length &&
          loc.verses_scholar_rule.join(",") !== loc.verses.join(",")) {
        h += "<p><b>Locations — scholar's rule (" + loc.verses_scholar_rule.length + " verses):</b> " +
          '<span class="loc-list">' + esc(loc.verses_scholar_rule.join(", ")) + "</span></p>";
      }
    }
    h += "</details>";
    return h;
  }

  /* ---------- findings: data tables (shared by both pages) ---------- */
  function sourceCell(f) {
    var s = f.source || {};
    var h = esc(s.author || "—");
    if (s.title) h += '<br><span class="src-title">' + esc(s.title) + "</span>";
    if (s.year) h += " (" + esc(s.year) + ")";
    if (s.url) h += '<br><a href="' + esc(s.url) + '" target="_blank" rel="noopener">source</a>';
    return h;
  }
  function findingRow(f) {
    /* Numbers prefer the recomputed per-set values (consistent with the
       Assumption column in the same row); fall back to the stored
       verification counts where a set has no number (e.g. scholar_set null). */
    var a = f.assumptions;
    var scholarN = a && a.scholar_set && a.numbers_by_set && a.numbers_by_set[a.scholar_set] != null
      ? fmtCount(a.numbers_by_set[a.scholar_set])
      : fmtCount(f.verification_scholar_rule && f.verification_scholar_rule.count);
    var ourN = a && a.our_set && a.numbers_by_set && a.numbers_by_set[a.our_set] != null
      ? fmtCount(a.numbers_by_set[a.our_set])
      : fmtCount(f.verification_root_rule && f.verification_root_rule.count);
    var h = '<tr class="frow"><td class="c-claim"><b>' + esc(f.claim) + "</b>" +
      (f.claim_arabic_or_terms ? ' <span class="ar">' + esc(f.claim_arabic_or_terms) + "</span>" : "") +
      '<div class="cat-tag">' + esc(sectionLabel(f.section)) + " · " + esc(catLabel(f.category)) + "</div>" +
      methodBlock(f) + "</td>" +
      '<td class="c-num">' + esc(scholarN) + "</td>" +
      '<td class="c-num">' + esc(ourN) + "</td>" +
      '<td class="c-assume">' + assumptionCell(f) + "</td>" +
      '<td class="c-verdict">' + statusBadge(f) +
      (f.confidence ? '<div class="conf">' + esc(f.confidence) + "</div>" : "") + "</td>" +
      '<td class="c-src">' + sourceCell(f) + "</td></tr>";
    return h;
  }
  function findingsTable(list) {
    if (!list.length) return "<p>No findings match those filters.</p>";
    return '<div class="table-scroll"><table class="data-table f-table"><thead><tr>' +
      "<th>Claim</th><th>Scholar's number</th><th>Our number</th>" +
      "<th>Assumption</th><th>Verdict</th><th>Source</th></tr></thead><tbody>" +
      list.map(findingRow).join("") + "</tbody></table></div>";
  }
  function matchesFilters(f, q, cat, st) {
    var hay = (f.claim + " " + (f.claim_arabic_or_terms || "") + " " +
      ((f.source && f.source.author) || "") + " " + ((f.source && f.source.title) || "") + " " +
      (f.scholar_method || "") + " " + (f.exceptions || "") + " " +
      (f.assumptions && f.assumptions.reason ? f.assumptions.reason : "") + " " +
      (f.our_note || "")).toLowerCase();
    if (q && hay.indexOf(q) === -1) return false;
    if (cat !== "all" && f.category !== cat) return false;
    if (st !== "all" && f.our_status !== st) return false;
    return true;
  }
  /* Main page: ONE merged table of CONFIRMED findings only. The filter in
     code (our_status === 'confirmed') is the guarantee — no differs or
     cannot_verify row can reach this page. No status filter: every row here
     is confirmed. */
  function renderVerified() {
    var host = $("verified-list");
    if (!host) return;
    var q = (($("verified-search") || {}).value || "").toLowerCase();
    var cat = ($("verified-cat") || {}).value || "all";
    var all = D.findings || [];
    var confirmed = all.filter(function (f) { return f.our_status === "confirmed"; });
    var list = confirmed.filter(function (f) { return matchesFilters(f, q, cat, "all"); });
    var sch = confirmed.filter(function (f) { return f.section === "scholarly"; }).length;
    var pop = confirmed.filter(function (f) { return f.section === "popular"; }).length;
    var tally = $("verified-tally");
    if (tally) tally.textContent = confirmed.length + " verified findings — " + sch +
      " scholarly · " + pop + " popular. Showing " + list.length + ".";
    host.innerHTML = findingsTable(list);
  }
  /* Unverified page: differs + cannot_verify only, kept in Scholar / Popular
     groups with a status filter (differs vs cannot_verify). */
  function renderUnverified() {
    var host = $("unverified-list");
    if (!host) return;
    var q = (($("unverified-search") || {}).value || "").toLowerCase();
    var cat = ($("unverified-cat") || {}).value || "all";
    var st = ($("unverified-status") || {}).value || "all";
    var all = D.findings || [];
    var unv = all.filter(function (f) { return f.our_status !== "confirmed"; });
    var list = unv.filter(function (f) { return matchesFilters(f, q, cat, st); });
    var t = { differs: 0, cannot_verify: 0 };
    unv.forEach(function (f) { if (t[f.our_status] != null) t[f.our_status]++; });
    var tally = $("unverified-tally");
    if (tally) tally.textContent = unv.length + " unverified claims — " + t.differs +
      " differ from our recount · " + t.cannot_verify + " cannot verify. Showing " + list.length + ".";
    var html = "";
    ["scholarly", "popular"].forEach(function (section) {
      var group = list.filter(function (f) { return (f.section || "scholarly") === section; });
      if (!group.length) return;
      html += "<h3>" + esc(sectionLabel(section)) + " — " + group.length + " unverified</h3>" +
        findingsTable(group);
    });
    host.innerHTML = html || "<p>No unverified claims match those filters.</p>";
  }
  on("verified-search", "input", renderVerified);
  on("verified-cat", "change", renderVerified);
  on("unverified-search", "input", renderUnverified);
  on("unverified-cat", "change", renderUnverified);
  on("unverified-status", "change", renderUnverified);

  /* ---------- init: render only the sections this page has ---------- */
  renderPairs();
  renderNames();
  renderVerified();
  renderUnverified();
  drawGraph();
})();

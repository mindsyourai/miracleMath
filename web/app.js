/* miracleMath app — renders from window.MIRACLE_DATA (embedded data.js).
   No network calls, no backend. Charts are CSS bars; the Name network is a
   guarded canvas drawing (no-ops safely where canvas is unavailable). */
(function () {
  "use strict";
  var D = window.MIRACLE_DATA || {};
  var $ = function (id) { return document.getElementById(id); };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function catLabel(c) {
    return { paired_counts: "Paired counts", letter_counts: "Letter counts",
      code19: "Code 19", corpus_linguistics: "Corpus linguistics" }[c] || c;
  }
  function statusBadge(f) {
    if (f.our_status === "confirmed")
      return '<span class="badge ok">Confirmed by our recount</span>';
    if (f.our_status === "differs")
      return '<span class="badge bad">Differs from our recount</span>';
    return '<span class="badge warn">Cannot verify</span>';
  }
  function confBadge(f) {
    var c = f.confidence || "";
    if (c.indexOf("confirmed") === 0) return '<span class="badge ok">' + esc(c) + "</span>";
    if (c === "contested") return '<span class="badge bad">contested</span>';
    return '<span class="badge warn">' + esc(c) + "</span>";
  }

  /* ---------- tabs ---------- */
  var tabs = document.querySelectorAll(".tab");
  tabs.forEach(function (btn) {
    btn.addEventListener("click", function () {
      tabs.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      document.querySelectorAll(".panel").forEach(function (p) { p.classList.remove("active"); });
      $("tab-" + btn.getAttribute("data-tab")).classList.add("active");
      if (btn.getAttribute("data-tab") === "names") drawGraph();
    });
  });

  /* ---------- hero stats ---------- */
  (function stats() {
    var c = D.corpus || {};
    var items = [
      [c.words ? c.words.toLocaleString("en-US") : "77,429", "words in the corpus"],
      [c.verses ? c.verses.toLocaleString("en-US") : "6,236", "verses"],
      [c.surahs || 114, "surahs"],
      [(D.names || []).length || 99, "Names of God"],
      [(D.names_totals && D.names_totals.total_occurrences) || 1120, "Name occurrences"],
      [(D.findings || []).length || 64, "scholar findings reviewed"]
    ];
    $("stats").innerHTML = items.map(function (it) {
      return '<div class="stat"><b>' + esc(it[0]) + "</b><span>" + esc(it[1]) + "</span></div>";
    }).join("");
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
    var q = ($("pair-search").value || "").toLowerCase();
    var eqOnly = $("pair-equal-only").checked;
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
    $("extras-list").innerHTML = ex || "<p>No single counts match that search.</p>";
  }
  $("pair-search").addEventListener("input", renderPairs);
  $("pair-equal-only").addEventListener("change", renderPairs);

  /* ---------- names ---------- */
  var namesById = {};
  (D.names || []).forEach(function (n) { namesById[n.id] = n; });
  var maxName = 1;
  (D.names || []).forEach(function (n) { maxName = Math.max(maxName, n.count || 0); });

  function renderNames() {
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
    if (!n) return;
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
  $("name-search").addEventListener("input", renderNames);
  $("name-filter").addEventListener("change", renderNames);

  /* ---------- network graph ---------- */
  var graphState = { nodes: [], edges: [], pos: {}, selected: null };
  function drawGraph() {
    var canvas = $("graph");
    if (!canvas) return;
    var ctx = null;
    try { ctx = canvas.getContext("2d"); } catch (e) { ctx = null; }
    var scope = parseInt($("graph-scope").value, 10) || 25;
    var edgeKind = $("graph-edges").value;
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
    var cx = W / 2, cy = H / 2, R = Math.min(W, H) / 2 - 70;
    graphState.pos = {};
    top.forEach(function (n, i) {
      var a = (i / top.length) * Math.PI * 2 - Math.PI / 2;
      graphState.pos[n.id] = { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) };
    });
    if (!ctx) {
      $("graph-detail").textContent = "Graph needs a canvas-capable browser; the pair counts below are the same data in table form.";
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
      ctx.strokeStyle = active ? "rgba(34,211,238," + Math.min(0.85, 0.12 + e.weight / 40) + ")"
        : "rgba(120,140,170,0.07)";
      ctx.lineWidth = Math.max(0.6, Math.min(7, e.weight / 9));
      ctx.stroke();
    });
    graphState.nodes.forEach(function (n) {
      var p = graphState.pos[n.id];
      var r = 7 + Math.sqrt(n.count || 0) * 1.6;
      var dim = sel != null && n.id !== sel && !neighbours[n.id];
      ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      ctx.fillStyle = n.id === sel ? "#eab308" : (dim ? "#233247" : "#22d3ee");
      ctx.fill();
      ctx.font = "11px system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.fillStyle = dim ? "#5b6b82" : "#e8eef7";
      ctx.fillText(n.transliteration.replace("Ar-", "").replace("Al-", ""), p.x, p.y + r + 13);
    });
    if (sel != null) {
      var n = namesById[sel];
      var parts = Object.keys(neighbours).map(function (k) {
        return { name: namesById[+k], w: neighbours[k] };
      }).filter(function (x) { return x.name; })
        .sort(function (a, b) { return b.w - a.w; }).slice(0, 8);
      $("graph-detail").innerHTML = n ? "<b>" + esc(n.transliteration) + "</b> (" + esc(n.count) +
        " occurrences) co-occurs most with: " +
        parts.map(function (x) { return esc(x.name.transliteration) + " (" + x.w + ")"; }).join(" · ") +
        (parts.length ? "" : " — no verse partners in this scope.") : "";
    }
  }
  $("graph").addEventListener("click", function (ev) {
    var canvas = $("graph");
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
      if (graphState.selected == null)
        $("graph-detail").textContent = "Select a Name in the graph to see its strongest partners.";
      else showNameDetail(graphState.selected);
    }
  });
  $("graph-scope").addEventListener("change", drawGraph);
  $("graph-edges").addEventListener("change", drawGraph);

  /* ---------- findings ---------- */
  function renderFindings() {
    var q = ($("finding-search").value || "").toLowerCase();
    var cat = $("finding-cat").value, st = $("finding-status").value;
    var list = (D.findings || []).filter(function (f) {
      var hay = (f.claim + " " + (f.claim_arabic_or_terms || "") + " " +
        ((f.source && f.source.author) || "") + " " + ((f.source && f.source.title) || "")).toLowerCase();
      if (q && hay.indexOf(q) === -1) return false;
      if (cat !== "all" && f.category !== cat) return false;
      if (st !== "all" && f.our_status !== st) return false;
      return true;
    });
    var tally = { confirmed: 0, differs: 0, cannot_verify: 0 };
    (D.findings || []).forEach(function (f) { if (tally[f.our_status] != null) tally[f.our_status]++; });
    $("finding-tally").textContent = (D.findings || []).length + " findings in total — " +
      tally.confirmed + " confirmed by our recount · " + tally.differs +
      " differ from our recount · " + tally.cannot_verify + " cannot verify. Showing " +
      list.length + ".";
    var html = "";
    list.forEach(function (f) {
      var s = f.source || {};
      html += '<article class="finding"><h3>' + esc(f.claim) +
        (f.claim_arabic_or_terms ? ' <span class="ar">' + esc(f.claim_arabic_or_terms) + "</span>" : "") + "</h3>" +
        '<div class="label-row"><span class="badge cat">' + esc(catLabel(f.category)) + "</span>" +
        statusBadge(f) + confBadge(f) + "</div>" +
        '<p class="meta"><b>Source:</b> ' + esc(s.author || "—") + " — " + esc(s.title || "") +
        (s.year ? " (" + esc(s.year) + ")" : "") +
        (s.url ? ' · <a href="' + esc(s.url) + '" target="_blank" rel="noopener">source link</a>' : "") + "</p>" +
        "<p><b>Corpus &amp; method:</b> " + esc(f.corpus_and_method || "Method not stated by the source.") + "</p>" +
        '<p class="note"><b>Our recount:</b> ' + esc(f.our_note || "") + "</p>" +
        "</article>";
    });
    $("findings-list").innerHTML = html || "<p>No findings match those filters.</p>";
  }
  $("finding-search").addEventListener("input", renderFindings);
  $("finding-cat").addEventListener("change", renderFindings);
  $("finding-status").addEventListener("change", renderFindings);

  /* ---------- init ---------- */
  renderPairs();
  renderNames();
  renderFindings();
  drawGraph();
})();

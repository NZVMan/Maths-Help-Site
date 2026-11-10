/* VMANZ Maths — shared page script.
   1. Builds the "On this page" contents box for long notes pages.
   2. Renders maths with KaTeX:  inline \( ... \)   display \[ ... \]  or  $$ ... $$
      (single $ is deliberately NOT used, so money like $45.50 is safe).
   3. Graph helpers for JSXGraph (loaded only on pages that contain a .jxgbox):
      VMANZ.graph, plot, point, vline, segment, text, slider, readout.
      See CONTENT_GUIDE.md for how to use them. */
(function () {
  "use strict";

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  /* ---- building TeX strings that change as sliders move ---- */
  var tex = {
    /* 2.50 -> "2.5", -0 -> "0" */
    num: function (n) {
      var r = Math.round(n * 100) / 100;
      if (r === 0) r = 0;
      return String(r);
    },
    /* coefficient in front of a variable: 1x -> x, -1x -> -x */
    coef: function (a, v) {
      if (!v) return tex.num(a);
      if (a === 1) return v;
      if (a === -1) return "-" + v;
      return tex.num(a) + v;
    },
    /* [[2, "x^2"], [-3, "x"], [1, ""]] -> "2x^2 - 3x + 1" (zero terms dropped) */
    poly: function (terms) {
      var out = "";
      terms.forEach(function (t) {
        var c = Math.round(t[0] * 100) / 100, v = t[1];
        if (c === 0) return;
        var body = tex.coef(Math.abs(c), v);
        out += out === "" ? (c < 0 ? "-" : "") + body : (c < 0 ? " - " : " + ") + body;
      });
      return out || "0";
    },
    /* (x - h): h = 3 -> "(x - 3)", h = -2 -> "(x + 2)", h = 0 -> "x" */
    shift: function (h, v) {
      v = v || "x";
      if (Math.round(h * 100) === 0) return v;
      return "(" + v + (h > 0 ? " - " : " + ") + tex.num(Math.abs(h)) + ")";
    },
    pair: function (x, y) { return "(" + tex.num(x) + ",\\ " + tex.num(y) + ")"; }
  };

  window.VMANZ = {
    tex: tex,

    colours: function () {
      return { ink: css("--ink"), muted: css("--muted"), line: css("--line"),
               accent: css("--accent"), warn: css("--warn"), rule: css("--rule-line") };
    },

    /* opts: x:[min,max], y:[min,max], step: n or [xStep, yStep], square, zoom */
    board: function (id, opts) {
      opts = opts || {};
      var x = opts.x || [-6, 6], y = opts.y || [-6, 6], c = this.colours();
      var step = Array.isArray(opts.step) ? opts.step : [opts.step || 1, opts.step || 1];
      JXG.Options.text.cssDefaultStyle = "font-family: inherit;";
      var board = JXG.JSXGraph.initBoard(id, {
        boundingbox: [x[0], y[1], x[1], y[0]],
        keepaspectratio: !!opts.square,
        showCopyright: false, showNavigation: !!opts.zoom, pan: { enabled: !!opts.zoom },
        zoom: { enabled: !!opts.zoom },
        axis: false
      });
      ["x", "y"].forEach(function (dir, i) {
        board.create("axis", dir === "x" ? [[0, 0], [1, 0]] : [[0, 0], [0, 1]], {
          strokeColor: c.ink, highlight: false,
          ticks: { strokeColor: c.line, majorHeight: -1, minorTicks: 0, insertTicks: false,
                   ticksDistance: step[i], drawZero: false,
                   label: { strokeColor: c.muted, fontSize: 13 } }
        });
      });
      return board;
    },

    /* Preferred way to make a graph: draw(board) runs now, or, if the graph is
       inside a closed "Show solution", the first time it is opened (a hidden
       board would otherwise be drawn at zero size). */
    graph: function (id, opts, draw) {
      var self = this, el = document.getElementById(id), done = false;
      var go = function () { if (!done) { done = true; draw(self.board(id, opts)); } };
      var d = el && el.closest("details");
      if (d && !d.open) {
        d.addEventListener("toggle", function () { if (d.open) go(); });
      } else {
        go();
      }
    },

    /* Draw y = fn(x) in the accent colour. */
    plot: function (board, fn, opts) {
      var c = this.colours();
      return board.create("functiongraph", [fn], Object.assign(
        { strokeColor: c.accent, strokeWidth: 3, highlight: false }, opts || {}));
    },

    /* A fixed, labelled point. xy can be [x, y] or [function, function]. */
    point: function (board, xy, label, opts) {
      var c = this.colours(), o = opts || {};
      var lab = Object.assign({ offset: [8, 10], strokeColor: c.ink, fontSize: 14, highlight: false }, o.label || {});
      return board.create("point", xy, Object.assign({
        name: label || "", fixed: true, size: 3, strokeColor: c.ink, fillColor: c.ink, highlight: false
      }, o, { label: lab }));
    },

    /* Dashed vertical line x = k (e.g. an axis of symmetry). */
    vline: function (board, k, opts) {
      var c = this.colours();
      return board.create("line", [[k, 0], [k, 1]], Object.assign(
        { strokeColor: c.muted, dash: 2, strokeWidth: 1.5, fixed: true, highlight: false }, opts || {}));
    },

    /* Line segment between two points (each [x, y] or a point object). */
    segment: function (board, p, q, opts) {
      var c = this.colours();
      return board.create("segment", [p, q], Object.assign(
        { strokeColor: c.ink, strokeWidth: 2, fixed: true, highlight: false }, opts || {}));
    },

    /* Plain text placed on the board, e.g. an axis name. */
    text: function (board, xy, str, opts) {
      var c = this.colours();
      return board.create("text", [xy[0], xy[1], str], Object.assign(
        { strokeColor: c.muted, fontSize: 14, fixed: true, highlight: false }, opts || {}));
    },

    /* A slider in a control panel underneath the graph (so it never covers the
       curve, and is easy to drag on a phone). range = [min, start, max],
       step = how far each notch moves. Read it with slider.Value().
       (The "row" argument is kept for older pages and no longer used.) */
    slider: function (board, name, range, row, step) {
      var box = document.getElementById(board.container);
      var panelId = board.container + "-controls";
      var panel = document.getElementById(panelId);
      if (!panel) {
        panel = document.createElement("div");
        panel.id = panelId;
        panel.className = "controls";
        box.insertAdjacentElement("afterend", panel);
        box.classList.add("has-controls");
      }
      var fmt = function (v) { return v < 0 ? "−" + tex.num(-v) : tex.num(v); };
      var label = document.createElement("label");
      label.className = "ctl";
      label.innerHTML = '<span class="ctl-name"></span><input type="range"><output></output>';
      label.querySelector(".ctl-name").textContent = name;
      var input = label.querySelector("input"), out = label.querySelector("output");
      input.min = range[0]; input.max = range[2]; input.step = step || 0.5; input.value = range[1];
      input.setAttribute("aria-label", name);
      out.textContent = fmt(range[1]);
      input.addEventListener("input", function () {
        out.textContent = fmt(parseFloat(input.value));
        board.update();
      });
      panel.appendChild(label);
      return { Value: function () { return parseFloat(input.value); }, input: input };
    },

    /* Live maths that updates as the board changes (e.g. when a slider moves).
       fn returns { eq: "TeX for the big equation", rows: [["Label", "TeX"], ...] }.
       Put <div id="..." class="readout"></div> just above the graph. */
    readout: function (board, id, fn) {
      var el = document.getElementById(id), last = "";
      el.setAttribute("aria-live", "polite");
      document.getElementById(board.container).classList.add("has-readout");
      var render = function () {
        var r = fn(), key = JSON.stringify(r);
        if (key === last) return;
        last = key;
        var k = function (s, display) {
          return katex.renderToString(s, { displayMode: !!display, throwOnError: false });
        };
        el.innerHTML = k(r.eq, true) + (r.rows && r.rows.length ? "<dl>" + r.rows.map(function (row) {
          return "<div><dt>" + row[0] + "</dt><dd>" + k(row[1]) + "</dd></div>";
        }).join("") + "</dl>" : "");
      };
      board.on("update", render);
      render();
    }
  };

  /* "On this page" box: one link per section heading (h2) in the notes. */
  function buildContents() {
    var notes = document.querySelector(".notes");
    if (!notes) return;
    var heads = notes.querySelectorAll(":scope > section > h2");
    if (heads.length < 5) return;
    var used = {}, items = [];
    heads.forEach(function (h) {
      var base = (h.id || h.textContent).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "section";
      var id = base, n = 2;
      while (used[id]) id = base + "-" + n++;
      used[id] = true;
      h.id = id;
      items.push('<li><a href="#' + id + '">' + h.innerHTML + "</a></li>");
    });
    var nav = document.createElement("nav");
    nav.className = "toc";
    nav.setAttribute("aria-label", "On this page");
    nav.innerHTML = '<p class="toc-title">On this page</p><ul>' + items.join("") + "</ul>";
    notes.insertBefore(nav, notes.firstChild);
  }

  /* Printing shows every solution (and draws any graphs inside them). */
  window.addEventListener("beforeprint", function () {
    document.querySelectorAll("details.solution").forEach(function (d) { d.open = true; });
  });

  document.addEventListener("DOMContentLoaded", function () {
    buildContents();
    if (window.renderMathInElement) {
      renderMathInElement(document.querySelector("main") || document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "\\(", right: "\\)", display: false }
        ],
        throwOnError: false
      });
    }
  });
})();

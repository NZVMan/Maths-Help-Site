/* VMANZ Maths — shared page script.
   1. Renders maths with KaTeX:  inline \( ... \)   display \[ ... \]  or  $$ ... $$
      (single $ is deliberately NOT used, so money like $45.50 is safe).
   2. VMANZ.board(id, {x:[min,max], y:[min,max]}) makes a JSXGraph board
      styled to match the site. Only loaded on pages that contain a .jxgbox. */
(function () {
  "use strict";

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  window.VMANZ = {
    colours: function () {
      return { ink: css("--ink"), muted: css("--muted"), line: css("--line"),
               accent: css("--accent"), warn: css("--warn"), rule: css("--rule-line") };
    },

    board: function (id, opts) {
      opts = opts || {};
      var x = opts.x || [-6, 6], y = opts.y || [-6, 6], c = this.colours();
      JXG.Options.text.cssDefaultStyle = "font-family: inherit;";
      var board = JXG.JSXGraph.initBoard(id, {
        boundingbox: [x[0], y[1], x[1], y[0]],
        keepaspectratio: !!opts.square,
        showCopyright: false, showNavigation: !!opts.zoom, pan: { enabled: !!opts.zoom },
        zoom: { enabled: !!opts.zoom },
        axis: false
      });
      ["x", "y"].forEach(function (dir) {
        board.create("axis", dir === "x" ? [[0, 0], [1, 0]] : [[0, 0], [0, 1]], {
          strokeColor: c.ink, highlight: false,
          ticks: { strokeColor: c.line, majorHeight: -1, minorTicks: 0, insertTicks: false,
                   ticksDistance: opts.step || 1, drawZero: false,
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

    /* A slider in the top-left corner of the board. row 0, 1, 2 stacks them.
       range = [min, start, max]. Read it with slider.Value(). */
    slider: function (board, name, range, row, snap) {
      var c = this.colours(), bb = board.getBoundingBox();
      var w = bb[2] - bb[0], h = bb[1] - bb[3];
      var y = bb[1] - (0.07 + 0.08 * (row || 0)) * h;
      return board.create("slider", [[bb[0] + 0.1 * w, y], [bb[0] + 0.45 * w, y], range], {
        name: name, snapWidth: snap || 0.5, precision: 1,
        strokeColor: c.accent, fillColor: c.accent, highlightFillColor: c.accent,
        baseline: { strokeColor: c.line }, highline: { strokeColor: c.accent },
        label: { strokeColor: c.ink, fontSize: 14 }
      });
    }
  };

  /* Printing shows every solution (and draws any graphs inside them). */
  window.addEventListener("beforeprint", function () {
    document.querySelectorAll("details.solution").forEach(function (d) { d.open = true; });
  });

  document.addEventListener("DOMContentLoaded", function () {
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

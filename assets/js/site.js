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
    }
  };

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

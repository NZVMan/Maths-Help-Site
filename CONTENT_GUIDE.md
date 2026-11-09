# Content guide: writing VMANZ Maths pages

Read this before adding notes. Every component below appears live on the
**Page components** page (`guide/index.html`), so open that in a browser and copy
from its source.

## How the site fits together

```
curriculum.json            the site map: courses > topics > groups > subtopics
tools/build.py             builds every page from curriculum.json
tools/subtopic-template.html   what a brand-new subtopic page starts as
assets/css/site.css        all styling and colours (VMANZ green, light + dark)
assets/js/site.js          maths rendering + graph helper
index.html                 home            (generated: don't edit)
year-9/index.html          course page     (generated: don't edit)
year-9/algebra/index.html  topic page      (generated: don't edit)
year-9/algebra/factorising/index.html   subtopic page: YOUR NOTES GO HERE
```

On a subtopic page, only edit between these two lines; the build rewrites
everything outside them (header, breadcrumbs, previous/next, footer):

```html
<!-- vmanz:content:start -->
   ... your notes ...
<!-- vmanz:content:end -->
```

### Everyday workflow

1. Write notes in the subtopic's `index.html`.
2. Delete the `<!-- vmanz:placeholder -->` line when the page is ready for students.
3. Run `python3 tools/build.py` (updates "Coming soon" badges, progress bars and `PROGRESS.md`).
4. Preview: `python3 -m http.server 8765`, then open http://localhost:8765
5. Commit and push. GitHub Pages updates the live site in about a minute.

### Adding or renaming a subtopic

Edit `curriculum.json`, then run the build. New pages are created; existing
notes are never overwritten. If you **rename** a subtopic, its web address
changes too. Either give it `"slug"` with the old address, or move the old
folder to the new name before building, or you will get a fresh empty page.

## Maths: KaTeX

| You want | Write |
|---|---|
| Inline maths | `\( x^2 + 3x \)` |
| Display (own line, centred) | `\[ x = \frac{-b \pm \sqrt{b^2-4ac}}{2a} \]` |
| Lined-up working | `\[ \begin{aligned} 3x+5 &= 20 \\ 3x &= 15 \end{aligned} \]` |
| Units | `\( 12\,\text{cm}^2 \)` |
| Money | just type `$45.50`: single `$` is **not** a maths delimiter here |
| Degrees | `\( 35^\circ \)` |
| Multiply sign | `\( 3 \times 4 \)` (not `x`) |
| Minus in plain text | use the real minus sign `−` in tables and SVG labels, not a hyphen |

KaTeX is used rather than MathJax because it renders instantly with no
page jump, which matters on pages with dozens of equations and on phones.

## Building blocks

```html
<div class="note"><span class="box-label">Key idea</span> <p>…</p></div>
<div class="rule"><span class="box-label">Rule</span> \[ a^2 + b^2 = c^2 \]</div>
<div class="warn"><span class="box-label">Common mistake</span> <p>…</p></div>

<div class="example">                       <!-- numbered automatically -->
  <h3>Short title</h3>
  <p>Question…</p>
  <details class="solution">
    <summary>Show solution</summary>
    <ol class="steps"><li>…</li><li>…</li></ol>
    <p class="answer">Final answer</p>
  </details>
</div>
```

Solutions are hidden until clicked on screen and always shown when printed.

## Tables

Plain HTML tables with `class="mtable"`, wrapped so they scroll on phones.
Maths works inside cells.

```html
<div class="table-scroll">
  <table class="mtable value-table">          <!-- value-table = horizontal x / y table -->
    <caption>Table of values for \(y = 2x - 1\)</caption>
    <tr><th>\(x\)</th><td>−2</td><td>−1</td><td>0</td></tr>
    <tr><th>\(y\)</th><td>−5</td><td>−3</td><td>−1</td></tr>
  </table>
</div>
```

## Graphs and diagrams: which tool?

| What you're drawing | Use | Why |
|---|---|---|
| Anything on coordinate axes: linear, quadratic, scatter, simultaneous equations, transformations on a grid | **JSXGraph** via `VMANZ.board()` | Accurate, crisp, zoomable; add a slider to make it interactive |
| Geometry figures, number lines, box plots, tree diagrams, bar charts, nets, formula triangles | **Inline SVG** with the `dg-*` classes | Lightweight, prints well, follows light/dark mode, and Claude can draw these directly |
| An applet you already built in GeoGebra | GeoGebra embed (`<iframe>` from geogebra.org) | Use sparingly: heavy to load and styled differently |
| A diagram you'd rather draw in TikZ | Compile to SVG (`dvisvgm`), save as `diagram.svg` in the subtopic folder, use `<img>` | Fine, but it won't switch to dark mode, so give it a white background |

Avoid screenshots and scanned images of diagrams: blurry on phones, and
unreadable to screen readers.

### Inline SVG

```html
<figure class="diagram">
  <svg viewBox="0 0 320 220" role="img" aria-label="Describe the diagram in words">
    <polygon class="dg-fill" points="40,180 280,180 40,30"/>
    <text class="dg-label" x="160" y="205" text-anchor="middle">4 cm</text>
  </svg>
  <figcaption>Caption, can include \(maths\).</figcaption>
</figure>
```

Classes: `dg-line` (main lines), `dg-thin` (right-angle marks, ticks),
`dg-grid`, `dg-accent` (the thing to notice), `dg-fill` (shaded shape),
`dg-dot`, `dg-label` (+ `muted` / `accent`), `dg-soft` (plain shape, paper
fill), `dg-var` (add to a label for an italic maths letter like *x*).
Never hard-code colours, so diagrams stay readable in dark mode. Always
include `aria-label`. Worked examples: `year-9/measurement/pythagoras-theorem/`.

### JSXGraph

Any page containing a `jxgbox` loads JSXGraph automatically on the next build.
Always use `VMANZ.graph(id, options, draw)`. It also works for graphs inside a
closed "Show solution", which would otherwise draw at zero size.

```html
<div id="graph-1" class="jxgbox" role="img" aria-label="Describe the graph in words"></div>
<script>
document.addEventListener("DOMContentLoaded", function () {
  VMANZ.graph("graph-1", { x: [-5, 5], y: [-5, 5] }, function (b) {
    VMANZ.vline(b, 1);                                        // dashed line x = 1
    VMANZ.plot(b, function (x) { return x * x - 2 * x - 3; }); // the curve
    VMANZ.point(b, [3, 0], "(3, 0)");                          // labelled point
    VMANZ.point(b, [-1, 0], "(−1, 0)", { label: { offset: [-52, 14] } }); // label moved left
  });
});
</script>
```

| Helper | Does |
|---|---|
| `VMANZ.plot(b, fn)` | draws \(y = f(x)\) in the site green |
| `VMANZ.point(b, [x, y], "label", opts)` | fixed, labelled point; `opts.label.offset` moves the label (pixels) |
| `VMANZ.vline(b, k)` | dashed vertical line \(x = k\) (axis of symmetry, asymptote) |
| `VMANZ.slider(b, "a", [min, start, max], row, step)` | slider in the top-left; read it with `a.Value()` |

Each graph on a page needs its own `id`. Options: `x`, `y` (ranges), `step`
(tick spacing), `square: true` (equal scales, for geometry), `zoom: true`
(pan and zoom buttons). Worked examples, including a slider explorer:
`year-10/algebra/quadratic-graphs/`.

## House style

* New Zealand spelling (colour, metre, centre); `−` minus sign in plain text.
* Short paragraphs; one idea per `.note`.
* Worked examples go easiest first; every step on its own line.
* "Try these" answers go in one `details.solution` at the end, not under each question.
* Write for the student, not the teacher: "you" not "students".

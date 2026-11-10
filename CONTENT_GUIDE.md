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
   Then run `python3 tools/check_answers.py`: it substitutes numbers into every exercise question and its answer where both are a single expression (expanding, factorising, simplifying) and lists any that don't match. Worded answers still need checking by hand.
4. Preview: `python3 -m http.server 8765`, then open http://localhost:8765
5. Commit and push. GitHub Pages updates the live site in about a minute.

### Adding or renaming a subtopic

Edit `curriculum.json`, then run the build. New pages are created; existing
notes are never overwritten. If you **rename** a subtopic, its web address
changes too. Either give it `"slug"` with the old address, or move the old
folder to the new name before building, or you will get a fresh empty page.

## Each subtopic is a textbook chapter

The site is an electronic textbook. A printed course would be about 300 pages,
so each subtopic page is a chapter of roughly **8 printed pages (3,000–5,000
words)**. Every chapter follows the same structure, in this order. Model
chapters: `year-9/algebra/expanding-two-brackets/`,
`year-9/measurement/pythagoras-theorem/`, `year-10/algebra/quadratic-graphs/`.

| Section | What goes in it | Size |
|---|---|---|
| What you'll learn | "I can …" statements | 4–6 |
| Before you start | warm-up on prior skills, with answers and links back | 4–6 questions |
| Key words | `dl.keywords` | 4–8 terms |
| 1., 2., 3. … | numbered teaching sections: explanation, `.note`/`.rule`, a diagram or graph, worked examples, then a `.check` | 4–9 sections; 8–14 worked examples in total |
| Exercise A · Practice | fluency, grouped by type with `h3`s, in columns | 20–30 questions |
| Exercise B · Apply | problems and contexts, multi-part with `ol.parts` | 8–10 questions |
| Exercise C · Challenge | extension, proof, puzzles | 4–6 questions |
| Common mistakes | `.warn` boxes with short labels | 3–4 |
| Summary | `.summary` bullet list | 5–7 points |
| Check-in | mixed end-of-chapter questions covering every section | 6–8 questions |
| Where next? | links to related chapters, this year and next | 2–3 links |

Every set of questions has its answers in a `details.solution` straight after
it. The "On this page" contents box is added automatically from the `h2`
headings. Worked examples are numbered automatically through the chapter.

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

```html
<dl class="keywords"><dt>Hypotenuse</dt><dd>The longest side…</dd></dl>

<div class="check"><span class="box-label">Quick check</span>
  <ol class="exercise cols-3"><li>…</li></ol>
  <details class="solution"><summary>Show answers</summary>
    <ol class="answers cols-3"><li>…</li></ol></details>
</div>

<div class="investigate"><span class="box-label">Investigate</span> <p>…</p></div>
<div class="summary"><ul><li>…</li></ul></div>

<section class="block exercise">
  <h2>Exercise A <span class="level">Practice</span></h2>
  <h3>Group heading</h3>
  <ol class="exercise cols-3"><li>…</li></ol>
  <ol class="exercise cols-3" start="10"><li>…</li></ol>   <!-- carry numbering on -->
  <ol class="exercise"><li>Question with parts
    <ol class="parts"><li>(a)…</li><li>(b)…</li></ol></li></ol>
  <details class="solution"><summary>Show answers</summary>
    <ol class="answers cols-3"><li>…</li></ol></details>
</section>
```

`cols-2`, `cols-3`, `cols-4` set the number of columns on a computer; phones
drop to fewer automatically. Use columns for short questions only.

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
| `VMANZ.slider(b, "a", [min, start, max], row, step)` | slider in a panel under the graph (easy to drag on a phone, never covers the curve); read it with `a.Value()`. `row` is ignored; `step` is how far each notch moves |
| `VMANZ.segment(b, [x1, y1], [x2, y2], opts)` | line segment |
| `VMANZ.text(b, [x, y], "t (s)")` | text on the board, e.g. axis names |
| `VMANZ.readout(b, "id", fn)` | live equation above the graph that updates as sliders move (see below) |

Each graph on a page needs its own `id`. Options: `x`, `y` (ranges), `step`
(tick spacing, a number or `[xStep, yStep]`), `square: true` (equal scales,
for geometry), `zoom: true` (pan and zoom buttons). Several curves on one
graph: give each a colour (`{ strokeColor: c.rule }`, `c.warn`, `c.muted`)
and add a key underneath with `<p class="legend"><span class="key key-rule">…</span></p>`.

### Interactive explorers with a live equation

Put an empty `.readout` div straight above the graph. In the draw function,
return the equation (and any feature rows) as TeX built from the slider
values; `VMANZ.tex` has helpers so signs and 1s come out right:
`tex.poly([[a, "x^2"], [b, "x"], [c, ""]])` gives `2x^2 - 3x + 1`,
`tex.shift(h)` gives `(x - 3)` or `(x + 2)`, `tex.pair(x, y)` a coordinate,
`tex.num(n)` a tidy number.

```html
<div id="ex-eq" class="readout"></div>
<div id="ex" class="jxgbox" role="img" aria-label="…"></div>
<script>
document.addEventListener("DOMContentLoaded", function () {
  VMANZ.graph("ex", { x: [-7, 7], y: [-7, 7], step: 2 }, function (b) {
    var T = VMANZ.tex, m = VMANZ.slider(b, "m", [-3, 1, 3], 0, 0.5), c = VMANZ.slider(b, "c", [-5, 0, 5], 1, 1);
    VMANZ.plot(b, function (x) { return m.Value() * x + c.Value(); });
    VMANZ.readout(b, "ex-eq", function () {
      return { eq: "y = " + T.poly([[m.Value(), "x"], [c.Value(), ""]]),
               rows: [["Gradient", T.num(m.Value())], ["<i>y</i>-intercept", T.num(c.Value())]] };
    });
  });
});
</script>
```

Full examples (two explorers): `year-10/algebra/quadratic-graphs/`.

## House style

* New Zealand spelling (colour, metre, centre); `−` minus sign in plain text.
* Short paragraphs; one idea per `.note`.
* Worked examples go easiest first; every step on its own line.
* Exercise answers go in one `details.solution` at the end of each exercise, not under each question.
* Give every number answer its units, and say how to round (e.g. "to 3 significant figures").
* Check every answer twice. Where a value can be checked another way (substitution, a second method), show the check.
* Write for the student, not the teacher: "you" not "students".

# VMANZ Maths: to-do list

`PROGRESS.md` ticks itself off as pages are finished (run `python3 tools/build.py`).
This file is the plan for getting there.

## Phase 0: decisions before writing (one sitting)

- [ ] Check the Year 9 and Year 10 topic lists in `curriculum.json` against the department scheme.
      They came from the King's Maths skill catalogue. Year 10 Geometry has only *Similar shapes*:
      add congruence, enlargement, bearings, or circle geometry if taught?
- [ ] Decide each subtopic's order within a topic (it drives the previous/next links).
- [ ] Push the skeleton and check https://nzvman.github.io/Maths-Help-Site/ on a phone.
- [ ] Optional: custom domain (e.g. a vmanz domain) via a `CNAME` file and the repo's Pages settings.

## Phase 1: three pilot pages to set the house style

Write these fully first, review on a phone and in print, and adjust `CONTENT_GUIDE.md` before mass-producing.

- [x] Year 9 › Algebra › **Expanding two brackets**: maths-heavy (area model SVG, grid method tables)
- [x] Year 9 › Measurement › **Pythagoras' theorem**: diagram-heavy (inline SVG triangles, squares proof, ladder)
- [x] Year 10 › Algebra › **Quadratic graphs**: graph-heavy (JSXGraph features graph, a/h/k slider explorer)
- [ ] Review the three pilots (content level, wording, length) and note any house-style changes here

## Definition of done for every subtopic page

- [ ] 2–4 "I can…" learning goals
- [ ] Key ideas: short explanation, vocabulary, rule/formula in a `.rule` box
- [ ] 2–3 worked examples, easiest first, step-by-step hidden solutions
- [ ] 1–2 common mistakes (`.warn`)
- [ ] 4–8 "Try these" questions with answers
- [ ] The visual(s) listed below
- [ ] Checked on a phone and in dark mode, with no red KaTeX errors
- [ ] `<!-- vmanz:placeholder -->` deleted, build run

## Phase 2: Year 9 (38 pages)

Suggested order follows a typical teaching year. **Visual** = what the page needs.

### Number
- [ ] Directed number (visual: SVG number line)
- [ ] Fractions of amounts (visual: SVG bar model)
- [ ] Percentages (visual: SVG percentage bar)
- [ ] Sharing in a ratio (visual: SVG bar model)
- [ ] Best buys (visual: comparison table)
- [ ] Indices (visual: table of index laws)
- [ ] Standard form (visual: place-value table)
- [ ] GST and simple interest (visual: worked receipt table)

### Algebra
- [ ] Collecting like terms
- [ ] Expanding single brackets (visual: grid-method table)
- [ ] Expanding two brackets (pilot)
- [ ] Factorising
- [ ] Substitution into formulae
- [ ] Linear equations (visual: balance diagram SVG)
- [ ] Rearranging formulae
- [ ] Linear inequalities (visual: SVG number lines)
- [ ] Arithmetic sequences (visual: SVG pattern + table)
- [ ] Gradient (visual: JSXGraph rise/run triangle)
- [ ] Linear graphs (visual: table of values + JSXGraph)
- [ ] Simultaneous equations (visual: JSXGraph two lines crossing)

### Measurement
- [ ] Perimeter (visual: SVG shapes)
- [ ] Area (visual: SVG rectangle/triangle/parallelogram/trapezium)
- [ ] Compound area (visual: SVG L-shapes, split and subtract)
- [ ] Unit conversion (visual: conversion ladder SVG)
- [ ] Pythagoras' theorem (pilot)
- [ ] Speed, distance and time (visual: formula triangle SVG)

### Geometry
- [ ] Angle facts (visual: SVG angles on a line, at a point, in a triangle)
- [ ] Parallel lines (visual: SVG corresponding/alternate/co-interior)
- [ ] Coordinates (visual: JSXGraph grid with points)
- [ ] Reflections and rotations (visual: JSXGraph or SVG grid with shapes)
- [ ] 3D shapes and nets (visual: SVG nets)

### Statistics
- [ ] Averages (visual: frequency table)
- [ ] Charts (visual: SVG bar chart, dot plot, stem-and-leaf table)
- [ ] Five-number summary (visual: ordered data with quartiles marked)
- [ ] Box plots (visual: SVG box plot on a scale)

### Probability
- [ ] Probability (visual: SVG probability scale 0–1)
- [ ] Complementary and mutually exclusive events (visual: SVG Venn diagram)
- [ ] Experimental probability (visual: tally/frequency table)

## Phase 3: Year 10 (21 pages)

### Number
- [ ] Compound percentages (visual: multiplier table)
- [ ] Calculating in standard form
- [ ] Surds (visual: rules table)
- [ ] Significant figures (visual: annotated number)
- [ ] Compound interest and currency (visual: year-by-year table)

### Algebra
- [ ] Expanding (ax + b)(cx + d) (visual: grid-method table)
- [ ] Factorising ax² + bx + c (visual: grid/AC-method table)
- [ ] Rearranging formulae with powers and roots
- [ ] Simultaneous equations (visual: JSXGraph)
- [ ] Solving quadratic equations (visual: JSXGraph roots)
- [ ] Equation of a line (visual: JSXGraph)
- [ ] Quadratic graphs (pilot)

### Measurement
- [ ] Circles (visual: SVG circle parts, sectors)
- [ ] Trigonometry (visual: SVG labelled triangle O/A/H)
- [ ] Prism, pyramid and cylinder volume (visual: SVG solids)
- [ ] Surface area (visual: SVG nets)
- [ ] Scale factors for area and volume (visual: SVG similar solids + table)

### Geometry
- [ ] Similar shapes (visual: SVG pairs of similar triangles)

### Statistics
- [ ] Scatter graphs (visual: JSXGraph scatter + line of best fit)
- [ ] Sampling and inference (visual: SVG side-by-side box plots)

### Probability
- [ ] Tree diagrams (visual: SVG tree diagram)

## Phase 4: senior courses

Each is a "Coming soon" card on the home page. To open one: change its `status` to
`"live"` in `curriculum.json`, add its `topics`, then build.

- [ ] Cambridge IGCSE (0580): topic list from the syllabus
- [ ] NCEA Level 1, 2, 3: topic list by standard
- [ ] Cambridge AS / A Level (9709): Pure 1, Pure 3, Mechanics, Probability & Statistics

## Phase 5: nice to have

- [ ] "Builds on" links between Year 9 and Year 10 versions of the same idea
- [ ] Site search (e.g. Pagefind, which runs on a static site)
- [ ] Printable one-page summary per topic
- [ ] Accessibility check (screen reader on a full page, contrast in both themes)
- [ ] Simple, privacy-friendly visit counts, if wanted

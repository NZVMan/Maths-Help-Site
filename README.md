# VMANZ Maths

Maths notes and worked examples, brought to you by VMANZ.
Live at https://nzvman.github.io/Maths-Help-Site/ (GitHub Pages, `main` branch).

Plain static HTML: no framework and no build service. A small Python script
turns `curriculum.json` into the page structure:

```
Home  →  Course (Year 9, Year 10, …)  →  Topic (Number, Algebra, …)  →  Subtopic (notes)
```

```bash
python3 tools/build.py          # create/refresh pages after any change
python3 -m http.server 8765     # preview at http://localhost:8765
```

* **Writing notes:** see `CONTENT_GUIDE.md`, and `guide/index.html` for every component.
* **What's left:** `TODO.md` (the plan) and `PROGRESS.md` (auto-generated tick list).
* **Maths:** KaTeX. **Graphs:** JSXGraph. **Diagrams:** inline SVG.

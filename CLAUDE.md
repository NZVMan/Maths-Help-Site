# VMANZ Maths site

Static GitHub Pages site. Branding is **VMANZ** only. Keep it separate from Sum Revision
(no blue/purple gradients, no sigma logo, no "Sum Revision" wording).

* Site map: `curriculum.json`. After any change run `python3 tools/build.py`.
* Never hand-edit home, course or topic pages; they are regenerated.
* On subtopic pages only edit between `<!-- vmanz:content:start -->` and `<!-- vmanz:content:end -->`.
* Follow `CONTENT_GUIDE.md` (KaTeX with `\( \)` / `\[ \]`, never single `$`; SVG with `dg-*` classes; JSXGraph via `VMANZ.board`).
* When a page is finished, delete `<!-- vmanz:placeholder -->` and rebuild. Tick-list: `PROGRESS.md`; plan: `TODO.md`.
* Preview: `python3 -m http.server 8765`. Check phone width and dark mode.

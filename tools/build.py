#!/usr/bin/env python3
"""Build the VMANZ Maths site from curriculum.json.

    python3 tools/build.py

What it does:
  * Rewrites the home page, every course page and every topic page (these are
    purely structural, so never edit them by hand).
  * Creates any subtopic page that does not exist yet, using the notes template.
  * For subtopic pages that already exist, rewrites ONLY the frame around your
    notes (header, breadcrumbs, previous/next links, footer). Everything between
        <!-- vmanz:content:start -->  and  <!-- vmanz:content:end -->
    is kept exactly as you wrote it.
  * Writes PROGRESS.md: a tick list of which subtopics have notes.

A subtopic counts as "coming soon" while its content still contains the line
    <!-- vmanz:placeholder -->
Delete that line once real notes are in, then rebuild.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "curriculum.json").read_text(encoding="utf-8"))
SITE = DATA["site"]

KATEX = "0.16.11"
JSXGRAPH = "1.10.1"

START, END = "<!-- vmanz:content:start -->", "<!-- vmanz:content:end -->"
PLACEHOLDER = "<!-- vmanz:placeholder -->"

def asset_version(rel: str) -> str:
    """Short content hash, so browsers fetch the new file whenever it changes."""
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]


CSS_V = asset_version("assets/css/site.css")
JS_V = asset_version("assets/js/site.js")

# Extra hand-written pages that use the same frame (path, title).
EXTRA_PAGES = [("guide", "Page components")]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def slugify(title: str) -> str:
    s = title.lower().replace("²", "2").replace("³", "3").replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def norm_sub(entry) -> dict:
    if isinstance(entry, str):
        return {"title": entry, "slug": slugify(entry)}
    return {"title": entry["title"], "slug": entry.get("slug") or slugify(entry["title"])}


# ---------------------------------------------------------------- frame ----

def head(title: str, root: str, description: str, maths: bool = False, jsx: bool = False) -> str:
    full = title if title == SITE["name"] else f"{title} · {SITE['name']}"
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en-NZ">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(full)}</title>",
        f'<meta name="description" content="{esc(description)}">',
        f'<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Fraunces:opsz,wght@9..144,600;9..144,800&display=swap">',
    ]
    if maths:
        parts += [
            f'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@{KATEX}/dist/katex.min.css">',
            f'<script defer src="https://cdn.jsdelivr.net/npm/katex@{KATEX}/dist/katex.min.js"></script>',
            f'<script defer src="https://cdn.jsdelivr.net/npm/katex@{KATEX}/dist/contrib/auto-render.min.js"></script>',
        ]
    if jsx:
        parts += [
            f'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jsxgraph@{JSXGRAPH}/distrib/jsxgraph.css">',
            f'<script src="https://cdn.jsdelivr.net/npm/jsxgraph@{JSXGRAPH}/distrib/jsxgraphcore.js"></script>',
        ]
    parts += [
        f'<link rel="stylesheet" href="{root}assets/css/site.css?v={CSS_V}">',
        f'<script defer src="{root}assets/js/site.js?v={JS_V}"></script>',
        "</head>",
    ]
    return "\n".join(parts)


def header(root: str) -> str:
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="wordmark" href="{root}index.html" aria-label="{esc(SITE['name'])} home">
      <span class="wordmark-mark" aria-hidden="true">V</span>
      <span class="wordmark-text"><strong>{esc(SITE['brand'])}</strong> Maths</span>
    </a>
    <nav class="header-nav" aria-label="Courses">
{course_links(root)}
    </nav>
  </div>
</header>"""


def course_links(root: str) -> str:
    out = []
    for c in DATA["courses"]:
        if c["status"] == "live":
            out.append(f'      <a href="{root}{c["slug"]}/index.html">{esc(c["title"])}</a>')
    return "\n".join(out)


def footer(root: str) -> str:
    return f"""<footer class="site-footer">
  <div class="wrap footer-inner">
    <p class="byline"><span class="wordmark-mark small" aria-hidden="true">V</span> {esc(SITE['byline'])}</p>
    <p class="footer-links"><a href="{root}index.html">All courses</a> · <a href="{root}guide/index.html">Page components</a></p>
  </div>
</footer>
</body>
</html>
"""


def crumbs(root: str, trail: list[tuple[str, str | None]]) -> str:
    items = [f'<li><a href="{root}index.html">Home</a></li>']
    for label, href in trail:
        if href:
            items.append(f'<li><a href="{href}">{esc(label)}</a></li>')
        else:
            items.append(f'<li aria-current="page">{esc(label)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


# ---------------------------------------------------------------- model ----

def live_courses():
    return [c for c in DATA["courses"] if c["status"] == "live"]


def topics_of(course):
    for t in course.get("topics", []):
        t.setdefault("slug", slugify(t["title"]))
        for g in t["groups"]:
            g["subs"] = [norm_sub(s) for s in g["subtopics"]]
        yield t


def subs_of(topic):
    for g in topic["groups"]:
        yield from g["subs"]


def sub_path(course, topic, sub) -> Path:
    return ROOT / course["slug"] / topic["slug"] / sub["slug"] / "index.html"


def is_ready(course, topic, sub) -> bool:
    p = sub_path(course, topic, sub)
    if not p.exists():
        return False
    return PLACEHOLDER not in p.read_text(encoding="utf-8")


# ---------------------------------------------------------------- pages ----

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old != text:
        path.write_text(text, encoding="utf-8")


def build_home():
    root = ""
    cards = []
    for c in DATA["courses"]:
        live = c["status"] == "live"
        if live:
            topics = list(topics_of(c))
            n_sub = sum(len(list(subs_of(t))) for t in topics)
            meta = f"{len(topics)} topics · {n_sub} subtopics"
            cards.append(f"""      <li class="course-card">
        <a href="{c['slug']}/index.html">
          <span class="eyebrow">{esc(c.get('label', ''))}</span>
          <span class="course-title">{esc(c['title'])}</span>
          <span class="course-blurb">{esc(c.get('blurb', ''))}</span>
          <span class="course-meta">{meta}</span>
        </a>
      </li>""")
        else:
            cards.append(f"""      <li class="course-card is-soon">
        <div>
          <span class="eyebrow">{esc(c.get('label', ''))}</span>
          <span class="course-title">{esc(c['title'])}</span>
          <span class="course-blurb">{esc(c.get('blurb', ''))}</span>
          <span class="badge">Coming soon</span>
        </div>
      </li>""")
    body = f"""<main id="main" class="wrap">
  <section class="hero">
    <p class="eyebrow">{esc(SITE['byline'])}</p>
    <h1>Maths, one step at a time.</h1>
    <p class="lede">{esc(SITE['tagline'])} Pick your course, choose a topic, then work through the notes and examples.</p>
  </section>
  <section aria-labelledby="courses-h">
    <h2 id="courses-h" class="section-h">Courses</h2>
    <ul class="course-grid">
{chr(10).join(cards)}
    </ul>
  </section>
</main>"""
    write(ROOT / "index.html", "\n".join([head(SITE["name"], root, SITE["tagline"]), header(root), body, footer(root)]))


def build_course(course):
    root = "../"
    topics = list(topics_of(course))
    cards = []
    for t in topics:
        subs = list(subs_of(t))
        ready = sum(is_ready(course, t, s) for s in subs)
        cards.append(f"""      <li class="topic-card">
        <a href="{t['slug']}/index.html">
          <span class="topic-title">{esc(t['title'])}</span>
          <span class="topic-blurb">{esc(t.get('blurb', ''))}</span>
          <span class="progress" style="--done:{ready};--total:{len(subs)}"><span class="progress-bar"></span><span class="progress-text">{ready} of {len(subs)} ready</span></span>
        </a>
      </li>""")
    body = f"""<main id="main" class="wrap">
  {crumbs(root, [(course['title'], None)])}
  <header class="page-head">
    <p class="eyebrow">{esc(course.get('label', ''))}</p>
    <h1>{esc(course['title'])}</h1>
    <p class="lede">{esc(course.get('blurb', ''))}</p>
  </header>
  <ul class="topic-grid">
{chr(10).join(cards)}
  </ul>
</main>"""
    write(ROOT / course["slug"] / "index.html",
          "\n".join([head(course["title"], root, course.get("blurb", "")), header(root), body, footer(root)]))


def build_topic(course, topic):
    root = "../../"
    sections = []
    for g in topic["groups"]:
        rows = []
        for s in g["subs"]:
            ready = is_ready(course, topic, s)
            tag = "" if ready else '<span class="badge">Coming soon</span>'
            rows.append(f'        <li><a href="{s["slug"]}/index.html"><span>{esc(s["title"])}</span>{tag}</a></li>')
        sections.append(f"""    <section class="group">
      <h2>{esc(g['title'])}</h2>
      <ul class="sub-list">
{chr(10).join(rows)}
      </ul>
    </section>""")
    body = f"""<main id="main" class="wrap">
  {crumbs(root, [(course['title'], '../index.html'), (topic['title'], None)])}
  <header class="page-head">
    <p class="eyebrow">{esc(course['title'])}</p>
    <h1>{esc(topic['title'])}</h1>
    <p class="lede">{esc(topic.get('blurb', ''))}</p>
  </header>
  <div class="groups">
{chr(10).join(sections)}
  </div>
</main>"""
    write(ROOT / course["slug"] / topic["slug"] / "index.html",
          "\n".join([head(f"{topic['title']} · {course['title']}", root, topic.get("blurb", "")),
                     header(root), body, footer(root)]))


TEMPLATE = (ROOT / "tools" / "subtopic-template.html")


def existing_content(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    i, j = text.find(START), text.find(END)
    if i == -1 or j == -1:
        sys.exit(f"ERROR: {path.relative_to(ROOT)} is missing its vmanz:content markers - not touching it.")
    return text[i + len(START):j]


def framed_page(path: Path, title: str, root: str, description: str, crumb_html: str,
                eyebrow: str, content: str, pager: str = "") -> str:
    jsx = "jxgbox" in content
    body = f"""<main id="main" class="wrap narrow">
  {crumb_html}
  <header class="page-head">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h1>{esc(title)}</h1>
  </header>
  <article class="notes">
{START}{content}{END}
  </article>
{pager}
</main>"""
    return "\n".join([head(title, root, description, maths=True, jsx=jsx), header(root), body, footer(root)])


def build_subtopics(course):
    root = "../../../"
    flat = [(t, s) for t in topics_of(course) for s in subs_of(t)]
    for i, (topic, sub) in enumerate(flat):
        path = sub_path(course, topic, sub)
        content = existing_content(path)
        if content is None:
            content = "\n" + TEMPLATE.read_text(encoding="utf-8").replace("{{TITLE}}", sub["title"]) + "\n"
        prev_link = next_link = "<span></span>"
        if i > 0:
            pt, ps = flat[i - 1]
            prev_link = (f'<a class="pager-prev" href="../../{pt["slug"]}/{ps["slug"]}/index.html">'
                         f'<span class="pager-dir">Previous</span><span>{esc(ps["title"])}</span></a>')
        if i < len(flat) - 1:
            nt, ns = flat[i + 1]
            next_link = (f'<a class="pager-next" href="../../{nt["slug"]}/{ns["slug"]}/index.html">'
                         f'<span class="pager-dir">Next</span><span>{esc(ns["title"])}</span></a>')
        pager = f'  <nav class="pager" aria-label="Previous and next">{prev_link}{next_link}</nav>'
        crumb_html = crumbs(root, [(course["title"], "../../index.html"),
                                   (topic["title"], "../index.html"), (sub["title"], None)])
        write(path, framed_page(path, sub["title"], root,
                                f"{sub['title']} - {course['title']} {topic['title']} notes and worked examples.",
                                crumb_html, f"{course['title']} · {topic['title']}", content, pager))


def build_extras():
    for folder, title in EXTRA_PAGES:
        path = ROOT / folder / "index.html"
        content = existing_content(path)
        if content is None:
            content = f"\n<p>{esc(title)}</p>\n"
        crumb_html = crumbs("../", [(title, None)])
        write(path, framed_page(path, title, "../", title, crumb_html, "For authors", content))


def build_progress():
    lines = ["# Progress", "", "Generated by `python3 tools/build.py` - do not edit by hand.",
             "A box is ticked once the subtopic page no longer contains `<!-- vmanz:placeholder -->`.", ""]
    grand_done = grand_total = 0
    for c in live_courses():
        lines.append(f"## {c['title']}")
        for t in topics_of(c):
            subs = list(subs_of(t))
            done = sum(is_ready(c, t, s) for s in subs)
            grand_done += done
            grand_total += len(subs)
            lines.append(f"\n### {t['title']} ({done}/{len(subs)})\n")
            for s in subs:
                tick = "x" if is_ready(c, t, s) else " "
                lines.append(f"- [{tick}] [{s['title']}]({c['slug']}/{t['slug']}/{s['slug']}/index.html)")
        lines.append("")
    lines.insert(4, f"**{grand_done} of {grand_total} subtopics have notes.**\n")
    write(ROOT / "PROGRESS.md", "\n".join(lines) + "\n")
    return grand_done, grand_total


def main():
    for c in live_courses():
        build_subtopics(c)          # subtopics first so "ready" counts are current
        build_course(c)
        for t in topics_of(c):
            build_topic(c, t)
    build_extras()
    build_home()
    done, total = build_progress()
    print(f"Built. {done} of {total} subtopics have notes. See PROGRESS.md.")


if __name__ == "__main__":
    main()

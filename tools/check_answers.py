#!/usr/bin/env python3
"""Check exercise answers by substituting numbers.

    python3 tools/check_answers.py                 # every finished chapter
    python3 tools/check_answers.py year-9/algebra/factorising/index.html

For every list of questions (<ol class="exercise">) followed by its answers
(<details class="solution"> containing <ol class="answers">), questions and
answers are paired up in order. Where BOTH are a single maths expression, such
as "\\((x + 2)(x + 3)\\)" and "\\(x^2 + 5x + 6\\)", random numbers are put in
for every letter and the two sides are compared. Worded questions and answers,
equations and multi-part questions are skipped, so check those by hand.

This catches slips in expanding, factorising and simplifying answers. It
cannot tell whether an answer is in the form the question asked for (for
example "factorise fully").
"""
from __future__ import annotations

import random
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- vmanz:content:start -->", "<!-- vmanz:content:end -->"


class Lists(HTMLParser):
    """Collects, in page order, ('q', items) for ol.exercise and ('a', items) for ol.answers."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack = [], []   # stack of [kind, items, depth_of_li]

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "") or ""
        if tag == "ol":
            kind = "q" if "exercise" in cls.split() else "a" if "answers" in cls.split() else None
            self.stack.append([kind, [], None, 0])
        elif tag == "li" and self.stack:
            top = self.stack[-1]
            top[3] += 1
            if top[3] == 1:
                top[1].append("")
        if self.stack and tag not in ("ol", "li"):
            pass

    def handle_endtag(self, tag):
        if tag == "ol" and self.stack:
            kind, items, _, _ = self.stack.pop()
            if kind:
                self.out.append((kind, [i.strip() for i in items]))
            if self.stack:          # nested list: mark the parent item as multi-part
                p = self.stack[-1]
                if p[1]:
                    p[1][-1] += " [parts]"
        elif tag == "li" and self.stack:
            self.stack[-1][3] -= 1

    def handle_data(self, data):
        if self.stack and self.stack[-1][1] and self.stack[-1][3] >= 1:
            self.stack[-1][1][-1] += data


def to_python(tex: str) -> str | None:
    s = tex.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
    for _ in range(5):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    for a, b in [("\\times", "*"), ("\\div", "/"), ("\\cdot", "*"), ("−", "-"), ("\\left", ""),
                 ("\\right", ""), ("\\,", ""), ("{", "("), ("}", ")"), ("^", "**"), (" ", "")]:
        s = s.replace(a, b)
    if "\\" in s or not re.fullmatch(r"[0-9a-z+\-*/().]+", s):
        return None
    s = re.sub(r"(?<=[0-9a-z)])(?=[a-z(])", "*", s)
    s = re.sub(r"(?<=\))(?=[0-9])", "*", s)
    return s


def expression(text: str) -> str | None:
    m = re.fullmatch(r"\\\((.*)\\\)", text.strip(), re.S)
    if not m or "\\(" in m.group(1) or "=" in m.group(1) or "[parts]" in text:
        return None
    return to_python(m.group(1))


def equal(p: str, q: str) -> bool:
    rng = random.Random(1)
    for _ in range(4):
        env = {c: rng.choice([2, 3, 5, 7, -3, 1.5, 0.4]) * rng.choice([1, 1.1]) for c in "abcdefghijklmnopqrstuvwxyz"}
        x, y = eval(p, {}, env), eval(q, {}, env)
        if abs(x - y) > 1e-9 * max(1, abs(x), abs(y)):
            return False
    return True


def check(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    if START in text:
        text = text[text.index(START):text.index(END)]
    parser = Lists()
    parser.feed(text)
    checked = bad = 0
    questions: list[str] = []
    for kind, items in parser.out:
        if kind == "q":
            questions += items
            continue
        for n, (q, a) in enumerate(zip(questions, items), 1):
            pq, pa = expression(q), expression(a)
            if pq is None or pa is None:
                continue
            try:
                ok = equal(pq, pa)
            except Exception:
                continue
            checked += 1
            if not ok:
                bad += 1
                print(f"  MISMATCH  {path.relative_to(ROOT)}  Q{n}:  {q}   answer: {a}")
        questions = []
    return checked, bad


def main():
    if len(sys.argv) > 1:
        pages = [Path(p).resolve() for p in sys.argv[1:]]
    else:
        pages = [p for p in sorted(ROOT.glob("year-*/*/*/index.html"))
                 if "<!-- vmanz:placeholder -->" not in p.read_text(encoding="utf-8")]
    total = wrong = 0
    for p in pages:
        c, b = check(p)
        total += c
        wrong += b
        print(f"{p.relative_to(ROOT)}: {c} answers checked, {b} wrong")
    print(f"\n{total} answers checked, {wrong} wrong.")
    sys.exit(1 if wrong else 0)


if __name__ == "__main__":
    main()

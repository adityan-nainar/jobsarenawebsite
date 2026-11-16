#!/usr/bin/env python3
"""Builds the Mr AI Decoder site: src/*.html templates -> public/*.html.

    python src/build.py

Placeholders in a template:
  {{HEAD title | description}}   <head> with fonts, styles, favicon and share tags
  {{HEADER page}}                site header; page = home | ep | method (marks the current link)
  {{FOOTER}}                     site footer
  {{SVG name}}                   inline character drawing from src/art/<name>.svg
                                 (drawn from studio/world/guy.js and claude.js; use each one once per page)
Pure static output: no build step on Cloudflare, publish the public/ folder as it is.
"""
import html, pathlib, re

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent / "public"
IG = "https://www.instagram.com/mr.ai.decoder/"


def head(title, desc):
    t, d = html.escape(title), html.escape(desc)
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#F4F4F2">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/inter-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">
</head>"""


def header(page, svg):
    cur = lambda p: ' aria-current="page"' if p == page else ""
    return f"""<header class="site-head"><div class="wrap">
  <a class="brand" href="index.html"><span class="duo" aria-hidden="true"><span>{svg('chad_head')}</span><span>{svg('claude_head')}</span></span>Mr AI Decoder</a>
  <nav class="site-nav" aria-label="Main">
    <a href="ep5.html"{cur('ep')}>Latest check</a>
    <a href="index.html#files">Free files</a>
    <a href="method.html"{cur('method')}>Method</a>
    <a class="btn follow" href="{IG}" rel="noopener">Follow</a>
  </nav>
</div></header>"""


FOOTER = f"""<footer class="site-foot"><div class="wrap">
  <p><b>Mr AI Decoder</b> · claim checks on AI and jobs · <a href="{IG}" rel="noopener">@mr.ai.decoder on Instagram</a></p>
  <p>Chad and Claude are our animated characters. Independent page, not affiliated with Anthropic or with any organisation whose claims we check.</p>
  <p>Spot a mistake? DM us on Instagram. We fix it and note the change on the page.</p>
</div></footer>"""


def build():
    used = {}

    def svg(name):
        used[name] = used.get(name, 0) + 1
        return (SRC / "art" / f"{name}.svg").read_text(encoding="utf-8").strip()

    OUT.mkdir(exist_ok=True)
    for tpl in sorted(SRC.glob("*.html")):
        used.clear()
        s = tpl.read_text(encoding="utf-8")
        s = re.sub(r"\{\{HEAD (.+?) \| (.+?)\}\}", lambda m: head(m.group(1), m.group(2)), s)
        s = re.sub(r"\{\{HEADER (\w+)\}\}", lambda m: header(m.group(1), svg), s)
        s = s.replace("{{FOOTER}}", FOOTER).replace("{{IG}}", IG)
        s = re.sub(r"\{\{SVG (\w+)\}\}", lambda m: svg(m.group(1)), s)
        left = re.findall(r"\{\{[^}]*\}\}", s)
        if left:
            raise SystemExit(f"{tpl.name}: unfilled placeholders {left}")
        twice = [k for k, v in used.items() if v > 1]
        if twice:
            raise SystemExit(f"{tpl.name}: drawing used twice on one page {twice} (its gradient ids would clash)")
        if tpl.name == "404.html":          # served at any missing path, so resolve links from the site root
            s = s.replace("<head>", '<head>\n<base href="/">', 1)
        (OUT / tpl.name).write_text(s, encoding="utf-8")
        print("built", tpl.name)


if __name__ == "__main__":
    build()

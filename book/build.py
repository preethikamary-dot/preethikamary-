#!/usr/bin/env python3
"""
Builds everything for "Color & Smile!":

  print-ready/  KDP files: paperback + hardcover interiors and full-wrap covers,
                Kindle eBook cover (JPG) and Kindle interior (PDF)
  docs/         the free sales website (GitHub Pages) + interactive coloring app

Usage:
  python3 book/build.py                    # default spines
  python3 book/build.py --hc-spine 0.432   # paste the spine from KDP's hardcover cover calculator

Requires Python 3 and Node with Playwright (Chromium) for rendering.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from art import all_art  # noqa: E402

# ----------------------------------------------------------------- settings --
TITLE_1 = "Color"
TITLE_2 = "& Smile!"
SUBTITLE = "Big & Easy Coloring Book for Kids Ages 3-5"
AUTHOR = "Preethika Mary"
SITE_URL = "preethikamary-dot.github.io/preethikamary-"
YEAR = 2026

PAPER_FACTOR_WHITE = 0.002252   # KDP paperback, white paper, inches per page
PB_TRIM = (8.5, 11.0)           # paperback trim
HC_TRIM = (8.25, 11.0)          # KDP hardcover largest trim
BLEED = 0.125
HC_WRAP = 0.51
HC_HINGE = 0.4

COLORS = ["#ef476f", "#ff9f1c", "#ffd166", "#06d6a0", "#118ab2", "#8338ec"]
FONT = os.path.join(ROOT, "docs", "assets", "fonts", "fredoka.woff2")
BUILD = os.path.join(HERE, "build")
OUT = os.path.join(ROOT, "print-ready")
DOCS = os.path.join(ROOT, "docs")

ARTS = all_art()
BY = {a.title.lower(): a for a in ARTS}


def head(page_w=None, page_h=None, extra_css=""):
    size = f"@page {{ size: {page_w}in {page_h}in; margin: 0 }}" if page_w else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Fredoka; src: url('file://{FONT}') format('woff2'); font-weight: 300 700; }}
{size}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
html, body {{ font-family: Fredoka, sans-serif; color: #1d1d1f; -webkit-print-color-adjust: exact; print-color-adjust: exact }}
svg {{ display: block }}
{extra_css}
</style></head><body>"""


def rainbow_text(text, stroke="#fff"):
    out, i = [], 0
    for ch in text:
        if ch == " ":
            out.append(" ")
            continue
        out.append(f'<span style="color:{COLORS[i % len(COLORS)]}">{ch}</span>')
        i += 1
    return "".join(out)


# -------------------------------------------------------------------- covers --
COVER_CSS = """
.sky { position:absolute; inset:0; background:
   linear-gradient(160deg, #8ee3ff 0%, #b8f2ff 45%, #fff3b0 100%); }
.dots { position:absolute; inset:0; background-image: radial-gradient(#ffffff88 1.2px, transparent 1.6px); background-size: 0.32in 0.32in; }
.panel { position:absolute; display:flex; flex-direction:column; }
.title { font-weight:700; line-height:.9; text-align:center; letter-spacing:.02em;
   -webkit-text-stroke: .045in #fff; paint-order: stroke fill;
   filter: drop-shadow(0 .05in 0 #1d3557); }
.sub { align-self:center; background:#1d3557; color:#fff; font-weight:600; border-radius:999px; text-align:center; }
.cards { flex:1; display:grid; grid-template-columns:1fr 1fr; gap:.18in; min-height:0; }
.card { background:#fff; border-radius:.25in; border:.05in solid #1d3557; box-shadow:0 .07in 0 #1d3557; padding:.08in; display:flex; align-items:center; justify-content:center; overflow:hidden }
.card svg { width:100%; height:100%; }
.badge { position:absolute; border-radius:50%; background:#ef476f; color:#fff; font-weight:700; display:flex; flex-direction:column; align-items:center; justify-content:center; line-height:.95; border:.05in solid #fff; box-shadow:0 .05in 0 #1d3557; transform:rotate(12deg); text-align:center }
.ribbon { background:#ffd166; border:.04in solid #1d3557; border-radius:.2in; text-align:center; font-weight:600; color:#1d3557 }
.pub { text-align:center; font-weight:600; color:#1d3557 }
.back h2 { font-weight:700; color:#1d3557; line-height:1.05 }
.back p { color:#1d3557; line-height:1.35 }
.thumbs { display:grid; grid-template-columns:repeat(4,1fr); gap:.12in }
.thumbs div { background:#fff; border-radius:.14in; border:.035in solid #1d3557; padding:.04in }
.ticks { list-style:none; color:#1d3557; font-weight:600 }
.ticks li::before { content:"\\2605"; color:#ef476f; margin-right:.1in }
.spine { position:absolute; display:flex; align-items:center; justify-content:center; background:#1d3557; }
.spine span { transform:rotate(90deg); white-space:nowrap; color:#fff; font-weight:600 }
"""


def front_panel(x, y, w, h, s=1.0, safe_l=0.45, safe_r=0.45, safe_t=0.45, safe_b=0.45):
    """Front cover content inside a w x h (inch) panel at (x, y). s = size scale."""
    cards = "".join(
        f'<div class="card" style="transform:rotate({r}deg)">{BY[n].svg(colored=True, label=False)}</div>'
        for n, r in [("dinosaur", -3), ("cat", 2), ("rocket", 2), ("butterfly", -2)])
    return f"""
<div class="panel" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in;padding:{safe_t}in {safe_r}in {safe_b}in {safe_l}in;gap:{.16 * s}in">
  <div class="title" style="font-size:{1.55 * s}in">{rainbow_text(TITLE_1)}<br>{rainbow_text(TITLE_2)}</div>
  <div class="sub" style="font-size:{.25 * s}in;padding:{.08 * s}in {.3 * s}in">{SUBTITLE.replace(' for Kids', '<br>for Kids')}</div>
  <div class="cards" style="padding:{.1 * s}in {.15 * s}in">{cards}</div>
  <div class="ribbon" style="font-size:{.23 * s}in;padding:{.09 * s}in">50 Fun Pages &bull; Thick Lines &bull; Simple Shapes</div>
  <div class="pub" style="font-size:{.24 * s}in">by {AUTHOR}</div>
  <div class="badge" style="right:{safe_r - .05}in;top:{safe_t + 2.95 * s}in;width:{1.25 * s}in;height:{1.25 * s}in;font-size:{.22 * s}in">AGES<br><b style="font-size:{.42 * s}in">3-5</b></div>
</div>"""


def back_panel(x, y, w, h, safe_l=0.5, safe_r=0.5, safe_t=0.5, safe_b=0.5):
    thumbs = "".join(f"<div>{BY[n].svg(label=False)}</div>" for n in ("sun", "fish", "train", "teddy"))
    return f"""
<div class="panel back" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in;padding:{safe_t}in {safe_r}in {safe_b}in {safe_l}in;gap:.22in">
  <h2 style="font-size:.52in">Big, bold &amp; <span style="color:#ef476f">so</span> <span style="color:#118ab2">much</span> <span style="color:#8338ec">fun!</span></h2>
  <p style="font-size:.21in">Little hands love big pictures! <b>Color &amp; Smile!</b> is packed with 25 friendly characters &mdash;
  a smiling sun, a silly dinosaur, a zooming rocket and more &mdash; drawn with extra-thick lines and simple shapes
  that are perfect for toddlers and preschoolers just learning to hold a crayon.</p>
  <div class="thumbs">{thumbs}</div>
  <ul class="ticks" style="font-size:.21in;line-height:1.55">
    <li>25 cute designs &mdash; each printed twice (50 pages to color)</li>
    <li>Thick, bold outlines and big, easy spaces</li>
    <li>Single-sided pages &mdash; no bleed-through</li>
    <li>Name page, crayon test page &amp; a &ldquo;Great Job!&rdquo; certificate</li>
    <li>Builds fine-motor skills, focus &amp; color recognition</li>
  </ul>
  <div style="margin-top:auto;display:flex;align-items:flex-end;gap:.2in">
    <div style="flex:1;background:#fff;border:.035in solid #1d3557;border-radius:.18in;padding:.14in .18in;font-size:.17in;color:#1d3557;line-height:1.3">
      <b style="color:#ef476f">Bonus:</b> color every page on a tablet or computer for free at<br><b>{SITE_URL}</b></div>
    <div style="width:2.1in;height:1.3in;flex:none"></div><!-- KDP barcode area: keep clear -->
  </div>
</div>"""


def cover_doc(total_w, total_h, panels, pad=0.1):
    # canvas is drawn slightly oversize; the PDF MediaBox is cropped to the exact size afterwards
    return head(total_w + pad, total_h + pad, COVER_CSS) + f"""
<div style="position:relative;width:{total_w + pad}in;height:{total_h + pad}in;overflow:hidden">
  <div class="sky"></div><div class="dots"></div>{panels}
</div></body></html>"""


def spine_div(x, y, w, h, font_in):
    if w < 0.2:  # too thin for text
        return f'<div class="spine" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in"></div>'
    return (f'<div class="spine" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in">'
            f'<span style="font-size:{font_in}in">{TITLE_1.upper()} {TITLE_2.upper()} &nbsp;&bull;&nbsp; {AUTHOR.upper()}</span></div>')


def paperback_cover(pages):
    tw, th = PB_TRIM
    spine = round(pages * PAPER_FACTOR_WHITE, 4)
    W = round(BLEED + tw + spine + tw + BLEED, 4)
    H = round(th + 2 * BLEED, 4)
    sx = BLEED + tw
    font = max(0.08, min(0.3, (spine - 0.125) * 0.8))   # 0.0625" clear each side of spine text
    panels = (back_panel(BLEED, BLEED, tw, th)
              + spine_div(sx, 0, spine, H, font)
              + front_panel(sx + spine, BLEED, tw, th))
    return cover_doc(W, H, panels), W, H, spine


def hardcover_cover(pages, spine):
    tw, th = HC_TRIM
    W = round(HC_WRAP + tw + spine + tw + HC_WRAP, 4)
    H = round(th + 2 * HC_WRAP, 4)
    sx = HC_WRAP + tw
    font = max(0.08, min(0.3, (spine - 0.125) * 0.8))
    panels = (back_panel(HC_WRAP, HC_WRAP, tw, th, safe_r=HC_HINGE + 0.2)
              + spine_div(sx, 0, spine, H, font)
              + front_panel(sx + spine, HC_WRAP, tw, th, s=0.97, safe_l=HC_HINGE + 0.2))
    return cover_doc(W, H, panels), W, H


def front_only(w, h, s=1.0):
    return cover_doc(w, h, front_panel(0, 0, w, h, s))


def back_only(w, h):
    return cover_doc(w, h, back_panel(0, 0, w, h))


# ------------------------------------------------------------------ interior --
INTERIOR_CSS = """
.page { position:relative; overflow:hidden; page-break-after:always; break-after:page }
.art { position:absolute; inset:0.6in 0.6in 0.6in 0.6in; display:flex; align-items:center; justify-content:center }
.art svg { width:100%; height:100%; }
.c { text-align:center; color:#111 }
.big { font-weight:700; -webkit-text-stroke:.03in #111; color:#fff; paint-order:stroke fill; line-height:1 }
.note { position:absolute; left:0; right:0; bottom:.7in; text-align:center; color:#999; font-size:9pt }
"""


def page(w, h, inner):
    return f'<div class="page" style="width:{w}in;height:{h}in">{inner}</div>'


def p_title(w, h):
    return page(w, h, f"""
<div style="position:absolute;inset:1in .8in;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.35in" class="c">
  <div class="big" style="font-size:1.4in">{TITLE_1}<br>{TITLE_2}</div>
  <div style="font-size:.3in;font-weight:600">{SUBTITLE}</div>
  <div style="width:3.6in">{BY['sun'].svg(label=False)}</div>
  <div style="font-size:.3in;font-weight:600">by {AUTHOR}</div>
</div>""")


def p_copyright(w, h):
    return page(w, h, f"""
<div style="position:absolute;left:1in;right:1in;bottom:1in;font-size:10.5pt;line-height:1.5;color:#333">
  <p style="font-size:14pt;font-weight:600;margin-bottom:.12in">Tips for grown-ups</p>
  <p>&bull; Start with chunky crayons or washable markers &mdash; the thick lines are made for little hands.<br>
  &bull; Every picture appears twice, so your child can try new colors the second time.<br>
  &bull; Pages are printed on one side only. Slip a piece of card behind a page when using markers.<br>
  &bull; Name the colors and shapes together &mdash; &ldquo;What color is the sun?&rdquo;<br>
  &bull; Color for free on a tablet or computer at <b>{SITE_URL}</b></p>
  <p style="margin-top:.4in">{TITLE_1} {TITLE_2} &mdash; {SUBTITLE}<br>
  Copyright &copy; {YEAR} {AUTHOR}. All rights reserved. No part of this book may be reproduced
  without written permission from the author, except for personal, non-commercial use.<br>
  Illustrations created with the help of AI tools.</p>
</div>""")


def p_belongs(w, h):
    a, b = BY['star' if 'star' in BY else 'stars'], BY['heart']
    return page(w, h, f"""
<div style="position:absolute;inset:.9in;border:.08in dashed #111;border-radius:.5in;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.5in" class="c">
  <div class="big" style="font-size:.85in">This book<br>belongs to</div>
  <div style="width:80%;border-bottom:.04in solid #111;height:1.1in"></div>
  <div style="display:flex;gap:.6in"><div style="width:2.2in">{a.svg(label=False)}</div><div style="width:2.2in">{b.svg(label=False)}</div></div>
</div>""")


def p_test(w, h):
    crayon = ('<svg viewBox="0 0 120 400" style="height:3.2in"><g stroke="#111" stroke-width="6" stroke-linejoin="round" fill="#fff">'
              '<polygon points="20,90 60,10 100,90"/><rect x="20" y="90" width="80" height="290" rx="12"/>'
              '<line x1="20" y1="150" x2="100" y2="150"/><line x1="20" y1="320" x2="100" y2="320"/></g></svg>')
    row = "".join(crayon for _ in range(5))
    return page(w, h, f"""
<div style="position:absolute;inset:.8in;display:flex;flex-direction:column;align-items:center;justify-content:space-evenly" class="c">
  <div class="big" style="font-size:.8in">Test your colors!</div>
  <div style="display:flex;gap:.3in">{row}</div>
  <div style="display:flex;gap:.3in">{row}</div>
</div>""")


def p_art(w, h, a):
    return page(w, h, f'<div class="art">{a.svg()}</div>')


def p_blank(w, h):
    return page(w, h, '<div class="note">This page is left blank so colors don&rsquo;t show through.</div>')


def p_cert(w, h):
    return page(w, h, f"""
<div style="position:absolute;inset:.8in;border:.1in solid #111;border-radius:.4in;display:flex;flex-direction:column;align-items:center;justify-content:space-evenly" class="c">
  <svg viewBox="0 0 600 260" style="width:5in"><g stroke="#111" stroke-width="7" stroke-linejoin="round" fill="#fff">
    <polygon points="100,40 125,100 190,105 140,145 155,210 100,175 45,210 60,145 10,105 75,100"/>
    <polygon points="300,10 333,90 420,95 353,148 375,235 300,188 225,235 247,148 180,95 267,90"/>
    <polygon points="500,40 525,100 590,105 540,145 555,210 500,175 445,210 460,145 410,105 475,100"/></g></svg>
  <div class="big" style="font-size:1in">Great Job!</div>
  <div style="font-size:.32in;font-weight:600">You finished your coloring book!</div>
  <div style="width:70%;border-bottom:.04in solid #111;height:.8in"></div>
  <div style="font-size:.2in">Name</div>
  <div style="width:3in">{BY['teddy'].svg(label=False)}</div>
</div>""")


def p_end(w, h):
    return page(w, h, f"""
<div style="position:absolute;inset:2in 1in;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.3in" class="c">
  <div class="big" style="font-size:1in">The End</div>
  <div style="font-size:.22in;line-height:1.5;max-width:5.5in">Thank you for coloring with us! If your little artist enjoyed this book,
  a short review on Amazon helps other families find it.</div>
  <div style="font-size:.2in">Color more for free at <b>{SITE_URL}</b></div>
</div>""")


def print_interior(w, h):
    pages = [p_title(w, h), p_copyright(w, h), p_belongs(w, h), p_test(w, h)]
    for a in ARTS:
        for _ in range(2):  # each picture twice, single-sided
            pages += [p_art(w, h, a), p_blank(w, h)]
    pages += [p_cert(w, h), p_end(w, h)]
    return head(w, h, INTERIOR_CSS) + "".join(pages) + "</body></html>", len(pages)


def kindle_interior(w, h):
    pages = [p_title(w, h), p_belongs(w, h)] + [p_art(w, h, a) for a in ARTS] + [p_cert(w, h), p_end(w, h)]
    return head(w, h, INTERIOR_CSS) + "".join(pages) + "</body></html>", len(pages)


def sample_pdf(w, h):
    pages = [p_art(w, h, BY[n]) for n in ("sun", "cat", "rocket")]
    return head(w, h, INTERIOR_CSS) + "".join(pages) + "</body></html>"


# --------------------------------------------------------------------- site --
def write_site_data():
    data = [{"title": a.title, "svg": a.svg(interactive=True), "colored": a.svg(colored=True, label=False)} for a in ARTS]
    with open(os.path.join(DOCS, "assets", "pages.js"), "w") as f:
        f.write("// Generated by book/build.py - do not edit by hand\nwindow.PAGES = ")
        json.dump(data, f, separators=(",", ":"))
        f.write(";\n")


# --------------------------------------------------------------------- main --
def crop_covers(jobs):
    """Set each cover PDF's MediaBox to the exact KDP size (top-left anchored)."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject
    for j in jobs:
        if "crop" not in j:
            continue
        r = PdfReader(j["out"])
        wtr = PdfWriter()
        pg = r.pages[0]
        top = float(pg.mediabox.top)
        cw, ch = j["crop"][0] * 72, j["crop"][1] * 72
        box = RectangleObject([0, top - ch, cw, top])
        pg.mediabox = box
        pg.cropbox = box
        pg.trimbox = box
        pg.bleedbox = box
        wtr.add_page(pg)
        with open(j["out"], "wb") as f:
            wtr.write(f)


def w(path, text):
    with open(path, "w") as f:
        f.write(text)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hc-spine", type=float, default=None,
                    help="hardcover spine width in inches from KDP's cover calculator")
    args = ap.parse_args()
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(DOCS, "assets", "img"), exist_ok=True)
    os.makedirs(os.path.join(DOCS, "downloads"), exist_ok=True)

    jobs = []
    pb_html, pb_pages = print_interior(*PB_TRIM)
    jobs.append(dict(type="pdf", html=w(f"{BUILD}/interior-pb.html", pb_html), out=f"{OUT}/paperback-interior-8.5x11.pdf", width=PB_TRIM[0], height=PB_TRIM[1]))
    hc_html, hc_pages = print_interior(*HC_TRIM)
    jobs.append(dict(type="pdf", html=w(f"{BUILD}/interior-hc.html", hc_html), out=f"{OUT}/hardcover-interior-8.25x11.pdf", width=HC_TRIM[0], height=HC_TRIM[1]))
    k_html, k_pages = kindle_interior(*PB_TRIM)
    jobs.append(dict(type="pdf", html=w(f"{BUILD}/interior-kindle.html", k_html), out=f"{OUT}/kindle-interior.pdf", width=PB_TRIM[0], height=PB_TRIM[1]))

    cov, W, H, pb_spine = paperback_cover(pb_pages)
    jobs.append(dict(type="pdf", html=w(f"{BUILD}/cover-pb.html", cov), out=f"{OUT}/paperback-cover-full-wrap.pdf", width=W + 0.1, height=H + 0.1, crop=[W, H]))
    jobs.append(dict(type="png", html=f"{BUILD}/cover-pb.html", out=f"{DOCS}/assets/img/paperback-wrap.jpg", vw=round(W * 96), vh=round(H * 96), scale=1))

    hc_spine = args.hc_spine or round(hc_pages * PAPER_FACTOR_WHITE + 0.189, 3)  # estimate; verify with KDP calculator
    hcov, HW, HH = hardcover_cover(hc_pages, hc_spine)
    jobs.append(dict(type="pdf", html=w(f"{BUILD}/cover-hc.html", hcov), out=f"{OUT}/hardcover-cover-full-wrap.pdf", width=HW + 0.1, height=HH + 0.1, crop=[HW, HH]))

    # Kindle eBook cover: 1600 x 2560 px (1.6:1), JPG
    jobs.append(dict(type="png", html=w(f"{BUILD}/cover-kindle.html", front_only(800 / 96, 1280 / 96, s=1.08)), out=f"{OUT}/kindle-ebook-cover-1600x2560.jpg", vw=800, vh=1280, scale=2))
    # website images
    jobs.append(dict(type="png", html=w(f"{BUILD}/front.html", front_only(*PB_TRIM)), out=f"{DOCS}/assets/img/front-cover.jpg", vw=816, vh=1056, scale=1.5))
    jobs.append(dict(type="png", html=w(f"{BUILD}/back.html", back_only(*PB_TRIM)), out=f"{DOCS}/assets/img/back-cover.jpg", vw=816, vh=1056, scale=1.5))
    jobs.append(dict(type="pdf", html=w(f"{BUILD}/sample.html", sample_pdf(*PB_TRIM)), out=f"{DOCS}/downloads/free-sample-pages.pdf", width=PB_TRIM[0], height=PB_TRIM[1]))

    with open(f"{BUILD}/jobs.json", "w") as f:
        json.dump(jobs, f, indent=1)
    write_site_data()
    subprocess.run(["node", os.path.join(HERE, "render.js"), f"{BUILD}/jobs.json"], check=True)

    crop_covers(jobs)
    specs = {
        "paperback": {"trim_in": PB_TRIM, "pages": pb_pages, "paper": "white", "interior": "black & white, no bleed",
                      "spine_in": pb_spine, "cover_in": [W, H], "cover_finish": "glossy"},
        "hardcover": {"trim_in": HC_TRIM, "pages": hc_pages, "paper": "white", "interior": "black & white, no bleed",
                      "spine_in": hc_spine, "spine_note": "estimate - check KDP hardcover cover calculator and rebuild with --hc-spine",
                      "cover_in": [HW, HH], "wrap_in": HC_WRAP, "hinge_in": HC_HINGE},
        "kindle": {"cover_px": [1600, 2560], "interior_pages": k_pages},
    }
    with open(f"{OUT}/specs.json", "w") as f:
        json.dump(specs, f, indent=2)
    print(json.dumps(specs, indent=2))


if __name__ == "__main__":
    main()

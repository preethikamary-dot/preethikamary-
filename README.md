# Color & Smile! — Big & Easy Coloring Book for Kids Ages 3–5

An AI-assisted coloring book with 25 thick-line designs (each printed twice), KDP-ready
print files for **Kindle, paperback and hardcover**, and a free sales website with an
interactive coloring studio.

## What's here

| Path | What it is |
|---|---|
| `print-ready/paperback-interior-8.5x11.pdf` | Paperback interior, 8.5 × 11 in, 106 pages, no bleed, B&W |
| `print-ready/paperback-cover-full-wrap.pdf` | Paperback full wrap (back + spine + front), 17.4887 × 11.25 in incl. 0.125 in bleed, spine 0.2387 in |
| `print-ready/hardcover-interior-8.25x11.pdf` | Hardcover interior, 8.25 × 11 in, 106 pages |
| `print-ready/hardcover-cover-full-wrap.pdf` | Hardcover case-laminate wrap, 0.51 in wrap, 0.4 in hinge clearance |
| `print-ready/kindle-ebook-cover-1600x2560.jpg` | Kindle eBook cover (1.6:1) |
| `print-ready/kindle-interior.pdf` | Kindle interior (29 pages, each design once) for Kindle Create / print-replica |
| `print-ready/specs.json` | Trim, page count, spine and cover sizes |
| `docs/` | The sales website + interactive coloring studio (GitHub Pages) |
| `book/` | Source: `art.py` (line art), `build.py` (builds everything), `render.js` |

## Publish on Amazon KDP

1. **Paperback**: trim 8.5 × 11, white paper, black & white interior, *no bleed*, glossy cover.
   Upload the paperback interior + cover PDFs.
2. **Hardcover**: trim 8.25 × 11, white paper, B&W, no bleed. KDP does not publish a hardcover
   spine formula, so the spine here (0.428 in) is an estimate. Open KDP's cover calculator for
   hardcover, 106 pages, then rebuild with the exact value:
   `python3 book/build.py --hc-spine 0.XXX`
3. **Kindle eBook**: upload `kindle-ebook-cover-1600x2560.jpg`; import `kindle-interior.pdf`
   into Kindle Create (or use it as a printable PDF bonus).
4. KDP adds the barcode to the bottom-right of the back cover; that area is left clear.
5. Check "AI-generated content: Yes (images)" in KDP's content questionnaire.

## Free website (GitHub Pages)

1. Merge this branch into `main`.
2. In GitHub: **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/docs`**.
3. Your site goes live at `https://preethikamary-dot.github.io/preethikamary-/`
   (this URL is printed on the back cover and inside the book).
4. After your book is live on Amazon, paste the three product links into `window.BUY_LINKS`
   at the top of `docs/index.html`. Until then, buy buttons open an Amazon search for the title.

## Rebuild

```bash
python3 book/build.py            # needs Python 3 + pypdf, Node + Playwright (Chromium)
```
Change the title, publisher, prices or site URL at the top of `book/build.py` and `docs/index.html`.

Fonts: Fredoka (SIL Open Font License) and Nunito via Google Fonts.

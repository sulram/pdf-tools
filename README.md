# pdf-tools

Single-file Python scripts for PDF chores. Each one declares its own dependencies ([PEP 723](https://peps.python.org/pep-0723/)) and runs straight from GitHub with [uv](https://docs.astral.sh/uv/), no clone, no install:

```sh
uv run --script https://raw.githubusercontent.com/sulram/pdf-tools/main/<script>.py ...
```

First run takes a few seconds while uv sets up an isolated environment; after that it is instant. Replace `main` with a tag or commit hash to pin a version.

| Script | What it does |
|---|---|
| [`cjk-pdf-embed.py`](cjk-pdf-embed.py) | Fixes Chinese PDFs that break in macOS Preview by embedding the missing CJK fonts |
| [`pdf-compress.py`](pdf-compress.py) | Shrinks PDFs by recompressing images and cleaning up |

## cjk-pdf-embed

Chinese forms (visa, residence, accommodation registration) often reference CJK fonts such as SimSun or STSong-Light without embedding them. Chrome has its own fallback and renders them fine; macOS Preview, printing and `sips` substitute Helvetica with the wrong metrics, giving overlapping text. This script redraws only the affected text with an embedded CJK font and leaves everything else untouched.

```sh
uv run --script .../cjk-pdf-embed.py in.pdf out.pdf [font.ttf]
```

The default font is a sans. For a serif look, download [Noto Serif SC](https://fonts.google.com/noto/specimen/Noto+Serif+SC), copy `static/NotoSerifSC-Bold.ttf` to `~/Library/Fonts/` and pass it as the third argument. Use the static `.ttf` files: CFF `.otf` builds and variable fonts are not handled by MuPDF.

Verify with `pdffonts out.pdf`: every row should show `emb yes`.

## pdf-compress

Resamples images above a target DPI, recompresses them as JPEG, subsets fonts and removes unused objects. Text-only PDFs barely change; scans and photo-heavy files shrink a lot.

```sh
uv run --script .../pdf-compress.py in.pdf [out.pdf] [--dpi 150] [--quality 75]
```

Defaults are fine for email and portal uploads. Use `--dpi 100 --quality 60` for screen only, `--dpi 200 --quality 85` for print. Output defaults to `in_small.pdf`.

## Shell shortcuts

In `~/.zshrc`:

```sh
PDFTOOLS=https://raw.githubusercontent.com/sulram/pdf-tools/main

fixpdf()   { uv run --script $PDFTOOLS/cjk-pdf-embed.py "$1" "${1:r}_fixed.pdf" ~/Library/Fonts/NotoSerifSC-Bold.ttf }
pdfsmall() { uv run --script $PDFTOOLS/pdf-compress.py "$@" }
```

`fixpdf form.pdf` writes `form_fixed.pdf`; `pdfsmall scan.pdf` writes `scan_small.pdf`.

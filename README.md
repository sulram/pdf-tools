# cjk-pdf-embed

Fixes Chinese PDFs (visa forms, registration forms) that look fine in Chrome but render with wrong fonts and overlapping text in macOS Preview, when printing, or when converting with `sips`.

**Why:** these PDFs reference CJK fonts (SimSun, STSong-Light, SimHei...) without embedding them. Chrome has its own fallback; Quartz substitutes Helvetica with wrong metrics. This script redraws that text with an embedded CJK font and leaves everything else untouched.

## Usage

Requires [uv](https://docs.astral.sh/uv/). No install needed:

```sh
uv run --script https://raw.githubusercontent.com/sulram/cjk-pdf-embed/main/cjk-pdf-embed.py in.pdf out.pdf
```

Optional third argument: a font file to use instead of the default sans. For a serif look, download [Noto Serif SC](https://fonts.google.com/noto/specimen/Noto+Serif+SC), copy `static/NotoSerifSC-Bold.ttf` to `~/Library/Fonts/`, then:

```sh
uv run --script cjk-pdf-embed.py in.pdf out.pdf ~/Library/Fonts/NotoSerifSC-Bold.ttf
```

Use the static `.ttf` files: CFF `.otf` builds and variable fonts are not handled by MuPDF.

Check the result with `pdffonts out.pdf`: every row should show `emb yes`.

## Shell shortcut

In `~/.zshrc`, running straight from GitHub (no clone):

```sh
fixpdf() {
  uv run --script https://raw.githubusercontent.com/sulram/cjk-pdf-embed/main/cjk-pdf-embed.py \
    "$1" "${1:r}_fixed.pdf" ~/Library/Fonts/NotoSerifSC-Bold.ttf
}
```

`fixpdf form.pdf` writes `form_fixed.pdf` next to the original. First run takes a few seconds while uv installs PyMuPDF; after that only the small script download repeats. Replace `main` with a tag or commit hash to pin a version.

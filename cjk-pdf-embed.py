#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pymupdf>=1.24"]
# ///
"""Redesenha texto de fontes CJK não embutidas (SimSun, STSong, SimHei...) com fonte embutida.
uso: fixform.py entrada.pdf saida.pdf [fonte.otf|ttf]"""
import sys, pymupdf

src, dst = sys.argv[1], sys.argv[2]
font = pymupdf.Font(fontfile=sys.argv[3]) if len(sys.argv) > 3 else pymupdf.Font("cjk")
doc = pymupdf.open(src)
total = 0

for page in doc:
    # fontes CID (Type0) sem arquivo embutido; ignora base14 (Helvetica, ZapfDingbats...)
    fonts = page.get_fonts(full=True)
    missing = {f[3] for f in fonts if f[1] == "n/a" and f[2] == "Type0"}
    embedded = {f[3].split("+", 1)[-1] for f in fonts if f[1] != "n/a"}
    if not missing:
        continue

    def is_missing(s):
        name = s["font"]
        # o span traz o nome do descriptor (STSong-Light); o recurso pode trazer sufixo (-UniGB-UCS2-H)
        if not any(m == name or m.startswith(name + "-") for m in missing):
            return False
        # mesmo nome também existe embutido (LNUHNF+SimSun): o não embutido não tem flags
        return name not in embedded or s["flags"] == 0

    spans = [s for b in page.get_text("dict")["blocks"]
               for l in b.get("lines", []) for s in l["spans"] if is_missing(s)]
    if not spans:
        continue
    total += len(spans)
    for s in spans:
        r = pymupdf.Rect(s["bbox"]); r.y0 += 2.5; r.y1 -= 2.5; r.x0 += 1; r.x1 -= 1
        page.add_redact_annot(r)
    # remove só o texto; preserva linhas, caixas e imagens
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    tw = pymupdf.TextWriter(page.rect)
    for s in spans:
        text = s["text"].lstrip(" ")
        x = s["origin"][0] + (len(s["text"]) - len(text)) * s["size"] / 2   # espaços de meia largura
        size = s["size"]
        w = font.text_length(text, size)
        maxw = s["bbox"][2] - x
        if w > maxw:                     # encolhe se a fonte proporcional passar do espaço original
            size *= maxw / w
        tw.append((x, s["origin"][1]), text, font=font, fontsize=size)
    tw.write_text(page)

if total:
    doc.subset_fonts()
    doc.save(dst, garbage=3, deflate=True)
    print(f"ok: {dst} ({total} trechos redesenhados)")
else:
    print("nada a corrigir: nenhuma fonte CJK não embutida encontrada")

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pymupdf>=1.24.7"]
# ///
"""Comprime PDF: recomprime imagens em JPEG, subseta fontes, limpa e deflata.
uso: pdf-compress.py entrada.pdf [saida.pdf] [--dpi 150] [--quality 75]"""
import argparse, os, pymupdf

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst", nargs="?")
ap.add_argument("--dpi", type=int, default=150, help="reamostra imagens acima disso (default 150)")
ap.add_argument("--quality", type=int, default=75, help="qualidade JPEG 1-100 (default 75)")
a = ap.parse_args()
dst = a.dst or os.path.splitext(a.src)[0] + "_small.pdf"

doc = pymupdf.open(a.src)
doc.rewrite_images(dpi_threshold=a.dpi + 1, dpi_target=a.dpi, quality=a.quality, lossy=True, lossless=True)
doc.subset_fonts()
doc.save(dst, garbage=4, deflate=True, deflate_images=True, deflate_fonts=True, clean=True)

before, after = os.path.getsize(a.src), os.path.getsize(dst)
print(f"{before/1e6:.2f} MB -> {after/1e6:.2f} MB ({100 - after*100//before}% menor): {dst}")

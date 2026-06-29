"""
Extract cover images from 10 project case PDFs.
Render page 1 as 800px-wide WebP for case cards.
Uses pypdfium2 (Chromium PDF engine, Windows-friendly).
"""
import pypdfium2 as pdfium
import os
from pathlib import Path
from PIL import Image

BASE = Path(r"C:\CompanyShare\案例项目\PDF成功案例 2024-2025")
OUT  = Path(r"C:\Users\admin\WorkBuddy\2026-05-26-task-1\hongye-furniture-website\images\proyectos")

# 10 cases: (subfolder, filename, output_stem)
CASES = [
    ("酒店",  "The Hilton DoubleTree Hotel.pdf",             "hilton-doubletree-zhuhai"),
    ("酒店",  "Kempinski Hotel & Resort Sariya Yanbu.pdf",   "kempinski-sariya-yanbu"),
    ("医养",  "Woodlands Health Campus.pdf",                 "woodlands-health-singapore"),
    ("医养",  "Saudi German Hospital Makkah.pdf",             "saudi-german-hospital-makkah"),
    ("学校",  "Charterhouse Lagos.pdf",                      "charterhouse-lagos"),
    ("学校",  "Rwanda Military Academy.pdf",                  "rwanda-military-academy"),
    ("办公",  "BYD Co., Ltd..pdf",                           "byd-shenzhen"),
    ("办公",  "Alibaba Group.pdf",                           "alibaba-hangzhou"),
    ("办公",  "Papua New Guinea International Convention Center.pdf", "png-convention-center"),
    ("银行",  "Congo National Bank.pdf",                     "congo-national-bank"),
]

TARGET_W = 800

for sub, fname, stem in CASES:
    pdf_path = BASE / sub / fname
    out_path = OUT / f"{stem}.webp"

    if out_path.exists():
        print(f"[SKIP] {stem}")
        continue

    if not pdf_path.exists():
        print(f"[MISSING] {pdf_path}")
        continue

    try:
        pdf = pdfium.PdfDocument(str(pdf_path))
        page = pdf[0]  # first page

        # Render at 2x scale for retina quality
        bitmap = page.render(scale=2)
        img = bitmap.to_pil()

        # Resize to target width
        w, h = img.size
        ratio = TARGET_W / w
        new_h = int(h * ratio)
        img = img.resize((TARGET_W, new_h), Image.LANCZOS)
        img.save(str(out_path), "WEBP", quality=82)

        pdf.close()
        print(f"[OK] {stem}.webp  ({TARGET_W}x{new_h})")
    except Exception as e:
        print(f"[FAIL] {stem}: {e}")

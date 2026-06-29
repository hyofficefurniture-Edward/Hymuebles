"""
Extract project-specific pages from 2023 combined PDFs for Kempinski/Rwanda/Congo.
"""
import pypdfium2 as pdfium
from pathlib import Path
from PIL import Image

BASE = Path(r'C:\CompanyShare\案例项目\PDF成功案例2023年')
OUT  = Path(r'C:\Users\admin\WorkBuddy\2026-05-26-task-1\hongye-furniture-website\images\proyectos')

def render_page(pdf, idx, out_path):
    page = pdf[idx]
    bitmap = page.render(scale=2)
    img = bitmap.to_pil()
    w, h = img.size
    ratio = 800 / w
    img = img.resize((800, int(h * ratio)), Image.LANCZOS)
    img.save(str(out_path), "WEBP", quality=82)
    print(f"  -> {out_path.name} (800x{int(h*ratio)})")

# 1. Kempinski: search hotel PDF
hp = BASE / '1 Hongye-Hotel-Furniture-Project Cases.pdf'
pdf = pdfium.PdfDocument(str(hp))
found = False
for i in range(min(len(pdf), 20)):
    try:
        text = pdf[i].get_textpage().get_text_range()
        if 'kempinski' in text.lower() or 'sariya' in text.lower():
            print(f'Kempinski: page {i+1}')
            render_page(pdf, i, OUT / 'kempinski-sariya-yanbu.webp')
            found = True
            break
    except: pass
if not found: print('Kempinski: NOT FOUND in hotel PDF (checked first 20 pages)')
pdf.close()

# 2. Rwanda: search office PDF
op = BASE / 'Hongye-Office-Furniture-Project-Cases.pdf'
pdf = pdfium.PdfDocument(str(op))
found = False
for i in range(min(len(pdf), 20)):
    try:
        text = pdf[i].get_textpage().get_text_range()
        if 'rwanda' in text.lower():
            print(f'Rwanda: page {i+1}')
            render_page(pdf, i, OUT / 'rwanda-military-academy.webp')
            found = True
            break
    except: pass
if not found: print('Rwanda: NOT FOUND in office PDF')
pdf.close()

# 3. Congo Bank: search office PDF
pdf = pdfium.PdfDocument(str(op))
found = False
for i in range(min(len(pdf), 48)):
    try:
        text = pdf[i].get_textpage().get_text_range()
        if 'congo' in text.lower() or 'banque' in text.lower():
            print(f'Congo Bank: page {i+1}')
            render_page(pdf, i, OUT / 'congo-national-bank.webp')
            found = True
            break
    except: pass
if not found: print('Congo Bank: NOT FOUND in office PDF')
pdf.close()

print('Done')

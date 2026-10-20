import fitz  # pymupdf
import hashlib
import json
from pathlib import Path

BASE = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/elijah-smiley-local")

pdfs = [
    ("smiley-summary-judgment-original.pdf", "smiley-summary-judgment-extracted.txt"),
    ("smiley-ccm-general-track-original.pdf", "smiley-ccm-general-track-extracted.txt"),
    ("smiley-ccm-streamlined-track-original.pdf", "smiley-ccm-streamlined-track-extracted.txt"),
]

for pdf_name, txt_name in pdfs:
    pdf_path = BASE / pdf_name
    txt_path = BASE / txt_name
    
    try:
        doc = fitz.open(str(pdf_path))
        pages = []
        for page in doc:
            pages.append(page.get_text())
        doc.close()
        
        text = "\n".join(pages)
        txt_path.write_text(text, encoding="utf-8")
        
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        size = len(text.encode("utf-8"))
        print(f"OK: {pdf_name} -> {txt_name} ({size} bytes, sha={sha[:16]}...)")
    except Exception as e:
        print(f"FAIL: {pdf_name} - {e}")

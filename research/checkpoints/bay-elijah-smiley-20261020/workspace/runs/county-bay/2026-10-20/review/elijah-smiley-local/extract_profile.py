from bs4 import BeautifulSoup
from pathlib import Path
import hashlib

BASE = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/elijah-smiley-local")
html = (BASE / "smiley-profile-original.html").read_bytes()
soup = BeautifulSoup(html, "html.parser")

# Remove scripts and styles
for tag in soup(["script", "style"]):
    tag.decompose()

text = soup.get_text(separator="\n")
# Remove excessive blank lines
lines = [l.strip() for l in text.split("\n")]
cleaned = "\n".join(l for l in lines if l)

out_path = BASE / "smiley-profile-extracted.txt"
out_path.write_text(cleaned, encoding="utf-8")
sha = hashlib.sha256(cleaned.encode("utf-8")).hexdigest()
print(f"Size: {len(cleaned.encode('utf-8'))} bytes")
print(f"SHA256: {sha}")
print("\n--- Content ---")
print(cleaned)

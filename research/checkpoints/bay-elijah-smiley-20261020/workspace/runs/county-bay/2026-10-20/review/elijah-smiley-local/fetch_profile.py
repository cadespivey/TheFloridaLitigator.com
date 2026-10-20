import httpx
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/elijah-smiley-local")

url = "https://jud14.flcourts.org/judges/elijah-smiley"
request_started_at = datetime.now(timezone.utc).isoformat()

client = httpx.Client(follow_redirects=True, timeout=30.0)
try:
    resp = client.get(url)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    content = resp.content
    sha = hashlib.sha256(content).hexdigest()
    
    # Save original
    out_path = BASE / "smiley-profile-original.html"
    out_path.write_bytes(content)
    
    receipt = {
        "url": url,
        "resolved_url": str(resp.url),
        "http_status": resp.status_code,
        "request_started_at": request_started_at,
        "retrieved_at": retrieved_at,
        "sha256": sha,
        "size_bytes": len(content),
        "content_type": resp.headers.get("content-type", ""),
        "path": "smiley-profile-original.html",
    }
    
    # Save receipt
    receipt_path = BASE / "smiley-profile-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    
    print(json.dumps(receipt, indent=2))
    print(f"\nSaved to: {out_path}")
    print(f"Receipt: {receipt_path}")
finally:
    client.close()

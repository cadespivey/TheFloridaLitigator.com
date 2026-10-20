import httpx
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/elijah-smiley-local")

pdfs = [
    {
        "id": "summary-judgment-procedures",
        "url": "https://jud14.flcourts.org/uploaded/media/SUMMARY%20JUDGMENT%20PROCEDURES%20AND%20TIMELINESpdfa.pdf",
        "filename": "smiley-summary-judgment-original.pdf",
        "purpose": "Individual procedure: Summary Judgement Procedures & Timeline linked from Smiley's profile page"
    },
    {
        "id": "ccm-general-track",
        "url": "https://jud14.flcourts.org/uploaded/20252104152959_General-Case-Track-Standing-Civil-Case-Management-Order-Establishing-Streamlined-Case-Track-Deadlines-1.pdf",
        "filename": "smiley-ccm-general-track-original.pdf",
        "purpose": "Individual procedure: Standing Civil Case Management Order: Establishing General Case Track Deadlines linked from Smiley's profile page"
    },
    {
        "id": "ccm-streamlined-track",
        "url": "https://jud14.flcourts.org/uploaded/20252104153129_Streamlined-Case-Track-Standing-Civil-Case-Management-Order-Establishing-Streamlined-Case-Track-Deadlines-1.pdf",
        "filename": "smiley-ccm-streamlined-track-original.pdf",
        "purpose": "Individual procedure: Standing Civil Case Management Order: Establishing Streamlined Case Track Deadlines linked from Smiley's profile page"
    },
]

client = httpx.Client(follow_redirects=True, timeout=60.0)
receipts = []

for pdf in pdfs:
    url = pdf["url"]
    request_started_at = datetime.now(timezone.utc).isoformat()
    try:
        resp = client.get(url)
        retrieved_at = datetime.now(timezone.utc).isoformat()
        content = resp.content
        sha = hashlib.sha256(content).hexdigest()
        
        out_path = BASE / pdf["filename"]
        out_path.write_bytes(content)
        
        receipt = {
            "id": pdf["id"],
            "url": url,
            "resolved_url": str(resp.url),
            "http_status": resp.status_code,
            "request_started_at": request_started_at,
            "retrieved_at": retrieved_at,
            "sha256": sha,
            "size_bytes": len(content),
            "content_type": resp.headers.get("content-type", ""),
            "path": pdf["filename"],
            "purpose": pdf["purpose"],
        }
        receipts.append(receipt)
        print(f"OK: {pdf['id']} - {resp.status_code}, {len(content)} bytes, sha={sha[:16]}...")
    except Exception as e:
        retrieved_at = datetime.now(timezone.utc).isoformat()
        receipt = {
            "id": pdf["id"],
            "url": url,
            "resolved_url": url,
            "http_status": None,
            "request_started_at": request_started_at,
            "retrieved_at": retrieved_at,
            "sha256": None,
            "size_bytes": None,
            "content_type": None,
            "path": pdf["filename"],
            "purpose": pdf["purpose"],
            "error": str(e),
        }
        receipts.append(receipt)
        print(f"FAIL: {pdf['id']} - {e}")

client.close()

receipts_path = BASE / "pdf-receipts.json"
receipts_path.write_text(json.dumps(receipts, indent=2) + "\n")
print(f"\nReceipts saved to: {receipts_path}")

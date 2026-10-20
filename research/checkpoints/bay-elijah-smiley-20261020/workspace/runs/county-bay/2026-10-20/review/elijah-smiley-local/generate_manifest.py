import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/elijah-smiley-local")
ROOT = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release")

def file_info(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }

files = {}

# All local files except manifest.json and worker logs
exclude = {"manifest.json", "worker-errors.log", "worker-events.jsonl", "worker-final.txt"}
for f in sorted(BASE.iterdir()):
    if f.is_file() and f.name not in exclude:
        info = file_info(f)
        files[f.name] = info
        print(f"  {f.name}: {info['size_bytes']} bytes, sha={info['sha256'][:16]}...")

# Referenced external files (shared)
roster_path = ROOT / "runs/county-bay/2026-10-20/review/initial-roster-cloud/judges-review-original.html"
if roster_path.exists():
    info = file_info(roster_path)
    files["[ref] judges-review-original.html"] = {
        **info,
        "absolute_path": "runs/county-bay/2026-10-20/review/initial-roster-cloud/judges-review-original.html",
        "note": "Shared roster source, reused from seed. Not re-fetched in this assignment."
    }
    print(f"  [ref] judges-review-original.html: {info['size_bytes']} bytes")

practice_path = ROOT / "runs/county-bay/2026-10-20/review/mallory-cloud/practice-index-http-original.html"
if practice_path.exists():
    info = file_info(practice_path)
    files["[ref] practice-index-http-original.html"] = {
        **info,
        "absolute_path": "runs/county-bay/2026-10-20/review/mallory-cloud/practice-index-http-original.html",
        "note": "Shared practice index source, reused from mallory-cloud. Not re-fetched in this assignment."
    }
    print(f"  [ref] practice-index-http-original.html: {info['size_bytes']} bytes")

manifest = {
    "person": "Elijah Smiley",
    "role": "Circuit Judge",
    "circuit": 14,
    "county": "Bay",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "files": files,
}

manifest_path = BASE / "manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(f"\nmanifest.json written ({len(files)} files)")

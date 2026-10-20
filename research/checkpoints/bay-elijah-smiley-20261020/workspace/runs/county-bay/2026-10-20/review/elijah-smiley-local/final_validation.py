import hashlib
import json
from pathlib import Path

BASE = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/elijah-smiley-local")
ROOT = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release")

# 1. Verify manifest hashes
manifest = json.loads((BASE / "manifest.json").read_text())
print("=== MANIFEST HASH VALIDATION ===")
all_pass = True
for fname, info in manifest["files"].items():
    if fname.startswith("[ref]"):
        fpath = ROOT / info["absolute_path"]
    else:
        fpath = BASE / fname
    
    if not fpath.exists():
        print(f"  FAIL: {fname} - file not found")
        all_pass = False
        continue
    
    data = fpath.read_bytes()
    actual_sha = hashlib.sha256(data).hexdigest()
    actual_size = len(data)
    
    if actual_sha != info["sha256"]:
        print(f"  FAIL: {fname} - hash mismatch")
        print(f"    expected: {info['sha256']}")
        print(f"    actual:   {actual_sha}")
        all_pass = False
    elif actual_size != info["size_bytes"]:
        print(f"  FAIL: {fname} - size mismatch")
        all_pass = False
    else:
        print(f"  PASS: {fname}")

# 2. Verify quotes from person.json against actual artifacts
print("\n=== QUOTE VALIDATION ===")
person = json.loads((BASE / "person.json").read_text())
profile_html = (BASE / "smiley-profile-original.html").read_bytes().decode("utf-8")
ccm_general = (BASE / "smiley-ccm-general-track-extracted.txt").read_text()
summary_judg = (BASE / "smiley-summary-judgment-extracted.txt").read_text()
roster_html = (ROOT / "runs/county-bay/2026-10-20/review/initial-roster-cloud/judges-review-original.html").read_bytes().decode("utf-8")

quotes_to_check = [
    # Office phone
    (person["contacts"]["office_phone"]["quote"], profile_html, "office_phone"),
    (person["contacts"]["office_phone"]["href_substring"], profile_html, "office_phone href"),
    # Fax
    (person["contacts"]["office_fax"]["quote"], profile_html, "office_fax"),
    # Assistant email
    ("mailto:cutlerd@jud14.flcourts.org", profile_html, "assistant email href (profile)"),
    ("mailto:cutlerd@jud14.flcourts.org", roster_html, "assistant email href (roster)"),
    # Assignment
    ("Bay County Circuit Court: Probate & Trusts, Guardianships, Baker Acts & Marchman Acts, Jimmy Ryce Cases Civil Court", profile_html, "assignment"),
    # CCM 20-day
    (person["civil_checklist"]["conferral_motion_hearing"]["quote"], ccm_general, "CCM 20-day"),
    # CCM 30-day
    (person["civil_checklist"]["submissions_certification"]["quote"], ccm_general, "CCM 30-day"),
    # Summary Judgment
    ("ALL motions \nfor summary judgment must be filed and served no later than 60 days before the trial", summary_judg, "SJ 60-day"),
    ("filed and served no later \nthan 30 days before the Pretrial Conference", summary_judg, "30-day motion"),
]

for quote, source, label in quotes_to_check:
    if quote in source:
        print(f"  PASS: {label}")
    else:
        print(f"  FAIL: {label}")
        print(f"    Quote: {repr(quote[:80])}")
        all_pass = False

# 3. Check for internal contradictions
print("\n=== CONSISTENCY CHECKS ===")
# Phone consistency between roster and profile
roster_phone = "(850) 767-3341"
profile_phone_display = "(850) 767- 3341"
if roster_phone in roster_html and profile_phone_display in profile_html:
    print("  NOTE: Phone formatting differs (roster no-space, profile has space). Same number confirmed via tel: href.")
else:
    print("  FAIL: Phone consistency check unexpected result")
    all_pass = False

# Assistant name consistency
if "Darlene Cutler" in profile_html and "Darlene Cutler" in roster_html:
    print("  PASS: Assistant name consistent across sources")
else:
    print("  FAIL: Assistant name inconsistency")
    all_pass = False

# Source count check
sources = json.loads((BASE / "sources.json").read_text())
new_sources = [s for s in sources["sources"] if s.get("acquisition") in ("httpx_direct",)]
print(f"  New sources fetched: {len(new_sources)} (limit: 5)")
if len(new_sources) > 5:
    print("  FAIL: Exceeded source limit")
    all_pass = False

print(f"\n{'='*50}")
print(f"FINAL RESULT: {'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED'}")

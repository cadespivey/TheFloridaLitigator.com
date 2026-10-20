from pathlib import Path
import json

BASE = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/elijah-smiley-local")

# Load artifacts
profile_html = (BASE / "smiley-profile-original.html").read_bytes().decode("utf-8")
ccm_general = (BASE / "smiley-ccm-general-track-extracted.txt").read_text()
ccm_streamlined = (BASE / "smiley-ccm-streamlined-track-extracted.txt").read_text()
summary_judg = (BASE / "smiley-summary-judgment-extracted.txt").read_text()
roster_html = Path("/Users/cadespivey/florida-litigator-weekly-update/runs/site-sync-20261019/release/runs/county-bay/2026-10-20/review/initial-roster-cloud/judges-review-original.html").read_bytes().decode("utf-8")

checks = [
    # Profile HTML checks
    ("(850) 767- 3341", profile_html, "profile phone display text"),
    ("tel:%2B18507673341", profile_html, "profile phone href"),
    ("(850) 747-5159 - Fax", profile_html, "profile fax"),
    ("Bay County Courthouse<br>300 East 4th Street<br>Panama City, FL 32401", profile_html, "profile address"),
    ("mailto:cutlerd@jud14.flcourts.org", profile_html, "assistant email href"),
    ("Bay County Circuit Court: Probate & Trusts, Guardianships, Baker Acts & Marchman Acts, Jimmy Ryce Cases Civil Court", profile_html, "assignment text"),
    ("Elijah Smiley, Circuit Judge", profile_html, "profile title"),
    ("Darlene Cutler", profile_html, "assistant name in profile"),
    
    # Roster checks
    ("mailto:cutlerd@jud14.flcourts.org", roster_html, "roster assistant email href"),
    ("tel:+18507673341", roster_html, "roster phone href"),
    ("(850) 767-3341", roster_html, "roster phone display text"),
    
    # CCM General checks
    ("Within 20 days of filing any motion for which a hearing is requested, the", ccm_general, "CCM general - 20 day rule"),
    ("moving party must contact the presiding judge's office to set the motion for hearing. Failure \nto seek such hearing may result in the motion being denied.", ccm_general, "CCM general - hearing requirement"),
    
    # Summary Judgment checks
    ("ALL motions \nfor summary judgment must be filed and served no later than 60 days before the trial", summary_judg, "SJ 60 day rule"),
    ("filed and served no later \nthan 30 days before the Pretrial Conference", summary_judg, "30 day motion rule"),
    ("No motion will be heard at or after the pretrial \nconference absent compelling circumstances and consent of the Court.", summary_judg, "pretrial conference rule"),
]

all_pass = True
for quote, source, label in checks:
    if quote in source:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}")
        print(f"  Quote: {repr(quote[:100])}")
        # Try to find partial match
        words = quote.split()
        if len(words) > 3:
            partial = " ".join(words[:5])
            if partial in source:
                print(f"  Partial match found for: {repr(partial)}")
                # Find context
                idx = source.index(partial)
                print(f"  Context: {repr(source[idx:idx+len(quote)+20])}")
        all_pass = False

print(f"\n{'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED'}")

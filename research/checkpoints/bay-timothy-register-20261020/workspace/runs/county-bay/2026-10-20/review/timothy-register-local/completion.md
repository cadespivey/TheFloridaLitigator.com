# Timothy Register — Bay County Circuit Judge — Completion Report

Date: 2026-10-20
Reviewer: Local agent (Qwen3.8-27B-8bit)
Basis capture: 7713

## Summary

Profile page reviewed. Judge assignment is **Bay County Criminal Division H** (criminal).
No individual procedure links present on the profile page. Contacts captured.
No additional sources fetched (0 new sources beyond profile page).

## Contact Fields (from profile page)

| Field | Value | Source |
|-------|-------|--------|
| Name | Timothy Register, Circuit Judge | H1, profile page |
| Assignment | Bay County Criminal Division H | Profile, "Judicial Assignment" |
| Courthouse | Bay County Courthouse, 300 East 4th Street, Panama City, Florida 32401 | Profile, "Contact information" |
| Phone | (850) 914-6486 | Profile, "Contact information" (tel link) |
| Fax | (850) 747-5159 | Profile, "Contact information" |
| Office Email | null (not stated) | — |
| Assistant Name | Patty Kelley | Profile, "Judicial Assistant" |
| Assistant Email | kelleyp@jud14.flcourts.org | Profile, mailto href |
| Assistant Phone | null (not separately stated) | — |
| Profile URL | https://jud14.flcourts.org/judges/timothy-register | — |
| Stated Dates | null (none on profile) | — |

## Exact Quotes and Locators

All quotes are literal substrings of `profile-original.html` (sha256: 12361e32d72fd5f339c66b2d886a47da12198112890c5892bb60df886ca43c93).

1. **Profile name** — H1 element text:
   `Timothy Register, Circuit Judge`

2. **Courthouse/address** — within `<p>` after "Contact information:" strong tag:
   `Bay County Courthouse`
   `300 East 4th Street`
   `Panama City, Florida 32401`

3. **Phone** — `<a href="tel:%2B18509146486">` display text:
   `(850) 914-6486`
   Href in HTML: `tel:%2B18509146486`

4. **Fax** — text in same paragraph:
   `Fax (850) 747-5159`

5. **Assistant name** — `<a href="mailto:kelleyp@jud14.flcourts.org">` display text:
   `Patty Kelley`
   Href in HTML: `mailto:kelleyp@jud14.flcourts.org`

6. **Assignment** — within `<p>` after "Judicial Assignment:" strong tag:
   `Bay County Criminal Division H`

## Bounded Procedure Checklist (Criminal Assignment)

Per AGENTS.md: "For primarily criminal, family, juvenile or diversionary assignments, capture contacts, assignment and official procedure links plus only basic scheduling, submission and appearance instructions readily available on those sources."

| Category | Finding |
|----------|---------|
| Scheduling | No individual scheduling instructions on profile page. Circuit-wide calendars link exists at `/calendars-schedules`. |
| Submission | No individual submission instructions on profile page. |
| Appearance | No individual appearance instructions on profile page. General video conferencing link at `/technology/video-conferencing`. |
| Official procedure links | No individual procedure links on profile page. Circuit-wide links noted: `/judicial-practice-procedures`, `/e-filing-proposed-orders`, `/administrative-orders`. |
| Proposed orders | No individual instructions. Shared proposed-order guide reviewed at Checkpoint 7715. |
| Communications | Office phone (850) 914-6486; assistant email kelleyp@jud14.flcourts.org. |

## Gaps

1. No individual procedure links present on profile page.
2. No office email address stated on profile.
3. No assistant phone separately stated.
4. No stated dates on profile page.
5. No individual scheduling, submission, or appearance instructions.
6. Assignment is criminal (Division H); civil/commercial checklist categories do not apply.

## Qualifications and Notes

- The phone (850) 914-6486 is listed under "Contact information" on the individual profile page. The constraint states "General courthouse address and administration phone are not personal chambers contacts." The profile does not label this as a chambers line or general line; it is recorded as stated without inference.
- The assistant email (kelleyp@jud14.flcourts.org) is from the mailto href in the original HTML, not visible-text extraction.
- No source conflicts identified.
- Shared sources (proposed-order guide, AO2025-00-01) already reviewed at Checkpoint 7715; not re-fetched.

## Review Scope

- Profile page fetched and reviewed in full.
- No additional sources fetched (no individual procedure links observed).
- Roster metadata from seed reused; not re-fetched.
- Shared sources from Checkpoint 7715 referenced but not re-researched.
- No database writes, no state changes, no other judge records modified.

## Files Produced

- `person.json` — structured person record
- `sources.json` — acquisition receipts and source references
- `completion.md` — this file
- `profile-original.html` — original HTTP response bytes
- `profile-extracted.txt` — BeautifulSoup text extraction (scripts/styles removed)

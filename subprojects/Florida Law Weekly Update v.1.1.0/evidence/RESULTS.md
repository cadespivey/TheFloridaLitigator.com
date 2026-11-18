# Florida Law Weekly Update v1.1.0 implementation results

The sequential candidate reduced median Python time per correctly accepted fixture review by 23.0% and p95 by 14.3%. An overlapping reporting window reused the earlier verification of a published opinion and returned the same public entry with one fewer substantive approval. The full-archive website comparison produced identical output. The full candidate suite passed all 1,579 tests. The operator approved local promotion. The cloud, personal and local profiles now load the release skill. [Candidate files and base commit](candidate.json) · [Implementation diff](implementation.patch)

## Baseline and performance

The baseline checkout was `e34fc629b8cdcf51a6bf782fca88b3a6315ee2ac`. The initial profile identified repeated task selection, queue refresh and history reads. The subsequent comparison used the same fixture server, source texts, evidence policy, interpreter, hardware and fixed answers in both checkouts. The original baseline also records the ownership of durable state, dependencies that invalidate a result, and the actual Pages inputs. [Baseline and dependency map](BASELINE.md) · [Replay and fixture manifest](replay.py)

| Measure | Original sequential | Candidate sequential |
| --- | ---: | ---: |
| Accepted reviews, three measured runs | 180 | 180 |
| Median time per accepted review | 47.78 ms | 36.77 ms |
| Nearest-rank p95 | 76.34 ms | 65.45 ms |
| Median elapsed time per 60-task run, including setup, failure and repair | 4.81 s | 4.22 s |
| Median CPU time per 60-task run | 4.70 s | 4.11 s |
| Median time to first issued card after acquisition | 20.18 ms | 17.57 ms |
| Peak resident memory | 66.48 MiB | 67.41 MiB |
| Median fixture storage per group | 5,276,200 bytes | 5,305,434 bytes |
| Authoritative selections per separately profiled 20-task group | 75 | 53 |
| Queue loads / refreshes per profiled group | 188 / 168 | 124 / 103 |
| Coordinator lock wait / hold per profiled group | 11.0 ms / 1.85 s | 8.9 ms / 1.60 s |

After an unmeasured warmup for each path, measured runs alternated A/B, B/A, A/B. Each mode accepted 117 source decisions, 36 qualified opinions, 18 exclusions and nine status exceptions. Nine explicit resumes and nine rejected answers with repairs remained in each mode's cost. Each mode used 207 transport calls and discarded zero tasks. The candidate delivered 27 scope reminders within those calls. The OS reported zero block I/O counters despite visible file writes, so physical disk throughput is undetermined. This comparison ran Python directly and issued zero model calls. It measures orchestration and includes no model idle time, context compaction, or human nudges. [Measured comparison](comparison.json) · [A1](A1.json), [A2](A2.json), [A3](A3.json) · [B1](B1.json), [B2](B2.json), [B3](B3.json) · [Original stage profile](A-profile.json) · [Candidate stage profile](B-profile.json)

**Stage 5 is deferred.** Both sequential targets were met. These measurements establish a saving from reducing repeated Python work. They do not establish an additional end-to-end saving from speculative opinion review. Sequential execution remains the release default. The ordinary Pages build and its commit-specific CI proof remain in use.

## Review, recovery and release

| Gate | Observed result |
| --- | --- |
| R1–R4, review and resume | Exact retries retain handles and original answers. Resume regenerates the current scope from saved decisions. Simultaneous reminder triggers produce one in-band reminder. Changed source, packet, policy or status blocks stale reuse. Projection rehearsal reports multiple structural failures without accepting a mapping. [Transport cases](../../../tests/test_review_transport.py) · [Incremental review cases](../../../tests/test_incremental_review.py) · [Projection cases](../../../tests/test_publication_driver.py) |
| R6, one campaign | The cloud trial preserved two sound entries and corrected a categorical tender rule attributed to a divided panel. Only the corrected entry returned. The published summary retained the distinction between an assumed and a decided issue, and the deadline fixture preserved the conflict with the separately supplied comparison rule. Final fixed-answer replay produced the same three-card sequence and completed preview. [Cloud submissions and source digests](cloud-trial.json) · [Final replay](semantic-replay.json) · [Preview screenshot](semantic-preview.png) |
| R6, coverage and personnel | A report-only person appears in final verification even when there is no supplement edit. The personnel trial repaired a truncated reply on its original handle, updated the supported assignment and chambers phone, and retained other contact details. The gap fixture carried a missing court listing beyond the next window and retried only its original channels. Available unfinished reviews and unresolved included content continued to block acceptance. [Personnel trial](cloud-personnel.json) · [Coverage and recovery cases](../../../tests/test_workflow.py) |
| Repeated operator work | A finalized fixture opinion appeared in a later explicitly overlapping window. The original path presented a publication approval. The candidate returned preview directly, with identical public title, summary, disposition text, dates, status and citations. This saved one semantic handoff. Human intervention frequency across production updates remains unmeasured. [Original](A-reuse.json) · [Candidate](B-reuse.json) · [Reproduction](reuse_trial.py) |
| R7, crash recovery | Fourteen process exits exercised seven review boundaries before and after persistence. Six aggregate interruptions recovered one batch decision, one aggregate decision and one domain acceptance. Interrupted immutable export and integration recovered exact bytes. The executor tests exercised commit, push, PR, merge, Pages upload/deploy observations and live-result recording, including reuse of a remote action that had already succeeded. Failed CI or mismatched delivered bytes prevents a completed release. [Transport](../../../tests/test_review_transport.py) · [Aggregate](../../../tests/test_publication_driver.py) · [Export](../../../tests/test_publication.py) · [Integration and live identity](../../../tests/test_workflow.py) · [Executor](../../../tests/test_publication_executor.py) |
| R8, public output | The existing Pages build used the full public archive, 67 county files and the Fifth DCA supplement. All 19 generated files matched byte for byte. Chromium matched six rendered states covering current issue, court menu, date filter, search, directory and historical issue. Two full-viewport screenshots also matched byte for byte. [Build inputs and file hashes](pages-build.json) · [DOM and screenshot results](browser.json) · [Updates](baseline-updates.png) · [Directory](baseline-directory.png) |
| R8, rollback | Quiescent runs can explicitly switch protocols before report preparation. Tests recovered an issued handle across rollback, preserved accepted history on re-upgrade and rejected transition while the reply lock was held. A frozen report resumes with its compatible reader. [Rollback test](../../../tests/test_review_transport.py) · [Operator procedure](../OPERATOR_AND_SKILL_ROLLOUT.md#operating-the-release-candidate) |

The bounded cloud trials used the invoking Codex session. Its precise model variant was unavailable. The legal fixture used three selected excerpts from saved originals and a synthetic current-rule comparison. The local Flash Next, 27B BF16 and 27B 8-bit configurations have no behavioral trial result. Profile discovery below starts app servers and performs no local inference. The tests used disposable SQLite databases, fixture repositories and mocked release boundaries. No production acquisition, publication, or live Pages deployment was performed.

## Installation and regression evidence

The approved installer bound the canonical package to this checkout and its pinned interpreter. Fresh cloud, personal and local app servers each discovered the enabled skill. All ten repository-owned files matched in every profile, each launcher reported protocols 1 and 2, and each issued a source-review card on a disposable fixture. The installed SKILL.md SHA-256 is `312eb5e3e9f1c3dfcb52ed87f1727ed6a66a800ea262679c08c49df26e1e5517`. The local profile again reported its existing configuration deprecation. [Installed profile results](profile-after-promotion.json)

Before promotion, fresh cloud, personal and local app servers discovered the same canonical skill and each installed launcher issued a source card on a disposable fixture. All three resolved to `/Users/cadespivey/Developer/CodexSkills/florida-update` at SKILL.md hash `a80fe0443f4ad531ef36e3abab92d522e302cc869289ddb32ee1bc088d7969fb`. That hash identifies the previous installation. The local app server emitted its existing `[features].multi_agent` deprecation diagnostic. [Per-profile evidence](profile-before-promotion.json) · [Discovery and launcher check](profile_check.py)

The final candidate passed 1,579 tests in 167.07 seconds. Pytest reported no warnings. Command from the checkout root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/cadespivey/Developer/FloridaLitigator/florida-litigator-weekly-update/.venv/bin/python -m pytest -q
```

The first full suite identified a removed bounded JSON download entry point and a progress-test double that did not accept the new event filter. The candidate restores the download entry point and the mock now accepts the filter. Earlier publication tests also exposed the missing verification item for report-only personnel. [Initial suite output](full-suite-initial.log) · [Report-only personnel failures](publication-development.log) · [Final suite output](full-suite.log)

A changed verifier policy prevented finalization and returned all three affected items. Restoring the matching policy recovered the saved preview with one aggregate acceptance. [Policy invalidation and recovery](policy-recovery.json)

The [operator handoff](../OPERATOR_AND_SKILL_ROLLOUT.md#operating-the-release-candidate) describes checked resume, correction, release and compatible rollback. The approved promotion covers this checkout and the canonical skill installation.

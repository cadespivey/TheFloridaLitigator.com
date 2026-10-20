# Local model replay trial

`local_model_replay.py ROOT` creates a fresh isolated workspace, a frozen plan and
an evaluator answer key outside that workspace. `run_local_replay.py ROOT` invokes
the configured local Qwen model in five fresh Codex contexts. The corpus is entirely
synthetic. It simulates pagination, 429 recovery, 503 outages and later restoration,
roster/JA changes, dated procedures and amendment comparison traps.

`evaluate_local_replay.py ROOT` grades objective coverage, saved evidence, structured
facts and persistence. Review legal summaries and the actual event logs separately:
keyword checks are not proof of semantic correctness. A prohibited direct corpus
read invalidates a clean acquisition/recovery acceptance claim even if the answers
are factually correct. The workspace instruction boundary is not an OS read sandbox.

Each phase has an exact prompt, JSONL event log, last message, execution metrics,
and a saved artifact snapshot. Four new-context launches exercise handoff recovery;
they do not establish native automatic compaction or long-context stability.
The trial is a limited replay, not a statewide live research run or PDF release.

The hardened successor is `controlled_replay.py prepare|run|restore ROOT`.
It uses `flwu.controlled_worker` and `flwu.worker_contract`, directly calls the
pinned local inference endpoint without tools, and lets trusted code own files,
source discovery, spans, task persistence, counters and HTML. See RUNBOOK.md for
the blocked/resume sequence and TEST_PLAN.md for rejection and live-trial gates.
The original shell-agent trial remains preserved for comparison.

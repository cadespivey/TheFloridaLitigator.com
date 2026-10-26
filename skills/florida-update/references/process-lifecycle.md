# Acquisition process lifecycle and recovery

Read this before launching collection, after compaction, and before any retry.
The CLI emits flushed JSON progress and 30-second heartbeats to stderr while
fetching sources. Stdout contains the final result; silence on stdout is normal. It
persists observations before exporting the queue. An empty output directory or
missing update-queue.json during collection is normal, not proof of a hang.

## One acquisition at a time

Before launch, inspect existing processes for the pinned launcher and its Python
children running `workflow acquire`, `update` or `source-gate run` against the selected database.
Do not launch while another acquisition is active. Current CLI acquisition commands enforce a nonblocking OS lock on the canonical
database path through queue export. A busy error includes the owner PID/run ID;
wait for that process. Do not delete the .acquisition.lock sidecar: the OS releases
the lock on process exit even when metadata remains. Earlier already-running
processes do not hold this new lock; wait for them before starting a guarded run.
Direct library callers and other database writers are outside this CLI guard.
If overlapping jobs already exist, report their PIDs/run IDs and preserve them.
Do not choose one to kill or start a replacement. Ask for an intentional recovery
choice; do not interrupt live work merely because it is silent.

Write RUN/RESUME.md BEFORE launch, containing absolute checkout/database/registry/
output paths, exact command and run ID, resolved dates, phase=acquiring, start time,
and next action=wait for this process. Immediately append the returned tool session
ID. Record OS PID if available, but keep it distinct from the tool session ID.

A tool result saying “Process running with session ID N” means RUNNING, not failed.
Use write_stdin with that numeric session ID and empty chars to await its result.
Use a 30–60 second wait, then provide a short progress update. Do not repeatedly
run ls -R, reread full logs, issue sleep subprocesses, or launch another command
as a substitute for waiting. No artificial wall-clock deadline applies.
A tool-call yield/timeout is not a child process exit or a source retrieval timeout.
Only an actual process exit code establishes completion/failure.

After compaction, read RESUME.md first. Resume waiting on the saved tool session.
If that session is unavailable, inspect the saved process and its children and
read the database in read-only mode for recent capture timestamps/counts. A lost
tool session does not mean the process stopped. Never write SQL to repair state.
If the process is still active, do not relaunch. If its terminal result cannot be
recovered, record that uncertainty and obtain a recovery decision before retrying.

## Completion and retries

Record the exit code and bounded error output in RESUME.md. Run `update --help`
once if a CLI usage error occurs; use only supported arguments. There is no
`--resume`, `--verbose`, `--log-level`, `source-gate resume`, or `source-gate kill`.
`FLWU_PAGE_SIZE` is not a supported setting. `--page-size` belongs to `update`,
not `source-gate`. Do not guess flags or reduce overlap/page size to cure silence.

- Exited 0: inspect acquisition_complete, then run workflow next-task. False means a saved coverage gap. This is not publication.
- Exited 2: distinguish argparse usage errors from a completed acquisition's
  incomplete-coverage result. Read stderr and the actual queue, not exit code alone.
- Interrupted and confirmed no longer running: repeat identical arguments/run ID
  to resume completed checkpoints. Do not mutate the run contract or registry.
- Recorded source failure after completion: one fresh run ID may retry it, only
  after all earlier acquisition processes have exited. Preserve original failure.
- Concurrent acquisition exception: first establish that other writers have exited;
  then resume the same run, not a new one. Do not bypass the concurrency guard.

Never fall back from `update` to `source-gate run`: that omits seven-court opinion
discovery. `source-gate queue` is read-only maintenance output, not a substitute
for the combined update queue or proof of complete research. Do not run code fixes,
change defaults, kill processes, or restart inference in response to silence.

If the same failure repeats after one evidenced corrective attempt, save its exact
error and checkpoint and report the blocker. Do not loop through new IDs, arguments,
background jobs or another model. Preserve valid evidence for later recovery.

## Persistent-goal continuation

The workflow goal stays active throughout acquisition. After a tool yields, wait
on the same process; after an automatic goal continuation or compaction, recover
its session/PID and exact command from RESUME.md before acting. A background job
finishing is the transition to review, not the end of the goal. Goal continuation
does not itself supervise or terminate child processes; retain all locking and
process-lifecycle checks above. Complete the goal only after database, website
and deployment criteria in SKILL.md are met, respecting narrower preview scope.

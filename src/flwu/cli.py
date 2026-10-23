"""CLI entry point for Florida Litigator Weekly Update.

The standard `update` command performs hash-gated acquisition and seven-court
opinion discovery; review commands persist validated interpretations separately.
Also provides preview (C08), with placeholders for future
commands (registry, fetch, analyze, produce, publish, schedule).

Args:
    preview --fixture PATH    Path to synthetic fixture JSON file.
    preview --state-root PATH Directory for SQLite state/database.
    preview --output PATH     Directory for output HTML/Markdown files.
    preview --observed-at UTC Optional observation timestamp.

Example:
    flwu preview --fixture fixtures/synthetic-source.json \
                 --state-root /tmp/flwu_state \
                 --output /tmp/flwu_output
"""

from __future__ import annotations

import argparse
from contextlib import nullcontext
from flwu.acquisition import acquisition
import sys
from pathlib import Path
from typing import Any


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns exit code 0 on success, 1 on failure."""
    parser = argparse.ArgumentParser(
        prog="flwu",
        description="Florida Litigator Weekly Update — evidence acquisition, review, and publication tools.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # preview subcommand (C08)
    preview_parser = subparsers.add_parser(
        "preview",
        help="Run a synthetic fixture and produce a preview HTML report.",
    )
    preview_parser.add_argument(
        "--fixture", required=True, dest="fixture_path",
        help="Path to synthetic fixture JSON file.",
    )
    preview_parser.add_argument(
        "--state-root", required=True, dest="state_root",
        help="Directory for SQLite state/database.",
    )
    preview_parser.add_argument(
        "--output", required=True, dest="output_path",
        help="Directory for output HTML files.",
    )
    preview_parser.add_argument(
        "--observed-at", default=None, dest="observed_at",
        help="ISO-8601 observation timestamp (default: current UTC).",
    )
    preview_parser.add_argument(
        "--mode", default="fixture", choices=["fixture", "production"],
        help="Pipeline mode. Preview defaults to fixture.",
    )
    preview_parser.add_argument(
        "--window-start", default=None,
        help="Report window start date (YYYY-MM-DD).",
    )
    preview_parser.add_argument(
        "--window-end", default=None,
        help="Report window end date (YYYY-MM-DD).",
    )

    directory_parser = subparsers.add_parser("directory", help="Import the reviewed judicial directory and render its appendix.")
    directory_parser.add_argument("--database", required=True, type=Path)
    directory_parser.add_argument("--output", required=True, type=Path)

    preview_parser.add_argument("--directory-db", type=Path, default=None, help="Read the current reviewed directory snapshot from this SQLite database.")

    research = subparsers.add_parser("research", help="Initialize or validate an evidence-backed research workspace.")
    research.add_argument("action", choices=["init", "status"])
    research.add_argument("--run-dir", required=True, type=Path)
    research.add_argument("--window-start")
    research.add_argument("--window-end")
    research.add_argument("--as-of", help="Aware timestamp on window-end for an explicitly partial final day")
    research.add_argument("--profile", choices=["weekly-seven", "statewide-circuits"], default="weekly-seven")
    research.add_argument("--history-db", type=Path, help="Shared cumulative history; defaults to FLWU_HISTORY_DB or ~/.local/share/flwu/research-history.sqlite")

    history = subparsers.add_parser("history", help="Capture research, compare time windows, and mark reviewed reports finalized.")
    history.add_argument("action", choices=["capture", "changes", "finalize", "streams", "artifact"])
    history.add_argument("--database", type=Path)
    history.add_argument("--run-dir", type=Path)
    history.add_argument("--stream")
    history.add_argument("--start", help="Inclusive New York date or aware timestamp; omit for last finalized report")
    history.add_argument("--end", help="Inclusive New York date or exclusive aware timestamp; default now")
    history.add_argument("--entity", help="Limit finding context to one stable entity key")
    history.add_argument("--output", type=Path)
    history.add_argument("--capture-id")
    history.add_argument("--report", type=Path)
    history.add_argument("--review", help="Explicit reviewer attestation of completed legal and visual review")
    history.add_argument("--sha256", help="Saved raw/extracted artifact to export with --output")

    gate = subparsers.add_parser("source-gate", help="Fetch sources, compare byte hashes, and queue bounded reviews.")
    gate.add_argument("action", choices=["inventory", "add", "run", "queue", "extract", "review"])
    gate.add_argument("--database", type=Path)
    gate.add_argument("--stream", help="Existing research stream (inventory only)")
    gate.add_argument("--registry", type=Path)
    gate.add_argument("--run-id", help="Unique acquisition run; reuse only to resume")
    gate.add_argument("--output", type=Path, help="New registry file or local queue directory")
    gate.add_argument("--receipt", type=Path)
    gate.add_argument("--url", help="Official source URL to add to the registry")
    gate.add_argument("--text", type=Path, help="UTF-8 reviewed extraction/transcription (extract only)")
    gate.add_argument("--start", help="Optional explicit comparison start for effective-date tasks")
    gate.add_argument("--end", help="Optional inclusive date or exclusive aware timestamp")

    update = subparsers.add_parser("update", help="Standard hash-driven update with mandatory seven-court opinion discovery.")
    update.add_argument("--database", type=Path)
    update.add_argument("--registry", type=Path, required=True)
    update.add_argument("--run-id", required=True)
    update.add_argument("--output", type=Path, required=True)
    update.add_argument("--start", help="Explicit reporting start date; default last finalized report")
    update.add_argument("--end", help="Inclusive reporting end date; default today in New York")
    update.add_argument("--overlap-days", type=int, default=30)
    update.add_argument("--page-size", type=int, default=50)
    update.add_argument("--max-pages", type=int, default=200)
    opinion_review = subparsers.add_parser("opinion-review", help="Validate and save one queued opinion interpretation.")
    opinion_review.add_argument("--database", type=Path)
    opinion_review.add_argument("--registry", type=Path, required=True)
    opinion_review.add_argument("--receipt", type=Path, required=True)

    # Future subcommand placeholders (C34, C37, C39, C40)
    subparsers.add_parser("registry", help="Manage source registries (future).")
    subparsers.add_parser("fetch", help="Acquire source data (future).")
    subparsers.add_parser("analyze", help="Run analysis jobs (future).")
    subparsers.add_parser("produce", help="Produce a report (future).")
    site = subparsers.add_parser("site", help="Export reviewed history or build the date-range website.")
    site.add_argument("action", choices=["export", "build"])
    site.add_argument("--archive", type=Path, required=True)
    site.add_argument("--database", type=Path)
    site.add_argument("--capture-id")
    site.add_argument("--output", type=Path)
    site.add_argument("--preview", action="store_true", help="Allow synthetic/unpublished data; never use for public deployment")
    site.add_argument("--county-directory", "--directory-supplement", type=Path, action="append", default=[], help="Dated county-directory supplement; repeat for multiple reviewed counties")
    publish = subparsers.add_parser("publish", help="Build a validated production Pages artifact; deployment uses GitHub Actions.")
    publish.add_argument("--archive", type=Path, default=Path("website/updates"))
    publish.add_argument("--output", type=Path, required=True)
    publish.add_argument("--county-directory", "--directory-supplement", type=Path, action="append", default=[])
    subparsers.add_parser("schedule", help="Schedule recurring runs (future).")

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "history":
        return _handle_history(args)

    if args.command in ("update", "opinion-review"):
        from flwu import source_gate, opinion_discovery, update as updater, history as memory
        import json
        import sqlite3
        try:
            registry = source_gate.load_registry(args.registry)
            with (acquisition(args.database, args.run_id, "update") if args.command == "update" else nullcontext()), memory.database(args.database) as conn:
                if args.command == "opinion-review":
                    print(json.dumps(opinion_discovery.accept_review(conn, registry, json.loads(args.receipt.read_text()))))
                    return 0
                result = updater.run(conn, registry, args.run_id, args.output, start=args.start, end=args.end,
                                     overlap=args.overlap_days, page_size=args.page_size, max_pages=args.max_pages)
                print(json.dumps({'acquisition_complete': result['acquisition_complete'],
                                  'courts': result['all_seven_courts_wired'],
                                  'opinion_tasks': len(result['opinion_reviews']['tasks']),
                                  'source_tasks': len(result['source_reviews']['tasks']),
                                  'queue': str(args.output/'update-queue.json'), 'publication_performed': False}))
                return 0 if result['acquisition_complete'] else 2
        except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
            print(f"Update error: {exc}", file=sys.stderr)
            return 1

    if args.command == "source-gate":
        from flwu import source_gate, history as memory
        import json
        import sqlite3
        try:
            if args.action == "inventory" and (not args.stream or not args.output):
                raise ValueError("inventory requires --stream and --output (new file)")
            if args.action != "inventory" and not args.registry:
                raise ValueError("--registry is required")
            if args.action in ("run", "queue") and not args.output:
                raise ValueError("--output queue directory is required")
            if args.action == "run" and not args.run_id:
                raise ValueError("run requires --run-id; reuse it only for resume")
            if args.action in ("review", "extract") and not args.receipt:
                raise ValueError("review/extract requires --receipt")
            if args.action == "extract" and not args.text:
                raise ValueError("extract requires --text")
            registry = source_gate.load_registry(args.registry) if args.registry else None
            if args.action == "add":
                if not args.url:
                    raise ValueError("add requires --url")
                source_gate._validate_url(args.url, is_live=True)
                if '#' in args.url or args.url in {s['url'] for s in registry['sources']}:
                    raise ValueError("URL is already registered or contains a fragment")
                registry['sources'].append({'id': source_gate.source_id(args.url), 'url': args.url})
                args.registry.write_text(json.dumps(registry, indent=2)+'\n')
                print("Registered source; start a new acquisition run ID.")
                return 0
            with (acquisition(args.database, args.run_id, "source-gate run") if args.action == "run" else nullcontext()), memory.database(args.database) as conn:
                if args.action == "inventory":
                    data = source_gate.inventory(conn, args.stream)
                    with args.output.open('x') as f:
                        json.dump(data, f, indent=2)
                    print(f"Wrote {len(data['sources'])} URL candidates; review registry scope before fetching.")
                elif args.action == "review":
                    print(json.dumps(source_gate.accept(conn, registry, json.loads(args.receipt.read_text()))))
                elif args.action == "extract":
                    print(json.dumps(source_gate.attach_text(conn, registry, json.loads(args.receipt.read_text()), args.text.read_text(encoding='utf-8'))))
                else:
                    if args.action == "run":
                        source_gate.run(conn, registry, args.run_id)
                    data = source_gate.write_queue(conn, registry, args.output, start=args.start, end=args.end)
                    print(json.dumps({'tasks': len(data['tasks']), 'reused_reviews': len(data['reused_reviews']),
                                      'effective_date_tasks': len(data['effective_date_tasks']),
                                      'queue': str(args.output / 'queue.json'), 'publication_performed': False}))
            return 0
        except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
            print(f"Source gate error: {exc}", file=sys.stderr)
            return 1

    if args.command in ("site", "publish"):
        from flwu.publication import export_capture
        from flwu.site import build_site
        import sqlite3
        try:
            if args.command == "site" and args.action == "export":
                if not args.database or not args.capture_id:
                    raise ValueError("export requires --database and --capture-id")
                result = export_capture(args.database, args.capture_id, args.archive, preview=args.preview)
            else:
                if not args.output:
                    raise ValueError("build requires --output (a new directory)")
                result = build_site(args.archive, args.output, preview=getattr(args, "preview", False),
                                    county_directories=args.county_directory)
            print(result)
            return 0
        except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
            print(f"Website error: {exc}", file=sys.stderr)
            return 1

    if args.command == "research":
        from flwu.research import initialize, inspect_run
        import json
        import sqlite3
        try:
            if args.action == "init":
                initialize(args.run_dir, args.window_start, args.window_end, args.profile, as_of=args.as_of)
            result = inspect_run(args.run_dir, history_db=args.history_db)
            print(json.dumps(result, indent=2))
            return 0 if args.action == "init" or result["status"] == "ready_for_review" else 2
        except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
            print(f"Research workspace error: {exc}", file=sys.stderr)
            return 1

    if args.command == "directory":
        from flwu.directory import load_directory, import_directory, read_directory
        from flwu.directory_render import render_directory
        from flwu.state import open_db, migrate
        import json
        args.database.parent.mkdir(parents=True, exist_ok=True)
        args.output.mkdir(parents=True, exist_ok=True)
        conn = open_db(args.database)
        try:
            migrate(conn)
            result = import_directory(conn, load_directory())
            data = read_directory(conn)
            (args.output / "judicial-directory.html").write_text(render_directory(data), encoding="utf-8")
            (args.output / "judicial-directory.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(json.dumps(result))
        finally:
            conn.close()
        return 0

    if args.command == "preview":
        return _handle_preview(args)

    # Future commands: print placeholder and return 0
    # Implementation will be added in later cards
    print(f"Command 'flwu {args.command}' is not yet implemented.", file=sys.stderr)
    return 1


def _handle_history(args):
    import json
    import sqlite3
    from flwu.history import database, compare, finalize
    from flwu.history_capture import capture
    from flwu.research import write_json
    try:
        if args.action == "capture":
            if not args.run_dir:
                raise ValueError("capture requires --run-dir")
            result = capture(args.run_dir, db_path=args.database)
        else:
            with database(args.database) as conn:
                if args.action == "streams":
                    result = [dict(r) for r in conn.execute("SELECT * FROM streams ORDER BY stream")]
                elif args.action == "changes":
                    if not args.stream:
                        raise ValueError("changes requires --stream (see history streams)")
                    if not conn.execute("SELECT 1 FROM streams WHERE stream=?", (args.stream,)).fetchone():
                        raise ValueError("Unknown history stream")
                    result = compare(conn, args.stream, start=args.start, end=args.end, entity=args.entity)
                elif args.action == "finalize":
                    if not args.capture_id or not args.report or not args.review:
                        raise ValueError("finalize requires --capture-id, --report and --review")
                    result = finalize(conn, args.capture_id, args.report, args.review)
                else:
                    if not args.sha256 or not args.output:
                        raise ValueError("artifact requires --sha256 and --output")
                    row = conn.execute("SELECT bytes FROM artifacts WHERE sha256=?", (args.sha256,)).fetchone()
                    if row is None:
                        raise ValueError("Unknown artifact")
                    args.output.parent.mkdir(parents=True, exist_ok=True)
                    args.output.write_bytes(row[0])
                    return 0
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            write_json(args.output, result)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"Research history error: {exc}", file=sys.stderr)
        return 1


def _handle_preview(args: argparse.Namespace) -> int:
    """Handle the preview subcommand."""
    from flwu.fixture_pipeline import run_fixture, PipelineError

    if args.mode != "fixture":
        print("Preview is fixture-only. Live acquisition is not implemented; use research init for evidence tracking.", file=sys.stderr)
        return 1
    fixture_path = Path(args.fixture_path)
    if not fixture_path.is_file():
        print(f"Error: fixture file not found: {fixture_path}", file=sys.stderr)
        return 1

    try:
        state_root = Path(args.state_root)
        output_dir = Path(args.output_path)

        directory = None
        if args.directory_db:
            import sqlite3
            from flwu.directory import read_directory
            conn = sqlite3.connect(args.directory_db.resolve().as_uri() + "?mode=ro", uri=True)
            try:
                directory = read_directory(conn)
            finally:
                conn.close()

        issue = run_fixture(
            input_path=fixture_path,
            directory=directory,
            state_root=state_root,
            output_dir=output_dir,
            observed_at=args.observed_at,
            window_start=args.window_start,
            window_end=args.window_end,
        )

        print(f"Preview generated: {issue.get('issue_id', 'unknown')}")
        print(f"  Mode: {issue.get('mode', 'N/A')}")
        print(f"  Window: {issue.get('window_start', '')} to {issue.get('window_end', '')}")
        print(f"  Cutoff: {issue.get('cutoff_utc', 'N/A')}")
        print(f"  Output: {output_dir}")

        # Show categories summary
        categories = issue.get("categories", {})
        for section_name, section_records in categories.items():
            print(f"  {section_name}: {len(section_records)} records")

        return 0

    except PipelineError as e:
        print(f"Pipeline error [{e.code}]: {e.message}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

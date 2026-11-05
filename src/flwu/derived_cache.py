"""Disposable, versioned computation cache; never acquisition or review evidence.

No research-schema changes. Missing, corrupt, disabled or unwritable caches take
the ordinary computation path. Source bytes and accepted receipts remain in SQLite.
"""
from functools import lru_cache
from importlib.metadata import version, PackageNotFoundError
import json
import os
from pathlib import Path
import sys
import tempfile

from flwu import history as h


@lru_cache(maxsize=1)
def policy():
    # Include transitive implementation and parser versions, not a handwritten
    # version callers could forget to bump when changing comparison semantics.
    root = Path(__file__).parent
    packages = {}
    for name in ('beautifulsoup4', 'soupsieve', 'pypdf'):
        try: packages[name] = version(name)
        except PackageNotFoundError: packages[name] = None
    return h.sha(dict(code={str(p.relative_to(root)): h.sha(p.read_bytes())
                            for p in sorted(root.rglob('*.py'))},
                      parsers=packages, python=list(sys.version_info[:3])))


class Cache:
    def __init__(self, conn):
        self.root = None
        if os.environ.get('FLWU_DISABLE_DERIVED_CACHE') == '1': return
        if conn.execute('PRAGMA query_only').fetchone()[0]: return
        name = next((row[2] for row in conn.execute('PRAGMA database_list') if row[1] == 'main'), '')
        if name:
            path = Path(name)
            self.root = path.parent/'.flwu-derived-cache'/path.name/policy()

    def path(self, kind, inputs):
        # Keep one latest mutable-state entry per source/run, rather than a
        # full queue copy for every receipt. The envelope still checks the exact
        # complete dependency key; an overwritten older state is simply a miss.
        address = inputs
        if kind == 'update-queue':
            address = {k: inputs[k] for k in ('registry','run_id','output','bounds')}
        elif kind == 'source-decision':
            address = dict(source=inputs['source'], protocol=inputs['review_protocol'])
        elif kind == 'source-export':
            address = dict(source_id=inputs['task']['source_id'],output=inputs['output'],protocol=inputs['protocol'])
        elif kind == 'opinion-export':
            address = dict(opinion_id=inputs['task']['opinion']['id'],output=inputs['output'])
        return self.root/kind/(h.sha(address)+'.json') if self.root else None

    def get(self, kind, inputs):
        path = self.path(kind, inputs)
        if path is None: return None
        try:
            record = json.loads(path.read_text())
            if (set(record) != {'key', 'result_sha256', 'result'}
                    or record['key'] != h.sha(inputs)
                    or h.sha(record['result']) != record['result_sha256']): return None
            return record['result']
        except (OSError, ValueError, TypeError, KeyError): return None

    def put(self, kind, inputs, result):
        path = self.path(kind, inputs)
        if path is None: return
        temporary = None
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(prefix='.cache-', dir=path.parent)
            with os.fdopen(fd, 'w') as handle:
                json.dump(dict(key=h.sha(inputs), result_sha256=h.sha(result), result=result), handle)
            os.replace(temporary, path)
        except OSError:
            # This optimization must also work in an unwritable cache directory.
            pass
        finally:
            if temporary:
                try: os.unlink(temporary)
                except OSError: pass

    def memo(self, kind, inputs, compute):
        value = self.get(kind, inputs)
        if value is not None: return value
        value = compute()
        if value is not None: self.put(kind, inputs, value)
        return value


def write_bytes(path, raw):
    """Repair projections atomically, leaving identical files/mtimes untouched."""
    path = Path(path)
    if path.is_file() and not path.is_symlink() and path.read_bytes() == raw: return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.projection-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle: handle.write(raw)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)


def dependencies(conn, streams):
    """Indexed event watermarks plus baseline state that changes without captures."""
    return dict(streams={stream: list(conn.execute(
        'SELECT seq,capture_id FROM captures WHERE stream=? ORDER BY seq DESC LIMIT 1', (stream,)).fetchone() or [0,None])
        for stream in streams},
        finalized=[list(row) for row in conn.execute(
            'SELECT stream,capture_seq,report_sha256,finalized_at FROM finalized_reports ORDER BY seq')],
        invalidations=[list(row) for row in conn.execute('SELECT * FROM report_invalidations ORDER BY capture_id')]
        if conn.execute("SELECT 1 FROM sqlite_master WHERE name='report_invalidations'").fetchone() else [])

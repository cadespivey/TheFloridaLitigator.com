#!/usr/bin/env python3
"""Reject credential-shaped Google API keys in Git's index without printing values.

Reads staged blobs (not working files), including extensionless evidence captures.
This targeted guard supplements GitHub secret scanning; it is not a universal scanner.
"""
import re
import subprocess
import sys

GOOGLE_API_KEY = re.compile(rb"AIza[0-9A-Za-z_-]{35}")


def main():
    records = subprocess.check_output(['git', 'ls-files', '--stage', '-z']).split(b'\0')
    failures = []
    process = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for record in records:
            if not record:
                continue
            metadata, path = record.split(b'\t', 1)
            mode, oid, stage = metadata.split()
            if mode == b'160000':  # Submodule contents are outside this repository.
                continue
            process.stdin.write(oid + b'\n')
            process.stdin.flush()
            header = process.stdout.readline().split()
            if len(header) != 3 or header[1] != b'blob':
                raise RuntimeError('Cannot inspect an indexed blob')
            size = int(header[2])
            blob = process.stdout.read(size)
            if len(blob) != size or process.stdout.read(1) != b'\n':
                raise RuntimeError('Incomplete indexed blob read')
            if GOOGLE_API_KEY.search(blob):
                failures.append(path.decode('utf-8', errors='replace'))
    finally:
        process.stdin.close()
        process.stdout.close()
        code = process.wait()
    if code:
        raise RuntimeError('Git blob inspection failed')
    if failures:
        print('Google API key pattern found in staged files (values withheld):', file=sys.stderr)
        for path in sorted(set(failures)):
            print(repr(path), file=sys.stderr)
        print('Keep source originals in the private research store; do not commit these captures.', file=sys.stderr)
        return 1
    print('No Google API key patterns found in Git index.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

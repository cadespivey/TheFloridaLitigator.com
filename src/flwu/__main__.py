"""Run the same supported CLI without relying on an editable-installed script."""
from flwu.cli import main

if __name__ == '__main__':
    raise SystemExit(main())

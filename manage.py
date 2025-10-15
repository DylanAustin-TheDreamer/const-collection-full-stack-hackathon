"""Wrapper manage.py at repo root.

This delegates to the real manage.py inside the `config/` directory so
contributors can run `python manage.py ...` from the project root.
"""
from pathlib import Path
import runpy
import sys
import os


def main():
    root = Path(__file__).resolve().parent
    real = root / "config" / "manage.py"
    if not real.exists():
        raise SystemExit("config/manage.py not found — expected Django project inside the 'config' folder")

    # Ensure the inner config package can be imported as 'config'
    # by adding the repo's config directory to sys.path and switching cwd.
    config_dir = str(real.parent)
    if config_dir not in sys.path:
        sys.path.insert(0, config_dir)

    # Change working directory so relative imports and settings resolve
    os.chdir(config_dir)

    # Run the real manage.py
    sys.argv[0] = str(real)
    runpy.run_path(str(real), run_name="__main__")


if __name__ == "__main__":
    main()

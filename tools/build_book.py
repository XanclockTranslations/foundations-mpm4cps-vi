"""Assemble and compile the book using Python and Tectonic from any working directory."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", default="tectonic", help="Tectonic command or executable path")
    parser.add_argument("--cache-dir", type=Path, help="Optional Tectonic cache directory")
    parser.add_argument("--skip-assembly", action="store_true", help="Compile an existing output/book-draft.tex")
    args = parser.parse_args()

    compiler = shutil.which(args.compiler)
    if compiler is None:
        parser.error("Tectonic was not found. Install 0.17.0 or supply --compiler PATH.")
    compiler = str(Path(compiler).resolve())
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    if not args.skip_assembly:
        result = subprocess.run([sys.executable, str(ROOT / "tools/assemble_book.py")], cwd=ROOT)
        if result.returncode:
            return result.returncode
    if not (output / "book-draft.tex").is_file():
        parser.error("output/book-draft.tex is missing; run without --skip-assembly.")

    environment = os.environ.copy()
    if args.cache_dir:
        environment["TECTONIC_CACHE_DIR"] = str(args.cache_dir.expanduser().resolve())
    log = output / "build-console.log"
    print("Compiling with Tectonic; its first run may download the TeX bundle.", flush=True)
    with log.open("w", encoding="utf-8", newline="\n") as stream:
        result = subprocess.run(
            [compiler, "--untrusted", "--keep-logs", "book-draft.tex"],
            cwd=output,
            env=environment,
            stdout=stream,
            stderr=subprocess.STDOUT,
        )
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines()[-30:]:
        print(line)
    if result.returncode:
        print(f"Compilation failed. See {log}", file=sys.stderr)
        return result.returncode
    pdf = output / "book-draft.pdf"
    if not pdf.is_file():
        print("Tectonic returned success without producing book-draft.pdf.", file=sys.stderr)
        return 1
    print(f"Built {pdf} ({pdf.stat().st_size:,} bytes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

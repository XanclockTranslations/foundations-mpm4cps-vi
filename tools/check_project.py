"""Check the portable book inputs without compiling or changing any files.

Artwork hashes describe the reviewed input snapshot. Intentional artwork changes
require an explicit review and refresh of source/asset-inventory.json; this tool
never updates that inventory automatically.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COVER = "assets/cover-donald-giannatti-unsplash.jpg"
TEXT_SUFFIXES = {".tex", ".md", ".py", ".ps1", ".json", ".txt", ".yaml", ".yml", ".toml"}
TEXT_NAMES = {".gitignore", ".gitattributes", ".editorconfig", ".python-version"}
EXCLUDED_DIRECTORIES = {
    ".git", "vendor", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "node_modules",
}
LOCAL_ROOT_DIRECTORIES = {"output", "review", "tmp", ".local-archives"}
READY_STATUSES = {"draft_complete_self_reviewed", "translation_complete_reviewed"}


class Checks:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def json(self, relative: str) -> dict | list | None:
        try:
            return json.loads((ROOT / relative).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.error(f"{relative}: cannot read JSON ({exc})")
            return None


def public_text_files():
    """Prune local build/archive directories before inspecting editable files."""
    for base, directories, filenames in os.walk(ROOT):
        directories[:] = sorted(
            d for d in directories if d not in EXCLUDED_DIRECTORIES
            and not (Path(base) == ROOT and d in LOCAL_ROOT_DIRECTORIES)
        )
        for name in sorted(filenames):
            path = Path(base) / name
            relative = path.relative_to(ROOT)
            if relative.parts[0] == "release" and relative.as_posix() != "release/release-manifest.json":
                continue
            if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
                yield path


def check_text(checks: Checks) -> int:
    count = 0
    for path in public_text_files():
        count += 1
        relative = path.relative_to(ROOT).as_posix()
        try:
            data = path.read_bytes()
            data.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            checks.error(f"{relative}: must be readable UTF-8 ({exc})")
            continue
        if data.startswith(b"\xef\xbb\xbf"):
            checks.error(f"{relative}: remove the UTF-8 BOM")
        if b"\r" in data:
            checks.error(f"{relative}: use LF line endings")
        if data and not data.endswith(b"\n"):
            checks.error(f"{relative}: add a final newline")
    return count


def check_chapters(checks: Checks) -> int:
    required = [f"translation/chapters/chapter-{n:02}.tex" for n in range(1, 10)]
    required += [
        "translation/bibliography.tex", "tools/assemble_book.py",
        "translation/frontmatter/cover.tex", "translation/frontmatter/original-notices.tex",
        "translation/frontmatter/opening.tex", "translation/frontmatter/contributors.tex",
        "translation/frontmatter/editorial-notes.tex", "assets/cover-photo.json",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            checks.error(f"Missing required input: {relative}")
    expected_chapters = {f"chapter-{n:02}.tex" for n in range(1, 10)}
    for path in (ROOT / "translation/chapters").glob("chapter-??.tex"):
        if path.name not in expected_chapters:
            checks.error(f"Unexpected chapter input in this nine-chapter edition: {path.name}")
    for relative in ("translation/progress.json", "source/manifest.json"):
        manifest = checks.json(relative)
        if not isinstance(manifest, dict):
            if manifest is not None:
                checks.error(f"{relative}: expected a JSON object")
            continue
        chapters = manifest.get("chapters")
        if not isinstance(chapters, list) or not all(isinstance(c, dict) for c in chapters):
            checks.error(f"{relative}: expected a chapters array of objects")
            continue
        numbers = [c.get("chapter") for c in chapters]
        if not all(type(n) is int for n in numbers) or sorted(numbers) != list(range(1, 10)):
            checks.error(f"{relative}: must list each of chapters 1–9 exactly once")
        if relative.startswith("translation/"):
            if manifest.get("full_book_complete") is not True:
                checks.error(f"{relative}: full_book_complete must be true for this complete edition")
            for chapter in chapters:
                if chapter.get("status") not in READY_STATUSES:
                    checks.error(f"Chapter {chapter.get('chapter')}: translation status is not ready for assembly")
    return sum((ROOT / p).is_file() for p in required[:9])


def inventory_path(value: object) -> str | None:
    if not isinstance(value, str) or "\\" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        return None
    if value == COVER or (path.parent.as_posix() == "assets/clean" and path.suffix == ".pdf"):
        return value
    return None


def check_jpeg(path: Path) -> None:
    """Validate the JPEG marker header and image dimensions without Pillow."""
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8") or not data.endswith(b"\xff\xd9"):
        raise ValueError("missing JPEG start/end markers")
    position = 2
    frame_found = False
    while position < len(data) - 2:
        if data[position] != 0xFF:
            raise ValueError("invalid JPEG marker boundary")
        while position < len(data) and data[position] == 0xFF:
            position += 1
        if position >= len(data):
            break
        marker = data[position]
        position += 1
        if marker == 0xDA:  # Compressed scan follows; its integrity is hash-checked.
            if not frame_found:
                raise ValueError("scan precedes image dimensions")
            return
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if position + 2 > len(data):
            raise ValueError("truncated JPEG segment")
        length = int.from_bytes(data[position:position + 2], "big")
        if length < 2 or position + length > len(data):
            raise ValueError("invalid JPEG segment length")
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if length < 8:
                raise ValueError("truncated JPEG frame")
            height = int.from_bytes(data[position + 3:position + 5], "big")
            width = int.from_bytes(data[position + 5:position + 7], "big")
            if width <= 0 or height <= 0:
                raise ValueError("invalid JPEG dimensions")
            frame_found = True
        position += length
    raise ValueError("missing JPEG image scan")


def check_inventory(checks: Checks, pdf_reader) -> set[str]:
    inventory = checks.json("source/asset-inventory.json")
    if not isinstance(inventory, dict) or inventory.get("schema_version") != 1:
        if inventory is not None:
            checks.error("source/asset-inventory.json: expected schema_version 1")
        return set()
    files = inventory.get("files")
    if not isinstance(files, list):
        checks.error("source/asset-inventory.json: expected a files array")
        return set()
    if len(files) != 182:
        checks.error(f"Artwork inventory must contain 182 entries (181 PDFs and the cover), found {len(files)}")
    registered: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict) or (relative := inventory_path(entry.get("path"))) is None:
            checks.error(f"Invalid artwork inventory entry: {entry!r}")
            continue
        if relative in registered:
            checks.error(f"Duplicate artwork inventory path: {relative}")
        registered.add(relative)
        expected_size, expected_hash = entry.get("bytes"), entry.get("sha256")
        if type(expected_size) is not int or expected_size <= 0 or not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            checks.error(f"{relative}: inventory requires positive bytes and lowercase SHA-256")
            continue
        path = ROOT / relative
        try:
            data = path.read_bytes()
            if len(data) != expected_size or hashlib.sha256(data).hexdigest() != expected_hash:
                checks.error(f"{relative}: differs from the reviewed inventory; review the edit and explicitly refresh its bytes/SHA-256")
            if path.suffix == ".pdf":
                reader = pdf_reader(path, strict=True)
                if reader.is_encrypted or len(reader.pages) != 1:
                    raise ValueError("expected an unencrypted, one-page PDF")
                page = reader.pages[0]
                if float(page.mediabox.width) <= 0 or float(page.mediabox.height) <= 0:
                    raise ValueError("invalid page dimensions")
                page.get_contents()  # Force the referenced page content to be readable.
            else:
                check_jpeg(path)
        except Exception as exc:
            checks.error(f"{relative}: invalid or unreadable artwork ({exc})")
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "assets/clean").glob("*.pdf")}
    expected = registered - {COVER}
    if len(actual) != 181:
        checks.error(f"assets/clean: expected 181 PDFs, found {len(actual)}")
    for relative in sorted(actual - expected):
        checks.error(f"Unregistered clean artwork: {relative}")
    for relative in sorted(expected - actual):
        checks.error(f"Missing clean artwork: {relative}")
    if COVER not in registered:
        checks.error("Artwork inventory is missing the cover JPEG")
    return registered


def group(text: str, start: int) -> tuple[str, int]:
    """Read a balanced TeX brace group, returning its content and end offset."""
    if start >= len(text) or text[start] != "{":
        raise ValueError("expected a TeX brace group")
    depth = 1
    index = start + 1
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
        index += 1
    raise ValueError("unterminated TeX brace group")


def strip_definitions(text: str, macros: dict[str, tuple[int, str]]) -> str:
    pattern = re.compile(r"\\(?:newcommand|renewcommand)\*?\s*\{\\([A-Za-z]+)\}\s*(?:\[(\d+)\]\s*)?")
    output, position = [], 0
    for match in pattern.finditer(text):
        if match.start() < position:
            continue
        body, end = group(text, match.end())
        macros[match.group(1)] = (int(match.group(2) or 0), body)
        output.append(text[position:match.start()])
        position = end
    output.append(text[position:])
    return "".join(output)


def resolve_tex_path(reference: str) -> Path:
    path = (ROOT / "output" / reference).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"build reference escapes the project: {reference}")
    return path


def selected_tex(text: str, macros: dict[str, tuple[int, str]], depth: int = 0) -> str:
    """Select existing-file branches and expand only local graphics wrappers.

    This covers Table 4.1's parameterized clean-first references. It is a small
    reference scanner, not a general TeX interpreter or a substitute for a build.
    """
    if depth > 20:
        raise ValueError("recursive graphics macro expansion")
    pattern = re.compile(r"\\([A-Za-z]+)\b")
    output, position = [], 0
    for match in pattern.finditer(text):
        if match.start() < position:
            continue
        name = match.group(1)
        if name == "IfFileExists":
            cursor = match.end()
            arguments = []
            for _ in range(3):
                while cursor < len(text) and text[cursor].isspace():
                    cursor += 1
                argument, cursor = group(text, cursor)
                arguments.append(argument)
            if "#" in arguments[0] or "\\" in arguments[0]:
                raise ValueError(f"unresolved conditional media reference: {arguments[0]}")
            replacement = arguments[1] if resolve_tex_path(arguments[0]).is_file() else arguments[2]
        elif name in macros and name not in {"sourcefigure", "sourceillustration"} and "\\includegraphics" in macros[name][1]:
            count, replacement = macros[name]
            cursor = match.end()
            for number in range(1, count + 1):
                while cursor < len(text) and text[cursor].isspace():
                    cursor += 1
                argument, cursor = group(text, cursor)
                replacement = replacement.replace(f"#{number}", argument)
        else:
            continue
        output.append(text[position:match.start()])
        output.append(selected_tex(replacement, macros, depth + 1))
        position = cursor
    output.append(text[position:])
    return "".join(output)


def check_references(checks: Checks, registered: set[str]) -> tuple[int, int]:
    manifest = checks.json("assets/figure-crops.json")
    definitions: dict[str, str] = {}
    if not isinstance(manifest, dict) or not isinstance(manifest.get("figures"), list):
        checks.error("assets/figure-crops.json: expected a figures array")
    else:
        for entry in manifest["figures"]:
            number = entry.get("number") if isinstance(entry, dict) else None
            if not isinstance(number, str) or not re.fullmatch(r"[1-9]\.[A-Za-z0-9]+", number):
                checks.error(f"Invalid figure identifier: {number!r}")
                continue
            if number in definitions:
                checks.error(f"Duplicate figure identifier: {number}")
            relative = f"assets/clean/figure-{number.replace('.', '-')}-vi.pdf"
            definitions[number] = relative
            if registered and relative not in registered:
                checks.error(f"Figure {number}: clean artwork is not registered ({relative})")
    try:
        assembler = (ROOT / "tools/assemble_book.py").read_text(encoding="utf-8")
        constants = [node.value for node in ast.walk(ast.parse(assembler)) if isinstance(node, ast.Constant) and isinstance(node.value, str)]
        preamble = next(value for value in constants if "\\documentclass" in value)
        texts = [("tools/assemble_book.py preamble", preamble)]
        texts += [(p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8")) for p in sorted((ROOT / "translation").rglob("*.tex"))]
        macros: dict[str, tuple[int, str]] = {}
        stripped = [(name, strip_definitions(re.sub(r"(?<!\\)%[^\n]*", "", text), macros)) for name, text in texts]
        used: set[str] = set()
        figure_calls = 0
        for name, text in stripped:
            for match in re.finditer(r"\\(?:sourcefigure|sourceillustration)\s*\{([^{}]+)\}", text):
                figure_calls += 1
                number = match.group(1)
                if number not in definitions:
                    checks.error(f"{name}: figure {number} has no registered definition")
                else:
                    used.add(definitions[number])
            selected = selected_tex(text, macros)
            pattern = r"\\(includegraphics\*?|input|include)\s*(?:\[[^\]]*\]\s*)?\{([^{}]+)\}"
            for match in re.finditer(pattern, selected):
                command, reference = match.groups()
                if "#" in reference or "\\" in reference:
                    checks.error(f"{name}: unresolved {command} reference: {reference}")
                    continue
                path = resolve_tex_path(reference)
                if not path.is_file() and command in {"input", "include"} and not path.suffix:
                    path = path.with_suffix(".tex")
                relative = path.relative_to(ROOT).as_posix()
                if not path.is_file():
                    checks.error(f"{name}: missing {command} input: {relative}")
                elif command.startswith("includegraphics"):
                    used.add(relative)
                    if registered and relative not in registered:
                        checks.error(f"{name}: media is outside the reviewed inventory: {relative}")
        unused = registered - used
        if unused:
            checks.error("Registered artwork is not referenced by the book: " + ", ".join(sorted(unused)))
        return figure_calls, len(used)
    except (OSError, UnicodeError, SyntaxError, ValueError, StopIteration) as exc:
        checks.error(f"Cannot resolve assembly references: {exc}")
        return 0, 0


def main() -> int:
    if sys.version_info < (3, 12):
        print("ERROR: Python 3.12 or newer is required.", file=sys.stderr)
        return 1
    try:
        from pypdf import PdfReader
    except ImportError:
        print("ERROR: Install dependencies with: python -m pip install -r requirements.txt", file=sys.stderr)
        return 1
    checks = Checks()
    chapters = check_chapters(checks)
    registered = check_inventory(checks, PdfReader)
    figures, media = check_references(checks, registered)
    texts = check_text(checks)
    if checks.errors:
        for message in checks.errors:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"Project check failed: {len(checks.errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Project check passed: {chapters} ready chapters; 181 one-page PDFs + cover JPEG; {figures} figure/illustration calls; {media} referenced media; {texts} UTF-8/LF text files; artwork hashes match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

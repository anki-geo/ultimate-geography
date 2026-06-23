#!/usr/bin/env python3
"""Lightweight checks for externalized deck HTML/CSS source files."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_ROOTS = [ROOT / "descriptions", ROOT / "templates"]
CSS_ROOTS = [ROOT / "styles"]


class FragmentParser(HTMLParser):
    def error(self, message: str) -> None:  # pragma: no cover; HTMLParser no longer calls this.
        raise ValueError(message)


def strip_css_comments_and_strings(source: str) -> str:
    out: list[str] = []
    i = 0
    quote: str | None = None
    in_comment = False
    while i < len(source):
        ch = source[i]
        nxt = source[i + 1] if i + 1 < len(source) else ""
        if in_comment:
            if ch == "*" and nxt == "/":
                in_comment = False
                i += 2
            else:
                i += 1
            continue
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch == "/" and nxt == "*":
            in_comment = True
            i += 2
            continue
        if ch in {'"', "'"}:
            quote = ch
            i += 1
            continue
        out.append(ch)
        i += 1
    if in_comment:
        raise ValueError("unterminated CSS comment")
    if quote:
        raise ValueError("unterminated CSS string")
    return "".join(out)


def check_balanced_css(path: Path, source: str) -> list[str]:
    errors: list[str] = []
    try:
        stripped = strip_css_comments_and_strings(source)
    except ValueError as exc:
        return [f"{path}: {exc}"]
    stack: list[tuple[str, int]] = []
    pairs = {"}": "{", ")": "(", "]": "["}
    openers = set(pairs.values())
    for line_no, line in enumerate(stripped.splitlines(), start=1):
        for ch in line:
            if ch in openers:
                stack.append((ch, line_no))
            elif ch in pairs:
                if not stack or stack[-1][0] != pairs[ch]:
                    errors.append(f"{path}:{line_no}: unmatched {ch!r}")
                else:
                    stack.pop()
    for ch, line_no in stack:
        errors.append(f"{path}:{line_no}: unmatched {ch!r}")
    return errors


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [f"{path}: not valid UTF-8: {exc}"]
    if not source:
        errors.append(f"{path}: empty file")
    if path.suffix == ".html":
        try:
            parser = FragmentParser(convert_charrefs=False)
            parser.feed(source)
            parser.close()
        except Exception as exc:  # HTMLParser is intentionally forgiving; catch hard failures.
            errors.append(f"{path}: HTML parser failed: {exc}")
    elif path.suffix == ".css":
        errors.extend(check_balanced_css(path, source))
    return errors


def main() -> int:
    files: list[Path] = []
    for root in HTML_ROOTS:
        files.extend(sorted(root.rglob("*.html")))
    for root in CSS_ROOTS:
        files.extend(sorted(root.rglob("*.css")))
    if not files:
        print("no external HTML/CSS source files found", file=sys.stderr)
        return 1
    errors: list[str] = []
    for path in files:
        errors.extend(check_file(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"checked {len(files)} external HTML/CSS source files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

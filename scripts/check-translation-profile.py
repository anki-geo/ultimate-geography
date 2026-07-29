#!/usr/bin/env python3
"""Keep both manifest translation profiles coherent and migration-safe."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (ROOT / "brainbrew.yaml", ROOT / "brainbrew-hardcore.yaml")
MARKER = "translation_profile:\n"
LIST_MESSAGE_PATTERN_CATEGORY = """    - key: list-message-pattern-glue
      label: List-message pattern glue
      paths:
        - 'note_types.*.fields.*.message_pattern.item_format'
        - 'note_types.*.fields.*.message_pattern.separator'
"""
LIST_MESSAGE_PATTERN_ORDER_ENTRY = "    - list-message-pattern-glue\n"
OBSOLETE_ENTRIES = (
    "    - key: structured-message-format\n",
    "        - 'notes.*.fields.*.message.format'\n",
)


def profile(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    if source.count(MARKER) != 1:
        raise ValueError(f"expected exactly one translation_profile in {path.relative_to(ROOT)}")
    return MARKER + source.split(MARKER, 1)[1]


def validate_list_message_pattern_category(path: Path, source: str) -> None:
    relative_path = path.relative_to(ROOT)
    if source.count(LIST_MESSAGE_PATTERN_CATEGORY) != 1:
        raise ValueError(
            f"expected exactly one canonical list-message pattern glue category in {relative_path}"
        )
    if source.count(LIST_MESSAGE_PATTERN_ORDER_ENTRY) != 1:
        raise ValueError(
            f"expected exactly one list-message pattern glue order entry in {relative_path}"
        )
    for obsolete_entry in OBSOLETE_ENTRIES:
        if obsolete_entry in source:
            raise ValueError(f"obsolete translation profile entry remains in {relative_path}")


def main() -> int:
    try:
        profiles = []
        for path in MANIFESTS:
            source = path.read_text(encoding="utf-8")
            validate_list_message_pattern_category(path, source)
            profiles.append(profile(path))
        main_profile, companion_profile = profiles
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    if main_profile != companion_profile:
        print("translation_profile differs between brainbrew.yaml and brainbrew-hardcore.yaml", file=sys.stderr)
        return 1
    print("translation profiles are identical and use list-message pattern glue paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

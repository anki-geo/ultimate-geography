#!/usr/bin/env python3
"""Keep the shared UG note-type map owned by one package-local include."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DECKS = (ROOT / "deck.yaml", ROOT / "deck-hardcore.yaml")
SHARED_NOTE_TYPES = ROOT / "note-types.yaml"
EXPECTED_INCLUDE = "note_types: !include note-types.yaml"
EXPECTED_NOTE_TYPE_ID = "note-type.ultimate-geography"
TOP_LEVEL_KEY = re.compile(r"^([^\s:#][^:]*):(?:\s|$)")


def main() -> int:
    try:
        for path in DECKS:
            declarations = [
                line
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.startswith("note_types:")
            ]
            if declarations != [EXPECTED_INCLUDE]:
                raise ValueError(
                    f"{path.relative_to(ROOT)} must declare exactly "
                    f"`{EXPECTED_INCLUDE}`"
                )

        top_level_keys = [
            match.group(1)
            for line in SHARED_NOTE_TYPES.read_text(encoding="utf-8").splitlines()
            if (match := TOP_LEVEL_KEY.match(line))
        ]
        if top_level_keys != [EXPECTED_NOTE_TYPE_ID]:
            raise ValueError(
                f"{SHARED_NOTE_TYPES.relative_to(ROOT)} must be a note-type map "
                f"rooted only at `{EXPECTED_NOTE_TYPE_ID}`"
            )
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    print("both deck shells use the shared Ultimate Geography note-type map")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

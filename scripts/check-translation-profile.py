#!/usr/bin/env python3
"""Keep the two alpha.2 manifest translation profiles byte-for-byte identical."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (ROOT / "brainbrew.yaml", ROOT / "brainbrew-hardcore.yaml")
MARKER = "translation_profile:\n"


def profile(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    if source.count(MARKER) != 1:
        raise ValueError(f"expected exactly one translation_profile in {path.relative_to(ROOT)}")
    return MARKER + source.split(MARKER, 1)[1]


def main() -> int:
    try:
        main_profile, companion_profile = (profile(path) for path in MANIFESTS)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    if main_profile != companion_profile:
        print("translation_profile differs between brainbrew.yaml and brainbrew-hardcore.yaml", file=sys.stderr)
        return 1
    print("translation profiles are identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

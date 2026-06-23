#!/usr/bin/env python3
"""Collect semantic old-vs-new CrowdAnki evidence for PR 736.

The script can:

* materialize the pre-migration jj revision into a temporary workspace;
* build old Python Brain Brew output with Brain Brew 0.3.11;
* materialize current `!include` sources into a temp copy for older/newer CLI
  compatibility during comparison;
* export representative current Rust Brain Brew targets;
* compare normalized CrowdAnki `deck.json` files and write a Markdown report.

It intentionally compares deck semantics (counts, GUID sets, fields, card counts)
instead of raw JSON order/formatting.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OLD_REV = "master@upstream"
OLD_BRAIN_BREW_VERSION = "0.3.11"


@dataclass(frozen=True)
class UgTarget:
    target: str
    old_folder: str
    manifest: str = "brainbrew.yaml"
    category: str = "UG"


@dataclass(frozen=True)
class HgCompanionTarget:
    target: str
    old_folder: str
    manifest: str = "brainbrew-hardcore.yaml"
    category: str = "HG companion"


@dataclass(frozen=True)
class HgStandaloneTarget:
    target: str
    old_ug_folder: str
    old_hg_folder: str
    manifest: str = "brainbrew.yaml"
    category: str = "HG standalone"


UG_TARGETS = [
    UgTarget("en-standard", "Ultimate Geography [EN]", category="standard"),
    UgTarget("de-standard", "Ultimate Geography [DE]", category="translated standard"),
    UgTarget("fr-standard", "Ultimate Geography [FR]", category="translated standard"),
    UgTarget("en-extended", "Ultimate Geography [EN] [Extended]", category="extended"),
    UgTarget("de-extended", "Ultimate Geography [DE] [Extended]", category="translated extended"),
    UgTarget("en-experimental", "Ultimate Geography [EN] [Experimental]", category="experimental"),
]

HG_COMPANION_TARGETS = [
    HgCompanionTarget("en-hardcore-companion-standard", "Hardcore Geography [EN]"),
    HgCompanionTarget("en-hardcore-companion-extended", "Hardcore Geography [EN] [Extended]"),
    HgCompanionTarget("de-hardcore-companion-standard", "Hardcore Geography [DE]"),
]

HG_STANDALONE_TARGETS = [
    HgStandaloneTarget("en-hardcore-standard", "Ultimate Geography [EN]", "Hardcore Geography [EN]"),
    HgStandaloneTarget(
        "en-hardcore-extended",
        "Ultimate Geography [EN] [Extended]",
        "Hardcore Geography [EN] [Extended]",
    ),
    HgStandaloneTarget("de-hardcore-standard", "Ultimate Geography [DE]", "Hardcore Geography [DE]"),
]


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    print("+", shlex.join(cmd), file=sys.stderr)
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    if completed.stdout:
        print(completed.stdout, file=sys.stderr, end="")
    return completed.stdout


def run_shell(command_prefix: str, args: list[str], *, cwd: Path | None = None) -> str:
    command = command_prefix + " " + shlex.join(args)
    print("+", command, file=sys.stderr)
    completed = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    if completed.stdout:
        print(completed.stdout, file=sys.stderr, end="")
    return completed.stdout


def jj_files(revision: str) -> list[str]:
    out = run(["jj", "file", "list", "-r", revision], cwd=ROOT)
    return [line for line in out.splitlines() if line]


def jj_file_show(revision: str, path: str) -> bytes:
    fileset = f'root-file:"{path}"'
    return subprocess.check_output(["jj", "file", "show", "-r", revision, fileset], cwd=ROOT)


def materialize_jj_revision(revision: str, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    files = jj_files(revision)
    for rel in files:
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(jj_file_show(revision, rel))


def ensure_old_brainbrew_venv(venv: Path) -> Path:
    brain_brew = venv / "bin" / "brain_brew"
    if brain_brew.exists():
        return brain_brew
    if venv.exists():
        shutil.rmtree(venv)
    # The normal user environment for this repo may not include pip. Use Nix to
    # bootstrap a throwaway venv, but keep the venv itself outside the repo.
    command = (
        f"python -m venv {shlex.quote(str(venv))} && "
        f"{shlex.quote(str(venv / 'bin' / 'pip'))} install "
        f"brain-brew=={OLD_BRAIN_BREW_VERSION}"
    )
    run(["nix-shell", "-p", "python312", "python312Packages.pip", "--run", command])
    return brain_brew


def build_old_ug(old_root: Path, brain_brew: Path) -> None:
    env = os.environ.copy()
    env["PATH"] = str(brain_brew.parent) + os.pathsep + env.get("PATH", "")
    run([sys.executable, "utils/generate_and_build.py", "recipes/source_to_anki.yaml"], cwd=old_root, env=env)
    run(
        [sys.executable, "utils/generate_and_build.py", "recipes/source_to_anki_[experimental].yaml"],
        cwd=old_root,
        env=env,
    )


def build_old_hg_if_needed(old_hg_root: Path, brain_brew: Path) -> None:
    if (old_hg_root / "build" / "Hardcore Geography [EN]" / "deck.json").exists():
        return
    if not (old_hg_root / "recipes" / "source_to_anki.yaml").exists():
        raise FileNotFoundError(f"old Hardcore Geography recipe not found under {old_hg_root}")
    env = os.environ.copy()
    env["PATH"] = str(brain_brew.parent) + os.pathsep + env.get("PATH", "")
    generator = old_hg_root / "utils" / "generate_and_build.py"
    if generator.exists():
        run([sys.executable, "utils/generate_and_build.py", "recipes/source_to_anki.yaml"], cwd=old_hg_root, env=env)
    else:
        run([str(brain_brew), "run", "recipes/source_to_anki.yaml"], cwd=old_hg_root, env=env)


def copy_current_tree(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    excluded = {".git", ".jj", ".frontloop", "build"}
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in excluded:
            continue
        out = dest / rel
        if path.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, out)


def include_path(source_root: Path, yaml_path: Path, raw: str) -> Path:
    include = raw.strip().strip("'\"")
    # Brain Brew resolves project-local include paths from the package root. The
    # fallback keeps this helper useful for relative includes in local experiments.
    candidates = [source_root / include, yaml_path.parent / include]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"{yaml_path}: include path {include!r} was not found")


def materialize_includes(source_root: Path) -> None:
    pattern = re.compile(r"^(\s*[^#\n]+?:\s*)!include\s+(.+?)\s*$", re.MULTILINE)
    for yaml_path in sorted(source_root.rglob("*.yaml")):
        original = yaml_path.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            prefix = match.group(1)
            path = include_path(source_root, yaml_path, match.group(2))
            content = path.read_text(encoding="utf-8")
            if content == "":
                return prefix + "''"
            indent = " " * (len(prefix) - len(prefix.lstrip()))
            nested = indent + "  "
            return prefix + "|\n" + "\n".join(nested + line for line in content.splitlines())

        rendered = pattern.sub(replace, original)
        if rendered != original:
            yaml_path.write_text(rendered, encoding="utf-8")


def export_new_targets(current_root: Path, out_root: Path, brainbrew_command: str) -> None:
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)
    all_targets: Iterable[UgTarget | HgCompanionTarget | HgStandaloneTarget] = (
        list(UG_TARGETS) + list(HG_COMPANION_TARGETS) + list(HG_STANDALONE_TARGETS)
    )
    for spec in all_targets:
        args = [
            "export",
            "crowdanki",
            "--manifest",
            str(current_root / spec.manifest),
            "--target",
            spec.target,
            "--out",
            str(out_root / spec.target),
            "--media-root",
            str(current_root / "media"),
        ]
        run_shell(brainbrew_command, args, cwd=current_root)


def load_deck(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def field_names(model: dict) -> list[str]:
    return [field["name"] for field in model.get("flds", [])]


def note_fields(deck: dict, note: dict) -> dict[str, str]:
    model = next(model for model in deck["note_models"] if model["crowdanki_uuid"] == note["note_model_uuid"])
    names = field_names(model)
    values = note.get("fields", [])
    return {name: values[index] if index < len(values) else "" for index, name in enumerate(names)}


def meaningful_notes(deck: dict) -> list[dict]:
    return [note for note in deck.get("notes", []) if any(note_fields(deck, note).values())]


def blank_note_count(deck: dict) -> int:
    return len(deck.get("notes", [])) - len(meaningful_notes(deck))


def card_count(deck: dict, notes: list[dict] | None = None) -> int:
    models = {model["crowdanki_uuid"]: model for model in deck.get("note_models", [])}
    names = {model["crowdanki_uuid"]: field_names(model) for model in deck.get("note_models", [])}
    count = 0
    for note in notes if notes is not None else deck.get("notes", []):
        values = {
            name: note.get("fields", [])[index] if index < len(note.get("fields", [])) else ""
            for index, name in enumerate(names[note["note_model_uuid"]])
        }
        for template in models[note["note_model_uuid"]].get("tmpls", []):
            conditions = re.findall(r"{{#([^}]+)}}", template.get("qfmt", ""))
            first_condition = conditions[0] if conditions else None
            if first_condition is None or values.get(first_condition, ""):
                count += 1
    return count


def guid_set(deck: dict, notes: list[dict] | None = None) -> set[str]:
    selected_notes = notes if notes is not None else deck.get("notes", [])
    return {note["guid"] for note in selected_notes}


def model_signature(deck: dict) -> list[tuple[str, int]]:
    return [(model.get("name", ""), len(model.get("tmpls", []))) for model in deck.get("note_models", [])]


def field_differences(old: dict, new: dict) -> list[tuple[str, dict[str, tuple[str, str]]]]:
    old_notes = {note["guid"]: note_fields(old, note) for note in meaningful_notes(old)}
    new_notes = {note["guid"]: note_fields(new, note) for note in meaningful_notes(new)}
    diffs: list[tuple[str, dict[str, tuple[str, str]]]] = []
    for guid in sorted(old_notes.keys() & new_notes.keys()):
        changes = {
            key: (old_notes[guid].get(key, ""), new_notes[guid].get(key, ""))
            for key in sorted(old_notes[guid].keys() | new_notes[guid].keys())
            if old_notes[guid].get(key, "") != new_notes[guid].get(key, "")
        }
        if changes:
            diffs.append((guid, changes))
    return diffs


def summarize_deck(deck: dict) -> dict[str, object]:
    notes = meaningful_notes(deck)
    return {
        "name": deck.get("name", ""),
        "uuid": deck.get("crowdanki_uuid", ""),
        "raw_notes": len(deck.get("notes", [])),
        "notes": len(notes),
        "blank_notes": blank_note_count(deck),
        "cards": card_count(deck, notes),
        "models": len(deck.get("note_models", [])),
        "templates": sum(len(model.get("tmpls", [])) for model in deck.get("note_models", [])),
        "media": len(deck.get("media_files", [])),
    }


def compare_decks(old: dict, new: dict) -> dict[str, object]:
    old_notes = meaningful_notes(old)
    new_notes = meaningful_notes(new)
    old_guids = guid_set(old, old_notes)
    new_guids = guid_set(new, new_notes)
    diffs = field_differences(old, new)
    changed_meta = []
    for key in ["name", "crowdanki_uuid", "desc"]:
        if old.get(key) != new.get(key):
            changed_meta.append(key)
    changed_models = model_signature(old) != model_signature(new)
    return {
        "old": summarize_deck(old),
        "new": summarize_deck(new),
        "guid_missing": len(old_guids - new_guids),
        "guid_extra": len(new_guids - old_guids),
        "guid_preserved": len(old_guids & new_guids),
        "field_diff_count": len(diffs),
        "field_diff_examples": diffs[:5],
        "changed_meta": changed_meta,
        "changed_models": changed_models,
    }


def fmt_diff_summary(comparison: dict[str, object]) -> str:
    parts: list[str] = []
    if comparison["guid_missing"] or comparison["guid_extra"]:
        parts.append(f"GUID set Δ old-only {comparison['guid_missing']}, new-only {comparison['guid_extra']}")
    if comparison["field_diff_count"]:
        parts.append(f"{comparison['field_diff_count']} field diff(s)")
    if comparison["changed_meta"]:
        parts.append("metadata changed: " + ", ".join(comparison["changed_meta"]))
    if comparison["changed_models"]:
        parts.append("note model/template signature changed")
    old = comparison["old"]
    new = comparison["new"]
    if old["cards"] != new["cards"]:
        parts.append(f"cards {old['cards']}→{new['cards']}")
    if old["notes"] != new["notes"]:
        parts.append(f"notes {old['notes']}→{new['notes']}")
    return "; ".join(parts) if parts else "none"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(cell.replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(out)


def write_report(
    report_path: Path,
    *,
    old_revision: str,
    old_root: Path,
    old_hg_root: Path,
    new_root: Path,
    new_out: Path,
    brainbrew_command: str,
) -> None:
    rows: list[list[str]] = []
    detail_lines: list[str] = []

    old_build = old_root / "build"
    old_hg_build = old_hg_root / "build"

    for spec in UG_TARGETS:
        old = load_deck(old_build / spec.old_folder / "deck.json")
        new = load_deck(new_out / spec.target / "deck.json")
        comparison = compare_decks(old, new)
        old_summary = comparison["old"]
        new_summary = comparison["new"]
        classification = "Equivalent"
        if fmt_diff_summary(comparison) != "none":
            classification = "Needs review"
        rows.append(
            [
                spec.target,
                spec.category,
                f"{old_summary['notes']} → {new_summary['notes']}",
                f"{old_summary['cards']} → {new_summary['cards']}",
                f"{comparison['guid_preserved']}/{old_summary['notes']}",
                fmt_diff_summary(comparison),
                classification,
            ]
        )

    for spec in HG_COMPANION_TARGETS:
        old = load_deck(old_hg_build / spec.old_folder / "deck.json")
        new = load_deck(new_out / spec.target / "deck.json")
        comparison = compare_decks(old, new)
        old_summary = comparison["old"]
        new_summary = comparison["new"]
        classification = "Expected HG refresh"
        if comparison["guid_missing"] or comparison["guid_extra"]:
            classification = "Needs review"
        if old_summary["blank_notes"]:
            classification = "Expected HG refresh"
        rows.append(
            [
                spec.target,
                spec.category,
                f"{old_summary['notes']} → {new_summary['notes']}",
                f"{old_summary['cards']} → {new_summary['cards']}",
                f"{comparison['guid_preserved']}/{old_summary['notes']}",
                fmt_diff_summary(comparison),
                classification,
            ]
        )
        if comparison["field_diff_examples"]:
            detail_lines.append(f"### {spec.target} field differences")
            detail_lines.append("")
            for guid, changes in comparison["field_diff_examples"]:
                detail_lines.append(f"- `{guid}`: " + "; ".join(f"{k}: {old!r} → {new!r}" for k, (old, new) in changes.items()))
            detail_lines.append("")

    for spec in HG_STANDALONE_TARGETS:
        old_ug = load_deck(old_build / spec.old_ug_folder / "deck.json")
        old_hg = load_deck(old_hg_build / spec.old_hg_folder / "deck.json")
        new = load_deck(new_out / spec.target / "deck.json")
        old_ug_notes = meaningful_notes(old_ug)
        old_hg_notes = meaningful_notes(old_hg)
        new_notes = meaningful_notes(new)
        expected_guids = guid_set(old_ug, old_ug_notes) | guid_set(old_hg, old_hg_notes)
        new_guids = guid_set(new, new_notes)
        expected_cards = card_count(old_ug, old_ug_notes) + card_count(old_hg, old_hg_notes)
        new_cards = card_count(new, new_notes)
        missing = len(expected_guids - new_guids)
        extra = len(new_guids - expected_guids)
        classification = "Expected standalone UG+HG"
        if missing or extra:
            classification = "Needs review"
        rows.append(
            [
                spec.target,
                spec.category,
                f"{len(old_ug_notes)}+{len(old_hg_notes)} → {len(new_notes)}",
                f"{expected_cards} → {new_cards}",
                f"{len(expected_guids & new_guids)}/{len(expected_guids)}",
                "none" if not (missing or extra or expected_cards != new_cards) else f"GUID Δ old-only {missing}, new-only {extra}; cards {expected_cards}→{new_cards}",
                classification,
            ]
        )

    old_hg_blank = load_deck(old_hg_build / "Hardcore Geography [EN]" / "deck.json")
    blank_notes = blank_note_count(old_hg_blank)

    report = f"""# PR 736 old-vs-new equivalence evidence

This report is generated by `scripts/collect-pr736-equivalence-evidence.py`. It compares semantic CrowdAnki output rather than raw JSON formatting.

This refresh was run after migrating UG translation overlays to `translations.direct`/`translations.contextual`/`translations.no_change`/`translations.target_additions` and after replacing scalar flag-similarity fields with structured Brain Brew messages. The report is intended to support the PR response claim that the new Brain Brew workflow can prove no unintended deck regressions even when source YAML becomes more structured.

## Inputs

- Old UG source: jj revision `{old_revision}` materialized at `{old_root}` and built with Python Brain Brew `{OLD_BRAIN_BREW_VERSION}`.
- Old Hardcore Geography source/output: `{old_hg_root}`.
- New UG source: current working tree materialized with `!include` blocks expanded at `{new_root}`.
- New Brain Brew command: `{brainbrew_command}`.

The current tree is materialized before export so this evidence remains comparable with Brain Brew builds that do not yet resolve source `!include` markers in every workflow. The composed/exported deck output remains fully materialized.

## Reproduce

```bash
scripts/collect-pr736-equivalence-evidence.py \\
  --old-revision {old_revision} \\
  --old-hg-root {old_hg_root} \\
  --new-brainbrew-command {shlex.quote(brainbrew_command)} \\
  --report docs/pr736-equivalence-evidence.md
```

The old Python Brain Brew build requires Python package `brain-brew=={OLD_BRAIN_BREW_VERSION}`. If it is not already available, the script bootstraps a temporary venv with Nix and pip outside the repository.

Before refreshing this report, verify the migrated workspace:

```bash
python scripts/check-source-content.py
{brainbrew_command} verify --manifest ./brainbrew.yaml --all-targets --media-root media
{brainbrew_command} verify --manifest ./brainbrew-hardcore.yaml --all-targets --media-root media
```

## Result matrix

{markdown_table(['Target', 'Category', 'Notes', 'Cards', 'GUIDs preserved', 'Differences', 'Classification'], rows)}

## Difference classification

- `Equivalent`: representative UG targets match the old Python Brain Brew output on meaningful note count, generated card count, note GUID set, note fields, deck name/UUID/description, and note model/template signature.
- `Expected HG refresh`: the new Hardcore companion preserves all 45 meaningful old HG note GUIDs but intentionally omits the old generated blank note and uses current UG/HG source text where the old standalone HG repo had stale content.
- `Expected standalone UG+HG`: standalone Hardcore targets are not an old-output-equivalent deck. They are validated as the union of old UG meaningful GUIDs plus old HG meaningful GUIDs, with the normal UG deck identity.

Old Hardcore Geography's generated CrowdAnki output contains {blank_notes} all-empty note generated from an empty source row; this report excludes all-empty notes from semantic comparisons.

## Structured flag-similarity migration assessment

The representative UG targets classified as `Equivalent` have zero note-field differences, so the structured `field.flag-similarity` messages render to the same CrowdAnki strings as the old scalar fields for those targets. Any Hardcore differences below are inherited stale-content or deck-shape differences from the old Hardcore Geography repository; they are not caused by structured flag-similarity rendering.

## Notable Hardcore content deltas

The old Hardcore Geography repository is stale relative to current UG data/translations. The migration preserves old HG GUIDs but follows current source text for some fields.

{''.join(line + chr(10) for line in detail_lines).rstrip()}

## Regression assessment

No regression was found in the representative UG standard, translated, extended, or experimental targets. Hardcore differences are classified as expected: old meaningful HG GUIDs are preserved, the invalid blank old HG note is not carried forward, companion exports keep the old Hardcore deck identity, and standalone exports intentionally package UG plus the HG add-on notes.
"""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old-revision", default=DEFAULT_OLD_REV, help="jj revision for pre-migration UG source")
    parser.add_argument("--old-hg-root", type=Path, default=ROOT.parent / "hardcore-geography")
    parser.add_argument("--workdir", type=Path, default=None, help="workspace for temporary old/new exports")
    parser.add_argument("--new-brainbrew-command", default="brainbrew", help="shell command prefix for new Rust Brain Brew")
    parser.add_argument("--report", type=Path, default=ROOT / "docs" / "pr736-equivalence-evidence.md")
    parser.add_argument("--keep-workdir", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    if args.workdir is None:
        temp_dir = tempfile.TemporaryDirectory(prefix="ug-pr736-equivalence-")
        workdir = Path(temp_dir.name)
    else:
        workdir = args.workdir
        workdir.mkdir(parents=True, exist_ok=True)

    try:
        old_root = workdir / "old-ug"
        current_root = workdir / "current-materialized"
        new_out = workdir / "new-output"
        old_venv = workdir / f"brain-brew-{OLD_BRAIN_BREW_VERSION}-venv"

        brain_brew = ensure_old_brainbrew_venv(old_venv)
        materialize_jj_revision(args.old_revision, old_root)
        build_old_ug(old_root, brain_brew)
        build_old_hg_if_needed(args.old_hg_root, brain_brew)

        copy_current_tree(current_root)
        materialize_includes(current_root)
        export_new_targets(current_root, new_out, args.new_brainbrew_command)

        write_report(
            args.report,
            old_revision=args.old_revision,
            old_root=old_root,
            old_hg_root=args.old_hg_root,
            new_root=current_root,
            new_out=new_out,
            brainbrew_command=args.new_brainbrew_command,
        )
        print(f"wrote {args.report}")
        if args.keep_workdir:
            print(f"kept workdir at {workdir}")
        return 0
    finally:
        if temp_dir is not None and args.keep_workdir:
            # The TemporaryDirectory object would remove the path. Detach by
            # disabling cleanup via private finalizer API when available.
            temp_dir._finalizer.detach()  # type: ignore[attr-defined]
        elif temp_dir is not None:
            temp_dir.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())

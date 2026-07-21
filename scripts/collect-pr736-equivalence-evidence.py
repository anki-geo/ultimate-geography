#!/usr/bin/env python3
"""Rebuild immutable pre-migration outputs and collect PR 736 parity evidence.

The default invocation downloads revision-bound source archives for Ultimate
Geography and Hardcore Geography, builds them with Python Brain Brew 0.3.11,
exports representative targets from this checkout with the pinned Rust Brain
Brew alpha.3, and writes a deterministic Markdown report. Unknown semantic
changes fail the collector instead of being silently summarized.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import os
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
OLD_PYTHON_DEPENDENCIES = (
    ("brain-brew", "0.3.11"),
    ("ruamel.yaml", "0.19.1"),
    ("ruamel.yaml.clib", "0.2.15"),
    ("yamale", "6.1.0"),
    ("PyYAML", "6.0.3"),
)
OLD_BRAIN_BREW_VERSION = dict(OLD_PYTHON_DEPENDENCIES)["brain-brew"]
PINNED_BRAINBREW_REVISION = "6ee570d427a1a8eec92c22668442f9b7186f9ba7"
PINNED_BRAINBREW_COMMAND = (
    f"nix run github:jeprecated/brain-brew/{PINNED_BRAINBREW_REVISION} --"
)

UG_REVISION = "fee657631c04684b69861465827c1c09a58e893b"
UG_ARCHIVE_URL = f"https://github.com/anki-geo/ultimate-geography/archive/{UG_REVISION}.tar.gz"
UG_ARCHIVE_SHA256 = "87e152ced4e22b73e87cd42d8e4dee24d0cfefa857a6e1fa3cd178c76241fcfa"
HG_REVISION = "09ce7c3ba665eac6b0794d089a4e0bbafbfc0f46"
HG_ARCHIVE_URL = f"https://github.com/anki-geo/hardcore-geography/archive/{HG_REVISION}.tar.gz"
HG_ARCHIVE_SHA256 = "3889265eaf3b455808b80892747098c64d5fe0551f2d3ba392c561a64df206d0"

BLANK_HG_GUIDS = {
    "en": "IS&&N{37<f",
    "de": "AHMrBBF^A)",
}
HARDCORE_TRANSLATION_LANGUAGES = ("cs", "de", "es", "fr", "it", "nb", "nl", "pl", "pt", "ru", "sv", "zh")
EXPECTED_HARDCORE_DESCRIPTION_HASHES = (
    "15499ec9e9e748ed264586926adde790c1d6821b368d96614da7c56e697a307e",
    "946699f54eaa38c8aa542fcff1cc29c38be423373eacbc10f7e3d2b79f54d5b5",
)
EXPECTED_HARDCORE_FIELD_DELTAS = {
    "en": frozenset(
        {
            (",LnVW8IL`", 1, "Province of Indonesia.", "Island of Indonesia."),
        }
    ),
    "de": frozenset(
        {
            (
                "B3<jn]}sDM",
                1,
                "Überseegebiet des Vereinigten Königreichs.",
                "Britisches Überseegebiet.",
            ),
            (
                "Br5zA8p_}G",
                1,
                "Französisches Überseegebiet.",
                "Übersee-Département Frankreichs.",
            ),
            ("MkUL%72%~W", 2, "", "Camp Justice"),
            (
                "mA.03]{R}v",
                1,
                "Autonome Region von Portugal.",
                "Autonome Region Portugals.",
            ),
            (
                "n/S)_Np9Y9",
                1,
                "Übersee-Département von Frankreich.",
                "Übersee-Département Frankreichs.",
            ),
            (
                "p/4yo-ZA_H",
                1,
                "Autonome Region von Portugal.",
                "Autonome Region Portugals.",
            ),
            (
                "p_|}0P5qv.",
                1,
                "Übersee-Département Frankreichs",
                "Übersee-Département Frankreichs.",
            ),
            ("v(aCZjiB`E", 0, "Kanarischen Inseln", "Kanarische Inseln"),
            (
                "v(aCZjiB`E",
                1,
                "Autonome Gemeinschaft von Spanien.",
                "Autonome Gemeinschaft Spaniens.",
            ),
            ("w4Uw*3mvbq", 1, "Indonesische Provinz.", "Insel von Indonesien."),
            (
                "zmZKA0W&Y`",
                1,
                "Halbautonomer Teilstaat von Tansania.",
                "Halbautonomer Teilstaat Tansanias.",
            ),
        }
    ),
}
PR733_MEDIA = (
    "_ug-interactive_map_config.js",
    "_ug-interactive_map_init.js",
    "_ug-jsvectormap.js",
    "_ug-world.js",
)


@dataclass(frozen=True)
class TargetSpec:
    target: str
    category: str
    manifest: str
    language: str
    old_ug_folder: str | None = None
    old_hg_folder: str | None = None


TARGETS = (
    TargetSpec("en-standard", "source standard", "brainbrew.yaml", "en", old_ug_folder="Ultimate Geography [EN]"),
    TargetSpec("de-standard", "translated standard", "brainbrew.yaml", "de", old_ug_folder="Ultimate Geography [DE]"),
    TargetSpec("he-standard", "RTL standard", "brainbrew.yaml", "he", old_ug_folder="Ultimate Geography [HE]"),
    TargetSpec("zh-standard", "CJK standard", "brainbrew.yaml", "zh", old_ug_folder="Ultimate Geography [ZH]"),
    TargetSpec("en-extended", "Extended", "brainbrew.yaml", "en", old_ug_folder="Ultimate Geography [EN] [Extended]"),
    TargetSpec("en-experimental", "Experimental / PR #733", "brainbrew.yaml", "en", old_ug_folder="Ultimate Geography [EN] [Experimental]"),
    TargetSpec(
        "en-hardcore-companion-standard",
        "companion Hardcore",
        "brainbrew-hardcore.yaml",
        "en",
        old_hg_folder="Hardcore Geography [EN]",
    ),
    TargetSpec(
        "de-hardcore-companion-standard",
        "localized companion Hardcore",
        "brainbrew-hardcore.yaml",
        "de",
        old_hg_folder="Hardcore Geography [DE]",
    ),
    TargetSpec(
        "en-hardcore-standard",
        "standalone UG + Hardcore",
        "brainbrew.yaml",
        "en",
        old_ug_folder="Ultimate Geography [EN]",
        old_hg_folder="Hardcore Geography [EN]",
    ),
    TargetSpec(
        "de-hardcore-standard",
        "localized standalone UG + Hardcore",
        "brainbrew.yaml",
        "de",
        old_ug_folder="Ultimate Geography [DE]",
        old_hg_folder="Hardcore Geography [DE]",
    ),
)

GOLDEN_TARGETS = (
    ("en-standard", "source", "brainbrew.yaml"),
    ("de-standard", "translated", "brainbrew.yaml"),
    ("he-standard", "RTL", "brainbrew.yaml"),
    ("zh-standard", "CJK", "brainbrew.yaml"),
    ("en-extended", "Extended", "brainbrew.yaml"),
    ("en-experimental", "Experimental", "brainbrew.yaml"),
    ("de-hardcore-standard", "localized standalone Hardcore", "brainbrew.yaml"),
    (
        "de-hardcore-companion-standard",
        "localized companion Hardcore",
        "brainbrew-hardcore.yaml",
    ),
)

DECK_METADATA_KEYS = (
    "__type__",
    "children",
    "crowdanki_uuid",
    "deck_config_uuid",
    "desc",
    "dyn",
    "extendNew",
    "extendRev",
    "name",
)


class EvidenceError(RuntimeError):
    """An unclassified or unsafe historical difference."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def run(cmd: Sequence[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    print("+", shlex.join(str(part) for part in cmd), file=sys.stderr)
    completed = subprocess.run(
        [str(part) for part in cmd],
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch_archive(url: str, expected_sha256: str, destination: Path, override: Path | None) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if override is not None:
        source = override.resolve()
        require(source.is_file(), f"archive override does not exist: {source}")
        actual = sha256_file(source)
        require(actual == expected_sha256, f"archive override hash mismatch: expected {expected_sha256}, got {actual}")
        return source
    if not destination.exists() or sha256_file(destination) != expected_sha256:
        request = urllib.request.Request(url, headers={"User-Agent": "ultimate-geography-pr736-evidence"})
        with urllib.request.urlopen(request) as response, destination.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    actual = sha256_file(destination)
    require(actual == expected_sha256, f"downloaded archive hash mismatch: expected {expected_sha256}, got {actual}")
    return destination


def extract_revision_archive(archive: Path, destination: Path, revision: str) -> None:
    marker = destination / ".pr736-evidence-revision"
    if marker.is_file() and marker.read_text(encoding="utf-8").strip() == revision:
        return
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        top_levels = {PurePosixPath(member.name).parts[0] for member in members if member.name}
        require(len(top_levels) == 1, f"archive for {revision} has an unexpected root layout")
        top = next(iter(top_levels))
        for member in members:
            parts = PurePosixPath(member.name).parts
            if not parts or parts[0] != top or len(parts) == 1:
                continue
            relative = PurePosixPath(*parts[1:])
            require(".." not in relative.parts and not relative.is_absolute(), "unsafe path in source archive")
            out = destination.joinpath(*relative.parts)
            if member.isdir():
                out.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                out.parent.mkdir(parents=True, exist_ok=True)
                source = bundle.extractfile(member)
                require(source is not None, f"could not read {member.name} from archive")
                with source, out.open("wb") as handle:
                    shutil.copyfileobj(source, handle)
                out.chmod(member.mode & 0o777)
            else:
                raise EvidenceError(f"unsupported archive entry type: {member.name}")
    marker.write_text(revision + "\n", encoding="utf-8")


def verify_old_python_dependencies(python: Path) -> None:
    package_names = [name for name, _ in OLD_PYTHON_DEPENDENCIES]
    script = (
        "import importlib.metadata, json; "
        f"names = {package_names!r}; "
        "print(json.dumps({name: importlib.metadata.version(name) for name in names}, sort_keys=True))"
    )
    installed = json.loads(run([str(python), "-c", script]))
    expected = dict(OLD_PYTHON_DEPENDENCIES)
    require(installed == expected, f"old Python dependency versions differ: expected {expected}, got {installed}")


def ensure_old_brainbrew_venv(venv: Path, override: Path | None) -> Path:
    if override is not None:
        executable = override.resolve()
        require(executable.is_file(), f"old Brain Brew override does not exist: {executable}")
        verify_old_python_dependencies(executable.parent / "python")
        return executable
    brain_brew = venv / "bin" / "brain_brew"
    python = venv / "bin" / "python"
    pip = venv / "bin" / "pip"
    requirements = [f"{name}=={version}" for name, version in OLD_PYTHON_DEPENDENCIES]
    if not python.exists():
        if venv.exists():
            shutil.rmtree(venv)
        command = f"python -m venv {shlex.quote(str(venv))}"
        run(["nix-shell", "-p", "python312", "python312Packages.pip", "--run", command])
    run([str(pip), "install", *requirements])
    require(brain_brew.is_file(), "pinned old Brain Brew executable was not installed")
    verify_old_python_dependencies(python)
    return brain_brew


def required_old_ug_outputs(root: Path) -> list[Path]:
    return [root / "build" / spec.old_ug_folder / "deck.json" for spec in TARGETS if spec.old_ug_folder]


def required_old_hg_outputs(root: Path) -> list[Path]:
    return [root / "build" / spec.old_hg_folder / "deck.json" for spec in TARGETS if spec.old_hg_folder]


def build_old_ug(root: Path, brain_brew: Path) -> None:
    if all(path.is_file() for path in required_old_ug_outputs(root)):
        return
    env = os.environ.copy()
    env["PATH"] = str(brain_brew.parent) + os.pathsep + env.get("PATH", "")
    run([sys.executable, "utils/generate_and_build.py", "recipes/source_to_anki.yaml"], cwd=root, env=env)
    run(
        [sys.executable, "utils/generate_and_build.py", "recipes/source_to_anki_[experimental].yaml"],
        cwd=root,
        env=env,
    )


def build_old_hg(root: Path, brain_brew: Path) -> None:
    if all(path.is_file() for path in required_old_hg_outputs(root)):
        return
    env = os.environ.copy()
    env["PATH"] = str(brain_brew.parent) + os.pathsep + env.get("PATH", "")
    run([str(brain_brew), "run", "recipes/source_to_anki.yaml"], cwd=root, env=env)


def export_new_targets(output_root: Path, command: Sequence[str]) -> None:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    for spec in TARGETS:
        output = output_root / spec.target
        run(
            [
                *command,
                "export",
                "crowdanki",
                "--manifest",
                spec.manifest,
                "--target",
                spec.target,
                "--out",
                str(output),
                "--media-root",
                "media",
            ],
            cwd=ROOT,
        )
        require((output / "deck.json").is_file(), f"missing new export for {spec.target}")


def export_current_hardcore_alignment_targets(
    output_root: Path,
    command: Sequence[str],
) -> dict[str, tuple[Path, Path, str]]:
    outputs: dict[str, tuple[Path, Path, str]] = {}
    alignment_root = output_root / "current-composition"
    for language in HARDCORE_TRANSLATION_LANGUAGES:
        main_target = f"{language}-hardcore-standard"
        companion_target = f"{language}-hardcore-companion-standard"
        if language == "de":
            outputs[language] = (output_root / main_target, output_root / companion_target, "strict")
            continue
        main_output = alignment_root / main_target
        companion_output = alignment_root / companion_target
        for manifest, target, output in (
            ("brainbrew.yaml", main_target, main_output),
            ("brainbrew-hardcore.yaml", companion_target, companion_output),
        ):
            run(
                [
                    *command,
                    "export",
                    "crowdanki",
                    "--manifest",
                    manifest,
                    "--target",
                    target,
                    "--out",
                    str(output),
                    "--media-mode",
                    "reference-only",
                ],
                cwd=ROOT,
            )
            require((output / "deck.json").is_file(), f"missing current-composition export for {target}")
        outputs[language] = (main_output, companion_output, "reference-only")
    return outputs


def load_deck(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"{path} is not a CrowdAnki deck object")
    return value


def models_by_uuid(deck: dict) -> dict[str, dict]:
    models = {model["crowdanki_uuid"]: model for model in deck.get("note_models", [])}
    require(len(models) == len(deck.get("note_models", [])), "duplicate note model UUID")
    return models


def field_names(deck: dict, note: dict) -> list[str]:
    model = models_by_uuid(deck)[note["note_model_uuid"]]
    return [field["name"] for field in model.get("flds", [])]


def is_blank_note(deck: dict, note: dict) -> bool:
    names = field_names(deck, note)
    values = note.get("fields", [])
    return not any(values[index] if index < len(values) else "" for index in range(len(names)))


def meaningful_notes(deck: dict) -> list[dict]:
    return [note for note in deck.get("notes", []) if not is_blank_note(deck, note)]


def require_blank_note_policy(
    deck: dict,
    expected_blank_guids: Sequence[str],
    context: str,
) -> None:
    raw_notes = deck.get("notes", [])
    meaningful = meaningful_notes(deck)
    blank_guids = tuple(note["guid"] for note in raw_notes if is_blank_note(deck, note))
    expected = tuple(expected_blank_guids)
    require(
        len(raw_notes) == len(meaningful) + len(expected),
        f"{context}: raw/meaningful note counts violate blank-note policy: "
        f"raw={len(raw_notes)}, meaningful={len(meaningful)}, expected blanks={len(expected)}",
    )
    require(
        blank_guids == expected,
        f"{context}: blank-note GUIDs differ: expected {expected!r}, got {blank_guids!r}",
    )


def notes_by_guid(deck: dict) -> dict[str, dict]:
    notes = {note["guid"]: note for note in meaningful_notes(deck)}
    require(len(notes) == len(meaningful_notes(deck)), "duplicate meaningful note GUID")
    return notes


def card_count(deck: dict, notes: Iterable[dict] | None = None) -> int:
    models = models_by_uuid(deck)
    count = 0
    for note in notes if notes is not None else meaningful_notes(deck):
        model = models[note["note_model_uuid"]]
        names = [field["name"] for field in model.get("flds", [])]
        values = {
            name: note.get("fields", [])[index] if index < len(note.get("fields", [])) else ""
            for index, name in enumerate(names)
        }
        for template in model.get("tmpls", []):
            conditions = []
            source = template.get("qfmt", "")
            start = 0
            while True:
                marker = source.find("{{#", start)
                if marker < 0:
                    break
                end = source.find("}}", marker)
                if end < 0:
                    break
                conditions.append(source[marker + 3 : end])
                start = end + 2
            if not conditions or values.get(conditions[0], ""):
                count += 1
    return count


def deck_metadata(deck: dict) -> dict[str, object]:
    return {key: deck.get(key) for key in DECK_METADATA_KEYS}


def compare_note_payloads(old: dict, new: dict) -> dict[str, object]:
    old_notes = notes_by_guid(old)
    new_notes = notes_by_guid(new)
    common = sorted(old_notes.keys() & new_notes.keys())
    field_diffs: list[tuple[str, list[tuple[int, str, str]]]] = []
    tag_order_changes = 0
    tag_membership_changes = 0
    other_changes: list[tuple[str, str]] = []
    model_uuid_changes = 0
    for guid in common:
        before = old_notes[guid]
        after = new_notes[guid]
        values = [
            (index, left, right)
            for index, (left, right) in enumerate(zip(before.get("fields", []), after.get("fields", [])))
            if left != right
        ]
        if len(before.get("fields", [])) != len(after.get("fields", [])):
            values.append((-1, repr(before.get("fields", [])), repr(after.get("fields", []))))
        if values:
            field_diffs.append((guid, values))
        if set(before.get("tags", [])) != set(after.get("tags", [])):
            tag_membership_changes += 1
        elif before.get("tags", []) != after.get("tags", []):
            tag_order_changes += 1
        if before.get("note_model_uuid") != after.get("note_model_uuid"):
            model_uuid_changes += 1
        for key in sorted(set(before) | set(after)):
            if key in {"fields", "guid", "note_model_uuid", "tags"}:
                continue
            if before.get(key) != after.get(key):
                other_changes.append((guid, key))
    return {
        "old_count": len(old_notes),
        "new_count": len(new_notes),
        "preserved": len(common),
        "old_only": sorted(old_notes.keys() - new_notes.keys()),
        "new_only": sorted(new_notes.keys() - old_notes.keys()),
        "field_diffs": field_diffs,
        "tag_order_changes": tag_order_changes,
        "tag_membership_changes": tag_membership_changes,
        "other_changes": other_changes,
        "model_uuid_changes": model_uuid_changes,
    }


def require_expected_hardcore_field_deltas(language: str, comparison: dict[str, object], target: str) -> None:
    actual = frozenset(
        (guid, index, before, after)
        for guid, changes in comparison["field_diffs"]
        for index, before, after in changes
    )
    expected = EXPECTED_HARDCORE_FIELD_DELTAS[language]
    require(actual == expected, f"{target}: Hardcore field deltas differ: expected {expected!r}, got {actual!r}")


def directory_media_hashes(deck: dict, output: Path) -> dict[str, str]:
    declared = deck.get("media_files", [])
    require(len(declared) == len(set(declared)), f"duplicate media filename under {output}")
    result: dict[str, str] = {}
    for filename in declared:
        path = output / "media" / filename
        require(path.is_file(), f"declared media missing from historical/export output: {filename}")
        result[filename] = sha256_file(path)
    actual = {path.name for path in (output / "media").iterdir() if path.is_file()}
    require(actual == set(declared), f"undeclared or uncopied media under {output}")
    return result


def union_media_hashes(parts: Sequence[tuple[dict, Path]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for deck, output in parts:
        for filename, digest in directory_media_hashes(deck, output).items():
            if filename in result:
                require(result[filename] == digest, f"historical media collision has different bytes: {filename}")
            result[filename] = digest
    return result


def changed_model_surface(old_model: dict, new_model: dict, language: str, target: str) -> dict[str, object]:
    expected_direction = "rtl" if language == "he" else "ltr"
    baseline_css = old_model["css"]
    if target == "en-experimental":
        baseline_css = baseline_css.replace('@import url("_ug-jsvectormap.min.css");\n\n', "", 1)
    expected_css = baseline_css.replace(
        "  color: black;\n",
        f"  color: black;\n  direction: {expected_direction};\n",
        1,
    )
    require(expected_css == new_model["css"], f"{target}: unclassified CSS difference")

    require(len(old_model["tmpls"]) == len(new_model["tmpls"]), f"{target}: template count changed")
    removed_wrappers = 0
    added_pr733_links = 0
    capital_hint_deltas: list[tuple[str, str]] = []
    for before, after in zip(old_model["tmpls"], new_model["tmpls"]):
        require(
            {key: value for key, value in before.items() if key not in {"qfmt", "afmt"}}
            == {key: value for key, value in after.items() if key not in {"qfmt", "afmt"}},
            f"{target}: card name/order/configuration changed for {before.get('name')}",
        )
        for key in ("qfmt", "afmt"):
            for line in difflib.ndiff(before[key].splitlines(), after[key].splitlines()):
                if line.startswith("  ") or line.startswith("? "):
                    continue
                value = line[2:]
                if line.startswith("- ") and value == f'<div dir="{expected_direction}">':
                    removed_wrappers += 1
                elif line.startswith("- ") and value == "</div>":
                    removed_wrappers += 1
                elif line.startswith("+ ") and value == '<link rel="stylesheet" href="_ug-jsvectormap.min.css" data-nn-media-src="_ug-jsvectormap.min.css">':
                    added_pr733_links += 1
                elif "{{Capital hint}}" in value and "<div class=\"info\">" in value:
                    if line.startswith("- "):
                        capital_hint_deltas.append((value, ""))
                    elif line.startswith("+ "):
                        require(capital_hint_deltas and capital_hint_deltas[-1][1] == "", f"{target}: unexpected capital-hint addition")
                        old_value, _ = capital_hint_deltas[-1]
                        capital_hint_deltas[-1] = (old_value, value)
                else:
                    raise EvidenceError(f"{target}: unclassified template line delta: {line}")
    require(removed_wrappers == len(old_model["tmpls"]) * 4, f"{target}: incomplete direction-wrapper relocation")
    expected_links = 2 if target == "en-experimental" else 0
    require(added_pr733_links == expected_links, f"{target}: unexpected Experimental stylesheet-link delta")
    expected_hint = 1 if target in {"de-standard", "zh-standard", "de-hardcore-companion-standard", "de-hardcore-standard"} else 0
    require(len(capital_hint_deltas) == expected_hint, f"{target}: unexpected capital-hint delta count")
    for before, after in capital_hint_deltas:
        require("Hint: {{Capital hint}}" in after, f"{target}: unexpected capital-hint fallback")
        require(before != after, f"{target}: capital-hint delta was not localized in the baseline")
    return {
        "direction": expected_direction,
        "templates": len(old_model["tmpls"]),
        "capital_hint_deltas": capital_hint_deltas,
        "pr733_links": added_pr733_links,
    }


def compare_ug_model(old_model: dict, new_model: dict, language: str, target: str) -> dict[str, object]:
    require(
        {key: value for key, value in old_model.items() if key not in {"css", "flds", "tmpls"}}
        == {key: value for key, value in new_model.items() if key not in {"css", "flds", "tmpls"}},
        f"{target}: note-model identity/name/configuration changed",
    )
    require(len(old_model["flds"]) == len(new_model["flds"]), f"{target}: field count changed")
    rtl_changes = 0
    for before, after in zip(old_model["flds"], new_model["flds"]):
        deltas = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
        if language == "he" and deltas == {"rtl"} and before.get("rtl") is True and after.get("rtl") is False:
            rtl_changes += 1
        else:
            require(not deltas, f"{target}: unclassified field schema/configuration change: {deltas}")
    require(rtl_changes == (6 if language == "he" else 0), f"{target}: unexpected RTL-field relocation count")
    layout = changed_model_surface(old_model, new_model, language, target)
    layout["rtl_field_changes"] = rtl_changes
    return layout


def compare_ug_target(spec: TargetSpec, old_output: Path, new_output: Path) -> dict[str, object]:
    old = load_deck(old_output / "deck.json")
    new = load_deck(new_output / "deck.json")
    require_blank_note_policy(old, (), f"{spec.target}: immutable UG")
    require_blank_note_policy(new, (), f"{spec.target}: alpha.3 UG")
    require(deck_metadata(old) == deck_metadata(new), f"{spec.target}: deck metadata/identity/description changed")
    require(old.get("deck_configurations") == new.get("deck_configurations"), f"{spec.target}: deck configuration changed")
    require(len(old["note_models"]) == len(new["note_models"]) == 1, f"{spec.target}: note model count changed")
    model = compare_ug_model(old["note_models"][0], new["note_models"][0], spec.language, spec.target)
    notes = compare_note_payloads(old, new)
    require(not notes["old_only"] and not notes["new_only"], f"{spec.target}: GUID set changed")
    require(not notes["field_diffs"], f"{spec.target}: note field values/order changed")
    require(notes["tag_membership_changes"] == 0, f"{spec.target}: tag membership changed")
    require(notes["other_changes"] == [], f"{spec.target}: note metadata changed")
    require(notes["model_uuid_changes"] == 0, f"{spec.target}: note model assignment changed")
    old_media = directory_media_hashes(old, old_output)
    new_media = directory_media_hashes(new, new_output)
    require(old_media == new_media, f"{spec.target}: media filenames or bytes changed")
    classification = "equivalent with direction represented in CSS"
    if model["capital_hint_deltas"]:
        classification = "known deferred capital-hint label fallback"
    if spec.target == "en-experimental":
        classification = "PR #733 bytes preserved; explicit stylesheet link added"
    return {
        "spec": spec,
        "old": old,
        "new": new,
        "notes": notes,
        "model": model,
        "media": new_media,
        "classification": classification,
    }


def compare_companion_target(
    spec: TargetSpec,
    old_output: Path,
    new_output: Path,
    old_ug_reference: Path,
) -> dict[str, object]:
    old = load_deck(old_output / "deck.json")
    new = load_deck(new_output / "deck.json")
    old_ug = load_deck(old_ug_reference / "deck.json")
    require_blank_note_policy(old_ug, (), f"{spec.target}: immutable UG model reference")
    require_blank_note_policy(old, (BLANK_HG_GUIDS[spec.language],), f"{spec.target}: immutable Hardcore")
    require_blank_note_policy(new, (), f"{spec.target}: alpha.3 companion")
    old_meta = deck_metadata(old)
    new_meta = deck_metadata(new)
    for key in DECK_METADATA_KEYS:
        if key == "desc":
            continue
        require(old_meta[key] == new_meta[key], f"{spec.target}: companion deck identity/metadata changed at {key}")
    description_hashes = (sha256_bytes(old["desc"].encode()), sha256_bytes(new["desc"].encode()))
    require(
        description_hashes == EXPECTED_HARDCORE_DESCRIPTION_HASHES,
        f"{spec.target}: companion description hashes differ: expected {EXPECTED_HARDCORE_DESCRIPTION_HASHES!r}, got {description_hashes!r}",
    )
    require(old.get("deck_configurations") == new.get("deck_configurations"), f"{spec.target}: deck configuration changed")
    require(len(old["note_models"]) == len(new["note_models"]) == 1, f"{spec.target}: note model count changed")
    old_model = old["note_models"][0]
    new_model = new["note_models"][0]
    old_ug_model = old_ug["note_models"][0]
    require(old_model["flds"] == new_model["flds"], f"{spec.target}: field schema/order/configuration changed")
    require(
        {key: value for key, value in old_model.items() if key not in {"css", "crowdanki_uuid", "flds", "name", "tmpls"}}
        == {key: value for key, value in new_model.items() if key not in {"css", "crowdanki_uuid", "flds", "name", "tmpls"}},
        f"{spec.target}: unclassified note-model configuration changed",
    )
    if spec.language == "en":
        require(
            (old_model["crowdanki_uuid"], old_model["name"]) == (new_model["crowdanki_uuid"], new_model["name"]),
            f"{spec.target}: English note-model identity changed",
        )
    else:
        require(
            (new_model["crowdanki_uuid"], new_model["name"])
            == (old_ug_model["crowdanki_uuid"], old_ug_model["name"]),
            f"{spec.target}: localized companion does not align to the immutable UG note model",
        )
    # The historical Hardcore repository carried a stale model surface. The
    # companion must align to the same-language immutable UG model so importing
    # it into UG reuses the correct note type rather than perpetuating that copy.
    layout = compare_ug_model(old_ug_model, new_model, spec.language, spec.target)
    notes = compare_note_payloads(old, new)
    require(not notes["old_only"] and not notes["new_only"], f"{spec.target}: meaningful Hardcore GUID set changed")
    require_expected_hardcore_field_deltas(spec.language, notes, spec.target)
    require(notes["tag_membership_changes"] == 0, f"{spec.target}: Hardcore tag membership changed")
    require(notes["other_changes"] == [], f"{spec.target}: Hardcore note metadata changed")
    expected_model_changes = 0 if spec.language == "en" else 45
    require(notes["model_uuid_changes"] == expected_model_changes, f"{spec.target}: unexpected note-model reassignment count")
    old_media = directory_media_hashes(old, old_output)
    new_media = directory_media_hashes(new, new_output)
    require(old_media == new_media, f"{spec.target}: companion media filenames or bytes changed")
    overlapping_old = sum("UG::Overlapping" in note.get("tags", []) for note in meaningful_notes(old))
    overlapping_new = sum("UG::Overlapping" in note.get("tags", []) for note in meaningful_notes(new))
    require(overlapping_old == overlapping_new, f"{spec.target}: overlap tag count changed")
    return {
        "spec": spec,
        "old": old,
        "new": new,
        "notes": notes,
        "model": layout,
        "media": new_media,
        "overlapping": overlapping_new,
        "description_hashes": description_hashes,
        "classification": "preserved identity/GUIDs with classified old-Hardcore refresh",
    }


def compare_standalone_target(
    spec: TargetSpec,
    old_ug_output: Path,
    old_hg_output: Path,
    new_output: Path,
) -> dict[str, object]:
    old_ug = load_deck(old_ug_output / "deck.json")
    old_hg = load_deck(old_hg_output / "deck.json")
    new = load_deck(new_output / "deck.json")
    require_blank_note_policy(old_ug, (), f"{spec.target}: immutable UG source")
    require_blank_note_policy(
        old_hg,
        (BLANK_HG_GUIDS[spec.language],),
        f"{spec.target}: immutable Hardcore source",
    )
    require_blank_note_policy(new, (), f"{spec.target}: alpha.3 standalone")
    require(deck_metadata(old_ug) == deck_metadata(new), f"{spec.target}: standalone does not preserve UG deck identity/metadata")
    require(old_ug.get("deck_configurations") == new.get("deck_configurations"), f"{spec.target}: standalone deck configuration changed")
    require(len(old_ug["note_models"]) == len(new["note_models"]) == 1, f"{spec.target}: standalone note model count changed")
    model = compare_ug_model(old_ug["note_models"][0], new["note_models"][0], spec.language, spec.target)

    ug_notes = notes_by_guid(old_ug)
    hg_notes = notes_by_guid(old_hg)
    new_notes = notes_by_guid(new)
    require(not (set(ug_notes) & set(hg_notes)), f"{spec.target}: immutable UG/HG GUID sources unexpectedly overlap")
    require(set(new_notes) == set(ug_notes) | set(hg_notes), f"{spec.target}: standalone GUID union changed")

    ug_view = dict(new)
    ug_view["notes"] = [new_notes[guid] for guid in sorted(ug_notes)]
    old_ug_view = dict(old_ug)
    old_ug_view["notes"] = [ug_notes[guid] for guid in sorted(ug_notes)]
    ug_comparison = compare_note_payloads(old_ug_view, ug_view)
    require(not ug_comparison["field_diffs"], f"{spec.target}: ordinary UG fields changed in standalone")
    require(ug_comparison["tag_membership_changes"] == 0, f"{spec.target}: ordinary UG tags changed in standalone")
    require(ug_comparison["other_changes"] == [], f"{spec.target}: ordinary UG note metadata changed in standalone")
    require(ug_comparison["model_uuid_changes"] == 0, f"{spec.target}: ordinary UG model assignment changed in standalone")

    hg_view = dict(new)
    hg_view["notes"] = [new_notes[guid] for guid in sorted(hg_notes)]
    old_hg_view = dict(old_hg)
    old_hg_view["notes"] = [hg_notes[guid] for guid in sorted(hg_notes)]
    hg_comparison = compare_note_payloads(old_hg_view, hg_view)
    require_expected_hardcore_field_deltas(spec.language, hg_comparison, spec.target)
    require(hg_comparison["tag_membership_changes"] == 0, f"{spec.target}: standalone Hardcore tags changed")
    require(hg_comparison["other_changes"] == [], f"{spec.target}: standalone Hardcore note metadata changed")
    expected_model_changes = 0 if spec.language == "en" else 45
    require(hg_comparison["model_uuid_changes"] == expected_model_changes, f"{spec.target}: standalone Hardcore model assignment changed")

    expected_media = union_media_hashes(((old_ug, old_ug_output), (old_hg, old_hg_output)))
    new_media = directory_media_hashes(new, new_output)
    require(expected_media == new_media, f"{spec.target}: standalone media is not the byte-exact UG/HG union")
    overlapping_old = sum("UG::Overlapping" in note.get("tags", []) for note in meaningful_notes(old_hg))
    overlapping_new = sum("UG::Overlapping" in new_notes[guid].get("tags", []) for guid in hg_notes)
    require(overlapping_old == overlapping_new, f"{spec.target}: standalone overlap tags changed")
    return {
        "spec": spec,
        "old_ug": old_ug,
        "old_hg": old_hg,
        "new": new,
        "ug_notes": ug_comparison,
        "hg_notes": hg_comparison,
        "model": model,
        "media": new_media,
        "overlapping": overlapping_new,
        "classification": "exact UG identity plus preserved 319+45 GUID/media union",
    }


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("|", "\\|").replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(lines)


def inline_code(value: str) -> str:
    return f"<code>{html.escape(value)}</code>"


def field_diff_samples(result: dict[str, object], limit: int = 10) -> list[str]:
    lines: list[str] = []
    old = result["old"]
    new = result["new"]
    old_model = old["note_models"][0]
    new_model = new["note_models"][0]
    old_names = [field["name"] for field in old_model["flds"]]
    new_names = [field["name"] for field in new_model["flds"]]
    for guid, changes in result["notes"]["field_diffs"][:limit]:
        rendered = []
        for index, before, after in changes:
            name = new_names[index] if 0 <= index < len(new_names) else old_names[index] if 0 <= index < len(old_names) else "field-list"
            rendered.append(f"{name}: {before!r} → {after!r}")
        lines.append(f"- {inline_code(guid)} — " + "; ".join(rendered))
    return lines


def write_report(
    report_path: Path,
    results: Sequence[dict[str, object]],
    command: Sequence[str],
    current_alignment: Sequence[dict[str, str]],
) -> None:
    ug_results = [result for result in results if result["spec"].old_ug_folder and not result["spec"].old_hg_folder]
    companion_results = [result for result in results if result["spec"].old_hg_folder and not result["spec"].old_ug_folder]
    standalone_results = [result for result in results if result["spec"].old_hg_folder and result["spec"].old_ug_folder]

    rows: list[list[str]] = []
    surface_rows: list[list[str]] = []
    for result in ug_results:
        spec = result["spec"]
        notes = result["notes"]
        deck = result["new"]
        rows.append(
            [
                spec.target,
                spec.category,
                f"{notes['old_count']} → {notes['new_count']}",
                f"{len(result['old']['notes'])} → {len(deck['notes'])}; 0 → 0 blanks",
                f"{notes['preserved']}/{notes['old_count']}",
                f"{card_count(result['old'])} → {card_count(deck)}",
                str(len(result["media"])),
                result["classification"],
            ]
        )
        schema = "exact"
        if result["model"]["rtl_field_changes"]:
            schema = f"{result['model']['rtl_field_changes']} `rtl` flags represented by CSS"
        template = "direction wrapper → CSS"
        if result["model"]["capital_hint_deltas"]:
            template += "; localized capital-hint label falls back to English"
        if result["model"]["pr733_links"]:
            template += "; explicit jsVectorMap stylesheet link"
        surface_rows.append(
            [spec.target, "exact", "exact", schema, template, "exact by GUID/field order/tag set", "exact", "exact names + SHA-256"]
        )

    for result in companion_results:
        spec = result["spec"]
        notes = result["notes"]
        model_identity = "exact" if spec.language == "en" else "aligned to immutable UG localized model UUID/name"
        rows.append(
            [
                spec.target,
                spec.category,
                f"{notes['old_count']} → {notes['new_count']}",
                f"{len(result['old']['notes'])} → {len(result['new']['notes'])}; 1 exact → 0 blanks",
                f"{notes['preserved']}/{notes['old_count']}",
                f"{card_count(result['old'])} → {card_count(result['new'])}",
                str(len(result["media"])),
                result["classification"],
            ]
        )
        surface_rows.append(
            [
                spec.target,
                "deck UUID/name/config exact; description refreshed",
                model_identity,
                "field order/config exact",
                "current UG direction/card surface; known hint debt where applicable",
                f"GUID exact; {len(notes['field_diffs'])} classified text refresh(es); tag membership exact",
                f"description SHA-256 {result['description_hashes'][0]} → {result['description_hashes'][1]}",
                "exact names + SHA-256",
            ]
        )

    for result in standalone_results:
        spec = result["spec"]
        ug_notes = result["ug_notes"]
        hg_notes = result["hg_notes"]
        rows.append(
            [
                spec.target,
                spec.category,
                f"{ug_notes['old_count']}+{hg_notes['old_count']} → {len(meaningful_notes(result['new']))}",
                f"{len(result['old_ug']['notes'])}+{len(result['old_hg']['notes'])} → {len(result['new']['notes'])}; 0+1 exact → 0 blanks",
                f"{ug_notes['preserved'] + hg_notes['preserved']}/{ug_notes['old_count'] + hg_notes['old_count']}",
                f"{card_count(result['old_ug']) + card_count(result['old_hg'], meaningful_notes(result['old_hg']))} → {card_count(result['new'])}",
                str(len(result["media"])),
                result["classification"],
            ]
        )
        surface_rows.append(
            [
                spec.target,
                "immutable UG deck UUID/name/description/config exact",
                "immutable UG localized model identity",
                "UG field order/config; RTL represented in CSS",
                "current UG direction/card surface; known hint debt where applicable",
                f"319 UG exact + 45 HG GUIDs; {len(hg_notes['field_diffs'])} classified HG refresh(es); tag membership exact",
                "immutable UG description exact",
                "byte-exact collision-free union",
            ]
        )

    pr733 = next(result for result in ug_results if result["spec"].target == "en-experimental")
    pr733_rows = [[name, digest] for name, digest in sorted(pr733["media"].items()) if name in PR733_MEDIA]
    require(len(pr733_rows) == len(PR733_MEDIA), "PR #733 media evidence is incomplete")

    hardcore_details: list[str] = []
    for result in companion_results:
        hardcore_details.append(f"### `{result['spec'].target}`")
        hardcore_details.append("")
        hardcore_details.extend(field_diff_samples(result))
        hardcore_details.append("")
        hardcore_details.append(
            f"Tag membership is exact; {result['notes']['tag_order_changes']} note(s) only changed tag serialization order. "
            f"`UG::Overlapping` remains on {result['overlapping']} of the 45 notes."
        )
        hardcore_details.append("")

    hint_rows: list[list[str]] = []
    for result in ug_results + companion_results + standalone_results:
        for before, after in result["model"]["capital_hint_deltas"]:
            hint_rows.append(
                [result["spec"].target, inline_code(before.strip()), inline_code(after.strip())]
            )

    alignment_rows = [
        [
            item["language"],
            item["main_target"],
            item["companion_target"],
            item["media_mode"],
            "0 blanks in both; 45 exact note objects; exact model; distinct deck UUID",
        ]
        for item in current_alignment
    ]
    old_dependencies = ", ".join(f"`{name}=={version}`" for name, version in OLD_PYTHON_DEPENDENCIES)
    new_command = shlex.join(command)
    report = f"""# PR 736 migration equivalence evidence

This file is generated by `scripts/collect-pr736-equivalence-evidence.py`. The collector rebuilds independent historical sources, exports this checkout through native alpha.3 includes, compares every declared surface below, and exits nonzero on an unclassified difference.

## Immutable inputs

- Ultimate Geography baseline: [`anki-geo/ultimate-geography@{UG_REVISION}`]({UG_ARCHIVE_URL}), archive SHA-256 `{UG_ARCHIVE_SHA256}`.
- Hardcore Geography baseline: [`anki-geo/hardcore-geography@{HG_REVISION}`]({HG_ARCHIVE_URL}), archive SHA-256 `{HG_ARCHIVE_SHA256}`.
- Historical Python environment (all exact): {old_dependencies}, installed in a disposable Nix-provided virtual environment.
- Migration builder: `{new_command}` (`1.0.0-alpha.3`, immutable source revision `{PINNED_BRAINBREW_REVISION}`).

The historical builds are independent of the committed parsed-JSON goldens. The collector downloads and hash-checks both revision archives, uses the repositories' original recipes, and exports the current manifests directly; it does not expand `!include` markers, read another Brain Brew checkout, or consume developer-local build output.

## Reproduce from a clean checkout

Prerequisites are Nix with flakes, Python 3, network access to GitHub archives, PyPI, and the pinned Brain Brew flake, and enough temporary disk space for historical builds. Exact package/archive pins prevent version drift, but Nix, PyPI, GitHub, and network availability remain external reproduction risks.

```bash
python scripts/check-translation-profile.py
for manifest in brainbrew.yaml brainbrew-hardcore.yaml; do
  nix run github:jeprecated/brain-brew/{PINNED_BRAINBREW_REVISION} -- \\
    verify --manifest "$manifest" --all-targets --media-root media
done
python scripts/collect-pr736-equivalence-evidence.py \\
  --report docs/pr736-equivalence-evidence.md
```

`--old-ug-archive` and `--old-hg-archive` accept offline archive files only when their SHA-256 values match the constants above. `--workdir` and `--keep-workdir` are optional diagnostics; neither path is written into this report.

## Native source validation transition

The one-time side-checker comparison used the pre-removal `scripts/check-source-content.py` and the then-pinned alpha.2. On the valid tree, the side checker reported `checked 22 external HTML/CSS source files`; native strict verification passed 74 main and 26 companion targets with zero warnings. Disposable malformed-source probes then showed:

- Appending an unclosed `<section>` to the included `templates/ultimate-geography/capital-country/question.html`: the forgiving Python `HTMLParser` side checker returned success, while native verification rejected it with `note_types.note-type.ultimate-geography.card_templates.template.capital-country.question_format:10: unclosed HTML tag <section>`.
- Appending `.task0050-probe {{` to the included `styles/ultimate-geography/card.css`: both checks rejected it; native verification reported `note_types.note-type.ultimate-geography.styling:95: unmatched '{{'`.

Thus native validation is strictly stronger for the observed HTML case and agrees on CSS balance. Both probes were restored byte-for-byte. The redundant content checker and its CI/docs invocation were deleted; the separate translation-profile drift guard remains because alpha.3 still cannot include a mapping-valued profile.

Reproduce the native negative probes without leaving a source change (each subshell restores its file on exit):

```bash
(
  file=templates/ultimate-geography/capital-country/question.html
  backup=$(mktemp)
  cp "$file" "$backup"
  trap 'cp "$backup" "$file"; rm -f "$backup"' EXIT
  printf '\\n<section data-evidence-probe="unclosed">\\n' >> "$file"
  ! nix run github:jeprecated/brain-brew/{PINNED_BRAINBREW_REVISION} -- \\
    verify --manifest brainbrew.yaml --target en-standard --media-root media
)
(
  file=styles/ultimate-geography/card.css
  backup=$(mktemp)
  cp "$file" "$backup"
  trap 'cp "$backup" "$file"; rm -f "$backup"' EXIT
  printf '\\n.evidence-probe {{\\n' >> "$file"
  ! nix run github:jeprecated/brain-brew/{PINNED_BRAINBREW_REVISION} -- \\
    verify --manifest brainbrew.yaml --target en-standard --media-root media
)
```

## Historical result matrix

{markdown_table(['Target', 'Equivalence class', 'Meaningful notes', 'Raw notes / blank policy', 'GUIDs', 'Cards', 'Media', 'Classification'], rows)}

### Compared surfaces

{markdown_table(['Target', 'Deck metadata / identity', 'Note-model identity', 'Field schema/order/config', 'Card HTML / CSS', 'Notes / fields / tags', 'Description', 'Media filenames / bytes'], surface_rows)}

Raw-note policy is enforced before semantic filtering: every ordinary UG and every current alpha.3 output must have `raw notes == meaningful notes` and zero blanks. The only permitted blank in any compared input is exactly one immutable old-Hardcore artifact per representative language build, with its language-specific GUID allowlisted below. Deck metadata includes name, deck UUID, configuration UUID, full description, and the other CrowdAnki deck flags. Model checks include model UUID/name, all field properties and order, all card names/order/front/back HTML and configuration, CSS, and remaining model configuration. Notes are keyed by GUID; field arrays (including order and values), model assignment, flags/data, and tag membership are compared. Media checks compare the declared filename set and SHA-256 of every exported file, not only counts.

## Current all-language Hardcore composition invariant

This is a current-composition invariant, separate from the representative historical classes above. The collector reuses the strict German historical exports, exports the remaining 11 localized main/companion standard pairs in `reference-only` mode, and checks all 12 supported localized pairs. The strict English historical pair is checked by the same assertion but is not part of the 12-language localization matrix.

{markdown_table(['Language', 'Standalone target', 'Companion target', 'Export media mode', 'Required invariant'], alignment_rows)}

For every row both raw outputs contain zero blank notes, the companion has exactly 45 unique meaningful GUIDs, each shared CrowdAnki note object is exactly equal in standalone and companion output, the complete `note_models` arrays are equal, and the standalone/companion deck UUIDs are distinct. A collector run fails if any language violates any part of this invariant.

## Classified presentation and content deltas

### Direction representation

The immutable Python outputs wrap every card front/back in `<div dir=\"ltr|rtl\">`. Alpha.2 places the same direction on the card CSS and removes those outer wrappers. Hebrew additionally moves six field-level `rtl: true` flags to `direction: rtl` on the rendered card CSS. Raw schema/template/CSS differences are therefore recorded rather than hidden; note values, GUIDs, model identity, descriptions, deck configuration, and media remain independently compared.

### PR #733 Experimental map

The immutable upstream baseline contains PR #733 and the subsequent PR #735. The four JavaScript payloads exercised by the representative Experimental target are byte-identical:

{markdown_table(['Media file', 'Old/new SHA-256'], pr733_rows)}

Alpha.2's external template adds an explicit `_ug-jsvectormap.min.css` link on the Experimental Country–Map front/back; the underlying PR #733 JavaScript and all 551 Experimental media files retain exact names and bytes. The Hebrew historical row independently proves that PR #735's 319 note payloads/GUIDs and full deck description are retained; only the separately classified direction representation changes.

### Capital-hint localization debt (deferred)

The migration still has the previously identified duplicated capital-hint label: translated baseline labels fall back to English `Hint:` in the canonical shared template. This task does **not** silently fix that content behavior; it records it for separate localization work:

{markdown_table(['Representative target', 'Immutable baseline HTML', 'Current alpha.3 HTML'], hint_rows)}

### Localized standalone Hardcore composition

The historical comparison initially exposed a real stack-ordering gap: a main-deck language overlay ran before Hardcore notes were added, so many localized standalone Hardcore fields fell back to English. The main manifest now reuses each existing companion-content translation overlay for all 12 Hardcore languages after `overlay.extension.hardcore` and before the smaller Hardcore refresh overlay. The German representative consequently has the same 45 translated Hardcore note payloads in standalone and companion form; only the 10 concrete revision-bound refreshes below remain. This is a composition correction, not an editorial rewrite.

### Hardcore refresh, overlap, and import identity

The old Hardcore generator emits exactly one language-build-specific all-empty note (English `{BLANK_HG_GUIDS['en']}`, German `{BLANK_HG_GUIDS['de']}`). This is the sole permitted historical blank artifact: every old UG input and every new output is explicitly required to have zero blanks. The migration classifies that invalid artifact as the `blank-note-removal` typed delta: all 45 meaningful GUIDs remain and no blank note is exported. Companion deck UUID/name/configuration identity remains exact. English keeps the old/current UG note-model UUID; German intentionally aligns all 45 notes to the immutable German UG model UUID/name so companion import composes with the localized main deck. Standalone exports retain the normal UG deck identity and are proven as the collision-free union of 319 UG GUIDs plus 45 Hardcore GUIDs.

The revision-bound Hardcore repository is stale relative to the immutable UG baseline. The comparator exact-allowlists the full old/new description SHA-256 pair and every field tuple `(GUID, field index, old value, new value)`; a count-preserving substitution still fails. These are the concrete field refreshes, and standalone exports must match the same tuple allowlist:

{''.join(line + chr(10) for line in hardcore_details).rstrip()}

The strict English/German historical companion and standalone pairs have identical payloads for the same 45 meaningful Hardcore GUIDs while retaining distinct deck identities and exact note-model surfaces. They preserve exact tag membership (including `UG::Overlapping`), and all 56 Hardcore media filenames/bytes. Standalone media is the exact 602-file union of 546 UG and 56 Hardcore assets. The separate current-composition invariant above enforces the corresponding payload/model/identity relationship for every localized language.

## Committed parsed-JSON goldens

Historical evidence answers “did the migration preserve/classify the old output?” Goldens independently answer “did a later change alter the accepted migration output?” Normal `verify --all-targets` checks these eight full parsed CrowdAnki JSON files with no allowlist:

{markdown_table(['Target', 'Class', 'Manifest'], [[target, category, manifest] for target, category, manifest in GOLDEN_TARGETS])}

Update an intentionally changed golden with the immutable tool, then delete copied media so only parsed JSON remains committed:

```bash
target=en-standard
manifest=brainbrew.yaml
rm -rf "goldens/$target"
nix run github:jeprecated/brain-brew/{PINNED_BRAINBREW_REVISION} -- \\
  export crowdanki --manifest "$manifest" --target "$target" \\
  --out "goldens/$target" --media-root media
rm -rf "goldens/$target/media"
nix run github:jeprecated/brain-brew/{PINNED_BRAINBREW_REVISION} -- \\
  verify --manifest "$manifest" --target "$target" --media-root media
```

A disposable edit of `goldens/en-standard/deck.json` changed `$.name`; verification failed with `CrowdAnki golden mismatch`, `1 CrowdAnki JSON difference(s)`, and the expected/actual values. The file was restored byte-for-byte.

## Assessment

Strict native verification covers all 74 main plus 26 companion targets; CI also transactionally exports all 100. The representative historical classes cover source, translation, RTL, CJK, Extended, Experimental, standalone Hardcore, and companion Hardcore, while the separate current-composition invariant covers every localized Hardcore pair. No unknown raw-note/blank artifact, GUID, note-field, tag-membership, deck identity, configuration, description, schema, template/CSS, or media-byte delta is accepted by this collector. The only non-exact historical surfaces are explicitly classified above: direction representation, the explicit Experimental stylesheet link with PR #733 bytes preserved, the corrected localized-standalone stack, exact-allowlisted stale old-Hardcore refreshes and blank artifact removal, and the deferred capital-hint label fallback.
"""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")


def require_hardcore_pair_alignment(language: str, main: dict, companion: dict) -> None:
    require_blank_note_policy(main, (), f"{language}: current standalone")
    require_blank_note_policy(companion, (), f"{language}: current companion")
    require(len(companion.get("notes", [])) == 45, f"{language}: companion does not contain exactly 45 notes")
    companion_notes = notes_by_guid(companion)
    standalone_notes = notes_by_guid(main)
    require(len(companion_notes) == 45, f"{language}: companion does not contain 45 unique meaningful GUIDs")
    require(set(companion_notes) <= set(standalone_notes), f"{language}: companion GUIDs are not a standalone subset")
    for guid in sorted(companion_notes):
        require(
            companion_notes[guid] == standalone_notes[guid],
            f"{language}: companion/standalone note object differs for GUID {guid}",
        )
    require(
        companion.get("note_models") == main.get("note_models"),
        f"{language}: companion/standalone note model surfaces differ",
    )
    require(
        companion.get("crowdanki_uuid") != main.get("crowdanki_uuid"),
        f"{language}: companion and standalone deck identities unexpectedly match",
    )


def verify_hardcore_pair_alignment(results: Sequence[dict[str, object]]) -> None:
    by_target = {result["spec"].target: result for result in results}
    for language in ("en", "de"):
        companion = by_target[f"{language}-hardcore-companion-standard"]["new"]
        standalone = by_target[f"{language}-hardcore-standard"]["new"]
        require_hardcore_pair_alignment(language, standalone, companion)


def verify_current_hardcore_alignment(
    outputs: dict[str, tuple[Path, Path, str]],
) -> list[dict[str, str]]:
    evidence: list[dict[str, str]] = []
    require(tuple(outputs) == HARDCORE_TRANSLATION_LANGUAGES, "current Hardcore alignment language matrix changed")
    for language, (main_output, companion_output, media_mode) in outputs.items():
        main = load_deck(main_output / "deck.json")
        companion = load_deck(companion_output / "deck.json")
        require_hardcore_pair_alignment(language, main, companion)
        evidence.append(
            {
                "language": language,
                "main_target": f"{language}-hardcore-standard",
                "companion_target": f"{language}-hardcore-companion-standard",
                "media_mode": media_mode,
            }
        )
    return evidence


def verify_main_hardcore_translation_wiring() -> None:
    manifest = (ROOT / "brainbrew.yaml").read_text(encoding="utf-8")
    for language in HARDCORE_TRANSLATION_LANGUAGES:
        overlay = f"overlay.translation.hardcore.companion.{language}"
        source = f"overlays/extensions/hardcore/companion-translations/{language}.yaml"
        require(overlay in manifest and source in manifest, f"missing localized standalone Hardcore wiring for {language}")


def collect(old_ug_root: Path, old_hg_root: Path, new_root: Path) -> list[dict[str, object]]:
    verify_main_hardcore_translation_wiring()
    results: list[dict[str, object]] = []
    for spec in TARGETS:
        new_output = new_root / spec.target
        if spec.old_ug_folder and not spec.old_hg_folder:
            results.append(compare_ug_target(spec, old_ug_root / "build" / spec.old_ug_folder, new_output))
        elif spec.old_hg_folder and not spec.old_ug_folder:
            ug_folder = "Ultimate Geography [EN]" if spec.language == "en" else "Ultimate Geography [DE]"
            results.append(
                compare_companion_target(
                    spec,
                    old_hg_root / "build" / spec.old_hg_folder,
                    new_output,
                    old_ug_root / "build" / ug_folder,
                )
            )
        else:
            require(spec.old_ug_folder is not None and spec.old_hg_folder is not None, "invalid target specification")
            results.append(
                compare_standalone_target(
                    spec,
                    old_ug_root / "build" / spec.old_ug_folder,
                    old_hg_root / "build" / spec.old_hg_folder,
                    new_output,
                )
            )
    verify_hardcore_pair_alignment(results)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, help="optional reusable temporary workspace")
    parser.add_argument("--keep-workdir", action="store_true", help="keep an automatically allocated workspace")
    parser.add_argument("--old-ug-archive", type=Path, help="offline UG archive override (pinned hash required)")
    parser.add_argument("--old-hg-archive", type=Path, help="offline HG archive override (pinned hash required)")
    parser.add_argument("--old-brainbrew", type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        "--new-brainbrew-command",
        default=PINNED_BRAINBREW_COMMAND,
        help="command prefix for alpha.3 (default: immutable pinned Nix revision)",
    )
    parser.add_argument("--report", type=Path, default=ROOT / "docs" / "pr736-equivalence-evidence.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command = shlex.split(args.new_brainbrew_command)
    require(command, "new Brain Brew command cannot be empty")
    temporary: tempfile.TemporaryDirectory[str] | None = None
    if args.workdir is None:
        temporary = tempfile.TemporaryDirectory(prefix="ug-pr736-equivalence-")
        workdir = Path(temporary.name)
    else:
        workdir = args.workdir.resolve()
        workdir.mkdir(parents=True, exist_ok=True)

    try:
        archives = workdir / "archives"
        ug_archive = fetch_archive(UG_ARCHIVE_URL, UG_ARCHIVE_SHA256, archives / "ultimate-geography.tar.gz", args.old_ug_archive)
        hg_archive = fetch_archive(HG_ARCHIVE_URL, HG_ARCHIVE_SHA256, archives / "hardcore-geography.tar.gz", args.old_hg_archive)
        old_ug_root = workdir / "old-ug"
        old_hg_root = workdir / "old-hg"
        extract_revision_archive(ug_archive, old_ug_root, UG_REVISION)
        extract_revision_archive(hg_archive, old_hg_root, HG_REVISION)
        old_brainbrew = ensure_old_brainbrew_venv(workdir / f"brain-brew-{OLD_BRAIN_BREW_VERSION}-venv", args.old_brainbrew)
        build_old_ug(old_ug_root, old_brainbrew)
        build_old_hg(old_hg_root, old_brainbrew)
        new_output = workdir / "new-output"
        export_new_targets(new_output, command)
        current_alignment_outputs = export_current_hardcore_alignment_targets(new_output, command)
        results = collect(old_ug_root, old_hg_root, new_output)
        current_alignment = verify_current_hardcore_alignment(current_alignment_outputs)
        write_report(args.report, results, command, current_alignment)
        print(f"wrote {args.report}")
        if args.keep_workdir or args.workdir is not None:
            print(f"kept workdir at {workdir}")
        return 0
    except EvidenceError as error:
        print(f"evidence collection failed: {error}", file=sys.stderr)
        return 1
    finally:
        if temporary is not None and args.keep_workdir:
            temporary._finalizer.detach()  # type: ignore[attr-defined]
        elif temporary is not None:
            temporary.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())

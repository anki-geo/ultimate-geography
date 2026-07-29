#!/usr/bin/env python3
"""Keep both manifest translation profiles coherent and migration-safe."""

from pathlib import Path
import re
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
TRANSLATION_OVERLAY_ROOT = ROOT / "overlays"
PATTERN_CONTEXT_HEADER = (
    "    note_types.note-type.ultimate-geography.fields.field.flag-similarity.message_pattern:"
)
POSITIONAL_COUNTRY_KEY = re.compile(
    r"(?P<path>[A-Za-z0-9_.-]+\.fields\.field\.flag-similarity\.message\.items\.\d+\.country)"
    r"\s*['\"]?\s*:"
)
REVIEWED_POSITIONAL_COUNTRY_EXCEPTION = (
    Path("overlays/languages/cs.yaml"),
    "poland.fields.field.flag-similarity.message.items.1.country",
    "        Monaco: Monako",
)

# Canonical-source snapshots make translation changes explicit even when a target
# has no configured golden. Counts are de=1, pt=9, zh-tw=43, zh=43, Hardcore zh=1.
PARAMETER_COUNTRY_SNAPSHOTS = {
    Path("overlays/languages/de.yaml"): """Moldova: Republik Moldau/Moldawien""".splitlines(),
    Path("overlays/languages/pt.yaml"): """Egypt: Egito
Latvia: 'Letônia'
Luxembourg: do Luxemburgo
Monaco: 'Mônaco'
Poland: 'Polônia'
Romania: 'Romênia'
Sahrawi Arab Democratic Republic: 'República Árabe Saaraui Democrática'
Slovenia: 'Eslovênia'
Yemen: 'Iêmen'""".splitlines(),
    Path("overlays/languages/zh-tw.yaml"): """Andorra: '安道爾'
Australia: '澳洲'
Austria: '奧地利'
Bahrain: '巴林'
Bolivia: '玻利維亞'
Cameroon: '喀麥隆'
Chad: '查德'
Colombia: '哥倫比亞'
Cuba: '古巴'
'Curaçao': '庫拉索'
Ecuador: '厄瓜多'
Egypt: '埃及'
El Salvador: '薩爾瓦多'
Faroe Islands: '法羅群島'
Ghana: '迦納'
Guinea: '幾內亞'
Iceland: '冰島'
Indonesia: '印尼'
Iraq: '伊拉克'
Ireland: '愛爾蘭'
Ivory Coast: '象牙海岸'
Latvia: '拉脫維亞'
Luxembourg: '盧森堡'
Mali: '馬利'
Moldova: '摩爾多瓦'
Monaco: '摩納哥'
Nauru: '諾魯'
Netherlands: '荷蘭'
New Zealand: '紐西蘭'
Nicaragua: '尼加拉瓜'
Norway: '挪威'
Palestine: '巴勒斯坦'
Poland: '波蘭'
Puerto Rico: '波多黎各'
Qatar: '卡達'
Romania: '羅馬尼亞'
Russia: '俄羅斯'
Sahrawi Arab Democratic Republic: '西撒哈拉'
Senegal: '塞內加爾'
Slovakia: '斯洛伐克'
Slovenia: '斯洛維尼亞'
Sudan: '蘇丹'
Yemen: '葉門'""".splitlines(),
    Path("overlays/languages/zh.yaml"): """Andorra: '安道尔'
Australia: '澳大利亚'
Austria: '奥地利'
Bahrain: '巴林'
Bolivia: '玻利维亚'
Cameroon: '喀麦隆'
Chad: '乍得'
Colombia: '哥伦比亚'
Cuba: '古巴'
'Curaçao': '库拉索'
Ecuador: '厄瓜多尔'
Egypt: '埃及'
El Salvador: '萨尔瓦多'
Faroe Islands: '法罗群岛'
Ghana: '加纳'
Guinea: '几内亚'
Iceland: '冰岛'
Indonesia: '印度尼西亚'
Iraq: '伊拉克'
Ireland: '爱尔兰'
Ivory Coast: '科特迪瓦'
Latvia: '拉脱维亚'
Luxembourg: '卢森堡'
Mali: '马里'
Moldova: '摩尔多瓦'
Monaco: '摩纳哥'
Nauru: '瑙鲁'
Netherlands: '荷兰'
New Zealand: '新西兰'
Nicaragua: '尼加拉瓜'
Norway: '挪威'
Palestine: '巴勒斯坦'
Poland: '波兰'
Puerto Rico: '波多黎各'
Qatar: '卡塔尔'
Romania: '罗马尼亚'
Russia: '俄罗斯'
Sahrawi Arab Democratic Republic: '阿拉伯撒哈拉民主共和国'
Senegal: '塞内加尔'
Slovakia: '斯洛伐克'
Slovenia: '斯洛文尼亚'
Sudan: '苏丹'
Yemen: '也门'""".splitlines(),
    Path("overlays/extensions/hardcore/translations/zh.yaml"): """Sierra Leone: '塞拉利昂'""".splitlines(),
}
EXPECTED_PARAMETER_COUNTRY_COUNTS = {
    Path("overlays/languages/de.yaml"): 1,
    Path("overlays/languages/pt.yaml"): 9,
    Path("overlays/languages/zh-tw.yaml"): 43,
    Path("overlays/languages/zh.yaml"): 43,
    Path("overlays/extensions/hardcore/translations/zh.yaml"): 1,
}
EXPECTED_PARAMETER_COUNTRY_TOTAL = 97


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


def translation_overlay_sources() -> dict[Path, str]:
    return {
        path.relative_to(ROOT): path.read_text(encoding="utf-8")
        for path in sorted(TRANSLATION_OVERLAY_ROOT.rglob("*.yaml"))
    }


def extract_parameter_country_snapshot(source: str) -> list[str] | None:
    lines = source.splitlines()
    snapshots: list[list[str]] = []
    for context_index, line in enumerate(lines):
        if line != PATTERN_CONTEXT_HEADER:
            continue
        block_end = context_index + 1
        while block_end < len(lines) and (
            not lines[block_end].strip() or len(lines[block_end]) - len(lines[block_end].lstrip()) > 4
        ):
            block_end += 1
        block = lines[context_index + 1 : block_end]
        for index, child in enumerate(block):
            if child != "      parameters:":
                continue
            if index + 1 >= len(block) or block[index + 1] != "        country:":
                raise ValueError("message pattern parameters must contain canonical country block")
            snapshot: list[str] = []
            for mapping in block[index + 2 :]:
                if not mapping.startswith("          "):
                    break
                if mapping.startswith("            ") or not mapping.strip():
                    raise ValueError("country parameter translations must be a flat canonical mapping")
                snapshot.append(mapping[10:])
            snapshots.append(snapshot)
    if len(snapshots) > 1:
        raise ValueError("multiple country parameter translation blocks found in one overlay")
    return snapshots[0] if snapshots else None


def validate_parameter_country_snapshots(sources: dict[Path, str]) -> None:
    if set(PARAMETER_COUNTRY_SNAPSHOTS) != set(EXPECTED_PARAMETER_COUNTRY_COUNTS):
        raise ValueError("parameter-country snapshot/count file inventories differ")
    if sum(EXPECTED_PARAMETER_COUNTRY_COUNTS.values()) != EXPECTED_PARAMETER_COUNTRY_TOTAL:
        raise ValueError("parameter-country expected counts do not total 97")

    found: dict[Path, list[str]] = {}
    for path, source in sources.items():
        snapshot = extract_parameter_country_snapshot(source)
        if snapshot is not None:
            found[path] = snapshot
    if set(found) != set(PARAMETER_COUNTRY_SNAPSHOTS):
        raise ValueError(
            "parameter-country overlay inventory changed: "
            f"expected {sorted(PARAMETER_COUNTRY_SNAPSHOTS)}, got {sorted(found)}"
        )

    for path, expected in PARAMETER_COUNTRY_SNAPSHOTS.items():
        expected_count = EXPECTED_PARAMETER_COUNTRY_COUNTS[path]
        if len(expected) != expected_count:
            raise ValueError(f"snapshot constant for {path} does not contain {expected_count} mappings")
        if found[path] != expected:
            raise ValueError(f"parameter-country translation snapshot changed in {path}")
    if sum(len(snapshot) for snapshot in found.values()) != EXPECTED_PARAMETER_COUNTRY_TOTAL:
        raise ValueError("parameter-country translation inventory does not contain exactly 97 mappings")


def validate_positional_country_contexts(sources: dict[Path, str]) -> None:
    found_exception = 0
    unexpected: list[str] = []
    exception_path, exception_key, exception_mapping = REVIEWED_POSITIONAL_COUNTRY_EXCEPTION
    for path, source in sources.items():
        lines = source.splitlines()
        for index, line in enumerate(lines):
            match = POSITIONAL_COUNTRY_KEY.search(line)
            if match is None:
                continue
            next_line = lines[index + 1] if index + 1 < len(lines) else ""
            if path == exception_path and match.group("path") == exception_key and next_line == exception_mapping:
                found_exception += 1
            else:
                unexpected.append(f"{path}:{index + 1}:{match.group('path')}")
    if unexpected:
        raise ValueError(
            "positional flag-similarity country context should use the field pattern parameter context: "
            + ", ".join(sorted(unexpected))
        )
    if found_exception != 1:
        raise ValueError("expected exactly one reviewed Czech Monaco positional country exception")


def validate_country_translation_contexts(sources: dict[Path, str]) -> None:
    validate_parameter_country_snapshots(sources)
    validate_positional_country_contexts(sources)


def expect_context_guard_failure(sources: dict[Path, str], path: Path, old: str, new: str) -> None:
    mutated = dict(sources)
    if mutated[path].count(old) != 1:
        raise ValueError(f"mutation self-check fixture is not unique in {path}: {old!r}")
    mutated[path] = mutated[path].replace(old, new, 1)
    try:
        validate_country_translation_contexts(mutated)
    except ValueError:
        return
    raise ValueError(f"country translation context mutation escaped validation in {path}")


def validate_context_guard_mutations(sources: dict[Path, str]) -> None:
    mutations = (
        (Path("overlays/languages/pt.yaml"), "          Egypt: Egito", "          Egypt: Errado"),
        (Path("overlays/languages/zh-tw.yaml"), "          Yemen: '葉門'", "          Yemen: '也門'"),
        (
            Path("overlays/extensions/hardcore/translations/zh.yaml"),
            "          Sierra Leone: '塞拉利昂'",
            "          Sierra Leone: 'Sierra Leone'",
        ),
        (
            Path("overlays/languages/de.yaml"),
            "    notes.note:",
            "    notes.note:\n"
            '      "andorra.fields.field.flag-similarity.message.items.0.country": '
            "{Moldova: Republik Moldau/Moldawien}",
        ),
    )
    for path, old, new in mutations:
        expect_context_guard_failure(sources, path, old, new)

    # Description arguments intentionally remain positional and must not trip the country-only guard.
    description_sources = dict(sources)
    path = Path("overlays/languages/de.yaml")
    description_sources[path] = description_sources[path].replace(
        "    notes.note:",
        "    notes.note:\n      'andorra.fields.field.flag-similarity.message.items.0.description':\n"
        "        wider, coat of arms with eagle: breiter, Wappen mit Adler",
        1,
    )
    validate_country_translation_contexts(description_sources)


def main() -> int:
    try:
        profiles = []
        for path in MANIFESTS:
            source = path.read_text(encoding="utf-8")
            validate_list_message_pattern_category(path, source)
            profiles.append(profile(path))
        main_profile, companion_profile = profiles
        sources = translation_overlay_sources()
        validate_country_translation_contexts(sources)
        validate_context_guard_mutations(sources)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    if main_profile != companion_profile:
        print("translation_profile differs between brainbrew.yaml and brainbrew-hardcore.yaml", file=sys.stderr)
        return 1
    print(
        "translation profiles are identical; exact 97 parameter-country mappings and the reviewed "
        "Czech positional exception are intact"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

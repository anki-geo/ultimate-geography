import argparse
import csv
import subprocess
from pathlib import Path


def validate_subtokens(tokens):
    toks = sorted(tokens, key=len)
    for i, a in enumerate(toks):
        for b in toks[i + 1:]:
            if a in b:
                raise ValueError(f"Translation key '{a}' is a subset of key '{b}'")


def load_translations(csv_path):
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemError("translations.csv has no headers")

        validate_subtokens(reader.fieldnames)

        rows = []
        for row in reader:
            for key in reader.fieldnames:
                if not row[key]:
                    language = row["__LANGUAGE_CODE__"]
                    raise ValueError(f"Missing value for '{key}' in {language}")
            rows.append(row)

    if not rows:
        raise SystemError("translations.csv has no translation rows")

    return reader.fieldnames, rows


def apply_replacements(text, replacements):
    for token, value in replacements:
        text = text.replace(token, value)
    return text


def generate_templates():
    csv_root = Path(__file__).resolve().parent.parent / "src" / "note_models"
    base_dir = csv_root / "templates" / "base"
    output_dir = csv_root / "templates" / "generated"
    translations_path = csv_root / "translations.csv"

    if not base_dir.is_dir():
        raise SystemError(f"Missing base templates directory at {base_dir}")
    if not translations_path.is_file():
        raise SystemError(f"Missing translations file at {translations_path}")

    fieldnames, rows = load_translations(translations_path)
    base_files = [path for path in base_dir.iterdir()]
    output_dir.mkdir(parents=True, exist_ok=True)
    english_base_case = [
        ('name: Ultimate Geography [EN]', 'name: Ultimate Geography')
    ]

    for row in rows:
        language = row["__LANGUAGE_CODE__"]
        output_dir_folder = output_dir / language
        output_dir_folder.mkdir(parents=True, exist_ok=True)
        replacements = [(name, row[name]) for name in fieldnames]

        for base_path in base_files:
            content = base_path.read_text(encoding="utf-8")
            rendered = apply_replacements(content, replacements)
            rendered = apply_replacements(rendered, english_base_case)

            output_name = apply_replacements(base_path.name, replacements)
            output_path = output_dir_folder / output_name
            output_path.write_text(rendered, encoding="utf-8")

    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate templates and optionally run a brain_brew recipe."
    )
    parser.add_argument(
        "recipe_path",
        nargs="?",
        help="If provided, run 'brain_brew run <recipe_path>' after generating templates.",
    )
    return parser.parse_args()


def run_brain_brew(recipe_path):
    result = subprocess.run(["brain_brew", "run", recipe_path])
    return result.returncode


def main():
    args = parse_args()
    generate_templates()
    print("Successfully generated template files.")
    if args.recipe_path:
        build_result = run_brain_brew(args.recipe_path)
        if build_result == 0:
            print("Successfully built deck.")
        return build_result

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

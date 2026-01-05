import csv
from pathlib import Path


def load_translations(csv_path):
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemError("translations.csv has no headers")

        rows = []
        for row in reader:
            for key in reader.fieldnames:
                if not row[key]:
                    language = row["_language-tag"]
                    raise ValueError(f"Missing value for {key} in {language}")
            rows.append(row)

    if not rows:
        raise SystemError("translations.csv has no translation rows")

    return reader.fieldnames, rows


def apply_replacements(text, replacements):
    for token, value in replacements:
        text = text.replace(token, value)
    return text


def main():
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
        ('name: Ultimate Geography [EN]', 'name: Ultimate Geography'),
        ('name: Ultimate Geography [EN] [Extended]', 'name: Ultimate Geography [Extended]')
    ]

    for row in rows:
        language = row["_language-tag"]
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


if __name__ == "__main__":
    raise SystemExit(main())

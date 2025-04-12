import re

from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path

# Adapted from https://github.com/python/cpython/blob/3.13/Lib/zipfile/__init__.py#L2328
def addToZip(zf, path, zippath):
    if path.is_file():
        zf.write(path, zippath, ZIP_DEFLATED)
    elif path.is_dir():
        if zippath:
            zf.write(path, zippath)
        for nm in sorted(path.iterdir()):
            addToZip(zf,
                     nm, zippath / nm.name)

DECK_DIR_REGEXP = re.compile(r"^Ultimate Geography \[([A-Z-]*)\] ?(|\[Extended\]|\[Experimental\])$")
def get_zip_filename(deck_dir, version):
    m = DECK_DIR_REGEXP.match(deck_dir)
    if m is not None:
        lang_code = m.group(1)
        deck_type = m.group(2)

        if deck_type == "[Extended]":
            deck_type = "_EXTENDED"
        elif deck_type == "[Experimental]":
            deck_type = "_EXPERIMENTAL"
        elif deck_type == "":
            deck_type = ""
        else:
            raise ValueError(f"Unknown deck type: {deck_type}")

        return f"Ultimate_Geography_{version}_{lang_code}{deck_type}.zip"

    else:
        raise ValueError(f"Unexpected deck directory name: {deck_dir}")

# Allow passing version string manually!
def zip_decks(aug_version=None):
    root = Path.cwd()

    build_dir = root / "build"

    desc_file = root / "src" / "headers" / "desc.html"
    if aug_version is None:
        with open(desc_file) as f:
            desc_text = f.read()
        m = re.search(r"Ultimate Geography (v[0-9]+\.[0-9]+)", desc_text)
        if m is None:
            raise ValueError("Description file does not contain version string!")
        aug_version = m.group(1)

    if build_dir.is_dir():
        for deck_dir in build_dir.iterdir():
            if deck_dir.is_dir():
                deck_dir_name = deck_dir.name
                zip_name = build_dir / get_zip_filename(deck_dir_name, aug_version)
                with ZipFile(zip_name, "w") as zf:
                    addToZip(zf, deck_dir, Path(deck_dir_name))


if __name__ == "__main__":
    zip_decks()

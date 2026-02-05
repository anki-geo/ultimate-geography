"""Check flags on Wikimedia for updates.

For each flag:

1. Fetch the latest flag from Wikimedia (based on `sources.csv`).
2. Adjust the width/height/viewBox as described in CONTRIBUTING.md
3. Run `svgo`.  (We assume that it's installed; if not we crash.)
4. Overwrite the current file in `src/media/flags/`.

Comparing the files is currently left to the user.  The idea is that
they can compare the current and the updated versions with `git diff`
using whatever tool they prefer.

Given the text nature of SVG and the fact that many of the files are
small, a naive text diff is itself quite useful, especially with word
diff (`git diff --word-diff`).  For an image diff, `git difftool -x
git-difftool-img` with:

```
compare -compose src "$1" "$2" png:- | montage -geometry 400x+2+2 "$1" "$2" png:- png:- | display -
```

(for marking up any changed pixels)

or

```
convert "$1" "$2" -fx "1 - sqrt(pow(u.r-v.r,2) + pow(u.g-v.g,2) + pow(u.b-v.b,2))" -normalize png:- | montage -geometry 400x+2+2 "$1" "$2" png:- png:- | display -
```

(for displaying the magnitude of the changes using a naive Euclidean
RGB distance)

as the `git-difftool-img` executable works well.

"""
import argparse
import csv
import tempfile
import re
import shutil
import subprocess
import webbrowser

from dataclasses import dataclass
from pathlib import Path

import requests

def fetch_flag_from_wikimedia(
    local_filename: str,
    wikimedia_filename: str,
    temp_dir: Path,
) -> Path:
    """Fetch flag from Wikimedia."""
    fetch_link = "https://commons.wikimedia.org/wiki/Special:FilePath/File:" + wikimedia_filename

    headers = {"user-agent": "aug-flag-update/0.0.0"}
    r = requests.get(
        fetch_link,
        headers=headers,
    )

    wikimedia_fetch = temp_dir / local_filename

    with open(wikimedia_fetch, "wb") as f:
        f.write(r.content)

    return wikimedia_fetch

@dataclass
class Attrib:
    """SVG attributes.

    Helps obtain, store and process the values of various attributes
    (height, width, viewBox) within the root `<svg>` tag.  Acts as a
    very partial XML parser.  (Unfortunately, the clean solution of
    just using an XML parser lead to minor, non-semantic (mainly (but
    not solely) whitespace) changes throughout the document.  On a
    casual overview, SVGO (slightly surprisingly) did not seem to
    entirely normalise the changes, hence leading to some spurious
    diffs.  The alternative solution of just extracting and properly
    XML-parsing the root `<svg>` tag did not work, as some XML
    namespace declarations (not used within the `<svg>` tag, but used
    elsewhere in the document) where removed.  Hence, this more ugly
    but more surgical approach of only directly modifying the target
    attributes of the `<svg>` was taken.

    """
    name: str
    value: str
    num: float | None = None

    @classmethod
    def extract(
        cls,
        attrib_name: str,
        text: str,
        start: int,
        end: int,
        obtain_num: bool = False,
    ):
        """Extract given attribute from sub-set of supplied text.

        start and end should delimit the range of the `<svg>` tag
        (i.e. the subset of the entire text from which we want to
        extract the attribute values).

        """
        regexp = re.compile(attrib_name + r'="([^"]*)"')
        m = regexp.search(text, start, end)
        if m is None:
            return None
        if obtain_num:
            return Attrib(attrib_name, m.group(1), float(m.group(1).removesuffix("px")))
        return Attrib(attrib_name, m.group(1))

    def replace(self, text: str, new_value: int):
        """Replace given attribute values.

        Assumes that the first occurrence of `attrib="value"` is the
        desired one.  (This should be generally correct, since it's
        highly unlikely there would be any such occurrences before the
        root SVG tag, though technically, they could occur in, say, a
        comment.)

        """
        regexp = re.compile(rf'{self.name}="({re.escape(self.value)})"')
        replacement = rf'{self.name}="{new_value}"'
        return re.sub(regexp, replacement, text, count=1)

def update_geometry(wikimedia_fetch: Path):
    """Update the SVG to have a height of 250.

    Change width proportionally.  Add viewBox if such did not exist.

    """
    with open(wikimedia_fetch) as f:
        svg_text = f.read()

    svg_start = svg_text.find("<svg")
    svg_end = svg_text.find(">", svg_start)

    width_a = Attrib.extract("width", svg_text, svg_start, svg_end, obtain_num=True)
    height_a = Attrib.extract("height", svg_text, svg_start, svg_end, obtain_num=True)
    view_box_a = Attrib.extract("viewBox", svg_text, svg_start, svg_end)

    if (width_a is None) and (height_a is None):
        view_box_str = re.split(" |,", view_box_a.value)
        if not len(view_box_str) == 4:
            raise ValueError(f"viewBox has incorrect length {len(view_box_str)}!")

        dimensions = [float(x) for x in view_box_str[2:4]]
        new_width = round(dimensions[0] * (250/dimensions[1]))
        new_height = 250

        svg_text = (svg_text[0:svg_end] +
                    f' width="{new_width}" height="{new_height}"' +
                    svg_text[svg_end:])
    elif (width_a is None) and (height_a is None):
        raise ValueError("Expected either both or none of width and height to be missing!")
    else:
        if view_box_a is None:
            view_box_str = f"0 0 {width_a.num} {height_a.num}"
            svg_text = svg_text[0:svg_end] + f' viewBox="{view_box_str}"' + svg_text[svg_end:]

        new_width = round(width_a.num * (250/height_a.num))
        new_height = 250

        svg_text = width_a.replace(svg_text, new_width)
        svg_text = height_a.replace(svg_text, new_height)

    with open(wikimedia_fetch, "w") as f:
        f.write(svg_text)

## This unfortunately leads to changes elsewhere (other than in the
## root svg element) in the file, so I've switched to the above more
## ugly regexp solution.
# def update_geometry_with_xml(wikimedia_fetch: Path) -> None:
#     t = ET.parse(wikimedia_fetch)
#     root = t.getroot()
#     root.attrib

#     if "height" in root.attrib:
#         initial_height_str = root.attrib["height"]
#     else:
#         raise ValueError("Missing height!")

#     if "width" in root.attrib:
#         initial_width_str = root.attrib["width"]
#     else:
#         raise ValueError("Missing width!")

#     if not "viewBox" in root.attrib:
#         root.attrib["viewBox"] = f"0 0 {initial_width_str} {initial_height_str}"

#     initial_height = float(initial_height_str.removesuffix("px"))
#     initial_width = float(initial_width_str.removesuffix("px"))

#     width = initial_width * (250/initial_height)

#     root.attrib["height"] = str(250)
#     root.attrib["width"] = str(width)

#     ET.register_namespace("", "http://www.w3.org/2000/svg")
#     t.write(
#         wikimedia_fetch,
#         xml_declaration=True,
#         encoding="utf-8",
#         default_namespace="",
#     )

def run_svgo(wikimedia_fetch) -> Path:
    """Run svgo.

    Currently, doesn't handle svgo errors, at all, but they should be
    visible in the terminal.

    """
    # svgo sometimes makes SVGs larger.  It happily reports that it's
    # making it larger, but still outputs the new, inflated version
    # (!).  Hence, we need to wrap around it.
    svgo_attempt = wikimedia_fetch.with_suffix(".svg.2")
    subprocess.run(["svgo", "-i", str(wikimedia_fetch), "-o", str(svgo_attempt)])

    if svgo_attempt.stat().st_size < wikimedia_fetch.stat().st_size:
        return svgo_attempt.move(wikimedia_fetch)

    return wikimedia_fetch

def move_svg_to_media_dir(wikimedia_fetch: Path) -> None:
    """Move the generated SVG to src/media/flags/"""
    target_dir = Path(".") / "src" / "media" / "flags"
    target_file = target_dir / wikimedia_fetch.name
    shutil.move(wikimedia_fetch, target_file)

def update_flag(
    local_filename: str,
    wikimedia_filename: str,
    temp_dir: Path,
) -> None:
    """Fetch and update given flag."""
    wikimedia_fetch = fetch_flag_from_wikimedia(
        local_filename,
        wikimedia_filename,
        temp_dir,
    )
    update_geometry(wikimedia_fetch)
    wikimedia_fetch = run_svgo(wikimedia_fetch)
    move_svg_to_media_dir(wikimedia_fetch)

def list_flags_with_sources() -> list[tuple[str, str]]:
    """Create a tuple of local and wikimedia filenames of flags."""

    flags = {}

    with open("sources.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mediatype = row["File"].split("-")[1]
            is_blurred = row["File"].split("-")[-1] == "blur.svg"
            if (mediatype == "flag") and (not is_blurred):
                local_filename = row["File"]
                # country = aug_map_country_dict[filename]
                wikimedia_source = row["Source"]
                WIKIMEDIA_DESCRIPTION_PAGE_PREFIX = "https://commons.wikimedia.org/wiki/File:"
                if not wikimedia_source.startswith(WIKIMEDIA_DESCRIPTION_PAGE_PREFIX):
                    raise ValueError(f"Non-wikimedia source: {wikimedia_source}!")
                wikimedia_filename = wikimedia_source.removeprefix(
                    WIKIMEDIA_DESCRIPTION_PAGE_PREFIX
                )

                flags[local_filename] = wikimedia_filename

    return flags

def browse_wikimedia_source():
    """Open in browser the sources for the first changed flag.

    We open the Wikimedia page for the relevant file and the Wikipedia
    article for the flag.

    """
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        check=True,
        text=True,
    )
    changed_flags = [
        s.removeprefix("src/media/flags/") for s in result.stdout.split("\n") if
        s.startswith("src/media/flags/")
    ]
    if len(changed_flags) == 0:
        print("No changed flags!")
        return
    first_changed_flag = changed_flags[0]

    wikimedia_filename = list_flags_with_sources()[first_changed_flag]

    wikimedia_url = "https://commons.wikimedia.org/w/index.php?title=File:" + \
        wikimedia_filename + "&limit=100#filehistory"
    country_name = first_changed_flag.removeprefix("ug-flag-").removesuffix(".svg")
    wikipedia_url = "https://en.wikipedia.org/w/index.php?search=flag of " + \
        country_name + "&title=Special%3ASearch"

    webbrowser.open(wikimedia_url)
    webbrowser.open(wikipedia_url)

def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='subparser_name')

    subparser.add_parser(
        "source",
        help="open Wikipedia and Wikimedia for the first changed flag."
    )
    parser_fetch = subparser.add_parser("fetch", help="update all flags, fetching from Wikimedia.")

    # parser_fetch.add_argument("--check-pixel-diff", action="store_true", help="use imagemagick to check pixel diff and discard changes with no diff")

    args = parser.parse_args()

    return args


def main():
    with tempfile.TemporaryDirectory(dir=".") as temp_dir_:
        temp_dir = Path(temp_dir_)
        for local_filename, wikimedia_filename in list_flags_with_sources().items():
            update_flag(local_filename, wikimedia_filename, temp_dir)


if __name__ == "__main__":
    args = parse_args()
    if args.subparser_name == "fetch":
        main()
    elif args.subparser_name == "source":
        browse_wikimedia_source()
    else:
        raise ValueError("Unknown arguments.")

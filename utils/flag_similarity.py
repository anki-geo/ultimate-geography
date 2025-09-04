"""Check for flag similarity between two countries.

Pass the name of the two countries in lower-case, with underscores
instead of spaces to the script.

pipenv run utils/flag_similarity.py country_1 country_2

Checks colours and geometries (width:height).  Does not verify that
the colours are in the same positions or indeed that the flags have
similar internal structure, at all.

"""

import argparse
import re
import logging

import xml.etree.ElementTree as ET

from typing import Self
from dataclasses import dataclass, asdict
from fractions import Fraction

logger = logging.getLogger(__name__)


## COLOUR DIFFERENCE CALCULATION

# The conversion functions are taken from Wikipedia, but are also
# compared with the reference spreadsheet:
# https://github.com/anki-geo/ultimate-geography/issues/50#issuecomment-525902404

@dataclass
class SRGB:
    """The sRGB values of the colour.

    This corresponds to "sRGB (IEC 61966-2-1)" in the reference
    spreadsheet.

    Each component is in the range [0, 1].

    """
    R: float
    G: float
    B: float

    @classmethod
    def from_hex(cls, hex_str: str) -> Self:
        """Obtain sRGB values from hex string.

        e.g. "#fff"

        The leading `#` is optional.

        Can process a hex-string of arbitrary "precision" (fff or
        ffffff or any multiple-of-three length).

        Will fail if alpha (transparency) is present.

        """
        hex_str = hex_str.lstrip("#")
        hex_length = len(hex_str)
        if not (hex_length % 3) == 0:
            raise ValueError("Length of hex colour is not divisible by 3!")

        colour_length = hex_length // 3

        rgb_hexes = (hex_str[i * colour_length: (i+1) * colour_length] for i in (0, 1, 2))
        rgb_decs = (int(c, 16) for c in rgb_hexes)
        R, G, B = (c/(16**colour_length - 1) for c in rgb_decs) # typically 255
        return cls(R=R, G=G, B=B)

@dataclass
class LinearIntensityRGB:
    """Linear intensities sRGB

    This corresponds to "Physically Linear RGB" in the reference
    spreadsheet.

 https://en.wikipedia.org/w/index.php?title=SRGB&oldid=1290230423#Definition

    Note that the reference spreadsheet uses terms of 0.0555 and
    1.0555.  I believe that here Wikipedia is correct and the standard
    values are indeed 0.055 and 1.055.

    """
    R: float
    G: float
    B: float

    @classmethod
    def from_srgb(cls, srgb: SRGB) -> Self:
        """Obtain physically linear sRGB from "raw" sRGB."""
        def intensity(x: float) -> float:
            if x <= 0.04045:
                return x/12.92
            return ((x + 0.055)/1.055) ** 2.4

        return cls(
            **{c: intensity(v) for c, v in asdict(srgb).items()}
        )

@dataclass
class CIEXYZ:
    """CIEXYZ values.

    CIEXYZ in the reference spreadsheet.

    """
    X: float
    Y: float
    Z: float

    @classmethod
    def from_linear_intensity(cls, rgb: LinearIntensityRGB) -> Self:
        """Convert from linear intensity to CIEXYZ.

        https://en.wikipedia.org/w/index.php?title=SRGB&oldid=1290230423#Primaries

        """
        X = 0.4124 * rgb.R + 0.3576 * rgb.G + 0.1805 * rgb.B
        Y = 0.2126 * rgb.R + 0.7152 * rgb.G + 0.0722 * rgb.B
        Z = 0.0193 * rgb.R + 0.1192 * rgb.G + 0.9505 * rgb.B

        return cls(X=X, Y=Y, Z=Z)

@dataclass
class CIELAB:
    """CIELAB L*, a* and b* values.

    "CIELAB" fields in the reference spreadsheet.

    """
    L_star: float
    a_star: float
    b_star: float

    @classmethod
    def from_ciexyz(cls, ciexyz: CIEXYZ) -> Self:
        """Convert from CIEXYZ to CIELAB.

        Equations from:

        https://en.wikipedia.org/w/index.php?title=CIELAB_color_space&oldid=1305739979#From_CIE_XYZ_to_CIELAB

        (The form of the equations matches those from the reference spreadsheet.)


        The whitepoint normalization values (X_n, Y_n, Z_n) depend on
        the choice of illuminant.  For the standard-ish "Illuminant
        D65", Wikipedia is subtly inconsistent.

        https://en.wikipedia.org/w/index.php?title=CIELAB_color_space&oldid=1305739979#From_CIE_XYZ_to_CIELAB
        gives X_n = 95.0489, Z_n = 108.8840 (for D65).

        https://en.wikipedia.org/w/index.php?title=Standard_illuminant&oldid=1308681429#D65_values
        gives X_n = 95.047, Z_n = 108.883.

        The change in the "CIELAB_color_space" article:

        https://en.wikipedia.org/w/index.php?title=CIELAB_color_space&diff=prev&oldid=891359981

        was motivated by alignment with the "Standard illuminant"
        article... (Currently, they're not aligned.)

        The source that the "Standard illuminant" article quotes
        ("Colorimetry: understanding the CIE system.") gives X =
        95.04, Z = 108.88.  (Again slightly different!)


        Given these slight inconsistencies, I've decided to use the
        less "precise" (fewer S.F.) values based on the reference
        spreadsheet:

        X_n = 95.05
        Z_n = 108.9

        The advantage of these values is that #FFF (pure white) gives
        exactly L*=100, a*=b*=0.


        (Y_n is always 100.)

        """
        def f(t):
            delta = 6/29

            if t > delta**3:
                return t**(1/3)
            return t/(3 * delta**2) + 4/29

        X_n = 95.05
        Y_n = 100.
        Z_n = 108.9

        # We're changing normalisation from [0, 1.0] to [0, 100.]
        X = 100 * ciexyz.X
        Y = 100 * ciexyz.Y
        Z = 100 * ciexyz.Z

        L_star = 116 * f(Y / Y_n) - 16
        a_star = 500 * (f(X / X_n) - f(Y / Y_n))
        b_star = 200 * (f(Y / Y_n) - f(Z / Z_n))

        return cls(
            L_star=L_star,
            a_star=a_star,
            b_star=b_star,
        )

    @classmethod
    def from_hex(cls, hex_str: str) -> Self:
        """Obtain CIELAB value from hex string."""
        return cls.from_ciexyz(
            CIEXYZ.from_linear_intensity(
               LinearIntensityRGB.from_srgb(
                   SRGB.from_hex(hex_str)
               )
            )
        )

    @classmethod
    def delta_e_star(cls, c1, c2):
        """Calculate the Delta_E_ab (CIE76) colour difference.

        https://en.wikipedia.org/w/index.php?title=Color_difference&oldid=1297370326#CIE76

        """

        return (
            (c1.L_star - c2.L_star)**2 +
            (c1.a_star - c2.a_star)**2 +
            (c1.b_star - c2.b_star)**2
        ) ** 0.5


def delta_e_star_from_hex(hex_str_1: str, hex_str_2: str) -> float:
    """Calculate the Delta_E_ab (CIE76) colour difference."""

    c1 = CIELAB.from_hex(hex_str_1)
    c2 = CIELAB.from_hex(hex_str_2)

    return CIELAB.delta_e_star(c1, c2)

def format_colour(hex_str: str) -> str:
    """Format the colour for printing in a terminal."""
    srgb = SRGB.from_hex(hex_str)
    r = round(255 * srgb.R)
    g = round(255 * srgb.G)
    b = round(255 * srgb.B)
    return f"\033[48;2;{r};{g};{b}m{hex_str}\033[0m"

# NB HTML green is #008000!  We're using #0f0, because we're
# interested in which colour "group" (red-ish, green-ish etc.) we're
# in.
STANDARD_COLOUR_GROUPS = {
    "black": CIELAB.from_hex("000"),
    "white": CIELAB.from_hex("fff"),
    "red": CIELAB.from_hex("f00"),
    "blue": CIELAB.from_hex("00f"),
    "green": CIELAB.from_hex("0f0"),
    "yellow": CIELAB.from_hex("ff0"),
}

def categorise_colour(hex_str: str) -> str:
    """Categorise colour.

    Choose which of the list of standard colours, we determine the
    colour to be (red, green, blue etc.)?

    """
    current_difference = float("inf")
    current_name = ""

    colour = CIELAB.from_hex(hex_str)

    for name, standard_colour in STANDARD_COLOUR_GROUPS.items():
        difference = CIELAB.delta_e_star(colour, standard_colour)

        # Hack so that, say, "#002B7F" is categorised as blue, not
        # black.  The justification is that we want to be _very_ close
        # to "black" and "white", to be categorised as such.  TBH
        # maybe using hue rather than ΔE* would have been better
        # here. (?)
        if name in ["white", "black"]:
            difference *= 3
        # Similar justification as above.  (Yellow isn't a primary
        # colour.)
        if name in ["yellow"]:
            difference *= 1.5

        if difference < current_difference:
            current_name = name
            current_difference = difference
        logger.info(f"{hex_str} {name} {difference}")

    return current_name


## SVG PARSING

HTML_COLOURS = {
    "red": "#f00",
}

def extract_flag_colours(filename: str) -> list[str]:
    """Extract the colours in a flag.

    This currently only looks at the `fill` attribute.

    """
    t = ET.parse(filename)
    root = t.getroot()

    colours = []

    for el in root.iter():
        if "fill" in el.attrib:
            colour = el.attrib["fill"]
            if not colour[0] == "#":
                if not colour in HTML_COLOURS:
                    raise ValueError(f"Invalid colour {colour}!")
                colour = HTML_COLOURS[colour]
            if colour not in colours:
                colours.append(colour)
    return colours

def extract_categorised_flag_colours(filename: str) -> dict[str, list[str]]:
    """Extract the colours in a flag categorised by colour-type.

    e.g. `{"green": ["0f0"]}`

    """
    colours = extract_flag_colours(filename)

    categorised_colours: dict[str, list[str]] = {}

    for c in colours:
        category = categorise_colour(c)
        if category in categorised_colours:
            categorised_colours[category].append(c)
        else:
            categorised_colours[category] = [c]

    return categorised_colours

def compare_flag_colours(
    country_name_1: str,
    country_name_2: str,
    colour: bool = True,
) -> None:
    """Compare the "matching" colours of the flags of two countries.

    If colour=True show the colours in the background when printing
 the relevant hex-strings.

    """

    filename_1 = f"src/media/flags/ug-flag-{country_name_1}.svg"
    filename_2 = f"src/media/flags/ug-flag-{country_name_2}.svg"
    flag1 = extract_categorised_flag_colours(filename_1)
    flag2 = extract_categorised_flag_colours(filename_2)

    flag1_categories = set(flag1.keys())
    flag2_categories = set(flag2.keys())

    if not flag1_categories == flag2_categories:
        logger.warning(f"{country_name_1} has colours {flag1_categories}.")
        logger.warning(f"{country_name_2} has colours {flag2_categories}.")

    flag1_ignored_categories = flag1_categories - flag2_categories
    flag2_ignored_categories = flag2_categories - flag1_categories

    if flag1_ignored_categories:
        logger.warning(f"{country_name_1}: ignoring colours {flag1_ignored_categories}")
    if flag2_ignored_categories:
        logger.warning(f"{country_name_2}: ignoring colours {flag2_ignored_categories}")

    common_categories = flag1_categories & flag2_categories

    for category in common_categories:
        if len(flag1[category]) > 1:
            raise ValueError(f"{country_name_1} has more than one {category} colour!")
        if len(flag2[category]) > 1:
            raise ValueError(f"{country_name_2} has more than one {category} colour!")
        # TODO Allow picking/ignoring "extra" colours.  This is
        # trickier than ignoring categories, since how would the
        # script or even the user know which is the "main" colour?

    print(f"\t{country_name_1[0:7]}\t{country_name_2[0:7]}\t")
    for category in common_categories:
        c1 = flag1[category][0]
        c2 = flag2[category][0]

        difference = delta_e_star_from_hex(c1, c2)
        if colour:
            print(
                f"{category}\t{format_colour(c1)}\t{format_colour(c2)}\t{difference:.2f}"
            )
        else:
            print(
                f"{category}\t{c1}\t{c2}\t{difference:.2f}"
            )

## Proportions

def flag_proportions(filename: str) -> Fraction:
    """Obtain the flag proportions."""

    t = ET.parse(filename)
    root = t.getroot()

    # Some flags have viewBox="x,y w,h" so we also need `,`
    view_box_str = re.split(" |,", root.attrib["viewBox"])

    if not len(view_box_str) == 4:
        raise ValueError(f"viewBox has incorrect length {len(view_box_str)}")

    dimensions_str = view_box_str[2:4]

    try:
        # Try as int first.
        width, height = [int(x) for x in dimensions_str]
        return Fraction(height, width)
    except ValueError:
        width_f, height_f = [float(x) for x in dimensions_str]
        logger.info("viewBox dimensions were floats!")
        logger.info(f"Decimal ratio was {height_f/width_f}!")
        return Fraction(height_f/width_f).limit_denominator(100)

def compare_flag_proportions(country_name_1: str, country_name_2: str) -> None:
    """Compare the proportions of the flags of two countries."""

    def prettify(fraction: Fraction) -> str:
        """Display fraction as x:y to match Wikipedia."""
        return f"{fraction.numerator}:{fraction.denominator}"

    filename_1 = f"src/media/flags/ug-flag-{country_name_1}.svg"
    filename_2 = f"src/media/flags/ug-flag-{country_name_2}.svg"

    proportions_1 = flag_proportions(filename_1)
    proportions_2 = flag_proportions(filename_2)

    if proportions_1 == proportions_2:
        print(f"Both flags have the same proportions {prettify(proportions_1)}!")
    else:
        print("The flags have different proportions!")
        print(f"{country_name_1}: {prettify(proportions_1)}")
        print(f"{country_name_2}: {prettify(proportions_2)}")

## Parsing

def parse_args() -> argparse.Namespace:
    """Parse args."""
    parser = argparse.ArgumentParser("Script to help determine flag similarity")
    parser.add_argument("countries", nargs=2, help="lowercase country names, with spaces as _")
    parser.add_argument(
        "--colour",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="show colours as background"
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    compare_flag_colours(args.countries[0], args.countries[1], colour=args.colour)
    print()
    compare_flag_proportions(args.countries[0], args.countries[1])

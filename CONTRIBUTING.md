# Contributing

:wave: Hello there! :tada: Thanks for taking the time to contribute!

Seen something outdated or plain wrong? Spotted a typo somewhere? Think something could be better translated, or want to translate the whole deck into a new language? Awesome! :100: Let us now right away by [opening a new issue](https://github.com/axelboc/anki-ultimate-geography/issues).

## Contributor's guide

Ready to start working on an issue? Here is what you need to know.

- If you're new to contributing on GitHub, [read this guide](https://guides.github.com/activities/contributing-to-open-source/) first.
- The deck is managed with [Anki Deck Manager](https://github.com/OnkelTem/anki-dm). The project's documentation explains the file structure in details, but the most important file is `data.csv`. It contains the actual content of the deck, including translations. In most cases, this is the only file you'll need to work on.
- If you add a new row to `data.csv`, make changes to other files, or would like to review the changes you made to the deck in Anki, you'll need to set up and use Anki Deck Manager.

### Set-up

1. Install the [CrowdAnki add-on](https://github.com/Stvad/CrowdAnki) in Anki.
1. Fork and clone this repository on your machine.
1. With the help of your favourite command-line package manager (e.g. `brew`, `chocolatey`, `apt-get`), install [PHP 7](http://php.net/) and [Composer](https://getcomposer.org/download/).
1. From the root of the project, run `composer install` to install Anki Deck Manager.

### Build and import

From here, building the deck is as simple as running `composer build`. Anki Deck Manager builds the deck into the `build` folder, in a format that CrowdAnki understands, which you can then import into Anki.

### Indexing

Anki requires each note to have a unique identifier. When you add a note to the deck, that is, when you add a row to `data.csv`, make sure to leave the first column empty. Then, tell Anki Deck Manager to re-index the deck by running `composer index`. The note you added will receive an identifier.

### Quotes normalisation

Anki Deck Manager has a very specific way of wrapping fields with double quotes  in `data.csv` to escape special characters (cf. #129). Whether you edit the file by hand or through an editor, chances are you won't end up with double quotes in the same places. If you commit the file as is, the diff will be cluttered with changes that have nothing to do with your edits. To avoid this, run `composer index` before commiting your changes. This command has the side effect of normalising the escaping of fields in the entire file.

## Maintainer's guide

### Versioning

The releases follow a versioning scheme of the form `x.y`, where:

- `x` increases in the case of a **major, breaking release** (e.g. v3.0),
- `y` increases in the case of a **minor, non-breaking release** (e.g. v2.6).

Content changes, such as adding or removing a note, replacing an image, or translating the deck into a new language, all constitute minor changes. A change is considered major when users are likely to **lose a significant part of their progress** when upgrading the deck with CrowdAnki (cf. [_Upgrading_](README.md#upgrading) section of README).

### Release process

1. Bump the version in `desc.html` and commit the change.
1. Run `composer index && composer build`.
1. Add each folder in the `build` directtoy to a separate ZIP archive named as follows:
  - `Ultimate Geography` ==> `Ultimate_Geography_v[x.y]_EN.zip`.
  - `Ultimate Geography [Extended]` ==> `Ultimate_Geography_v[x.y]_EN_EXTENDED.zip`.
  - `Ultimate Geography_de` ==> `Ultimate_Geography_v[x.y]_DE.zip`.
  - `Ultimate Geography [Extended]_de` ==> `Ultimate_Geography_v[x.y]_DE_EXTENDED.zip`.
1. In Anki, synchronise all your devices then import the folder of the standard English deck with CrowdAnki (i.e. `Ultimate Geography`). For major versions, make sure to perform a [clean import](README.md#major-version). Synchronise all your devices again once the import is complete.
1. Export the deck as an APKG package named `Ultimate_Geography_v[x.y]_EN.apkg`, making sure to exclude scheduling information but include all media.
1. Write the release notes on GitHub.
1. Attach the APKG file as well as all the ZIP files to the release and publish it.
1. Go to [AnkiWeb](https://ankiweb.net/decks/).
1. Find the _Ultimate Geography_ deck and select _Actions_ > _Share_
1. Update the version number in the title and the description if needed.
1. Enter the full legal name and click _Share_.
1. Close the milestone in GitHub and create a new one for the next version.

## Content guidelines

### _Flag similarity_ field

This field is used in the standard deck's _Flag - Country_ template.

In Anki, when you keep on confusing two flags, you can't put them side by side to learn their visual differences. The _Flag similarity_ field works around this limitation by providing a concise description of the differences a flag has with another. It allows users to more easily learn to distinguish pairs of similar flags and perhaps come up with mnemonics to remember their respective countries.

A note's _Flag similarity_ field contains a list of countries, each followed by a list of differences. For instance, the flag similarities for Iceland are written as follows: "Norway (red background, blue cross), Faroe Islands (white background, red and blue cross)". The list of differences must be **precise**, **clear** and **concise**. Advanced [vexillological](https://en.wikipedia.org/wiki/Vexillology) terms should be avoided.

Flag similarities are always **mutual**: if flag A is similar to flag B, then flag B is similar to flag A. To determine whether two flags are similar enough to warrant mutual _Flag similarity_ information, their differences must first be **identified** and **classified**. The following classification applies:

- **Critical differences (C)**
  - presence/absence of decoration - i.e. symbol, coat of arms, etc.
- **Major differences (M)**
  - same colours in different positions (e.g. two swapped, three rotated)
  - decorations of different types in same position (e.g. symbol vs. coat of arms)
  - decorations of same type in different positions (e.g. star(s) above/below band for Curaçao/Nauru)
- **Minor differences (m)**
  - slightly different colours (e.g. shade of blue, red vs. maroon, darker green)
  - slightly different geometry (e.g. width, number of serrated edges for Qatar/Bahrain, size of canton)
  - different decoration of same type in same position (e.g. different symbol, different coat of arms)
  - decorations of same type in different amounts (e.g. fewer stars)
  - decorations of same type with different colours (e.g. white vs. red stars for Australia/New Zealand)
- **Negligible differences (n)**
  - subtly different colours - i.e. [ΔE](https://github.com/axelboc/anki-ultimate-geography/issues/50#issuecomment-525902404) < 30
  - subtly different geometry

Two flags are then elligible for _Flag similarity_ information when they respect the two rules below:

- Their differences all fit in the above classification. For instance, France and Italy are not elligible because their left bands are respectively blue and green, and "different colours in same position" does not appear in the classification.
- Their classified differences form one the following combinations:
  - `1C 0M 0m {0+}n` = one critical difference and any number of negligible differences
  - `0C 1M {0-2}m {0+}n` = one major difference, up to two minor differences and any number of negligible differences
  - `0C 0M {0-3}m {0+}n` = up to three minor differences and any number of negligible differences

Critical, major and minor differences should be listed in the _Flag similarity_ field. Negligible differences should be listed only when relevant, notably when two flags share nothing but negligible differences.

### Translation sources

If you are contributing a new language, please add any sources to `TRANSLATION_SOURCES.md`, also explaining possible style choices.
If you are significantly changing the style or content of an existing translation, please update the sources and explanations.

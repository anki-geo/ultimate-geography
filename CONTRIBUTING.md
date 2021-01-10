# Contributing

:wave: Hello there! :tada: Thanks for taking the time to contribute!

Seen something outdated or plain wrong? Spotted a typo somewhere? Think something could be better translated, or want to translate the whole deck into a new language? Awesome! :100: Let us now right away by [opening a new issue](https://github.com/axelboc/anki-ultimate-geography/issues).

#### Table of contents

- [**Contributor's guide**](#contributors-guide)
  - [Set-up](#set-up)
  - [Build and import](#build-and-import)
  - [Indexing](#indexing)
  - [Quotes normalisation](#quotes-normalisation)
- [**Content inclusion rules**](#content-inclusion-rules)
  - [Political geography](#political-geography)
  - [Physical geography](#physical-geography)
- [**Content guidelines**](#content-guidelines)
  - [_Country_ field](#country-field)
  - [_Country info_ field](#country-info-field)
  - [_Capital_ field](#capital-field)
  - [_Capital info_ field](#capital-info-field)
  - [_Capital hint_ field](#capital-hint-field)
  - [_Flag_ field](#flag-field)
  - [_Flag similarity_ field](#flag-similarity-field)
  - [_Map_ field](#map-field)
- [**Translation sources**](#translation-sources)
  - [Norwegian Bokmål](#norwegian-bokmål)
- [**Maintainer's guide**](#maintainers-guide)
  - [Versioning](#versioning)
  - [Release process](#release-process)


## Contributor's guide

Ready to start working on an issue? Here is what you need to know.

- If you're new to contributing on GitHub, [read this guide](https://guides.github.com/activities/contributing-to-open-source/) first.
- The deck is managed with [Brain Brew][Brain Brew].
    - All data is (currently) stored in the split csv files in `src/data/split` with a column for each translation of the deck.
    - [Brain Brew][Brain Brew] allows for syncing to and from Anki, so one can edit this deck in either Csv format or in Anki itself. See the steps below for how to build the deck.
    - All dependencies are managed with [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html)
        - This ensures that this project runs in a virtual environment, which is not hampered by individual setups

### Set-up

1. Install the [CrowdAnki add-on](https://github.com/Stvad/CrowdAnki) in Anki.

1. Fork and clone this repository on your machine.

1. Install `Pip` (requires Python)
    - Linux: `sudo apt install python3-pip` (or use the below script)
    - Windows: Use the `get-pip.py` [script](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py) (See https://phoenixnap.com/kb/install-pip-windows)
    - Mac: Use the `get-pip.py` [script](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py) (See https://ahmadawais.com/install-pip-macos-os-x-python/)

1. Install `Pipenv`
    - `pip install pipenv` (may need to use `pip3` instead)

1. Setup the Pipenv environment. This will install [Brain Brew][Brain Brew] and all of its dependencies in a virtual environment.
    - `pipenv install`

    1. Use this new virtual environment
        - `pipenv shell` in the main directory
        - Use `deactivate` to exit the virtual environment, if you wish

### Project structure

#### Csvs

The data for the deck is stored in multiple csv files in `src/data/split`,
which are all split up by the different fields and their many translations.
It is split up this way as a single csv file with each translation is too unwieldy.

The main file is `main.csv` which contains the guid, country, flag, map, and tags.
All other csv files are Derivatives of main and contain extra data that is added onto main's rows.
Each contains the Country name as the first field,
which is used to match it together with the row in `main.csv`.

*Derivative entries are completely optional!* `Capital_hint.csv` only has 4 entries,
as those are the only ones that actually have any of the columns populated.
Only enter a row into a derivative csv if it is needed.


#### Media

Media files are stored in the `src/media` folder, under arbitrary subfolders.


### Source to Anki

From here, building the deck is as simple as running `brain_brew recipes/source_to_anki.yaml`.
[Brain Brew][Brain Brew] builds the deck into the `build` folder,
in a format that CrowdAnki understands, which you can then import into Anki.

On first run it will generate all the missing files and folders, with some warnings in the output.
This is normal.


### Anki to Source

One can also make changes in Anki, and pull the changes back into the csv files. Simply:

1. Make your edit(s) in Anki
1. Export the deck using CrowdAnki into the `build/Ultimate Geography` folder
    - Use this folder even if you are using the Extended deck.
      The below recipe yaml file is setup to look at this export.
      The end result will be the same.
    - If using a different language than English then this option will need further configuring :sweat:
1. Run `brain_brew recipes/source_from_anki.yaml`
    - This will take all changes to Notes and their Media.
        - Existing media will be updated in the folder it is already located.
          New media will be placed on the top level of the `src/media` folder.
          They can then be moved into any arbitrary subfolder.
    - However it will **not** take changes to Note Models, Card Templates, Deck Description, or Deck options.



### Making a change in source files

#### Adding a new country

Add the country to `main.csv`, and then any other derivative files that are needed.

Do not create a guid for the country, that will be autogenerated on the
first run of the `source_to_anki.yaml` recipe.

#### Changing an existing entry

If you change the country name, please remember to update each derivative file that contains that country.

#### Removing a country entirely

Same as above, remember the derivative files.

#### Adding a new translation

Add a new column to each of the csv files, following the
naming convention of `[field name]:[country code]`
(e.g. `country info:fr`) all in lowercase.

#### Adding a new column (e.g. Population, Currency, etc)

The most heavily requested change to the deck!
This will soon™ be solved using [Brain Brew][Brain Brew] by combining separate repositories.

#### Changing the Recipe builders

Advanced.
See [Brain Brew's Contributing](https://github.com/ohare93/brain-brew/blob/master/CONTRIBUTING.md) for more info.

`-v` can be used when building a recipe to only run verification on the recipe file.


## Content inclusion rules

In order for a geographical entity to be included in the deck, it must:

- belong to a well-defined, Wikipedia-sourced list of entities of a common type (e.g. sovereign states, seas, etc.);
- meet the inclusion criteria that apply to entities of this type.

### Political geography

Inclusion rules for political entities are documented and put into use in [political-entities.xlsx](political-entities.xlsx). They were discussed in [#137][ref137], [#221][ref221], [#306][ref306], [#312][ref312] and [#361][ref361].

A political entity can be included either fully (map, capital and flag) or partially (with only a map). In the rare case where a political entity belongs to more than one of the below categories, it will only be considered in the first category of which it's a member.

#### Sovereign states

- Source: https://en.wikipedia.org/wiki/List_of_sovereign_states
- All fully included, regardless of UN membership status or recognition by other states.

#### Dependent territories

- Sources:
  - https://en.wikipedia.org/wiki/Dependent_territory
  - https://en.wikipedia.org/wiki/Countries_of_the_United_Kingdom
- Specifically, inhabited dependent territories.
- Criteria for inclusion with map: `population >= 15,000 OR area >= 1,000 km2`
- Criteria for inclusion with map, capital and flag: `(population >= 15,000 AND area >= 1,000 km2) OR population >= 100,000`

#### Autonomous islands

- Source: https://en.wikipedia.org/wiki/List_of_autonomous_areas_by_country
- Specifically, insular autonomous territories.
- Criteria for inclusion with map: `population >= 100,000`
- Capitals and flags never included.

#### Transcontinental overseas territories

- Source: https://en.wikipedia.org/wiki/List_of_transcontinental_countries
- Specifically, inhabited territories located on a different content than their mainland.
- Criteria for inclusion with map: `population >= 100,000 AND distance from mainland >= 300 km`
- Capitals and flags never included.

#### Enclaves and exclaves

- Source: https://en.wikipedia.org/wiki/List_of_enclaves_and_exclaves#Semi-enclaves_and_semi-exclaves
- Specifically, inhabited full or semi land enclaves/exclaves.
- Relevant sections:
  - [Enclaves that are also exclaves > National level](https://en.wikipedia.org/wiki/List_of_enclaves_and_exclaves#National_level)
  - [Exclaves that are not enclaves > National level](https://en.wikipedia.org/wiki/List_of_enclaves_and_exclaves#National_level_2)
  - [Semi-enclaves and semi-exclaves > Non-sovereign semi-enclaves](https://en.wikipedia.org/wiki/List_of_enclaves_and_exclaves#Non-sovereign_semi-enclaves)
  - [Semi-enclaves and semi-exclaves > Non-sovereign semi-exclaves](https://en.wikipedia.org/wiki/List_of_enclaves_and_exclaves#Non-sovereign_semi-exclaves)
- Criteria for inclusion with map: `population >= 100,000 AND distance from mainland >= 300 km`
- Capitals and flags never included.

### Physical geography

A physical entity can only be included partially, with only a map.

#### Continents

- Source: https://en.wikipedia.org/wiki/Continent#Number
- Specifically the seven-continent model but with the continent of _Australia_ replaced with the world region of _Oceania_, as discussed in [#345][ref345].

#### Water bodies

The deck currently includes a number of water bodies (oceans, seas, gulfs, etc.) but inclusion rules have not yet been officialised.

## Content guidelines

### _Country_ field

The correct name to use for a given country or territory in each language is not always clear. This usually occurs in two cases:

- when the official name is changed but the old name remains more frequently used (in the media and in everyday conversation) - e.g. _Ivory Coast_ vs. _Côte d'Ivoire_;
- when the official name is simply shortened in everyday use - e.g. _China_ vs. _People's Republic of China_.

Unless otherwise stated in the [_Translation sources_](#translation-sources) section below, we take **the title of the Wikipedia article** for the country, in the language of the given deck. Alternative names may be mentioned in the _Country info_ field, when relevant.

If the title of the Wikipedia article contains a parenthetical portion for disambiguation purposes, it must be removed, except in the very unlikely case that two countries share the same name in a given language — e.g. _Saint-Martin (Antilles françaises)_ and _Saint-Martin (royaume des Pays-Bas)_ in the French deck.

Country names must not be preceded by articles, particularly in gendered languages (French, German, etc.) unless Wikipedia indicates otherwise - e.g. _United Kingdom_, _The Gambia_. This rule also applies to the _Flag similarity_ field, but not to other fields in which country names are used in sentences.

To understand the reasoning behind these decisions, see [#181][ref181] (Wikipedia as source), [#212][ref212] (disambiguating country names), and [#157#issuecomment-549143860][ref157] (no gender articles).

### _Country info_ field

To help with memorisation and provide context while learning, this field may contain:

- governance information - e.g. _Overseas territory of the United Kingdom_ (Cayman Islands)
- statehood information - e.g. _Independent state claimed by Moldova_ (Transnistria)
- alternative and former country names - e.g. _Also known as Timor-Leste_ (East Timor)
- in rare cases only, general knowledge information - see Melanesia for an example

The content of this field should be concise and consistent across notes. It may differ between languages, notably when dealing with alternative names.

### _Capital_ field

Unless otherwise stated in the [_Translation sources_](#translation-sources) section below, we use the capital given in the [infobox](https://en.wikipedia.org/wiki/Template:Infobox_country#Examples) of the Wikipedia article for the country, in the language of the given deck.

If the title of the Wikipedia article contains a parenthetical portion for disambiguation purposes, it must be removed. The _Capital hint_ field is used instead for disambiguation.

If a capital has alternative names, we take **the title of the Wikipedia article** for the capital, in the language of the given deck. This corresponds typically to the name used in the infobox of the country's Wikipedia article. Alternative names may be mentioned in the _Capital info_ field, when relevant.

If multiple capitals are listed in a country's infobox, the following guidelines apply:

- If the first capital is followed by a qualifier such as "official", "constitutional", "de jure", "claimed", or "political", it must be used alone in the _Capital_ field. The _Capital info_ field must then be used to detail the status and/or role of every capital - e.g. _While Dodoma is the official capital, Dar es Salaam is the de facto seat of government._
- If government branches such as "executive" or "legislative" are the only qualifiers used, then the capitals must all be listed in the _Capital_ field, separated by commas - e.g. _Pretoria, Cape Town, Bloemfontein_ (South Africa). The _Capital info_ field must again be used to detail the role of every capital.
- If no qualifiers are provided at all, then the capitals must all be listed in the _Capital_ field, separated by commas - e.g. _Santa Cruz de Tenerife, Las Palmas_ (Canary Islands). A concise explanation should then be provided in the _Capital info_ field.

### _Capital info_ field

As explained in the previous section, this field is typically used for countries with multiple capitals, to clarify the role and/or status of each capital, or to explain succinctly why the country has multiple capitals.

### _Capital hint_ field

This field is used in notes that share:

- the same exact capital - e.g. _London_ (United Kingdom and England);
- capitals with very similar names - e.g. _Georgetown_ and _George Town_.

The hints appear on _Capital - Country_ cards to avoid confusion or random guesses. They should
convey as little information as possible to not give away the answers.

### _Flag_ field

This field must contain a single HTML image element pointing to the SVG or PNG image of a flag - e.g. `<img src="ug-flag-seychelles.svg" />`. The image must be placed in the ` media` folder and named `ug-flag-<country_name>.<svg|png>`. SVG is the preferred format.

SVG flags are sourced from [Wikimedia](https://commons.wikimedia.org/). We use the flag that is presented in the [infobox](https://en.wikipedia.org/wiki/Template:Infobox_country#Examples) of the English Wikipedia article for the country. The flag's source URL and licence must be documented in `sources.csv`.

The following guidelines apply to flag images:

- The `viewBox`, `width` and `height` attributes are required.
- The height must be set to 250 px (`height="250"`) and the width adjusted proportionally.
- Each flag must be optimised with [SVGO](https://jakearchibald.github.io/svgomg/).
- SVG flags larger than 50 kB must be exported to PNG (still with a height of 250 px) and optimised with a tool like [PNGGauntlet](https://pnggauntlet.com/).

If the name of a country appears clearly on a flag, a second version of that flag may also be provided, with the name of the country blurred out. The name should be blurred using [Inkscape](https://inkscape.org/)'s Gaussian blur effect as explained in [#247][ref247]. The blurred flag must be named `ug-flag-<country_name>-blur.<svg|png>` and placed in the `media` folder. A second HTML element must then be added to the _Flag_ field _before_ the existing HTML element. This allows the blurred flag to appear on the front of the country's _Flag - Country_ card.

### _Flag similarity_ field

This field is used in the _Flag - Country_ template.

In Anki, when you keep on confusing two flags, you can't put them side by side to learn their visual differences. The _Flag similarity_ field works around this limitation by providing a concise description of the differences a flag has with another. It allows users to more easily learn to distinguish pairs of similar flags and perhaps come up with mnemonics to remember their respective countries.

A note's _Flag similarity_ field contains a list of countries, each followed by a list of differences. For instance, the flag similarities for Iceland are written as follows: _Norway (red background, blue cross), Faroe Islands (white background, red and blue cross)_. The list of differences must be **precise**, **clear**, and **concise**. Advanced [vexillological](https://en.wikipedia.org/wiki/Vexillology) terms should be avoided.

Flag similarities are always **mutual**: if flag A is similar to flag B, then flag B is similar to flag A. To determine whether two flags are similar enough to warrant mutual _Flag similarity_ information, their differences must first be **identified** and **classified**. The following classification applies:

- **Critical differences (C)**
  - presence/absence of decoration - e.g. symbol, coat of arms
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

Two flags are then eligible for _Flag similarity_ information when they respect the two rules below:

- Their differences all fit in the above classification. For instance, France and Italy are not eligible because their left bands are respectively blue and green, and "different colours in same position" does not appear in the classification.
- Their classified differences form one the following combinations:
  - `1C 0M 0m {0+}n` = one critical difference and any number of negligible differences
  - `0C 1M {0–2}m {0+}n` = one major difference, up to two minor differences, and any number of negligible differences
  - `0C 0M {0–3}m {0+}n` = up to three minor differences and any number of negligible differences

Critical, major, and minor differences should be listed in the _Flag similarity_ field. Negligible differences should be listed only when relevant, notably when two flags share nothing but negligible differences.

### _Map_ field

This field must contain a single HTML image element pointing to the PNG image of a map - e.g. `<img src="ug-map-seychelles.png" />`. The image must be placed in the ` media` folder and named `ug-map-<country_name>.png`. PNG is the preferred format.

The source SVG maps come, or are inspired, from the [SVG locator maps](https://commons.wikimedia.org/wiki/Category:SVG_locator_maps_of_countries_(16:9_regional_location_map_scheme)) project on Wikimedia. The maps' source URLs and licences must be documented in `sources.csv`.

The following guidelines apply to map images:

- The maps must be sourced or created as SVG, exported to PNG, and then optimised with a tool like [PNGGauntlet](https://pnggauntlet.com/).
- They should have a width of 500 px and a height of approximately 281 px.
- The style (colours, strokes, etc.) should match that of existing maps in the deck (note that water bodies use a different style than countries).
- For small islands or archipelagos, the map should include a zoom box to facilitate identification.

## Translation sources

When Wikipedia in a given language is not sufficently exhaustive to support the translation of this deck, additional sources may be used. This section references such sources, as well as any stylistic choices made by translators.

### Norwegian Bokmål

Norwegian Bokmål (nb) is the preferred written-language standard of roughly 90% of Norway's population, with the remaining 10% preferring Norwegian Nynorsk (nn).

The Norwegian Bokmål translation is based on the following sources in addition to the English and German decks, listed in order of priority:

- **[_Country names, capitals and national holidays_](https://www.regjeringen.no/no/dokumenter/statsnavn-hovedsteder-og-nasjonaldager/id87863/)** - This brochure from the Norwegian Ministry of Foreign Affairs is the most authoritative source for country names in Norwegian, as it is used by Norwegian diplomats. Only includes sovereign countries.
- **[_The Great Norwegian Encyclopedia_](https://snl.no/)** - Used for countries and territories that were not included in the above brochure.
- **[Wikipedia in Norwegian Bokmål](https://no.wikipedia.org/wiki/Portal:Forside)** - Used when neither of the above sources were enough to verify spelling.

In matters of style and grammar, a somewhat conservative style has been used, with feminine-gendered nouns used only in the case of bays and islands ("-bukta" and "-øya", e.g. Biscayabukta instead of Biscayabukten).


## Maintainer's guide

### Versioning

The releases follow a versioning scheme of the form `x.y`, where:

- `x` increases in the case of a **major, breaking release** (e.g. v3.0),
- `y` increases in the case of a **minor, non-breaking release** (e.g. v2.6).

Content changes, such as adding a note, replacing an image, or translating the deck into a new language, all constitute minor changes. A change is considered major when users are likely to **lose a significant part of their progress** when upgrading the deck with CrowdAnki.

### Release process

1. Bump the version in `desc.html` and commit the change.
1. Run `brain_brew recipes/source_to_anki.yaml`.
1. Add each folder in the `build` directory to a separate ZIP archive named as follows:
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

[ref129]: https://github.com/axelboc/anki-ultimate-geography/issues/129
[ref137]: https://github.com/axelboc/anki-ultimate-geography/issues/137
[ref157]: https://github.com/axelboc/anki-ultimate-geography/pull/157#issuecomment-549143860
[ref181]: https://github.com/axelboc/anki-ultimate-geography/issues/181
[ref212]: https://github.com/axelboc/anki-ultimate-geography/issues/212
[ref221]: https://github.com/axelboc/anki-ultimate-geography/issues/221
[ref247]: https://github.com/axelboc/anki-ultimate-geography/pull/247
[ref306]: https://github.com/axelboc/anki-ultimate-geography/pull/306
[ref312]: https://github.com/axelboc/anki-ultimate-geography/pull/312
[ref345]: https://github.com/axelboc/anki-ultimate-geography/pull/345
[ref361]: https://github.com/axelboc/anki-ultimate-geography/pull/361
[Brain Brew]: https://github.com/ohare93/brain-brew

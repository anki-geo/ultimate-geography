# Contributing

:wave: Hello there! :tada: Thanks for taking the time to contribute!

Seen something outdated or plain wrong? Spotted a typo somewhere? Think something could be better translated, or want to translate the whole deck into a new language? Awesome! :100: Let us know right away by [opening a new issue](https://github.com/anki-geo/ultimate-geography/issues).

#### Table of contents

- [**Contributor's guide**](#contributors-guide)
  - [Getting started](#getting-started)
  - [Brain Brew recipes](#brain-brew-recipes)
    - [Source to Anki](#source-to-anki)
    - [Anki to Source](#anki-to-source)
  - [How-to's](#how-tos)
- [**Content inclusion rules**](#content-inclusion-rules)
  - [Political geography](#political-geography)
    - [Sovereign states](#sovereign-states)
    - [Dependent territories](#dependent-territories)
    - [Autonomous islands](#autonomous-islands)
    - [Transcontinental overseas territories](#transcontinental-overseas-territories)
    - [Enclaves and exclaves](#enclaves-and-exclaves)
  - [Physical geography](#physical-geography)
    - [Continents](#continents)
    - [Oceans](#oceans)
    - [Marginal seas](#marginal-seas)
    - [Straits](#straits)
    - [Channels and passages](#channels-and-passages)
    - [Other water bodies](#other-water-bodies)
- [**Content guidelines**](#content-guidelines)
  - [_Country_ field](#country-field)
  - [_Country info_ field](#country-info-field)
  - [_Capital_ field](#capital-field)
  - [_Capital info_ field](#capital-info-field)
  - [_Capital hint_ field](#capital-hint-field)
  - [_Flag_ field](#flag-field)
  - [_Flag similarity_ field](#flag-similarity-field)
  - [_Map_ field](#map-field)
  - [Writing style](#writing-style)
- [**Translation sources**](#translation-sources)
  - [Norwegian Bokmål](#norwegian-bokmål)
- [**Maintainer's guide**](#maintainers-guide)
  - [Versioning](#versioning)
  - [Release process](#release-process)


## Contributor's guide

Ready to start working on an issue? Here is what you need to know.

> If you're new to contributing on GitHub, [read this guide](https://guides.github.com/activities/contributing-to-open-source/) first.

The deck is managed with [Brain Brew][Brain Brew], a deck manager that allows transforming _Ultimate Geography_ back and forth between its CrowdAnki JSON representation and a format that is easy for humans to read, modify and version-control (currently CSV). This means that one can edit this deck either here, in this repository, or in Anki itself.

Brain Brew and its dependencies are managed with [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html). Running Brain Brew inside a virtual environment guarantees that is not hampered by individual setups.

The content of the deck is stored in multiple CSV files under `src/data`. The main file is `main.csv`. Each row corresponds to a note and each column to a field.

Translated fields, such as _Country_ or _Capital info_, have their own CSV files called _derivatives_, in which each column corresponds to one language. The _Country_ field is used to map rows in the derivatives with notes in `main.csv`. The mapping is not necessarily one to one: if a note has no capital (e.g. because it's a water body), then it must not appear in `capital.csv`.

### Getting started

1. Fork and clone this repository on your machine.
1. [Install Python 3.7](https://www.python.org/downloads/release/python-379/)
  - During the installation, make sure to install `pip` (it's optional) and to tick _Add Python 3.7 to PATH_.
1. Install Pipenv with `pip install pipenv`.
  - If the `pip` executable is not available, try `pip3 install pipenv` instead.
1. In the root directory of your fork, run `pipenv install` to install Brain Brew and its dependencies in a new virtual environment.
1. You can now run this deck's Brain Brew recipes with `pipenv run brain_brew recipes/<filename>.yaml`.
  - Alternatively, run `pipenv run build` to build the deck for Anki with the `source_to_anki.yaml` recipe.

### Brain Brew recipes

#### Source to Anki

```bash
pipenv run brain_brew recipes/source_to_anki.yaml
```

This recipe builds the deck from source in a format that can be imported into Anki with the CrowdAnki add-on. More precisely, it generates every possible version of the deck (i.e. standard + extended, in every language) into sub-folders inside the `build` folder. Each of these sub-folders includes a CrowndAnki JSON file and all of the deck's images.

On first run, this recipe generates all the missing files and folders in the `build` folder, logging warnings in the output. Upon subsequent runs, the warnings disappear.

#### Anki to Source

```bash
pipenv run brain_brew recipes/anki_to_source.yaml
```

This recipe allows editing the English standard or extended deck in Anki, and then pulling the changes into the CSVs. Other languages are currently not supported. It also does not support editing the note model, card templates, deck description, etc. -- only the content of the notes.

1. Make your edits in Anki.
1. Export the deck with CrowdAnki into the `build/Ultimate Geography [EN]` folder (even if you've edited the extended deck).
1. Run `pipenv run brain_brew recipes/anki_to_source.yaml`.
1. Any new media will be placed at the top level of the `src/media` folder and will need to be moved into the appropriate sub-folder.

### How-to's

- To **add a new note** to the deck, add one row to `main.csv`, `guid.csv`, and any of the derivative CSVs as needed. Don't fill in any of the GUIDs in `guid.csv` -- they will be generated automatically by the `source_to_anki.yaml` recipe.
- To **change the _Country_ field** of a note, change it in `main.csv`, `guid.csv`, `country.csv`, and any other derivative CSV in which the note appears.
- To **add a new translation**, add a new column to each of the CSV files and name them as follows: `[field name]:[language code]` (e.g. `country info:fr`, all lowercase). In most cases, the language code should match the Wikipedia subdomain for that language (e.g. https://fr.wikipedia.org/).

When editing `guid.csv` please try to avoid using a spreadsheet, if possible, and instead use a text editor (e.g. notepad) since spreadsheets mangle some of the GUIDs that start with `=` signs.

> Adding new fields (e.g. population, currency, etc.), the most heavily requested change to the deck, will soon™ be solved using [Brain Brew][Brain Brew], by combining separate repositories. Stay tuned.

## Content inclusion rules

In order for a geographical entity to be included in the deck, it must:

- belong to a well-defined, well-sourced list of entities of a common type (e.g. sovereign states, seas, etc.);
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

Apart from continents and oceans, inclusion rules for physical entities are documented and put into use in [physical-entities.xlsx](physical-entities.xlsx). They were discussed in [#137][ref137] and [#346][ref346].

A physical entity can only be included partially, with only a map.

#### Continents

- Source: https://en.wikipedia.org/wiki/Continent#Number
- Specifically the seven-continent model but with the continent of _Australia_ replaced with the world region of _Oceania_, as discussed in [#345][ref345].

#### Oceans

- Source: https://en.wikipedia.org/wiki/Ocean#Oceanic_divisions

#### Marginal seas

- Sources:
  - [IHO, _Limits of Oceans and Seas_, 4th Edition (Final Draft), 2002](http://wiki.geosys.ru/lib/exe/fetch.php/ru/portal/lib/iho/s23.los.ed4draft.2002.pdf)
  - [IHO, _Limits of Oceans and Seas_, 3rd Edition, 1953](https://epic.awi.de/id/eprint/29772/1/IHO1953a.pdf) (adds _Sea of Japan_)
- Specifically all water bodies defined in the above publications, with the exception of oceans, basins, straits, channels, passages, and the _South China and Eastern Archipelagic Seas_.
- Criteria for inclusion:
  - for water bodies defined in 1953: `area >= 125,000 km2`
  - for water bodies added in 2002: `area >= 500,000 km2`
- Area calculations are based on the IHO's 2002 definitions.

#### Straits

- Sources:
  - [IHO, _Limits of Oceans and Seas_, 4th Edition (Final Draft), 2002](http://wiki.geosys.ru/lib/exe/fetch.php/ru/portal/lib/iho/s23.los.ed4draft.2002.pdf)
  - [Transit passage](https://en.wikipedia.org/wiki/Transit_passage) (adds _Bab-el-Mandeb_ and _Strait of Magellan_).
- Straits mentioned on the _Transit passage_ article as being governed by an international convention are included.
- Groups of straits and their constituents are excluded, namely the _Danish straits_ and _Turkish Straits_.
- Criteria for inclusion: `is transit passage OR (borders >= 2 states AND area <= 50,000 km2)`
- Area calculations are based on the IHO's 2002 definitions.

#### Channels and passages

- Source: [IHO, _Limits of Oceans and Seas_, 4th Edition (Final Draft), 2002](http://wiki.geosys.ru/lib/exe/fetch.php/ru/portal/lib/iho/s23.los.ed4draft.2002.pdf)
- Criterion for inclusion: `borders >= 2 states`

#### Other water bodies

The deck currently includes a number of lakes for which inclusion rules have not yet been officialised. Other kinds of water bodies may also be included in the future (e.g. rivers).

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

We use the capital(s) given in the [infobox](https://en.wikipedia.org/wiki/Template:Infobox_country#Examples) of the country's English Wikipedia article. This ensures consistency across languages and simplifies maintainance, as discussed in issue [#416#issuecomment-821864712][ref416].

For spelling, unless otherwise stated in the [_Translation sources_](#translation-sources) section below, we take **the title of the Wikipedia article** for the capital, in the language of the given deck. Alternative names may be mentioned in the _Capital info_ field, when relevant.

If the title of the Wikipedia article contains a parenthetical portion for disambiguation purposes, it must be removed. The _Capital hint_ field is used instead for disambiguation.

If multiple capitals are listed in a country's infobox, the following guidelines apply:

- If the first capital is followed by a qualifier such as "official", "constitutional", "de jure", "claimed", or "political", it must be used alone in the _Capital_ field. The _Capital info_ field must then be used to detail the status and/or role of every capital - e.g. _While Dodoma is the official capital, Dar es Salaam is the de facto seat of government._
- If government branches such as "executive" or "legislative" are the only qualifiers used, then the capitals must all be listed in the _Capital_ field, separated by commas - e.g. _Pretoria, Cape Town, Bloemfontein_ (South Africa). The _Capital info_ field must again be used to detail the role of every capital.
- If no qualifiers are provided at all, then the capitals must all be listed in the _Capital_ field, separated by commas. A concise explanation should then be provided in the _Capital info_ field.

### _Capital info_ field

As explained in the previous section, this field is typically used for countries with multiple capitals, to clarify the role and/or status of each capital, or to explain succinctly why the country has multiple capitals. In such case, the content of the field should be consistent across languages.

This field may also be used to provide alternative capital names and spellings, which may be language-specific.

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
  - subtly different colours - i.e. [ΔE](https://github.com/anki-geo/ultimate-geography/issues/50#issuecomment-525902404) < 30
  - subtly different geometry

Two flags are then eligible for _Flag similarity_ information when they respect the two rules below:

- Their differences all fit in the above classification. For instance, France and Italy are not eligible because their left bands are respectively blue and green, and "different colours in same position" does not appear in the classification.
- Their classified differences form one the following combinations:
  - `1C 0M 0m {0+}n` = one critical difference and any number of negligible differences
  - `0C 1M {0–2}m {0+}n` = one major difference, up to two minor differences, and any number of negligible differences
  - `0C 0M {0–3}m {0+}n` = up to three minor differences and any number of negligible differences

> The [_Flag similarities_ wiki page](https://github.com/anki-geo/ultimate-geography/wiki/Flag-similarities) lists the pairs of countries that have already been audited for flag similarities.

Critical, major, and minor differences should be listed in the _Flag similarity_ field. Negligible differences should be listed only when relevant, notably when two flags share nothing but negligible differences.

### _Map_ field

This field must contain a single HTML image element pointing to the PNG image of a map - e.g. `<img src="ug-map-seychelles.png" />`. The image must be placed in the ` media` folder and named `ug-map-<country_name>.png`. PNG is the preferred format.

The source SVG maps come, or are inspired, from the [SVG locator maps](https://commons.wikimedia.org/wiki/Category:SVG_locator_maps_of_countries_(16:9_regional_location_map_scheme)) project on Wikimedia. The maps' source URLs and licences must be documented in `sources.csv`.

The following guidelines apply to map images:

- The maps must be sourced or created as SVG, exported to PNG, and then optimised with a tool like [PNGGauntlet](https://pnggauntlet.com/).
- They should have a width of 500 px and a height of approximately 281 px.
- The style (colours, strokes, etc.) should match that of existing maps in the deck (note that water bodies use a different style than countries).
- For small islands or archipelagos, the map should include a zoom box to facilitate identification.

### Writing style

As mentioned above, we strive to keep the descriptive fields (_Capital info_, _Capital hint_, _Country info_, _Flag similarity_) as concise as possible. For instance, where the subject of the description is the same as the subject of the card, we use a truncated phrase instead of a full sentence — e.g. "Also known as Kiev.", rather than "Kyiv is also known as Kiev.".

By convention and for consistency, we use a full stop at the end of the _Capital info_ and _Country info_ fields and no full stop for the _Capital hint_ and _Flag similarity_ fields, in all languages, unless there are strong typographic or grammatical reasons against this in the given language. (No such language is currently in the deck.) The justification for this convention is described in [#383][ref383].

## Translation sources

When Wikipedia in a given language is not sufficently exhaustive to support the translation of this deck, additional sources may be used. This section references such sources, as well as any stylistic choices made by translators.

### Norwegian Bokmål

Norwegian Bokmål (nb-NO) is the preferred written-language standard of roughly 90% of Norway's population, with the remaining 10% preferring Norwegian Nynorsk (nn-NO). With regard to style and grammar, we have chosen a conservative style (riksmål), preferring feminine-gendered nouns only in the case of bays and islands ("-bukta" and "-øya", e.g. Biscayabukta instead of Biscayabukten).

The Norwegian Bokmål translation is based on the following sources (in addition to the English deck), listed in order of priority:

- **[_Store norske leksikon (The Large Norwegian Encyclopedia)_](https://snl.no/)** - Open to audience contributions, edited by professionals. The editors are usually academics. In the original translator's opinion a good trade-off between being quickly updated and being correct.
- **[_Country names, capitals and national holidays_](https://www.regjeringen.no/no/dokumenter/statsnavn-hovedsteder-og-nasjonaldager/id87863/)** - This brochure from the Norwegian Ministry of Foreign Affairs is the most authoritative source for country names in Norwegian, as it is used by Norwegian diplomats. There are a few weaknesses:
  - The brochure is not updated often, possibly due to a lack of attention or diplomatic reasons for lagging behind _de facto_ changes.
  - Only includes sovereign countries.
- **[Wikipedia in Norwegian (Bokmål)](https://no.wikipedia.org/wiki/Portal:Forside)** - Used when neither of the above sources were enough to verify spelling.

### Portuguese

Portuguese is used in several countries around the world, with some significant differences between the dialects from different countries.  The two principal sets of dialects are European Portuguese (pt-PT) and Brazilian Portuguese (pt-BR).  We have decided to use Brazilian Portuguese in the _Capital hint_, _Capital info_, _Country info_ and _Flag similarity_ fields.

In cases where the Wikipedia article about the given country or city provides two spellings, describing them as the Brazilian Portuguese and European Portuguese versions (e.g. `Romênia (português brasileiro) ou Roménia (português europeu)`), we provide both in the given _Country_ or _City_ field, with (BR) and (PT) in parentheses to indicate the dialects (e.g. `"Romênia (BR), Roménia (PT)"`).  This explicitly overrides the recommendation in the [_Country_ field content guidelines](#country-field) regarding using the title of the Wikipedia article.

As suggested above, the country or city names used in the other fields should be the Brazilian spellings.

## Maintainer's guide

### Versioning

The releases follow a versioning scheme of the form `x.y`, where:

- `x` increases in the case of a **major, breaking release** (e.g. v3.0),
- `y` increases in the case of a **minor, non-breaking release** (e.g. v2.6).

Content changes, such as adding a note, replacing an image, or translating the deck into a new language, all constitute minor changes. A change is considered major when users are likely to **lose a significant part of their progress** when upgrading the deck with CrowdAnki.

### Release process

1. Open a discussion thread named _Prepare for v[x.y]_ a few weeks ahead of the release to coordinate any remaining work.
1. When ready to release, bump the version number in `src/headers/desc.html`.
1. Run `pipenv run build`.
1. In Anki, synchronise all your devices then upgrade the standard English deck by following the recommended procedure, which was agreed upon in the discussion thread. Synchronise all your devices again once the upgrade is complete.
1. With the help of the Anki card browser, update the notes/cards stats in both `desc.html` and `README.md`, and commit the changes (including the version bump).
1. Run `pipenv run build` again.
1. Re-import the standard English deck in Anki and synchronise with AnkiWeb.
1. Add each folder in the `build` directory to a separate ZIP archive named as follows:
  - `Ultimate Geography [EN]` ==> `Ultimate_Geography_v[x.y]_EN.zip`.
  - `Ultimate Geography [EN] [Extended]` ==> `Ultimate_Geography_v[x.y]_EN_EXTENDED.zip`.
1. On GitHub, create a new **release** named after the version number.
1. Draft the release notes, making sure to add a link to the upgrade steps in the `README` and/or [in the wiki](https://github.com/anki-geo/ultimate-geography/wiki/Upgrade-instructions).
1. Attach all the ZIP files and save the draft release notes.
1. Post a link to the draft release notes on the _Prepare for v[x.y]_ dicussion thread and wait for feedback.
1. Once maintainers have reviewed the release notes and the upgrade process, open the draft release notes, and publish the release.
1. Open a discussion thread to announce the release, with links to the release notes and upgrade instructions.
1. Close the milestone and create a new one for the next minor version.
1. Go to [AnkiWeb](https://ankiweb.net/decks/).
1. Find the _Ultimate Geography_ deck and select _Actions_ > _Share_
1. Update the version number in the title and, if needed, update the description with the content of `desc.html`.
1. Tick the _Copyright_ box and click _Share_.
1. Announce the release [on Reddit](https://www.reddit.com/r/Anki/search?q=ultimate%20geography&restrict_sr=1), with links to the release notes, to the upgrade instructions, and to the _Discussions_ and _Issues_ pages.

[ref129]: https://github.com/anki-geo/ultimate-geography/issues/129
[ref137]: https://github.com/anki-geo/ultimate-geography/issues/137
[ref157]: https://github.com/anki-geo/ultimate-geography/pull/157#issuecomment-549143860
[ref181]: https://github.com/anki-geo/ultimate-geography/issues/181
[ref212]: https://github.com/anki-geo/ultimate-geography/issues/212
[ref221]: https://github.com/anki-geo/ultimate-geography/issues/221
[ref247]: https://github.com/anki-geo/ultimate-geography/pull/247
[ref306]: https://github.com/anki-geo/ultimate-geography/pull/306
[ref312]: https://github.com/anki-geo/ultimate-geography/pull/312
[ref345]: https://github.com/anki-geo/ultimate-geography/pull/345
[ref346]: https://github.com/anki-geo/ultimate-geography/pull/346
[ref361]: https://github.com/anki-geo/ultimate-geography/pull/361
[ref383]: https://github.com/anki-geo/ultimate-geography/issues/383
[ref416]: https://github.com/anki-geo/ultimate-geography/issues/416#issuecomment-821864712
[Brain Brew]: https://github.com/ohare93/brain-brew

# Contributing

:wave: Hello there! :tada: Thanks for taking the time to contribute!

Seen something outdated or plain wrong? Spotted a typo somewhere? Think something could be better translated, or want to translate the whole deck into a new language? Please [open an issue](https://github.com/anki-geo/ultimate-geography/issues) before doing large edits so maintainers can help coordinate the work.

## Contributor's guide

Ultimate Geography is still maintained with [Brain Brew](https://github.com/jeprecated/brain-brew), now using the new Rust-based Brain Brew federation workflow instead of the legacy Python recipe pipeline.

The source of truth is:

- `deck.yaml` — the English standard Canonical Deck.
- `overlays/languages/*.yaml` — translation overlays.
- `overlays/variants/extended*.yaml` and `overlays/variants/experimental*.yaml` — extended and experimental variant overlays.
- `brainbrew.yaml` — the manifest defining all standard, extended, experimental, and Hardcore targets.
- `media/` — the flat media root used by CrowdAnki exports.

### Getting started

You need Nix to run the Rust-based Brain Brew CLI from its flake.

List the available targets:

```bash
nix run github:jeprecated/brain-brew/rust-brainbrew -- targets --manifest brainbrew.yaml
```

Verify the whole workspace, including media references:

```bash
nix run github:jeprecated/brain-brew/rust-brainbrew -- verify --manifest brainbrew.yaml --all-targets --media-root media
```

Export one target with media:

```bash
rm -rf build/crowdanki/en-standard
nix run github:jeprecated/brain-brew/rust-brainbrew -- export crowdanki \
  --manifest brainbrew.yaml \
  --target en-standard \
  --out build/crowdanki/en-standard
mkdir -p build/crowdanki/en-standard/media
cp media/* build/crowdanki/en-standard/media/
```

Export every configured target for a release or CI smoke test:

```bash
nix run github:jeprecated/brain-brew/rust-brainbrew -- targets --manifest brainbrew.yaml | while read -r target; do
  out="build/crowdanki/$target"
  nix run github:jeprecated/brain-brew/rust-brainbrew -- export crowdanki \
    --manifest brainbrew.yaml \
    --target "$target" \
    --out "$out"
  mkdir -p "$out/media"
  cp media/* "$out/media/"
done
```

The full `verify` command above validates that every referenced media file exists in the source `media/` root.

Compose one target to inspect the resolved Canonical Deck YAML:

```bash
nix run github:jeprecated/brain-brew/rust-brainbrew -- compose \
  --manifest brainbrew.yaml \
  --target de-extended \
  --out /tmp/de-extended.yaml
```

### Common edits

- **Edit English content:** update the relevant note in `deck.yaml`.
- **Edit a translation:** update the language overlay under `overlays/languages/`.
- **Edit extended or experimental templates:** update the shared overlay in `overlays/variants/extended.yaml` or `overlays/variants/experimental.yaml`; language-specific files under those directories should stay limited to adapter identity or true language exceptions.
- **Edit Hardcore Geography fills:** put language-neutral/default blank-field fills in `overlays/extensions/hardcore/field-fills.yaml`; use `overlays/extensions/hardcore/field-fills/<lang>.yaml` only for localized overrides that differ from the default.
- **Replace or add media:** put the file directly in `media/`, reference the same filename from the note field HTML, and keep `sources.csv` up to date.

After any edit, run the full `verify` command above. If you change generated deck output intentionally, inspect an exported target before opening a pull request.

## Content inclusion rules

In order for a geographical entity to be included in the deck, it must:

- belong to a well-defined, well-sourced list of entities of a common type (e.g. sovereign states, seas, etc.);
- meet the inclusion criteria that apply to entities of this type.

### Political geography

Inclusion rules for political entities are documented and put into use in [political-entities.xlsx](political-entities.xlsx). They were discussed in [#137][ref137], [#221][ref221], [#306][ref306], [#312][ref312] and [#361][ref361].

A political entity can be included either fully (map, capital, and flag) or partially (with only a map). In the rare case where a political entity belongs to more than one of the below categories, it will only be considered in the first category of which it's a member.

#### Sovereign states

- Source: https://en.wikipedia.org/wiki/List_of_sovereign_states
- All fully included, regardless of UN membership status or recognition by other states.

#### Dependent territories

- Sources:
  - https://en.wikipedia.org/wiki/Dependent_territory
  - https://en.wikipedia.org/wiki/Countries_of_the_United_Kingdom
- Specifically, inhabited dependent territories.
- Criteria for inclusion with map: `population >= 15,000 OR area >= 1,000 km2`
- Criteria for inclusion with map, capital, and flag: `(population >= 15,000 AND area >= 1,000 km2) OR population >= 100,000`

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
- alternative and former country names - e.g. _Also known as East Timor_ (Timor-Leste)
- in rare cases only, general knowledge information - see Melanesia for an example

The content of this field should be concise and consistent across notes. It may differ between languages, notably when dealing with alternative names.

### _Capital_ field

We use the capital(s) given in the [infobox](https://en.wikipedia.org/wiki/Template:Infobox_country#Examples) of the country's English Wikipedia article. This ensures consistency across languages and simplifies maintenance, as discussed in issue [#416#issuecomment-821864712][ref416].

For spelling, unless otherwise stated in the [_Translation sources_](#translation-sources) section below, we take **the title of the Wikipedia article** for the capital, in the language of the given deck. Alternative names may be mentioned in the _Capital info_ field, when relevant.

If the title of the Wikipedia article contains a parenthetical portion for disambiguation purposes, it must be removed. The _Capital hint_ field is used instead for disambiguation.

If multiple capitals are listed in a country's infobox, the following guidelines apply:

- If the first capital is followed by a qualifier such as "official", "constitutional", "de jure", "claimed", or "political", it must be used alone in the _Capital_ field. The _Capital info_ field must then be used to detail the status and/or role of every capital - e.g. _While Dodoma is the official capital, Dar es Salaam is the de facto seat of government._
- If government branches such as "executive" or "legislative" are the only qualifiers used, then the capitals must all be listed in the _Capital_ field, separated by commas - e.g. _Pretoria, Cape Town, Bloemfontein_ (South Africa). The _Capital info_ field must again be used to detail the role of every capital.
- If no qualifiers are provided at all, then the capitals must all be listed in the _Capital_ field, separated by commas. A concise explanation should then be provided in the _Capital info_ field.

### _Capital info_ field

As explained in the previous section, this field is typically used for countries with multiple capitals, to clarify the role and/or status of each capital, or to explain succinctly why the country has multiple capitals. In such case, the content of the field should be consistent across languages.

This field may also be used to provide alternative capital names and spellings, which may be language-specific.  Minor spelling differences should usually be ignored, unless the main spelling was explicitly changed, on Wikipedia (for instance Kiev to Kyiv or Sana'a to Sanaa). In these cases, the old spelling is included mainly to avoid confusion for previous users of the deck. See [#672][ref672] and [#381][ref381].

### _Capital hint_ field

This field is used in notes that share:

- the same exact capital - e.g. _London_ (United Kingdom and England);
- capitals with very similar names - e.g. _Georgetown_ and _George Town_.

The hints appear on _Capital - Country_ cards to avoid confusion or random guesses. They should
convey as little information as possible to not give away the answers.

### _Flag_ field

This field must contain a single HTML image element pointing to the SVG image of a flag - e.g. `<img src="ug-flag-seychelles.svg" />`. The image must be placed in the `media/` folder and named `ug-flag-<country_name>.svg`.

SVG flags are sourced from [Wikimedia](https://commons.wikimedia.org/). We consider two possible sources for the flag: (1) the flag presented in the [infobox](https://en.wikipedia.org/wiki/Template:Infobox_country#Examples) of the English Wikipedia article for the country and (2) the primary flag presented in the English Wikipedia article for the country's flag. When both sources agree, we use the common flag; when they differ, we default to the state flag. We try to stay a few months behind edits in an attempt to avoid quick back-and-forth changes; in case of repeated back-and-forth changes, investigate reasons for the edit war, make a decision, document the decision in this document; review these decisions from time to time.

Discussion of some edit wars (in particular, some for Costa Rica, Peru, and Venezuela) can be found [here](https://github.com/anki-geo/ultimate-geography/issues/111#issuecomment-1382229132).

The flag's source URL and licence must be documented in `sources.csv`.

The following guidelines apply to flag images:

- The `viewBox`, `width` and `height` attributes are required.  (If the `viewBox` is originally missing, its value should usually be `viewBox="0 0 {width} {height}`, where `width` and `height` are the original values of these attributes.)
- The height must be set to 250 px (`height="250"`) and the width adjusted proportionally, rounded to the nearest integer.
- Each flag must be optimised with [SVGO](https://jakearchibald.github.io/svgomg/).

If the name of a country appears clearly on a flag, a second version of that flag may also be provided, with the name of the country blurred out. The name should be blurred using [Inkscape](https://inkscape.org/)'s Gaussian blur effect as explained in [587#issuecomment-1357163000][ref587]. The blurred flag must be named `ug-flag-<country_name>-blur.svg` and placed in the `media/` folder. A second HTML element must then be added to the _Flag_ field _before_ the existing HTML element. This allows the blurred flag to appear on the front of the country's _Flag - Country_ card.

### _Flag similarity_ field

This field is used in the _Flag - Country_ template.

In Anki, when you keep on confusing two flags, you can't put them side by side to learn their visual differences. The _Flag similarity_ field works around this limitation by providing a concise description of the differences a flag has with another. It allows users to more easily learn to distinguish pairs of similar flags and perhaps come up with mnemonics to remember their respective countries.

A note's _Flag similarity_ field contains a list of countries, each followed by a list of differences. For instance, the flag similarities for Iceland are written as follows: _Norway (red background, blue cross), Faroe Islands (white background, red and blue cross)_. The list of differences must be **precise**, **clear**, and **concise**. Advanced [vexillological](https://en.wikipedia.org/wiki/Vexillology) terms should be avoided.

Flag similarities are always **mutual**: if flag A is similar to flag B, then flag B is similar to flag A. To determine whether two flags are similar enough to warrant mutual _Flag similarity_ information, their differences must first be **identified** and **classified**. The following classification applies:

- **Critical differences (C)**
  - presence/absence of decoration - e.g. symbol, coat of arms
- **Major differences (M)**
  - same colours in different positions (e.g. two swapped, three cyclically permuted ("rotated"))
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

This field must contain a single HTML image element pointing to the PNG image of a map - e.g. `<img src="ug-map-seychelles.png" />`. The image must be placed in the `media/` folder and named `ug-map-<country_name>.png`. PNG is the preferred format.

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

When Wikipedia in a given language is not sufficiently exhaustive to support the translation of this deck, additional sources may be used. This section references such sources, as well as any stylistic choices made by translators.

### Norwegian Bokmål

Norwegian Bokmål (nb-NO) is the preferred written-language standard of roughly 90% of Norway's population, with the remaining 10% preferring Norwegian Nynorsk (nn-NO). With regard to style and grammar, we have chosen a conservative style (riksmål), preferring feminine-gendered nouns only in the case of bays and islands ("-bukta" and "-øya", e.g. Biscayabukta instead of Biscayabukten).

The Norwegian Bokmål translation is based on the following sources (in addition to the English deck), listed in order of priority:

- **[_Store norske leksikon (The Large Norwegian Encyclopedia)_](https://snl.no/)** - Open to audience contributions, edited by professionals. The editors are usually academics. In the original translator's opinion a good trade-off between being quickly updated and being correct.
- **[_Country names, capitals, and national holidays_](https://www.regjeringen.no/no/dokumenter/statsnavn-hovedsteder-og-nasjonaldager/id87863/)** - This brochure from the Norwegian Ministry of Foreign Affairs is the most authoritative source for country names in Norwegian, as it is used by Norwegian diplomats. There are a few weaknesses:
  - The brochure is not updated often, possibly due to a lack of attention or diplomatic reasons for lagging behind _de facto_ changes.
  - Only includes sovereign countries.
- **[Wikipedia in Norwegian (Bokmål)](https://no.wikipedia.org/wiki/Portal:Forside)** - Used when neither of the above sources were enough to verify spelling.

### Portuguese

Portuguese is used in several countries around the world, with some significant differences between the dialects from different countries.  The two principal sets of dialects are European Portuguese (pt-PT) and Brazilian Portuguese (pt-BR).  We have decided to use Brazilian Portuguese in the _Capital hint_, _Capital info_, _Country info_ and _Flag similarity_ fields.

In cases where the Wikipedia article about the given country or city provides two spellings, describing them as the Brazilian Portuguese and European Portuguese versions (e.g. `Romênia (português brasileiro) ou Roménia (português europeu)`), we provide both in the given _Country_ or _City_ field, with (BR) and (PT) in parentheses to indicate the dialects (e.g. `"Romênia (BR), Roménia (PT)"`).  This explicitly overrides the recommendation in the [_Country_ field content guidelines](#country-field) regarding using the title of the Wikipedia article.

As suggested above, the country or city names used in the other fields should be the Brazilian spellings.

### Danish

The Danish translation is based on the following sources (in addition to the
English deck), listed in order of priority:

- **[Lande og nationaliteter](https://sproget.dk/raad-og-regler/ordlister/andre-ordlister/lande-og-nationaliteter)** - This list is maintained by the "Danske Sprognævn".
- **[Den Store Danske](https://denstoredanske.lex.dk/)** - Denmarks national encyclopedia.
- **[Wikipedia in Danish](https://da.wikipedia.org)** - Used when neither of the above sources where enough to verify spelling.

### Hebrew

The Hebrew translation follows the general rule of using Hebrew Wikipedia article titles for country, territory, capital, and geography names. When the established Hebrew title differs materially from the English source name, the alternative name may be noted in the relevant info field, such as `ים סוף` with `הים האדום`.

## Maintainer's guide

### Versioning

The releases follow a versioning scheme of the form `x.y`, where:

- `x` increases in the case of a **major, breaking release** (e.g. v3.0),
- `y` increases in the case of a **minor, non-breaking release** (e.g. v2.6).

Content changes, such as adding a note, replacing an image, or translating the deck into a new language, all constitute minor changes. A change is considered major when users are likely to **lose a significant part of their progress** when upgrading the deck with CrowdAnki.

### Release process

1. Open a discussion thread named _Prepare for v[x.y]_ to coordinate remaining work.
1. Update the version string and release-facing description in `deck.yaml` and `README.md`.
1. Run `nix run github:jeprecated/brain-brew/rust-brainbrew -- verify --manifest brainbrew.yaml --all-targets --media-root media`.
1. Export every release target with the target loop in the contributor guide above, keeping `--media-root media` so each CrowdAnki folder receives the required media files.
1. Smoke-test at least the English standard export in Anki via CrowdAnki import.
1. Zip each exported CrowdAnki folder using the existing release naming convention, for example `Ultimate_Geography_v[x.y]_EN.zip` and `Ultimate_Geography_v[x.y]_EN_EXTENDED.zip`.
1. Draft a GitHub release, attach the ZIP files, and share the draft for maintainer review.
1. Publish the release, announce it, close the milestone, and create the next milestone.
1. Update the AnkiWeb shared deck entry if needed.

### Release notes

Release notes should be written for users rather than as a commit log. Include:

1. A short summary of the most significant changes.
1. Upgrade instructions, especially for major versions.
1. New translations, notes, removals, and significant factual corrections.
1. Changes to maps, flags, tags, note templates, or release packaging.
1. Contributors, especially first-time contributors and translators.

Be concise but specific: name affected countries/capitals, include language codes where relevant, and link to issues or pull requests.

[ref137]: https://github.com/anki-geo/ultimate-geography/issues/137
[ref157]: https://github.com/anki-geo/ultimate-geography/pull/157#issuecomment-549143860
[ref181]: https://github.com/anki-geo/ultimate-geography/issues/181
[ref212]: https://github.com/anki-geo/ultimate-geography/issues/212
[ref221]: https://github.com/anki-geo/ultimate-geography/issues/221
[ref306]: https://github.com/anki-geo/ultimate-geography/pull/306
[ref312]: https://github.com/anki-geo/ultimate-geography/pull/312
[ref345]: https://github.com/anki-geo/ultimate-geography/pull/345
[ref346]: https://github.com/anki-geo/ultimate-geography/pull/346
[ref361]: https://github.com/anki-geo/ultimate-geography/pull/361
[ref381]: https://github.com/anki-geo/ultimate-geography/issues/381
[ref383]: https://github.com/anki-geo/ultimate-geography/issues/383
[ref416]: https://github.com/anki-geo/ultimate-geography/issues/416#issuecomment-821864712
[ref587]: https://github.com/anki-geo/ultimate-geography/pull/587#issuecomment-1357163000
[ref672]: https://github.com/anki-geo/ultimate-geography/issues/672#issuecomment-2631222673


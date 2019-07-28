# Ultimate Geography

**Geography flashcard deck for [Anki](http://ankisrs.net/)** featuring:

- the world's **[206 sovereign states](https://en.wikipedia.org/wiki/List_of_sovereign_states)** (824 cards)
- **67 overseas territories** and dependent areas (227 cards)
- **39 oceans and seas** (39 cards, maps only)
- **7 continents** (7 cards, maps only)
- for a total of **319 unique notes**, **1096 cards**, **260 flags** and **317 maps**.

| Flag - Country | Map - Country |
| --- | --- |
| ![sample-3](https://cloud.githubusercontent.com/assets/2936402/21575808/3ac74916-cf6e-11e6-8857-1cd7aaa02b23.png) | ![sample-4](https://cloud.githubusercontent.com/assets/2936402/22322663/bd0552aa-e3f1-11e6-89d9-38b5a1048eff.png) |

| Country - Capital | Capital - Country |
| --- | --- |
| ![sample-1](https://cloud.githubusercontent.com/assets/2936402/21575807/3ac6ebec-cf6e-11e6-849a-19544d5dccf5.png) | ![sample-2](https://cloud.githubusercontent.com/assets/2936402/21575809/3ac77b7a-cf6e-11e6-8d72-76f4d3e21de8.png) |

The deck is available in **English** and **German**. An **extended version** is also available in both languages with the following additional note templates: _Country - Flag_ and _Country - Map_. Use Anki's [filtered deck feature](#custom-study) to study only a specific type of cards (e.g. map to country) or area of the world (e.g. Europe).

The flags and most of the maps are sourced from [Wikimedia Commons](https://commons.wikimedia.org/). They are provided as SVG or PNG and optimised for smaller file size. Some legacy JPEG maps from the original deck (cf. [Background](#background) section below) are still present, but are [marked for replacement](https://github.com/axelboc/anki-ultimate-geography/issues/1#issuecomment-275280721).

To help with memorisation and provide context while learning, most notes include **extra information**:
- similar flags - e.g. Iceland = _Norway (red background, blue cross)_
- governance information - e.g. Cayman Islands = _Overseas territory of the United Kingdom_
- alternative or former country names - e.g. East Timor = _Also known as Timer-Leste_
- additional capitals (executive or de facto only - e.g. Sucre, Bolivia = _While Sucre is the constitutional capital, La Paz is the seat of government._
- statehood information - e.g. Transnistria = _Independent state claimed by Moldova_.


## Getting started

First-time here? Welcome! If you're happy using the English version of the deck, here is how you can get started:

1. Go to the **[_Releases_ page](https://github.com/axelboc/anki-ultimate-geography/releases)** and find the latest release.
1. In the release's _Downloads_ section, find the Anki package `Ultimate_Geography_v[...]_EN.apkg` and download it.
1. Import it in Anki, synchronise your devices and you're good to go!

> You can also download the latest package from the [shared deck page]( https://ankiweb.net/shared/info/2109889812).

### Other languages and versions

The English deck is the only version available as an Anki package. If you'd like to use the German deck or the extended version of the deck in any language, first install the [CrowdAnki add-on](https://github.com/Stvad/CrowdAnki) then follow the steps below.

> Please note that importing an extended deck on top of a standard deck is not supported. You must either remove the standard deck first (by following the instructions in the [_Major version_](#major-version) section), or import the extended deck in a separate Anki profile.

1. Go to the [_Releases_ page](https://github.com/axelboc/anki-ultimate-geography/releases) and find the latest release.
1. In the release's _Downloads_ section, find the ZIP archive of the version you're interested in using (e.g. `Ultimate_Geography_v[...]_DE.zip` for the standard German deck) and download it.
1. Extract the content of the archive on your machine.
1. Open Anki and make sure your devices are all synchronised.
1. In the _File_ menu, select _CrowdAnki: Import from disk_.
1. Browse for and select the folder you extracted from the archive.
1. Perform the import.

### Stay in touch

Did you spot a mistake? Do you have a suggestion to improve the deck? Would you like to help translate it into another language? Let us know by **[opening a new issue](https://github.com/axelboc/anki-ultimate-geography/issues)**.

To stay informed of new releases, make sure to [watch this repository's releases](https://help.github.com/en/articles/watching-and-unwatching-releases-for-a-repository).


## Upgrading

If you're looking to upgrade to a newer version of the deck, this section is for you. The process differs depending on whether you're upgrading to a minor (e.g. v2.6) or a major (e.g. v3.0) version.

> For more information about versioning and the differences between minor and major, please refer to the [_Versioning_](CONTRIBUTING.md#versioning) section.

### Minor version

For a minor version upgrade (e.g. from 2.3 to 2.6), _do not_ import the APKG package in Anki as you may have done initially or you will lose your progress. Instead, proceed as described in the [_Other languages and versions_](#other-languages-and-versions) section, making sure to pick the correct archive (e.g. `Ultimate_Geography_v[...]_EN.zip` for the standard English deck).

### Major version

Upgrading to a major version (e.g. from 2.6 to 3.0) typically leads to a loss of progress. Therefore, unless the [release's page](https://github.com/axelboc/anki-ultimate-geography/releases) tells you otherwise, it is recommended to perform a clean import by following these steps:

1. Open Anki and make sure your devices are all synchronised.
1. Delete the `Ultimate Geography` deck.
1. In the _Tools_ menu, select _Manage Note Types_, then delete the `Ultimate Geography` note type.
1. In the _Tools_ menu, select _Check Database_.
1. Sync the changes with AnkiWeb and with all your devices.
1. You can now follow the steps of the [_Getting started_](#getting-started) section and install the major version with its APKG package.


## Background

This deck is built on top of an old [shared deck](https://ankiweb.net/shared/info/261823898) that is no longer maintained. Initially, the goal was to address the poor quality of the flag images. However, the scope of the work quickly increased to include putting the deck on GitHub, rethinking the tags and reviewing the whole content. For a full list of changes, check out the [initial release notes](https://github.com/axelboc/anki-ultimate-geography/releases/tag/v2.0).

> This deck was initially released as `v2.0` to distinguish it from its predecessor, which was commonly referred to as `v1.0` (cf. [_Versioning_](CONTRIBUTING.md#versioning) section.)


## Deck structure

> Please beware that changing the structure of the deck may **prevent you from upgrading it**.

The notes are based on a **note type** called _Ultimate Geography_, which defines **eight fields**: _Country_, _Country info_, _Capital_, _Capital info_, _Capital hint_, _Flag_, _Flag similarity_ and _Map_.

The cards are generated by Anki based on **four templates**: _Country - Capital_, _Capital - Country_, _Flag - Country_ and _Map - Country_. The extended version of the deck includes two additional templates: _Country - Flag_ and _Country - Map_.

The appearance of the cards is controlled solely with CSS; the content of the notes is free from HTML formatting.

Every note is tagged. The tags, which are listed below, are prefixed with `UG::` so they don't conflict with other decks. The prefix also allows the [Hierarchical Tags](https://ankiweb.net/shared/info/1089921461) add-on to collapse them into a single group in the Anki browser's sidebar.

- Type - `UG::Sovereign_State`, `UG::Oceans+Seas`, `UG::Continents`
- Continent - `UG::Africa`, `UG::America`, `UG::Asia`, `UG::Europe`, `UG::Oceania`
- Region - `UG::North+Central_America`, `UG::South_America`, `UG::Caribbean`, `UG::Middle_East`, `UG::Southeast_Asia`, `UG::European_Union`


## Custom study

Anki's [search feature](http://ankisrs.net/docs/manual.html#searching), coupled with the deck's comprehensive tag structure, allows for the creation of [filtered decks](https://apps.ankiweb.net/docs/manual.html#creating-manually) covering a wide range of learning goals and abilities. For instance, you can:

- use the `card` filter to focus your study on a specific note template - e.g. `card:"Flag - Country"`;
- use the `tag` filter to focus your study on a specific continent or region of the world - e.g. `tag:"UG::Africa"`;
- use `tag:"Sovereign_State"` to include only sovereign states and exclude many of the Caribbean and Pacific islands;
- use `-tag:"Oceans+Seas"` if you're not interested in learning oceans and seas;
- combine the filters above to create more targetted or more generic decks.

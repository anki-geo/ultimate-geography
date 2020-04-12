# Ultimate Geography

**Geography flashcard deck for [Anki](http://ankisrs.net/)** featuring:

- the world's **[206 sovereign states](https://en.wikipedia.org/wiki/List_of_sovereign_states)** (824 cards)
- **69 overseas territories** and dependent areas (235 cards)
- **39 oceans and seas** (39 cards, maps only)
- **7 continents** (7 cards, maps only)
- for a total of **321 unique notes**, **1105 cards**, **260 flags** and **321 maps**.

The deck is available in **English**, **German**, **Spanish**, **French** and **Norwegian Bokmål**.

---

#### Table of contents

- [**Features**](#features)
  - [Supplementary information](#supplementary-information)
  - [Custom study](#custom-study)
- [**Getting started**](#getting-started)
  - [Other languages and versions](#other-languages-and-versions)
- [**Upgrading**](#upgrading)
  - [Minor version](#minor-version)
  - [Major version](#major-version)
- [**Deck structure**](#deck-structure)

## Features

The standard version of the deck comes with four note templates: _Country - Capital_, _Capital - Country_, _Flag - Country_, and _Map - Country_. An [extended version](#other-languages-and-versions) is also available, with two additional note templates: _Country - Flag_ and _Country - Map_.

<table>
  <tr><th scope="col" colspan="2">Flag - Country</th></tr>
  <tr><th scope="col">Front</th><th scope="col">Back</th></tr>
  <tr>
    <td><img src="doc/Flag - Country -- Front -- Christmas island.png"></td>
    <td><img src="doc/Flag - Country -- Back -- Christmas island.png"></td>
  </tr>
</table>

<table>
  <tr><th scope="col" colspan="2">Map - Country</th></tr>
  <tr><th scope="col">Front</th><th scope="col">Back</th></tr>
  <tr>
    <td><img src="doc/Map - Country -- Front -- Mexico.png"></td>
    <td><img src="doc/Map - Country -- Back -- Mexico.png"></td>
  </tr>
</table>

<table>
  <tr><th scope="col" colspan="2">Country - Capital</th></tr>
  <tr><th scope="col">Front</th><th scope="col">Back</th></tr>
  <tr>
    <td><img src="doc/Country - Capital -- Front -- Sri Lanka.png"></td>
    <td><img src="doc/Country - Capital -- Back -- Sri Lanka.png"></td>
  </tr>
</table>

<table>
  <tr><th scope="col" colspan="2">Capital - Country</th></tr>
  <tr><th scope="col">Front</th><th scope="col">Back</th></tr>
  <tr>
    <td><img src="doc/Capital - Country -- Front -- Finland.png"></td>
    <td><img src="doc/Capital - Country -- Back -- Finland.png"></td>
  </tr>
</table>

### Supplementary information

To help with memorisation and provide context while learning, most notes include extra information:

- **similar flags** - e.g. Iceland = _Norway (red background, blue cross)_
- **governance information** - e.g. Cayman Islands = _Overseas territory of the United Kingdom_
- **alternative and former country names** - e.g. East Timor = _Also known as Timor-Leste_
- **additional capitals** - e.g. Sucre, Bolivia = _While Sucre is the constitutional capital, La Paz is the seat of government._
- **statehood information** - e.g. Transnistria = _Independent state claimed by Moldova_.

### Custom study

Anki's [search feature](https://apps.ankiweb.net/docs/manual.html#searching), coupled with the deck's comprehensive [tag structure](#deck-structure), allows for the creation of [filtered decks](https://apps.ankiweb.net/docs/manual.html#creating-manually) covering a wide range of learning goals and abilities. Here are some search queries you can use:

- `card:"Flag - Country"` to learn flags and nothing else;
- `tag:UG::Sovereign_State` to focus on soverign states and exclude dependent territories, water bodies and continents;
- `-tag:"UG::Oceans+Seas"` (with "`-`" in front of the filter) to learn everything except oceans, seas and other water bodies;
- `card:"Map - Country" tag:UG::Sovereign_State tag:UG::Europe` to learn the location of Europe's sovereign states;
- `(card:"Country - Capital" or card:"Capital - Country") tag:UG::Sovereign_State` to learn the capitals of the world's sovereign states.


## Getting started

First-time here? Welcome! If you're happy using the standard, English version of the deck, here is how to get started:

1. Go to the **[_Releases_ page](https://github.com/axelboc/anki-ultimate-geography/releases)** and find the latest release.
1. In the _Downloads_ section, find the Anki package `Ultimate_Geography_v[...]_EN.apkg` and download it.
1. Import it in Anki, synchronise your devices and you're good to go!
1. To stay informed of new releases, make sure to [watch this repository's releases](https://help.github.com/en/articles/watching-and-unwatching-releases-for-a-repository).

> You can also download the latest Anki package from the [shared deck page]( https://ankiweb.net/shared/info/2109889812).

### Other languages and versions

The standard English deck is the only version available as an Anki package. If you'd like to use the standard deck in another language, or the extended deck in any language, first install the [CrowdAnki add-on](https://github.com/Stvad/CrowdAnki) then follow the steps below.

> Please note that importing an extended deck on top of a standard deck is not recommended. You should either remove the standard deck first (by following the instructions in the [_Major version_](#major-version) section), or import the extended deck in a separate Anki profile.

1. Go to the [_Releases_ page](https://github.com/axelboc/anki-ultimate-geography/releases) and find the latest release.
1. In the release's _Downloads_ section, find the ZIP archive of the version you're interested in using (e.g. `Ultimate_Geography_v[...]_DE.zip` for the standard German deck) and download it.
1. Extract the content of the archive on your machine.
1. Open Anki and make sure your devices are all synchronised.
1. In the _File_ menu, select _CrowdAnki: Import from disk_.
1. Browse for and select the folder you extracted from the archive.
1. Perform the import.


## Upgrading

If you're looking to upgrade to a newer version of the deck, this section is for you. The process differs depending on whether you're upgrading to a minor (e.g. v2.6) or a major (e.g. v3.0) version.

> For more information about versioning and the differences between minor and major, please refer to the [_Versioning_](CONTRIBUTING.md#versioning) section.

### Minor version

For a minor version upgrade (e.g. from 2.3 to 2.6), _do not_ import the APKG package in Anki as you may have done initially or you will lose your progress. Instead, proceed as described in the [_Other languages and versions_](#other-languages-and-versions) section, making sure to pick the correct archive (e.g. `Ultimate_Geography_v[...]_EN.zip` for the standard English deck).

> If you've moved some of the cards out of the default _Ultimate Geography_ deck and into antoher deck, by default CrowdAnki will move those cards back on import. This behaviour [can be disabled](https://github.com/Stvad/CrowdAnki#configuration-settings).

### Major version

Upgrading to a major version (e.g. from 2.6 to 3.0) typically leads to a loss of progress. Therefore, unless the [release's page](https://github.com/axelboc/anki-ultimate-geography/releases) tells you otherwise, it is recommended to perform a clean import by following these steps:

1. Open Anki and make sure your devices are all synchronised.
1. Delete the `Ultimate Geography` deck.
1. In the _Tools_ menu, select _Manage Note Types_, then delete the `Ultimate Geography` note type.
1. In the _Tools_ menu, select _Check Database_.
1. Sync the changes with AnkiWeb and with all your devices.
1. You can now follow the steps of the [_Getting started_](#getting-started) section and install the major version with its APKG package.

## Deck structure

> Beware that changing the structure of the deck may **prevent you from upgrading it** without loss of progress.

The notes are based on a **note type** called _Ultimate Geography_, which defines **eight fields**: _Country_, _Country info_, _Capital_, _Capital info_, _Capital hint_, _Flag_, _Flag similarity_ and _Map_.

The cards are generated by Anki on import based on **four templates**: _Country - Capital_, _Capital - Country_, _Flag - Country_ and _Map - Country_. The extended version of the deck includes two additional templates: _Country - Flag_ and _Country - Map_.

The appearance of the cards is controlled solely with CSS; the content of the notes is free from HTML markup.

Every note is tagged. The tags, which are listed below by category, are prefixed with `UG::` so they don't conflict with other decks. They can be used to create [filtered decks](https://apps.ankiweb.net/docs/manual.html#creating-manually) for [custom study](#custom-study).

- Type - `UG::Sovereign_State`, `UG::Oceans+Seas`, `UG::Continents`
- Continent - `UG::Africa`, `UG::America`, `UG::Asia`, `UG::Europe`, `UG::Oceania`
- Region - `UG::North+Central_America`, `UG::South_America`, `UG::Caribbean`, `UG::Middle_East`, `UG::Southeast_Asia`, `UG::European_Union`, `UG::Mediterranean`

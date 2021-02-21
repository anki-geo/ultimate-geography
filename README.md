# Ultimate Geography

**Geography flashcard deck for [Anki](http://ankisrs.net/)** featuring:

- the world's **[206 sovereign states](https://en.wikipedia.org/wiki/List_of_sovereign_states)** (824 cards)
- **59 territories, world regions, and other entities** (105 cards)
- **39 oceans and seas** (39 cards, maps only)
- **7 continents** (7 cards, maps only)
- for a total of **311 unique notes**, **975 cards**, **222 flags** and **311 maps**.

The deck is available in **English**, **German**, **Spanish**, **French**, **Norwegian Bokmål**, **Czech**, **Russian**, **Dutch** and **Swedish**.

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

The standard version of the deck comes with four note templates: _Country - Capital_, _Capital - Country_, _Flag - Country_, and _Map - Country_. An **extended version** is also available, with two additional note templates: _Country - Flag_ and _Country - Map_.

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

Anki's [search feature](https://docs.ankiweb.net/#/searching), coupled with the deck's comprehensive [tag structure](#deck-structure), allows for the creation of [filtered decks](https://docs.ankiweb.net/#/filtered-decks?id=creating-manually) covering a wide range of learning goals and abilities. Here are some search queries you can use:

- `card:"Flag - Country"` to learn flags and nothing else;
- `tag:UG::Sovereign_State` to focus on sovereign states and exclude dependent territories, water bodies and continents;
- `-tag:"UG::Oceans+Seas"` (with "`-`" in front of the filter) to learn everything except oceans, seas and other water bodies;
- `card:"Map - Country" tag:UG::Sovereign_State tag:UG::Europe` to learn the location of Europe's sovereign states;
- `(card:"Country - Capital" or card:"Capital - Country") tag:UG::Sovereign_State` to learn the capitals of the world's sovereign states;
- `tag:UG::North_America -tag:UG::Caribbean` to focus on the countries in North America, but not in the Caribbean (i.e. those in Northern and Central America).

## Getting started

First-time here? Welcome! 👋

In order to install and later upgrade _Ultimate Geography_ you'll need to first install an Anki add-on called [CrowdAnki](https://github.com/Stvad/CrowdAnki):

1. Open Anki on your computer, go to the _Tools_ menu and select _Add-ons_.
1. In the dialog box, click on _Get Add-ons..._ and paste in the code provided on [this page](https://ankiweb.net/shared/info/1788670778).
1. Click on _OK_ to download the add-on, and then restart Anki.

You're now ready to install _Ultimate Geography_:

1. Go to the **[_Releases_ page](https://github.com/axelboc/anki-ultimate-geography/releases)**.
1. In the latest release's _Downloads_ section, download the ZIP archive of the version of the deck you'd like to use. You can choose between [a standard and an extended version](#features) in [a number of languages](#ultimate-geography) -- for instance, if you're after the standard German deck, download `Ultimate_Geography_v[...]_DE.zip`.
1. Extract the content of the archive on your computer.
1. Open Anki and make sure your devices are all synchronised.
1. In the _File_ menu, select _CrowdAnki: Import from disk_.
1. Browse for and select the folder you extracted from the archive, which should contain the deck's JSON file and `media` folder -- e.g. `Ultimate Geography [DE]`.
1. Don't change anything in the _CrowdAnki Import Settings_ dialog box that opens -- just press _OK_ to perform the import. A dialog box should then confirm that the import was successful.

To stay informed of new releases, make sure to [watch this repository's releases](https://help.github.com/en/articles/watching-and-unwatching-releases-for-a-repository).

## Upgrading

The upgrade process is typically the same as the installation process explained in the [previous section](#getting-started). However, some situations require extra care. As a general rule, **always read the release notes carefully**; they will likely tell you what to do or point you to a page that does.

### First upgrade after APKG import

You may have initially installed _Ultimate Geography_ by importing an **APKG file**. You may have downloaded such a file from this repo or from the [deck's page](https://ankiweb.net/shared/info/2109889812) on AnkiWeb, as this used to be the recommended installation process.

If you're in this situation and wish to upgrade, proceed as follows:

1. Perform the _Getting started_ steps exactly.
1. You should end up with two decks: your original deck called "Ultimate Geography" and a new, duplicated deck called "Ultimate Geography_2". Unless you created some notes of your own, every card in your original deck should have moved automatically to the new deck and your original deck should now be empty. You can verify this in Anki's [card browser](https://docs.ankiweb.net/#/browsing?id=browsing).
1. To get back to having a single deck, move any remaining cards out of the original deck and delete it. Then, rename the new deck to "Ultimate Geography". From here on, future upgrades will be seamless.

### Cards moved into other deck

If you've moved some of the cards out of the default _Ultimate Geography_ deck and into another deck, by default CrowdAnki will move those cards back on import.

To prevent this behaviour and update the existing cards in place, follow the steps in the [_Getting started_](@getting-started) section but in the last step, make sure to tick the _Do Not Move Existing Cards_ checkbox in the _CrowdAnki Import Settings_ dialog box.

### Standard to extended

Importing an extended deck on top of a standard deck may bring unexpected results. You should consider learning the extended deck from scratch. To do so, either:

- remove the standard deck first by following the instructions in the [_Major version_](#major-version) section below, or
- import the extended deck in a separate Anki profile.

If you'd rather keep your progress, proceed as follows:

1. Perform the _Getting started_ steps exactly or as per the [_Cards moved into other deck_](cards-moved-into-other-deck) scenario.
1. Instead of a dialog box confirming that the import was successful, you'll see another dialog box titled _Change Note Type_. In the _Cards_ section, set _Change Flag - Country to:_ to "Flag - Country" (instead of "Country - Flag"), and set _Change Map - Country to:_ to "Map - Country" (instead of "Flag - Country").
1. Check that the other cards and fields map correctly and click on _OK_.

### Major version

Major versions (e.g. `v3.0`) typically indicate that upgrading may lead to a loss of progress. This occurs, for instance, when cards are removed or when changes are made to the structure of the deck.

> For more information about versioning and the differences between minor and major, please refer to the [_Versioning_](CONTRIBUTING.md#versioning) section of the _CONTRIBUTING_ guide.

As for any release, the release notes of a major version will tell you how to upgrade, or point you to a page that does. In some cases, there may even be a way to keep your progress! However, this is rarely straightforward. If you don't mind losing your progress, the simplest way to upgrade to a major version is to perform a "clean import":

1. Open Anki and make sure your devices are all synchronised.
1. Delete the `Ultimate Geography` deck.
1. In the _Tools_ menu, select _Manage Note Types_, then delete the `Ultimate Geography` note type.
1. In the _Tools_ menu, select _Check Database_.
1. Sync the changes with AnkiWeb and with all your devices.
1. You can now follow the steps of the [_Getting started_](#getting-started) section to install the major version.

## Deck structure

> Beware that changing the structure of the deck may **prevent you from upgrading it** without loss of progress.

The notes are based on a **note type** called _Ultimate Geography_, which defines **eight fields**: _Country_, _Country info_, _Capital_, _Capital info_, _Capital hint_, _Flag_, _Flag similarity_ and _Map_.

The cards are generated by Anki on import based on **four templates**: _Country - Capital_, _Capital - Country_, _Flag - Country_ and _Map - Country_. The extended version of the deck includes two additional templates: _Country - Flag_ and _Country - Map_.

The appearance of the cards is controlled solely with CSS; the content of the notes is free from HTML markup.

Every note is tagged. The tags, which are listed below by category, are prefixed with `UG::` so they don't conflict with other decks. They can be used to create [filtered decks](https://docs.ankiweb.net/#/filtered-decks?id=creating-manually) for [custom study](#custom-study).

- Type - `UG::Sovereign_State`, `UG::Oceans+Seas`, `UG::Continents`
- Continent - `UG::Africa`, `UG::Asia`, `UG::Europe`, `UG::North_America`, `UG::Oceania`, `UG::South_America`
- Region - `UG::Caribbean`, `UG::Middle_East`, `UG::Southeast_Asia`, `UG::European_Union`, `UG::Mediterranean`, `UG::East_Africa`, `UG::West_Africa`

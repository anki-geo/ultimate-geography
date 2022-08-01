# Ultimate Geography

**Geography flashcard deck for [Anki](http://ankisrs.net/)** featuring:

- the world's **[206 sovereign states](https://en.wikipedia.org/wiki/List_of_sovereign_states)** (824 cards)
- **59 territories, world regions, and other entities** (103 cards)
- **48 oceans and seas** (48 cards, maps only)
- **7 continents** (7 cards, maps only)
- for a total of **320 unique notes**, **982 cards**, **222 flags** and **320 maps**.

The deck is available in **English**, **German**, **Spanish**, **French**, **Norwegian Bokmål**, **Czech**, **Russian**, **Dutch**, **Swedish**, **Portuguese**, **Chinese**, **Polish** and **Italian**.

---

#### Table of contents

- [**Features**](#features)
  - [Supplementary information](#supplementary-information)
  - [Custom study](#custom-study)
- [**Getting started**](#getting-started)
- [**Upgrading**](#upgrading)
  - [First upgrade after APKG import](#first-upgrade-after-apkg-import)
  - [Keeping deck customisations](#keeping-deck-customisations)
  - [Levelling up from standard to extended](#levelling-up-from-standard-to-extended)
  - [Major version](#major-version)
- [**Deck structure**](#deck-structure)
- [**Customising the deck**](#customising-the-deck)
  - [Changes that are or can be preserved](#changes-that-are-or-can-be-preserved-)
  - [Changes that get reverted](#changes-that-get-reverted-)
  - [Changes that prevent upgrading](#changes-that-prevent-upgrading-)

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

Anki's [search feature](https://docs.ankiweb.net/searching), coupled with the deck's comprehensive [tag structure](#deck-structure), allows for the creation of [filtered decks](https://docs.ankiweb.net/filtered-decks#creating-manually) covering a wide range of learning goals and abilities. Here are some search queries you can use:

- `card:"Flag - Country"` to learn flags and nothing else;
- `tag:UG::Sovereign_State` to focus on sovereign states and exclude dependent territories, water bodies and continents;
- `-tag:"UG::Oceans+Seas"` (with "`-`" in front of the filter) to learn everything except oceans, seas and other water bodies;
- `card:"Map - Country" tag:UG::Sovereign_State tag:UG::Europe` to learn the location of Europe's sovereign states;
- `(card:"Country - Capital" or card:"Capital - Country") tag:UG::Sovereign_State` to learn the capitals of the world's sovereign states;
- `tag:UG::North_America -tag:UG::Caribbean` to focus on the countries in North America, but not in the Caribbean (i.e. those in Northern and Central America).

## Getting started

First-time here? Welcome! 👋

In order to install and later upgrade _Ultimate Geography_, you'll need to first install an Anki add-on called [CrowdAnki](https://github.com/Stvad/CrowdAnki):

1. Open Anki on your computer, go to the _Tools_ menu and select _Add-ons_.
1. In the dialog box, click on _Get Add-ons..._ and paste in the code provided on [this page](https://ankiweb.net/shared/info/1788670778).
1. Click on _OK_ to install the add-on, and then restart Anki.

You're now ready to install _Ultimate Geography_:

1. Go to the **[_Releases_ page](https://github.com/anki-geo/ultimate-geography/releases)**.
1. In the latest release's _Assets_ section, download the ZIP archive of the version of the deck you'd like to use. You can choose between [a standard and an extended version](#features) in a number of [languages](#ultimate-geography) -- for instance, if you're after the standard German deck, download `Ultimate_Geography_v[...]_DE.zip`.
1. Extract the content of the archive on your computer.
1. Open Anki and make sure your devices are all synchronised.
1. In the _File_ menu, select _CrowdAnki: Import from disk_.
1. Browse for and select the folder you extracted from the archive, which contains the deck's JSON file and `media` folder -- e.g. `Ultimate Geography [DE]`.
1. Don't change anything in the _CrowdAnki Import Settings_ dialog box that opens -- just press _OK_ to start the import. A dialog box should then confirm that the import was successful.

👉 To stay informed of new releases, make sure to [watch this repository's releases](https://help.github.com/en/articles/watching-and-unwatching-releases-for-a-repository).

## Upgrading

The upgrade process is typically the same as the installation process explained in the [previous section](#getting-started). However, some situations require extra care. As a general rule, **always read the release notes carefully**; they will likely tell you what to do or point you to a page that does.

### First upgrade after APKG import

You may have initially installed _Ultimate Geography_ by importing an **APKG file**. You may have downloaded such a file from this repository or from the [deck's page](https://ankiweb.net/shared/info/2109889812) on AnkiWeb, as this used to be the recommended installation process.

If you're in this situation and wish to upgrade, proceed as follows:

1. Perform the _Getting started_ steps exactly.
1. You should end up with two decks: your original deck called "Ultimate Geography" and a new, duplicated deck called "Ultimate Geography_2". Unless you created some notes of your own, every card in your original deck should have moved automatically to the new deck and your original deck should now be empty. You can verify this in Anki's [card browser](https://docs.ankiweb.net/browsing).
1. To get back to having a single deck, move any of your own cards out of the original deck and delete it. Then, rename the new deck to "Ultimate Geography". From here on, future upgrades will be seamless.

### Keeping deck customisations

If you've made, or are thinking of making, any changes to your _Ultimate Geography_ deck, check the [_Customising the deck_](#customising-the-deck) section below to see what will happen to them the next time you upgrade, and whether you need to take any steps to preserve them.

### Levelling up from standard to extended

Importing an extended deck on top of a standard deck is tricky and needs care. You may instead consider learning the extended deck from scratch. To do so, either:

- remove the standard deck first by following the instructions in the [_Major version_](#major-version) section below, or
- import the extended deck in a separate Anki profile.

If you'd rather keep your progress, proceed as follows:

1. Perform the _Getting started_ steps exactly.
1. Instead of a dialog box confirming that the import was successful, you'll see another dialog box titled _Change Note Type_. In the _Cards_ section, set _Change Flag - Country to:_ to "Flag - Country" (instead of "Country - Flag"), and set _Change Map - Country to:_ to "Map - Country" (instead of "Flag - Country").
1. Check that the other cards and fields map correctly and click on _OK_ to start the import.

### Major version

Major versions (e.g. `v3.0`) typically indicate that upgrading ["the normal way"](#upgrading) may lead to a significant loss of progress, or to the loss of [some of the customisations](#customising-the-deck) you may have made to the deck that would normally be preserved. This can occur, for instance, when [significant changes](https://github.com/anki-geo/ultimate-geography/releases/tag/v3.0) are made to the structure of the deck.

The [release notes](https://github.com/anki-geo/ultimate-geography/releases) and [upgrade instructions](https://github.com/anki-geo/ultimate-geography/wiki/Upgrade-instructions) on the wiki will typically provide you with a way to upgrade to the major version _without_ losing your progress. However, in some cases, the process can be daunting. 😰 If keeping your progress isn't worth the effort, or if you just feel like starting the deck again from scratch, then we recommend you perform a "clean import" as follows:

1. Open Anki and make sure your devices are all synchronised.
1. Delete the `Ultimate Geography` deck.
1. In the _Tools_ menu, select _Manage Note Types_, then delete the `Ultimate Geography` note type.
1. In the _Tools_ menu, select _Check Database_.
1. Sync the changes with AnkiWeb and with all your devices.
1. You can now follow the steps of the [_Getting started_](#getting-started) section to install the major version.

## Deck structure

The notes are based on a **note type** called _Ultimate Geography_, which defines **eight fields**: _Country_, _Country info_, _Capital_, _Capital info_, _Capital hint_, _Flag_, _Flag similarity_, and _Map_.

The cards are generated by Anki on import based on **four templates**: _Country - Capital_, _Capital - Country_, _Flag - Country_, and _Map - Country_. The extended version of the deck includes two additional templates: _Country - Flag_ and _Country - Map_.

The appearance of the cards is controlled solely with CSS; the content of the notes is free from HTML markup.

Every note is tagged. The tags, which are listed below by category, are prefixed with `UG::` so they don't conflict with other decks. They can be used to create [filtered decks](https://docs.ankiweb.net/filtered-decks#creating-manually) for [custom study](#custom-study).

- Type - `UG::Sovereign_State`, `UG::Oceans+Seas`, `UG::Continents`
- Continent - `UG::Africa`, `UG::Asia`, `UG::Europe`, `UG::North_America`, `UG::Oceania`, `UG::South_America`
- Region - `UG::Caribbean`, `UG::Middle_East`, `UG::Southeast_Asia`, `UG::European_Union`, `UG::Mediterranean`, `UG::East_Africa`, `UG::West_Africa`

## Customising the deck

Interested in making changes to the deck in Anki? Here's what you need to know.

### Changes that are or can be preserved 💖

- **Adding your own cards and media files**

  Go wild. 🌊 Upgrading will not affect any new cards you create, or any new media files you add to the newly added cards.

  If a duplicated deck is [created on import](#first-upgrade-after-apkg-import), your own cards will stay in their original deck.

- **Moving cards into another deck**

  Some people prefer to combine multiple decks into one to review them together.

  By default, CrowdAnki will move all the cards back into the _Ultimate Geography_ deck on import. To prevent this behaviour and update the existing cards in place, make sure to tick the _Do Not Move Existing Cards_ checkbox in the _CrowdAnki Import Settings_ dialog box, when following the steps in the [_Getting started_](@getting-started) section.

  > Note that if you had previously deleted the _Ultimate Geography_ deck, it will be recreated and may contain new cards.

- **Changing the deck's options**

  Deck options are, for instance, the number of new cards per day, the maximum number of reviews per day, etc.

  When importing the deck for the first time, CrowdAnki creates a new "option group" called _Ultimate Geography_ (unless it already exists). If you've made any changes to this group's options, they will be reverted on import.

  To avoid losing your options, create your own option group and give it a distinctive name. After you upgrade, you'll just have to switch the deck back to this option group.

- **Customising the templates and styles**

  Any edits you make to the built-in templates of the _Ultimate Geography_ note type will be reverted on upgrade. Same goes with the CSS styles that are shared by all the templates.

  One way to work around this and preserve your changes is to first [clone the note type](https://docs.ankiweb.net/editing#adding-a-note-type) and switch all the cards to the new note type in the Anki browser. You can then make your template and style changes in the cloned note type without affecting the original note type. The next time you upgrade, all the cards will switch back to the original note type, but you can easily switch them back to your customised note type in the Anki browser.

  > Note that you may have to update your custom templates and styles afterwards to stay in line with the built-in templates.

  A word of caution ⚠️: the above workaround is not guaranteed to work, so you may want to back up your local deck before upgrading by first exporting it with CrowdAnki.

### Changes that get reverted 😬

The changes listed below will be lost the next time you upgrade and there's no other solution than to make the changes again manually after the upgrade.

- **Renaming the deck or changing its description**

  Upgrading always restores the deck's default name and description.

- **Editing the content of a note**

  Examples:

  - adding a link to Wikipedia in the _Country info_ field of Curaçao;
  - adding your own memoization hint to the _Flag similarity_ field of Poland;
  - adding or removing a tag from a note;
  - renaming a tag.

  > If you correct a typo or a mistake, don't forget to [open an issue](https://github.com/anki-geo/ultimate-geography/issues/new) or a Pull Request so you don't lose your correction the next time you upgrade. 😉

- **Deleting a card**

  Upgrading will bring the card back. If you don't want to learn a card at all or if you want to delay learning it, consider:

  - suspending or burying the card;
  - creating a [filtered deck](#custom-study) that doesn't include the card;
  - moving the card into an "icebox" deck and ticking the _Do Not Move Existing Cards_ the next time you upgrade, as explained in the previous section, under _Moving cards into another deck_.

- **Adding or removing a template**

  If you add your own template to the _Ultimate Geography_ note type, you will lose it and all the cards created from it when you upgrade. During the upgrade, you will see a dialog box asking you to match your current templates to the deck's built-in templates. (This same dialog box appears when importing the extended deck [on top of the standard deck](#levelling-up-from-standard-to-extended).) Unfortunately, you will have not choice but to map your extra template to "Nothing". You can re-add it again after the upgrade, to recreate the cards, but your progress on those cards will be lost.

  If you remove a template, you will see the same dialog box when you upgrade. The template and its associated cards will then be recreated. You can easily remove the template again after the upgrade, if you so wish.

### Changes that prevent upgrading ⛔

- **Adding a new field (population, currency, etc.)**

  Adding a new field to the _Ultimate Geography_ note type will prevent you from upgrading the deck entirely. When you'll try to import it again, Anki will likely error and you'll risk losing your entire progress. Hopefully Anki, CrowdAnki, Brain Brew, and UG will [one day](https://github.com/ohare93/brain-brew/issues/4#issuecomment-644975261) find a way to make this possible.

  Note that the technique of cloning the note type explained under _Customising the templates and styles_ will not work here. If you've added a new field and are wanting to upgrade, you have no choice but to first **remove the field** from the note type.

  > If you really know what you're doing, you could try exporting your deck with CrowdAnki, carefully merging the JSON file of the new version of the deck into your exported deck's JSON file, and then importing your deck back into Anki ... but if you're capable of this, your skills would be put to much better use contributing to [CrowdAnki](https://github.com/Stvad/CrowdAnki) and [Brain Brew](https://github.com/ohare93/brain-brew/)! 😁

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

## Maintainer's guide

### Versioning

The releases follow a versioning scheme of the form `x.y`, where:

- `x` increases in the case of a **major, breaking release** (e.g. v3.0),
- `y` increases in the case of a **minor, non-breaking release** (e.g. v2.6).

Content changes, such as adding or removing a note, replacing an image, or translating the deck into a new language, all constitute minor changes. A change is considered major when users are likely to **lose a significant part of their progress** when upgrading the deck with CrowdAnki (cf. [_Upgrading_](README.md#upgrading) section of README).

### Release process

1. Bump the version in `desc.html` and commit the change.
1. Run `composer index && composer build`.
1. Add the content of the `build` folder to a ZIP archive named `Ultimate_Geography_v[x.y]_UPGRADE.zip`.
1. In Anki, synchronise all your devices and import the deck with CrowdAnki. For major versions, make sure to perform a [clean import](README.md#major-version).
1. Export the deck as an APKG package named `Ultimate_Geography_v[x.y].apkg`, making sure to exclude scheduling information but include all media.
1. Write the release notes on GitHub.
1. Attach the ZIP and APKG files to the release and publish it.
1. Go to [AnkiWeb](https://ankiweb.net/decks/).
1. Find the _Ultimate Geography_ deck and select _Actions_ > _Share_
1. Update the version number in the title and the description if needed.
1. Enter the full legal name and click _Share_.

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

# Connected links

* Mindmap - [GitMind](https://gitmind.com/app/docs/mkgt1xiu)
* Database design - [DrawSQL](https://drawsql.app/teams/pupsy/diagrams/reaboo)
* Color palette - [Atmos](https://app.atmos.style/66c371d6cdbfbc09b873f826)
* UI design - [Marvel](https://marvelapp.com/project/7011111)


# Installation

Choose folder on your computer, where you want to have this repository. 
The use next command to clone it:

```
git clone https://github.com/ruslkhay/ReaBooKivyMD.git
```

Install PDM package manager and run:

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
pdm install
```

In order to run formatting and linting manually use one of the following commands:

```bash
pre-commit run --files file.py
pre-commit run --all-files
```


# Overview

This is a cross-platform app for studying foreign words. 
Main goal for this version of project is a basic application, where user can generally do two things:
- Swipe cards to segregate them into learned and unlearned piles
- Manage cards dictionary: add, delete, amend cards.

Future version features are already considered.

## :door: Main window

It's a blank welcome screen, from which user can start learning cards.
In future it would be nice to have user's progress here in some way.

## :technologist: Study window
<img src='source/_static/study.png' width='300'>

Here all words from cardset are shown. By tapping on card user can see meaning (translation) of the word. 
Right button mark word as learned and remove card from pile.
Left button put card on piles bottom.

## :memo: Dictionary window
<img src='source/_static/dict_list.png' width='300'>

This screen provide options for viewing all added cards. User can add new ones, delete and amending old ones, searching cards by patterns.
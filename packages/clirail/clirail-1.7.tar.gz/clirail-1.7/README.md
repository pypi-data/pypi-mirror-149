# clirail

Command line application for the iRail API

iRail provides an API for Belgian trains.

## Installation
```
pip install --user --upgrade clirail
```

Then make sure the installed executable will be found. On UNIX-like systems, this means checking that `~/.local/bin/` is [in your PATH](https://opensource.com/article/17/6/set-path-linux).

## Usage
|Command                                         |Function                                       |
|------------------------------------------------|-----------------------------------------------|
|`clirail <station> ['' <moment>]`               |Liveboard (list of trains departing in station)|
|`clirail <from_station> <to_station> [<moment>]`|Route planning                                 |
|`clirail`                                       |Analyse current timeliness in a few stations   |

Omit the `<moment>` for ASAP departures.

Give either the station's name or its telegraphic code. Names are matched fuzzily and intuitively.
Telegraphic codes are short and sweet, you can learn them by looking at liveboards.

## What are these telegraphic codes?
A lot of stations have a short code, like FR for Bruges, FBMZ for Brussels-South and MWL for
Aywaille. These come from the days when signalling was done in Morse via the telegraph. Having a
short code for common names in the railway world meant the message took significantly less time to
send. By memorizing the codes for your favourite stations, you can benefit from them in the same
way! [More
information](https://nl.wikipedia.org/wiki/Telegrafische_code_van_Belgische_spoorwegstations) on
the Dutch-language Wikipedia.

## Licenses
* clirail code is released under GNU GPLv3+.
* xdg is released under ISC.

## Known issues
* If `<moment>` is just a time, it will be considered as today, even though in some cases it would
  make more sense to consider it as tomorrow (e.g. at 11 PM planning a route with departure at 7 AM).

## Development
To create a virtualenv and install the dependencies in it:
```
tools/create_venv.py
```

Activate the virtualenv with `source venv/bin/activate`. Then run `bin/clirail` to run the program.

Important: make sure the virtualenv is activated each time you run, otherwise your global `clirail`
installation may be used.

If you introduce dependencies, list them in `setup.py` under `install_requires`, and run
`tools/update_requirements.sh`.

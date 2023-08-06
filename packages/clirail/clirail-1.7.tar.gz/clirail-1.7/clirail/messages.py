# clirail: command line interface to iRail
# Copyright © 2019 Midgard
# License: GPLv3+

from .config import LANG


_messages = {
	"en": {
		"public_log": """This program uses the iRail API. All requests to iRail are \x1b[1mpublically logged\x1b[0m.
Learn more at the iRail API documentation: https://docs.irail.be/#log-and-feedback-data
If you are okay with this, press Enter to continue. Otherwise, press Ctrl+C.""",

		"downloading_stations": "Downloading list of stations… This only needs to be done once.",

		"didnt_understand_moment": """Didn’t understand moment “{moment}”, try writing it in another way.
Examples of easily understood moments are “8:30” and “2019-01-01, 8:30”.""",

		"canceled": "canceled",

		"departure_in": "Departure in {station}",
		"departure_in_w_code": "Departure in {station} ({telegraphic_code})",

		"train": "train",
		"destination": "destination",
		"platform": "platform",
		"departure": "departure",
		"duration": "dur.",
		"dep_arr": "dep/arr",
		"station": "station",
		"towards": "towards",

		"go_to_next_station": "go to the next station on your own",

		"m_duration_fmt": "{}m",
		"hm_duration_fmt": "{}h{:02}m",
		"m_delay_fmt": "{}",
		"hm_delay_fmt": "{}h{:02}",

		"delay_0": "On time",
		"delay_1": "1-6m delay",
		"delay_6": "6-30m delay",
		"delay_30": ">30m delay",
		"delay_canceled": "Canceled",
		"departed": "Departed",
		"not_yet_departed": "Not yet departed",
		"canceled_explanation": "For canceled trains this means: should have departed by now",

		"day_of_week_0": "Monday",
		"day_of_week_1": "Tuesday",
		"day_of_week_2": "Wednesday",
		"day_of_week_3": "Thursday",
		"day_of_week_4": "Friday",
		"day_of_week_5": "Saturday",
		"day_of_week_6": "Sunday",

		"help": """clirail: command line interface to iRail

Usage:
  clirail <station> ['' <moment>]                   List of trains departing in station
  clirail <from_station> <to_station> [<moment>]    Route planning
  clirail                                           Analyse current timeliness in a few stations
Omit the <moment> for ASAP departures.

Usage example:
  clirail gent flv         Plan route from Gent-Sint-Pieters to Leuven

Give either the station's name or its telegraphic code. Names are matched fuzzily and intuitively.
Telegraphic codes are short and sweet, you can learn them by looking at liveboards.

If <moment> is just a time, it will be considered as today, even though in some cases it would make
more sense to consider it as tomorrow (e.g. at 11 PM planning a route with departure at 7 AM).""",
	},

	"nl": {
		"public_log": """Dit programma gebruikt de iRail-API. Alle opzoekingen bij iRail worden \x1b[1mpubliek gelogd\x1b[0m.
Lees meer in de iRail-API-documentatie (in het Engels): https://docs.irail.be/#log-and-feedback-data
Als dit oké is, druk dan Enter om door te gaan. Druk anders Ctrl+C.""",

		"downloading_stations": "Lijst van stations downloaden… Dit moet maar één keer gebeuren.",

		"didnt_understand_moment": """Moment “{moment}” werd niet begrepen, probeer het eens op een andere manier te schrijven.
Voorbeelden van gemakkelijk te begrijpen momenten zijn “8:30” en “2019-01-01, 8:30”.""",

		"canceled": "afgeschaft",

		"departure_in": "Vertrek in {station}",
		"departure_in_w_code": "Vertrek in {station} ({telegraphic_code})",

		"train": "trein",
		"destination": "bestemming",
		"platform": "spoor",
		"departure": "vertrek",
		"duration": "duur",
		"dep_arr": "ver/aan",
		"station": "station",
		"towards": "richting",

		"go_to_next_station": "raak zelf in volgende station",

		"m_duration_fmt": "{}m",
		"hm_duration_fmt": "{}u{:02}m",
		"m_delay_fmt": "{}",
		"hm_delay_fmt": "{}u{:02}",

		"delay_0": "Op tijd",
		"delay_1": "1-6m vertraging",
		"delay_6": "6-30m vertraging",
		"delay_30": ">30m vertraging",
		"delay_canceled": "Afgeschaft",
		"departed": "Vertrokken",
		"not_yet_departed": "Nog niet vertrokken",
		"canceled_explanation": "Voor afgeschafte treinen betekent dit: had nu al vertrokken moeten zijn",

		"day_of_week_0": "maandag",
		"day_of_week_1": "dinsdag",
		"day_of_week_2": "woensdag",
		"day_of_week_3": "donderdag",
		"day_of_week_4": "vrijdag",
		"day_of_week_5": "zaterdag",
		"day_of_week_6": "zondag",

		"help": """clirail: commandolijninterface voor iRail

Syntaxis:
  clirail <station> ['' <vertrek>]                  Vertrekkende treinen in station
  clirail <van_station> <naar_station> [<vertrek>]  Routeplanning
  clirail                                           Analyseer huidige stiptheid in een paar stations
Laat <vertrek> weg voor "zo snel mogelijk".

Voorbeeld:
  clirail gent flv         Plan route van Gent-Sint-Pieters naar Leuven

Geef de naam of telegrafische code van een station. Namen worden gezocht op intuïtieve manier en
moeten niet volledig correct gespeld zijn. Telegrafische codes zijn kort en handig, ze worden
getoond bij de lijst van vertrekkende treinen in een station, zo kun je ze leren.

Als <vertrek> enkel een tijdtip is, wordt het beschouwd als vandaag, ook al zou je soms verwachten
dat het morgen is (bv. om 23 uur een route plannen met vertrek om 7 uur 's ochtends)."""
	}
}

def t(key):
	return _messages \
		.get(LANG, _messages["en"]) \
		.get(key, "Missing translation for " + key)

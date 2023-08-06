#!/usr/bin/env python

# clirail: command line interface to iRail
# Copyright © 2019 Midgard
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.


import sys
import json
from typing import Sequence, Mapping
import pathlib
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import requests
from .data import station_codes
from .xdg import XDG_DATA_HOME
from .printing import print_connections, print_liveboard, print_disturbances
from .messages import t
from .config import LANG


BASE_URL = "https://api.irail.be"
LIVEBOARD_URL = f"{BASE_URL}/liveboard/"
CONNECTIONS_URL = f"{BASE_URL}/connections/"
DISTURBANCES_URL = f"{BASE_URL}/disturbances/"


def load_or_fetch_stations():
	stations_file = XDG_DATA_HOME / "clirail" / ("stations_" + LANG + ".json")
	stations_url = f"{BASE_URL}/stations/"

	try:
		with open(str(stations_file), mode="r") as file:
			return json.load(file)["station"]
	except FileNotFoundError:
		print(t("public_log"), file=sys.stderr)
		_ = input()
		print(t("downloading_stations"))
		print("")
		stations_file.parent.mkdir(exist_ok=True, parents=True)
		req = requests.get(stations_url, params={"format": "json", "lang": LANG})
		stations = req.json()

		with open(str(stations_file), mode="w") as file:
			json.dump(stations, file)

		return stations["station"]

STATIONS: Sequence[Mapping] = load_or_fetch_stations()


def uri_to_id(uri, default=None):
	for station in STATIONS:
		if station["@id"] == uri:
			return station["id"]
	return default


def tele_to_uri(telegraphic_code, default=None):
	return station_codes.get(str.upper(telegraphic_code), default)

def uri_to_tele(in_uri, default=None):
	for telegraphic_code, uri in station_codes.items():
		if uri == in_uri:
			return telegraphic_code
	return default


def irail_date(moment):
	"""
	Convert a datetime to the "ddmmyy" and "HHMM" that iRail expects.
	"""
	if moment is None:
		return None, None
	else:
		return moment.strftime("%d%m%y"), moment.strftime("%H%M")


def get_liveboard(station=None, station_is_id=True, moment=None, departure=True, alerts=False):
	date, time = irail_date(moment)

	params = {
		"lang": LANG,
		"format": "json",

		("id" if station_is_id else "station"): station,
		"alerts": alerts,
		"arrdep": "departure" if departure else "arrival",
		"date": date, "time": time
	}

	req = requests.get(LIVEBOARD_URL, params=params)
	return req.json()


def get_connections(fro, to, moment=None, alerts=False):
	date, time = irail_date(moment)

	params = {
		"lang": LANG,
		"format": "json",

		"from": fro, "to": to,
		"alerts": alerts,
		"date": date, "time": time
	}

	req = requests.get(CONNECTIONS_URL, params=params)
	return req.json()


def get_disturbances():
	params = {
		"lang": LANG,
		"format": "json"
	}

	req = requests.get(DISTURBANCES_URL, params=params)
	return req.json()


# FIXME split into get_summary and print_summary
def show_summary():
	now = datetime.now()
	hour_ago = now - timedelta(hours=1)

	for station in ["Brugge", "Gent-Sint-Pieters", "Brussel-Zuid", "Liège-Guillemins"]:
		canceled   = [0, 0]
		delay_6    = [0, 0]
		delay_30   = [0, 0]
		delay_more = [0, 0]
		on_time    = [0, 0]

		for departure in get_liveboard(station, False, hour_ago)["departures"]["departure"]:
			is_canceled = departure["canceled"] != "0"
			departure_time = int(departure["time"]) + (0 if is_canceled else int(departure["delay"]))
			past = departure_time < now.timestamp()
			delay = int(departure["delay"])

			if is_canceled:
				canceled[past] += 1
			elif delay == 0:
				on_time[past] += 1
			elif delay <= 6 * 60:
				delay_6[past] += 1
			elif delay <= 30 * 60:
				delay_30[past] += 1
			else:
				delay_more[past] += 1

		print("\x1b[1m" + station + "\x1b[0m")
		print(f"{t('delay_0'):>16}: {on_time[0]:3d} {on_time[1]:3d}")
		print(f"{t('delay_1'):>16}: {delay_6[0]:3d} {delay_6[1]:3d}")
		print(f"{t('delay_6'):>16}: {delay_30[0]:3d} {delay_30[1]:3d}")
		print(f"{t('delay_30'):>16}: {delay_more[0]:3d} {delay_more[1]:3d}")
		print(f"{t('delay_canceled'):>16}: {canceled[0]:3d} {canceled[1]:3d}\n")

	print(f"{t('departed'):>18}* ↑   ↑ {t('not_yet_departed')}")

	print(f"*{t('canceled_explanation')}")


def coalesce(iterable):
	"""
	Return first non-None element of iterable, or None if none are non-None.
	"""
	for element in iterable:
		if element is not None:
			return element
	return None


STATION_ID, STATION_FREEFORM = range(2)

def local_resolve_station(station_input):
	"""
	Try to locally resolve station. Returns a tuple: station description and the type of station
	description: either STATION_ID or STATION_FREEFORM.
	"""
	if station_input is None:
		return None, STATION_FREEFORM

	id_from_tele = uri_to_id(tele_to_uri(station_input))
	if id_from_tele is not None:
		return id_from_tele, STATION_ID

	return station_input, STATION_FREEFORM


def print_help():
	print(t("help"))


def main(fro=None, to=None, moment=None):
	if fro in ("-h", "--help"):
		print_help()
		return

	if not fro:
		show_summary()
		return

	if fro == "d":
		disturbances = get_disturbances()
		print_disturbances(disturbances)
		return

	fro, fro_type = local_resolve_station(fro)
	to,  to_type  = local_resolve_station(to)

	try:
		moment_datetime = dateparser.parse(moment) if moment else None
	except ValueError:
		print(t("didnt_understand_moment").format(moment=moment),
			file=sys.stderr)
		return

	if to:
		connections = get_connections(fro, to, moment=moment_datetime)
		if "error" in connections:
			# TODO Translate common messages
			print(connections["message"])
			return
		print_connections(connections)

	else:
		liveboard = get_liveboard(fro, fro_type == STATION_ID, moment=moment_datetime)
		if "error" in liveboard:
			print(liveboard["message"])
			return
		telegraphic_code = uri_to_tele(liveboard["stationinfo"]["@id"])
		print_liveboard(liveboard, telegraphic_code)

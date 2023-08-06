# clirail: command line interface to iRail
# Copyright © 2019 Midgard
# License: GPLv3+

from datetime import datetime, date
from .messages import t
import re


icons = [
	("BUS",  "🚌"), # bus, typically to replace train in case of railroad works
	("EUR",  "🚄"), # Eurostar
	("ICE",  "🚄"), # ICE, German high-speed train
	("THA",  "🚄"), # Thalys
	("TGV",  "🚄"), # TGV, French high-speed train
	("IC",   "🚅"), # intercity train
	("ICT",  "🚅"), # tourist intercity train
	("P",    "🚅"), # peak train
	("TRN",  "🚅"), # just a train
	("EXT",  "🚅"), # replacement train or something
	("S",    "🚂"), # sprinter train
	("L",    "🚂"), # local train
	("WALK", "🚶"), # walking
	("",     "🚀")  # unknown, go by rocket
]

IGNORED_ALERTS = {
	"Mondmaskerplicht",
	"Port du masque obligatoire",
	"Face mask mandatory",
	"Maskenpflicht"
}


def without_colours(s):
	return re.sub(r"\x1b\[[^m]*m", "", s)


def icon_from_ref(ref):
	for prefix, icon in icons:
		if ref.startswith(prefix):
			return icon
	assert False


def format_duration(seconds, hm=t("hm_duration_fmt"), m=t("m_duration_fmt")):
	minutes = int(seconds) // 60
	if minutes < 60:
		return m.format(minutes)
	return hm.format(minutes // 60, minutes % 60)

def format_delay(seconds):
	seconds = int(seconds)
	formt = "\x1b[33m" if seconds // 60 < 5 else "\x1b[91m"
	return "" if seconds == 0 else (
		" " + formt + sign_str(seconds) +
		format_duration(abs(seconds), t("hm_delay_fmt"), t("m_delay_fmt")) +
		"\x1b[0m"
	)


def format_time(timestamp):
	return datetime.fromtimestamp(int(timestamp)).strftime("%H:%M")


def format_datetime(timestamp):
	return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d, %H:%M")


def sign_str(number):
	return "-" if number < 0 else "+"


def substring_from_last(string, char):
	try:
		last_pos = string.rindex(char)
		return string[last_pos+1:]
	except ValueError:
		return string


def print_liveboard_item(item):
	canceled = item["canceled"] != "0"
	delay_str = format_delay(int(item["delay"])) if not canceled else ""

	time_str = datetime.fromtimestamp(int(item["time"])).strftime("%H:%M")
	pretty_to = pad_trunc(item["station"] + " ", 30, ".")

	pretty_platform = pad_trunc(" " + item["platform"], 4, ".", left=False)

	ref = substring_from_last(item["vehicle"], ".")

	print((
		"{vehicle_id:>8} {icon} {to}.{pretty_platform}  {time_str}{delay_str}"
		if not canceled else
		"\x1b[9m{vehicle_id:>8} {icon} {to}.....  {time_str}\x1b[0m \x1b[31m{canceled_str}\x1b[0m"
	).format(
		**item,
		icon=icon_from_ref(ref),
		vehicle_id=ref,
		pretty_platform=pretty_platform,
		to=pretty_to,
		time_str=time_str,
		delay_str=delay_str,
		canceled_str=t("canceled")
	))


def print_liveboard(liveboard, tele=None):
	print()
	print(t("departure_in" if tele is None else "departure_in_w_code").format(
		station="\x1b[1m" + liveboard["station"] + "\x1b[0m",
		telegraphic_code=tele
	))
	print()

	print("\x1b[4;3m   {train:8} {destination:25} {platform:>9}  {departure:15}\x1b[0m".format(
		train=t("train"), destination=t("destination"), platform=t("platform"),
		departure=t("departure")
	))

	prev_date = date.today()
	for line in liveboard["departures"]["departure"]:
		dep_time = datetime.fromtimestamp(int(line["time"]))
		if dep_time.date() != prev_date:
			print(" " * 12 + format_date(dep_time))
			prev_date = dep_time.date()
		print_liveboard_item(line)


def print_connection_item(item, max_duration_len, max_delay_len):
	print()

	if item["departure"]["canceled"] != "0" or item["arrival"]["canceled"] != "0":
		print(t("canceled").upper())

	dep = item["departure"]
	arr = item["arrival"]
	dep_ref = substring_from_last(dep["vehicle"], ".")
	arr_ref = substring_from_last(arr["vehicle"], ".")

	print((
		(" " * max_duration_len) + " ┌← {time}{delay:>{max_delay_len}}  {fro}.{platform} {ref} {icon} {direction}"
	).format(
		max_delay_len=max_delay_len,
		fro=pad_trunc(dep["station"] + " ", 20, "."),
		platform=pad_trunc(" " + dep["platform"], 3, ".", left=False),
		ref=pad_trunc(" " + dep_ref, 10, ".", left=False),
		icon=icon_from_ref(dep_ref),
		time=format_time(dep["time"]),
		delay=format_delay(dep["delay"]),
		direction=dep["direction"]["name"]
	))

	if "vias" in item:
		for via in item["vias"]["via"]:
			via_dep = via["departure"]
			via_arr = via["arrival"]
			via_ref = substring_from_last(via_dep["vehicle"], ".")

			if int(via_dep.get("walking")):
				print((
					(" " * max_duration_len) + " ├\x1b[38;5;245m→ {time}{delay:>{max_delay_len}}\x1b[38;5;245m  {via}. 🚶 {go_to_next_station}\x1b[0m"
				).format(
					max_delay_len=max_delay_len,
					via=pad_trunc(via["station"] + " ", 20, "."),
					time=format_time(via_arr["time"]),
					delay=format_delay(via_arr["delay"]),
					go_to_next_station=t("go_to_next_station")
				))
			else:
				print((
					(" " * max_duration_len) + " ├\x1b[38;5;245m← {time}{delay:>{max_delay_len}}\x1b[38;5;245m  {via}.{platform:2} {ref} {icon} {direction}\x1b[0m"
				).format(
					max_delay_len=max_delay_len,
					via=pad_trunc(via["station"] + " ", 20, "."),
					platform=pad_trunc(" " + via_dep["platform"], 3, ".", left=False),
					ref=pad_trunc(" " + via_ref, 10, ".", left=False),
					icon=icon_from_ref(via_ref),
					time=format_time(via_dep["time"]),
					delay=format_delay(via_dep["delay"]),
					direction=via_dep["direction"]["name"]
				))

	print((
		"{duration:>{max_duration_len}} └→ {time}{delay:>{max_delay_len}}  {to}.{platform:2} "
	).format(
		max_duration_len=max_duration_len,
		max_delay_len=max_delay_len,
		duration=format_duration(item["duration"]),
		to=pad_trunc(arr["station"] + " ", 20, "."),
		platform=pad_trunc(" " + arr["platform"], 3, ".", left=False),
		time=format_time(arr["time"]),
		delay=format_delay(arr["delay"])
	))


	for alert in item.get("alerts", {}).get("alert", []):
		if alert["header"] in IGNORED_ALERTS:
			continue
		print("""⚠  {}
\x1b[38;5;245m{}
van {} tot {}\x1b[0m""".format(alert["header"], alert["description"], format_datetime(alert["startTime"]), format_datetime(alert["endTime"])))

	remarks = set(remark["description"] for remark in item.get("remarks", {}).get("remark", []))
	for remark in remarks:
		print((" " * max_duration_len) + "  \x1b[38;5;245m{}\x1b[0m".format(remark))


def delay_str_len(delay):
	return len(without_colours(format_delay(delay)))


def max_delay_str_length(connection_item):
	return max(
		delay_str_len(connection_item["departure"]["delay"]),
		delay_str_len(connection_item["arrival"]["delay"]),
		*(
			delay_str_len(via["departure"]["delay"])
			for via in connection_item.get("vias", {}).get("via", [])
		)
	)


def format_date(d):
	return "\x1b[1m{:%Y-%m-%d} {}\x1b[0m".format(
		d,
		t("day_of_week_{}".format(d.weekday()))
	)


def print_connections(connections):
	max_duration_len = max(max((
		len(format_duration(item["duration"]))
		for item in connections["connection"]
	), default=0), len(t("duration")))

	max_delay_len = max((
		max_delay_str_length(item)
		for item in connections["connection"]
	), default=0)

	print("\x1b[4;3m{duration:>{max_duration_len}} {dep_arr:>8} {delay_spaces} {station:12} {platform:>11} {train:>10}    {towards}\x1b[0m".format(
		max_duration_len=max_duration_len,
		duration=t("duration"), dep_arr=t("dep_arr"),
		delay_spaces=" " * max_delay_len,
		station=t("station"), platform=t("platform"),
		train=t("train"), towards=t("towards")
	))

	prev_date = date.today()
	for line in connections["connection"]:
		dep_time = datetime.fromtimestamp(int(line["departure"]["time"]))
		if dep_time.date() != prev_date:
			print("\n" + format_date(dep_time))
			prev_date = dep_time.date()

		print_connection_item(line, max_duration_len, max_delay_len)


def print_disturbances(disturbances):
	for disturbance in reversed(disturbances["disturbance"]):
		print("""{}
\x1b[38;5;245m{}\x1b[0m
\x1b[38;5;33m{}\x1b[0m
""".format(
	disturbance["title"],
	re.sub(
		r'(Webnews|Info) [A-Z]{2}',
		'',
		re.sub(r'[.:]([A-Z*-])', lambda m: ".\n" + m[1], disturbance["description"])
	).strip(),
	disturbance["link"]))


def pad_trunc(string, width, filler=" ", left=True):
	if len(string) >= width:
		return string[:width]
	if left:
		return (string + (filler * width))[:width]
	else:
		return ((filler * width) + string)[-width:]

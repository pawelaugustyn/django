import json
import re

to_parse = open("RA170918.TXT", "r")


class ParseLine:
    def __init__(self):
        self.stops = dict()

    def GetLineSymbol(self, line):
        number = re.sub(" +", " ", line)
        number = re.sub(r"Linia: (.*) - .*", r"\g<1>", number)
        number=number.strip("\n")
        number = number.strip(" ")
        return number

start_parsing = False
read=False
read_time=False
day=0
parser = ParseLine()
op=False
line_no=""
stops_dictionary=dict()
stop_number=0

for line in to_parse:
    if "Linia:" in line:
        line_no=parser.GetLineSymbol(line)
    if "LINIA ZWYKŁA" in line:
        break
    if "*RP" in line:
        read = True
        day = 0
        continue
    if "#OP" in line:
        op=True
        continue
    if op and "#RP" in line:
        op=False
        continue
    if op:
        op=False
        day = 0
        read = True
    if read:
        line=line.lstrip(" ")
        stop_number = line[:6]
        if stop_number not in stops_dictionary:
            stops_dictionary[stop_number] = open("application/timetable/"+stop_number+".json", "w")
        read=False
        continue
    if "*OD" in line:
        read_time=True
        continue
    if "#OD" in line:
        read_time=False
        day=day+1
        continue
    if read_time:
        line = line.lstrip(" ")
        hour = line[:5].rstrip(" ")
        destination=line[6:].lstrip(" ")
        destination=destination.split("/")
        destination=destination[0]
        if stop_number not in parser.stops:
            parser.stops[stop_number] = {}
        if day not in parser.stops[stop_number]:
            parser.stops[stop_number][day]=[]
        parser.stops[stop_number][day].append([hour,destination,line_no])
        continue
    if "#LL" in line:
        break

for file in stops_dictionary:
    stops_dictionary[file].write(json.dumps(parser.stops[file]))
for file in stops_dictionary:
    stops_dictionary[file].close()
to_parse.close()

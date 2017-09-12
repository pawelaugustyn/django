import json

to_parse = open("RA170909.TXT", "r")
data = open("data.txt", "w")


class ParseLine:
    def __init__(self):
        self.stops_dict = {}

start_parsing = False
read=False
read_time=False
day=0
parser = ParseLine()

for line in to_parse:
    if "*RP" in line or "#RP" in line:
        read=True
        day = 0
        continue
    if "#OP" in line:
        read = True
        continue
    if read:
        if "#RP" in line:
            day = 0
            continue
        line=line.lstrip(" ")
        stop_number = line[:6]
        read=False
        continue
    if "*OD" in line:
        read_time=True
        continue
    if "#OD" in line:
        read_time=False
        day=day+1
        if day==3:
            day=0
        continue
    if read_time:
        line = line.lstrip(" ")
        hour = line[:5].rstrip(" ")
        destination=line[6:].lstrip(" ")
        destination=destination.split("/")
        destination=destination[0]

        if stop_number not in parser.stops_dict:
            parser.stops_dict[stop_number] = {}
        if day not in parser.stops_dict[stop_number]:
            parser.stops_dict[stop_number][day]=[]
        parser.stops_dict[stop_number][day].append([hour,destination])
        continue
    if "#LL" in line:
        break

data.write(json.dumps(parser.stops_dict))
data.close()
to_parse.close()

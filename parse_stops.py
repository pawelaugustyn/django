import re

to_parse = open("RA170828.TXT", "r")

lines_numbers = []


class ParseLine:
    def __init__(self):
        pass

    trams_lines_list = ['1', '2', '3', '4', '7', '9', '10', '13', '14', '15', '17', '18', '20', '22', '23', '24', '25',
                        '26', '27', '31', '33', '35', '44', '71', 'T']
    trams_stops = []

    def GetStationName(self, line):
        name = re.sub(" +", " ", line)
        name = re.sub(r"[0-9]+ (.*), .*", r"\g<1>", name)
        return name

    def GetStationNumber(self, line):
        number = re.sub(" +", " ", line)
        number = re.sub(r"([0-9]+).*", r"\g<1>", number)
        return number

    def GetStationCoords(self, line):
        coords = re.sub(" +", " ", line)
        coords = re.sub(r".*Y= ([0-9]+\.[0-9]+) X= ([0-9]+\.[0-9]+)", r"\g<1> \g<2>", coords)
        coords = coords.split(" ")
        return coords[0], coords[1]

    def CheckIfTramLine(self, line, stationid, coords, stationname):
        lines = re.sub(" +", " ", line)
        lines = lines.split(":")[1].lstrip(" ")
        lines = lines.split(" ")

        for line in lines:
            if line in self.trams_lines_list:
                stop = dict()
                stop["Name"] = stationname
                stop["Number"] = stationid
                stop["Line"] = line
                stop["Y"] = coords[0]
                stop["X"] = coords[1]
                self.trams_stops.append(stop)

        if lines in self.trams_lines_list:
            return True
        return False


start_parsing = False
parser = ParseLine()
stationid = None
stationname = None
coords = None
for line in to_parse:
    if not start_parsing and "*ZP" in line:
        start_parsing = True
        continue
    if not start_parsing:
        continue

    diff = len(line) - len(line.lstrip(" "))
    line = line.rstrip("\n").lstrip(" ")

    if diff == 3:
        stationid = parser.GetStationNumber(line)
        stationname = parser.GetStationName(line)

    if diff == 9:
        coords = parser.GetStationCoords(line)

    if diff == 12:
        parser.CheckIfTramLine(line, stationid, coords, stationname)

    if "#ZP" in line:
        break

print(parser.trams_stops)
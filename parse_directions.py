import re
import json

to_parse = open("RA170909.TXT", "r")

lines_numbers = []


class ParseLine:
    def __init__(self):
        self.lines_directions = dict()

    def GetLineSymbol(self, line):
        number = re.sub(" +", " ", line)
        number = re.sub(r"Linia: (.*) - .*", r"\g<1>", number)
        return number

    def GetDetails(self, line, lineNumber):
        details = re.sub(",", "", line)
        details = re.sub("=", "", details)
        details = re.sub(">", "", details)
        details = re.sub(" +", " ", details)
        details = re.sub(r"([^ ]*) .* [A-Z\-0-9]{2} (.*) [A-Z\-0-9]{2} .*", r"\g<1><splitter>\g<2>", details)
        results = details.split("<splitter>")

        if lineNumber not in self.lines_directions:
            self.lines_directions[lineNumber] = []
        addedResult = dict()
        addedResult["Symbol"] = results[0]
        addedResult["Direction"] = results[1]
        self.lines_directions[lineNumber].append(addedResult)


start_parsing = False
parser = ParseLine()
lineNumber = None
isDirectionDescriber = False

for line in to_parse:
    if not start_parsing and "*LL" in line:
        start_parsing = True
        continue
    if not start_parsing:
        continue

    indentation = len(line) - len(line.lstrip(" "))
    line = line.rstrip("\n").lstrip(" ")

    if indentation == 3:
        if "TRAMWAJOWA" not in line:
            skipLine = True
            continue
        else:
            skipLine = False
        lineNumber = parser.GetLineSymbol(line)

    if skipLine:
        continue

    if indentation == 6:
        if "*TR" in line:
            isDirectionDescriber = True
        if "#TR" in line:
            isDirectionDescriber = False

    if indentation == 9:
        if isDirectionDescriber:
            parser.GetDetails(line, lineNumber)

to_parse.close()

result = open("directions.json", mode='w', encoding='utf-8')
result.write(json.dumps(parser.lines_directions))
result.close()
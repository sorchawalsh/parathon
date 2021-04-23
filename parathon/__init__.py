import re
import json
import csv

class Detect:
    def __init__(self, file, language=None):
        self.file = open(file, "r", encoding="utf8")
        self.language = language

    def parathon(self):
        with open('dictionaries/neutral.json') as json_file:
            cue_dictionary = json.load(json_file)
        txt = self.file.read()
        split = re.findall(r"[\w']+|[.,!?;:)]+|\s+|[\U00010000-\U0010ffff]", txt, flags=re.UNICODE)
        position = 0
        output = list()
        for token in split:
            start = position
            position = position + len(token)
            end = position
            matches_for_token = list()
            for key in cue_dictionary:
                if re.search(key, token):
                    matches_for_token.append([token, cue_dictionary[key], start, end])

            if len(matches_for_token)>1:
                ftf_properties=list()
                cmc_properties=list()
                for match in matches_for_token:
                    ftf_properties.append(match[1][0])
                    cmc_properties.append(match[1][1])
            elif len(matches_for_token) == 1:
                ftf_properties=matches_for_token[0][1][0]
                cmc_properties=matches_for_token[0][1][1]
            elif (token, "\t", "\t", start, end) not in output:
                ftf_properties="\t"
                cmc_properties="\t"
            output.append((token, ftf_properties, cmc_properties, start, end))
        return output

    def csvify(self, parathon, filename):
        header=["token", "ftf", "cmc", "start", "end"]
        with open(filename+".csv", "w", newline="\n", encoding="utf-8") as csvfile:
            filewriter=csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(header)
            for item in parathon:
                filewriter.writerow(item)
        csvfile.close()


test=Detect("input_test.txt")
test.csvify(test.parathon(), "testcsv")


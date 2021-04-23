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
            elif (token, " ", " ", start, end) not in output:
                ftf_properties=" "
                cmc_properties=" "
            output.append((token, ftf_properties, cmc_properties, start, end))
        return output

    def csvify(self, parathon, filename):
        header=["token", "ftf", "cmc", "start", "end"]
        with open(filename+".csv", "w", newline="\n", encoding="utf-8") as csvfile:
            filewriter=csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(header)
            for item in parathon:
                filewriter.writerow(item)
        csvfile.close()

    def xmlify(self, parathon, filename):
        xml_file = open(filename+".xml", "w", encoding="utf8")
        output_str_xml = '<?xml version="1.0" encoding="UTF-8"?>\n\t<input>'
        xml_output=list()
        for token in parathon:
            print(token[0])
            #output_str_xml = output_str_xml + str(token)
            if token[1]!=" ":
                token_info_xml='<cue ftf="'+str(token[1])+'" cmc="'+str(token[2])+'">'+str(token[0])+'</cue>'
                xml_output.append(token_info_xml)
            else:
                xml_output.append(token[0])
        for token in xml_output:
            output_str_xml = output_str_xml + token
        output_str_xml = output_str_xml + "\n</input>"
        xml_file.write(output_str_xml)
        xml_file.close()

test=Detect("input_test.txt")
#test.csvify(test.parathon(), "testcsv")
test.xmlify(test.parathon(), "testxml")

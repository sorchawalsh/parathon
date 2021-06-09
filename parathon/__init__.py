import re
import json
import csv

class Detect:
    def __init__(self, file, language=None, mode=None):
        self.file = open(file, "r", encoding="utf8")
        self.language = language
        self.mode = mode
    def parathon(self):
        with open('dictionaries/neutral.json', encoding='utf-8') as json_file:
            cue_dictionary = json.load(json_file)
            if self.language == "english":
                with open('dictionaries/english.json', encoding='utf-8') as english_file:
                    english_dictionary = json.load(english_file)
                    cue_dictionary.update(english_dictionary)
            if self.mode == "whatsapp":
                with open('dictionaries/whatsapp.json', encoding='utf-8') as whatsapp_file:
                    whatsapp_dictionary = json.load(whatsapp_file)
                    cue_dictionary.update(whatsapp_dictionary)
        txt = self.file.read()
        split = re.findall(r"[\w'*_~]+|[.,!?;:)\*]+|\s+|[\U00010000-\U0010ffff]", txt, flags=re.UNICODE)
        position = 0
        output = list()
        for token in split:
            start = position
            position = position + len(token)
            end = position
            matches_for_token = list()
            for key in cue_dictionary:
                try:
                    if cue_dictionary[key][3]:
                        if re.search(key, token, flags=eval(cue_dictionary[key][3])):
                            matches_for_token.append([token, cue_dictionary[key], start, end])
                except IndexError:
                    if re.search(key, token):
                        matches_for_token.append([token, cue_dictionary[key], start, end])

            if len(matches_for_token) > 1:
                ftf_properties = list()
                cmc_properties_main = list()
                cmc_properties_sub = list()
                for match in matches_for_token:
                    ftf_properties.append(match[1][0])
                    cmc_properties_main.append(match[1][1])
                    cmc_properties_sub.append(match[1][2])
            elif len(matches_for_token) == 1:
                ftf_properties = matches_for_token[0][1][0]
                cmc_properties_main = matches_for_token[0][1][1]
                cmc_properties_sub = matches_for_token[0][1][2]
            elif (token, " ", " ", start, end) not in output:
                ftf_properties = " "
                cmc_properties_main = " "
                cmc_properties_sub = " "
            output.append((token, ftf_properties, cmc_properties_main, cmc_properties_sub, start, end))
        return output

    def csvify(self, parathon, filename):
        header=["token", "ftf", "cmc_main", "cmc_sub", "start", "end"]
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
            if token[1]!=" ":
                token_info_xml='<cue f2f="'+str(token[1])+'" cmc_main="'+str(token[2])+'" cmc_sub="'+str(token[3])+'">'+str(token[0])+'</cue>'
                xml_output.append(token_info_xml)
            else:
                xml_output.append(token[0])
        for token in xml_output:
            output_str_xml = output_str_xml + token
        output_str_xml = output_str_xml + "\n</input>"
        xml_file.write(output_str_xml)
        xml_file.close()


test=Detect("jacinto_sample.txt", language="english")
test.csvify(test.parathon(), "testcsv")
#test.xmlify(test.parathon(), "testxml")

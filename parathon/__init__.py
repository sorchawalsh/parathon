import re
import json
import csv
import os

# Our main class, a detection object sets the parameters for the actual detection.
class Detect:
    def __init__(self, file, language=None, mode=None):
        self.file = open(file, "r", encoding="utf8")
        self.language = language
        self.mode = mode

    # Function for the detection of paralinguistic cues
    def parathon(self):
        os.chdir('..')
        with open('dictionaries/neutral.json', encoding='utf-8') as json_file:
            cue_dictionary = json.load(json_file)
            # here our two optional extra dictionaries are loaded
            if self.language:
                try:
                    with open('dictionaries/'+self.language+'.json', encoding='utf-8') as language_file:
                        language_dictionary = json.load(language_file)
                        cue_dictionary.update(language_dictionary)
                except FileNotFoundError:
                    print("ERROR: language file could not be found. Analysing with neutral dictionary.")
            if self.mode:
                try:
                    with open('dictionaries/'+self.mode+'.json', encoding='utf-8') as mode_file:
                        mode_dictionary = json.load(mode_file)
                        cue_dictionary.update(mode_dictionary)
                except FileNotFoundError:
                    print("ERROR: mode dictionary could not be found. Analysing with neutral dictionary.")
        txt = self.file.read()
        # Here we split the text into tokens. Emojis count as tokens. Some punctuation
        # is included as a word character so we may take into account,
        # for example, *corrections and _whatsapp formatting_.

        split = re.findall(r"[\w'*_~]+|[.,!?;:)\*]+|\s+|[\U00010000-\U0010ffff]", txt, flags=re.UNICODE)
        position = 0
        output = list()
        for token in split:
            start = position
            position = position + len(token)
            end = position
            matches_for_token = list()
            for key in cue_dictionary:
                # Some of the regexes require flags.
                # This part allows us to use those flags.
                try:
                    if cue_dictionary[key][3]:
                        if re.search(key, token, flags=eval(cue_dictionary[key][3])):
                            matches_for_token.append([token, cue_dictionary[key], start, end])
                except IndexError:
                    if re.search(key, token):
                        matches_for_token.append([token, cue_dictionary[key], start, end])
            # Append properties to lists for later
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

    # Function to return a csv file from the output.
    # User can define filename.
    def csvify(self, parathon, filename):
        header=["token", "ftf", "cmc_main", "cmc_sub", "start", "end"]
        with open(filename+".csv", "w", newline="\n", encoding="utf-8") as csvfile:
            filewriter=csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(header)
            for item in parathon:
                filewriter.writerow(item)
        csvfile.close()

    # Same as CSV but it's XML this time.
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

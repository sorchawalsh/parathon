import re
import json


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
            for key in cue_dictionary:
                if re.search(key, token):
                    output.append((token, cue_dictionary[key], start, end))
                else:
                    output.append((token, start, end))
        return output


test=Detect("input_test.txt")
print(test.parathon())
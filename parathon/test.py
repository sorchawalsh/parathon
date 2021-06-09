import csv
import re
import nltk
from nltk.metrics.scores import (precision, recall)

"""out = open('cleancsv.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(out)
with open('testcsv.csv', 'r', encoding='utf-8') as in_file:
    read = csv.reader(in_file)
    for row in read:
        if re.match(r"(\S)",row[1]):
          writer.writerow((row[1],row[2],row[3],row[0],))

with open('cleancsv.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    test = list(reader)
with open('roxanechat.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    reference = list(reader)
nltk.metrics.scores.accuracy(reference, test)"""
with open("jacinto_sample_tagged.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    ref = list(reader)

final_list = list()
ignoremode = bool()
for item in ref:
    item = str(item)[2:-2]
    for word in item.split(" "):
        if word == "<cue":
            ignoremode = True
        if re.search("'</cue>", word):
            ignoremode = False
            print("deactivate ignore mode")
    if ignoremode:
        pass
    else:
        new_list = item.split(" ")
        final_list.append(str(new_list)[1:-1])
out = open('jacinto_sample_tagged.txt', 'w', encoding='utf-8')
out.write(str(new_list))

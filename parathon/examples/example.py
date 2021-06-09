from parathon import Detect

test=Detect("example_chat.txt", language="english", mode="whatsapp")
#test.csvify(test.parathon(), "testcsv")
test.xmlify(test.parathon(), "testxml")

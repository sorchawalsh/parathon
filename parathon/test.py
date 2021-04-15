import os
import re
import regex
import nltk
import emoji
def run(file):
    txt=file.read()
    print(txt)
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    split = re.findall(r"[\w']+|[.,!?;:)]+|\s+|[\U00010000-\U0010ffff]", txt, flags=re.UNICODE)
    position=0
    output = list()
    xml_output=list()
    for token in split:
        start=position
        position=position+len(token)
        end=position
        if re.search(r"(\w)\1{2,}", token):
            type_cue="VQ"
            cmc_cue_type="Vocal spelling"
            token_info=(token,start,end,type_cue,cmc_cue_type)
            token_info_xml='<cue ftf="'+type_cue+'" cmc="'+cmc_cue_type+'">'+token+'</cue>'
            xml_output.append(token_info_xml)
        else:
            token_info=(token,start,end)
            xml_output.append(token)
        if re.match(r"[\w']+|[.,!?;:)]+|[\U00010000-\U0010ffff]", token, flags=re.UNICODE):
            output.append(token_info)
    print(output)
    new_file=open("new_file.txt", "w", encoding="utf8")
    xml_file=open("parathon_out.xml", "w", encoding="utf8")
    output_str_xml = '<?xml version="1.0" encoding="UTF-8"?>\n\t<input>'
    for token in xml_output:
        output_str_xml=output_str_xml+token
    output_str_xml=output_str_xml+"</input>"
    xml_file.write(output_str_xml)
    xml_file.close()
    new_file.write(str(output))
    new_file.close()

file=open("input_test.txt", "r", encoding="utf8")
if __name__== "__main__":
    run(file)
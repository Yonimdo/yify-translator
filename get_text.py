import os

import requests
import sys
import io
import re

URL = 'https://www.googleapis.com/language/translate/v2?target={}&key=AIzaSyDMkOnUCvBjNg551HafsB2W8UHqCPsKCFg' \
      '{}' \
      ''
name = '######################### NAME #########################'
sort_description = '######################### SHORT DESCRIPTION #########################'
long_description = '######################### LONG DESCRIPTION #########################'
sagi_template = "\n\n{}\n\n{}\n\n\n\n{}\n\n"
sagi_inner = "{}\n\n\n\n\n\n{}"
# sagi_template = "\n\n{}\n\n{}\n\n\n\n{}\n\n".format(name, sort_description, long_description)
q_template = '&q={}'
xml_template = '<string tag="py" name="{}">{}</string>\n'


def get_languages(default, base_file):
    languages = requests.get("https://www.googleapis.com/language/translate/v2/languages"
                             "?target=en&key=AIzaSyDMkOnUCvBjNg551HafsB2W8UHqCPsKCFg")
    assert languages.ok
    if not os.path.exists("res"):
        os.makedirs("res")
    languages = languages.json()['data']['languages']
    counter = len(languages)
    strings = []
    constants = []
    template_concat = ""
    template_concat2 = ""
    max_word_for_request = 80
    with open(base_file, encoding="UTF-8") as readfile:
        for line in readfile:
            if 'tag="py"' in line:
                max_word_for_request = max_word_for_request - 1
                title = re.findall(r'name="(.+)"', line).pop()
                value = re.findall(r'>(.+)<', line).pop()
                strings.append(title)
                if max_word_for_request > 0:
                    template_concat += q_template.format(value)
                else:
                    template_concat2 += q_template.format(value)

            elif 'name=' in line:
                constants.append(line)

    for language in languages:
        target = language['language']
        direc = "values" if target == default else "values-{}".format(target)
        if not os.path.exists("res/{}".format(direc)):
            os.makedirs("res/{}".format(direc))
        else:
            print("{} Already translated. ({} to go..)".format(language, counter))
            counter-=1
            continue
        r = requests.get(URL.format(target, template_concat))
        if max_word_for_request <= 0:
            r2 = requests.get(URL.format(target, template_concat2))
        counter -= 1
        try:
            assert r.ok
            r = r.json()['data']['translations']
            if max_word_for_request <= 0:
                assert r2.ok
                r2 = r2.json()['data']['translations']
                r = r + r2

            with open("res/{}/strings.xml".format(direc), 'w', encoding="UTF-8") as outfile:
                outfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
                outfile.write("<resources>")
                outfile.write("\n")
                outfile.writelines(constants)
                titles = list(reversed(strings))
                outfile.write("\n")
                for text in r:
                    outfile.write(xml_template.format(titles.pop(), text['translatedText'].replace("&#39;", "\\&#39;")))
                outfile.write("\n")
                outfile.write("\n")
                outfile.write("</resources>")
            print("Translated : {} ({} to go..)".format(language, counter))
        except AssertionError:
            print("Falied to translate: {} ({} to go..)".format(language, counter))
    return 1


def get_description(default, base_file):
    languages = requests.get("https://www.googleapis.com/language/translate/v2/languages"
                             "?target=en&key=AIzaSyDMkOnUCvBjNg551HafsB2W8UHqCPsKCFg")
    assert languages.ok
    if not os.path.exists("res"):
        os.makedirs("res")
    languages = languages.json()['data']['languages']
    strings = []
    template_concat = ""
    with open(base_file, encoding="UTF-8") as readfile:
        file = ""
        for line in readfile:
            file += line
        name_val, short_val, long_val = file.split("\n\n\n\n\n")
        template_concat += (q_template + q_template + q_template).format(name_val, short_val,
                                                                         long_val.replace("\n", "ג…“"))
    for language in languages:
        target = language['language']
        if target < "mk":
            continue
        r = requests.get(URL.format(target, template_concat))
        try:
            assert r.ok
            if not os.path.exists("Description"):
                os.makedirs("Description")
            r = r.json()['data']['translations']
            with open("Description/{}".format(language['name'] + "({})".format(language['language'])), 'w',
                      encoding="UTF-8") as outfile:
                outfile.write(sagi_template.format(sagi_inner.format(name, r[0]['translatedText']),
                                                   sagi_inner.format(sort_description, r[1]['translatedText']),
                                                   sagi_inner.format(long_description, r[2]['translatedText'].replace(
                                                       r"ג…“", "\n"))))
            print("Translate Description: {}".format(language))
        except AssertionError:
            print("Failed to translate Description: {}".format(language))
    return 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please insert translate able string xml")
    else:
        if 'descrption.default' in sys.argv[2]:
            get_description(sys.argv[1], sys.argv[2])
        if 'strings.default' in sys.argv[2]:
            get_languages(sys.argv[1], sys.argv[2])

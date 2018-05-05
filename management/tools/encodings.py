import json
import re

import requests
from html2text import HTML2Text
from pprint import pprint

from lenguatranslator import settings


def get(url):
    '''Retrieve page content and use html2text to convert into readable text.'''
    text = ""
    try:
        # get webpage content for this url
        r = requests.get(url)
        # raise exception if status code is not 200
        r.raise_for_status()

        # use html2text to transfer html to readable text
        h = HTML2Text()
        h.ignore_links = False
        text = h.handle(r.text)
    except Exception as e:
        pass
    return text


# result = {}
# langs = settings.dict_languages.keys()
# for lang in langs:
#     text = get("http://usefulwebtool.com/en/characters_{}.php".format(lang))
#     letters = re.findall(r'(\[.+\]).+\|  \| &#[0-9]', text)
#
#     str = ""
#     while letters:
#         letter ascii = letters.pop()
#         str += letter
#     result[lang] = str
#     pprint(result[lang])
# with open('blabla.json', 'w') as f:
#     f.write(json.dumps(result))


langs = settings.dict_languages

check = {}
for lang in langs:
    pass

lines = []
with open('valid.csv', 'r', encoding="utf8") as f:
    r = f.read()
    lines = [line.split(",") for line in r.split("\n")]

for line in lines:
    for word in line:
        check[word] = check.get(word, 0) + 1


pprint(check)
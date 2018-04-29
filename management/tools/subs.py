import html
import os
import re

from  lenguatranslator.settings import dict_languages


class OrderBy:
    def pk(pk, frm, to, text):
        return pk, text

    def frm(pk, frm, to, text):
        return frm, text

    def to(pk, frm, to, text):
        return to, text

    def frmto(pk, frm, to, text):
        return "{}->{}".format(frm, to), text

    def all(pk, frm, to, text):
        return "{}:{}->{}".format(pk, frm, to), text

    def getsort(s):
        s = s.strip()
        if s == 'pk':
            return OrderBy.pk
        elif s == 'from':
            return OrderBy.frm
        elif s == 'to':
            return OrderBy.to
        elif s == 'fromto':
            return OrderBy.frmto
        elif s == 'all':
            return OrderBy.all


BASE_DIR = 'management/tools/tmps'
BASE_JSON_DIR = 'management/tools/jsons'


def get_import_options():
    return os.listdir(BASE_JSON_DIR)


def get_options():
    return os.listdir(BASE_DIR)


def get_folder_data(dir, sort):
    result = {}
    folder = "{}/{}".format(BASE_DIR, dir)
    if not os.path.isdir(folder):
        print("Movie is downloaded yet? or just spelling (Enter to folder name)")
        return None
    directory_files = os.listdir(folder)
    for name in directory_files:
        path = "{}/{}".format(folder, name)
        language_code = dict_languages.get(name.split("-")[0].lower(), None)
        # If the extension of the file matches some text followed by ext...
        if not os.path.isfile(path):
            print("Movie {} still has folders in it we are missing some data!")
            print("Please fix manually...")
            continue
        if not language_code:
            print("An Unknown language {} continuing...".format(name.split("-")[0]))
            continue
        else:
            language_code = language_code['code']
        try:
            with open(path, 'r', encoding='utf8') as f:
                result[language_code] = format_subtitle(f.read())
                continue
        except UnicodeDecodeError as e:
            print("language {} UnicodeDecodeError on utf8 {}".format(language_code, e))
        try:
            print("tring Unicode cp1251")
            with open(path, 'r', encoding='cp1251') as f:
                result[language_code] = format_subtitle(f.read())
                print("Unicode cp1251 was ok!")
                continue
        except UnicodeDecodeError as e:
            print("language {} UnicodeDecodeError on cp1251 {}".format(language_code, e))
        try:
            print("tring Unicode ISO-8859-1")
            with open(path, 'r', encoding='ISO-8859-1') as f:
                result[language_code] = format_subtitle(f.read())
                print("Unicode ISO-8859-1 was ok!")
                continue
        except UnicodeDecodeError as e:
            print("language {} UnicodeDecodeError on ISO-8859-1 {}".format(language_code, e))
    return sync_keys_to_languages(result, orderby=sort)


def format_subtitle(raw_str, orderby=OrderBy.frmto, lines_pattern='\n\n',
                    single_pattern=r'(?P<full>(?P<pk>\d+)\n(?P<from>[\d:,]+)[ --> ]+(?P<to>[\d:,]+))'):
    result = {}
    lines = raw_str.split("\n\n")
    for line in lines:
        m = re.match(single_pattern, line)
        if m:
            full, pk, frm, to = m.group('full'), m.group('pk'), m.group('from'), m.group('to')
            line = line.replace(full, "").strip()
            line = html.unescape(line).strip()
            key, value = orderby(pk, frm, to, line)
            result[key] = value
    return result


def sync_keys_to_languages(subtitle_dict, orderby=OrderBy.frmto):
    print("\n\n")
    print("-" * 20, end="")
    print("Syncing")
    print("-" * 20, end="")
    print("...")
    en = subtitle_dict.get('en', None)
    if not en:
        print("No english jsons to work with")

    del subtitle_dict['en']
    strength = {}
    result = {}
    for key in en:
        item = {'en': en[key]}
        for lang in subtitle_dict:
            val = subtitle_dict[lang].get(key, None)
            if val:
                item[lang] = val
                strength[lang] = strength.get(lang, 0) + 1
        result[key] = item

    # We got the json we wanted!
    # I just want to print the strength of the SortBy
    # they vary in result so try different options
    # (pk, only from, only to, from & to, all)
    total = len(en)

    print("Strength of the SortBy: {}".format(orderby.__name__))
    for lang in strength:
        percent = strength[lang] / total * 100
        percent = int(percent / 10)  # Score of 0 - 10
        score = "|{}﴾﴿{}|".format("-" * (percent - 1), "-" * (10 - percent))
        print("{:}:{:>15}".format(lang, score))

    print("Change SortBy: --sort [fromto(DEFAULT), pk,from,to, all]")
    return result


def create_json_from_folder(dir, sort):
    get_folder_data(dir, sort)


def insert_lengua_text(dict):
    pass


def get_json(name):
    return None

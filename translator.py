import html
import re
import uuid
from queue import Queue
from threading import Thread

import requests as r
from django.http import HttpResponseNotFound

from texts.models import LenguaText, OriginalText, SmartText

q_template = '&q={}'
WEB_URL_REGEX = r'(([ ,\.。។।။]+)?(http|ftp|https?\:?\/?\/?)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?([ ,\.。។।။]+)?|(([ ,\.。។।။]+)?(content\:\/\/)([\w.,@?^=%&:/~+#-]+)([ ,\.。។।။]+)?))'
NUMBERS_REGEX = r'(([A-Z\-:=_]+)?[0-9\+]+([A-Z\-:=_]+)?)'
DOTS_REGEX = re.compile(r'(\<br\>|[\.。។।။]+ ?)')
MARKS_REGEX = re.compile(r'( ?[?？؟՞፧!]+ ?)')
TRANSLATABLE = 'text'
NOT_TRANSLATABLE = 'not_text'
MAX_WORD_FOR_REQUEST = 80
str = '''
The regex patterns in this gist are intended only to match web URLs -- http,
https, and naked https://play.google.com/store/apps/details?id=com.facebook.katana domains like "example.com". For a pattern that attempts to
match all URLs, regardless of protocol, see: https://gist.github.com/gruber/249502
'''


# @auditit()
def translate_dot(log, dots, target):
    if dots == "<br>":
        return "<br>"
    if target == 'km':
        return re.sub(DOTS_REGEX, dots, '។') + " "
    elif target == 'ja' or target.startswith('zh'):
        return re.sub(DOTS_REGEX, dots, '。') + " "
    elif target == 'my':
        return re.sub(DOTS_REGEX, dots, '။') + " "
    elif target in ('bn', 'ne', 'hi'):
        return re.sub(DOTS_REGEX, dots, '।') + " "
    else:
        return re.sub(DOTS_REGEX, dots, ".") + " "


# @auditit()
def array_divide_dots(log, mtexts, target):
    texts = mtexts
    ctr = 0
    while texts and ctr < len(texts):
        text, is_text = texts[ctr]
        if is_text == TRANSLATABLE:
            paragraphs = DOTS_REGEX.split(text.strip())
            while paragraphs and not paragraphs[-1]:
                del paragraphs[-1]
            del texts[ctr]
            if not paragraphs:
                continue
            paragraphs = paragraphs[::-1]
            sentences = []
            while len(paragraphs):
                popped = paragraphs.pop()
                if not popped:
                    continue
                if DOTS_REGEX.match(popped):
                    sentences.append((translate_dot(log, popped, target), NOT_TRANSLATABLE))
                else:
                    sentences.append((popped, TRANSLATABLE))
            sentences = sentences[::-1]
            while len(sentences):
                texts.insert(ctr, sentences.pop())
                ctr += 1
        ctr += 1
    return texts


# @auditit()
def array_divide_marks(log, mtexts):
    texts = mtexts
    ctr = 0
    while texts and ctr < len(texts):
        text, is_text = texts[ctr]
        if is_text == TRANSLATABLE:
            paragraphs = MARKS_REGEX.split(text.strip())
            while paragraphs and not paragraphs[-1]:
                del paragraphs[-1]
            del texts[ctr]
            if not paragraphs:
                continue
            paragraphs = paragraphs[::-1]
            sentences = []
            while len(paragraphs):
                popped = paragraphs.pop()
                if not popped:
                    continue
                if MARKS_REGEX.match(popped):
                    if sentences:
                        text, i = sentences[-1]
                        sentences[-1] = ("{}{}".format(text, popped), i)
                    else:
                        text, is_text = (popped, is_text)
                        sentences.insert(0, (text, is_text))

                else:
                    sentences.append((popped, TRANSLATABLE))
            sentences = sentences[::-1]
            while len(sentences):
                texts.insert(ctr, sentences.pop())
                ctr += 1
        ctr += 1
    return texts


# @auditit()
def excape_space_marks(log, mtexts):
    texts = mtexts
    ctr = 0
    while texts and ctr < len(texts):
        text, is_text = texts[ctr]
        if is_text == TRANSLATABLE and (text.endswith("?")
                                        or text.endswith("!")
                                        or text.endswith("؟")
                                        or text.endswith("？")
                                        or text.endswith("፧")
                                        or text.endswith("՞")
                                        ):
            texts[ctr] = (text + " ", TRANSLATABLE)
        ctr += 1
    return texts


# @auditit()
def translate(log, key, original, target):
    '''
    This function is the API for this translator
    It should be able to digest a text with links etc and return an error or VALID text only
    this translator also takes care of the LenguaText cache manipulation therefore no extra steps needed
    just ask and you shall receive.
    :param key: The Langua API key
    :param original: The Original text to translate
    :param target: The target language
    :return: VALID Translated String Or 404
    '''
    original = original.strip()
    texts = divide_string_with_link(log, original)
    texts = array_divide_marks(log, texts)
    texts = array_divide_dots(log, texts, target)
    texts = [(log, key, is_text, text, target, Queue()) for text, is_text in texts]
    threads = []
    for text in texts:
        t = Thread(target=translate_thread, args=text)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    results = excape_space_marks(log, [(t_queue.get(), is_text) for log, key, is_text, text, target, t_queue in texts])
    # Todo: This function should return 404 if the one of the t_queue.get() is 404

    return "".join([res for res, is_text in results]).strip()


# @auditit()
def translate_file(log, key, original, target, content_type):
    '''
    This function is the API for this translator
    It should be able to digest a file with links etc and return an error or VALID text only
    this translator also takes care of the LenguaText cache manipulation therefore no extra steps needed
    just ask and you shall receive.
    :param key: The Langua API key
    :param original: The Original text to translate
    :param target: The target language
    :param content_type: The file type
    :return: VALID Translated String Or 404
    '''
    file_lines = []
    if content_type == 'xml':
        file_lines = divide_string_with_pattern(r'<.+ltexto([^>]+)?>(?P<ltexto>[^<]+)<.+>', original)
    else:
        # Not supported
        return None

    ctr = 0
    while ctr < len(file_lines):
        line, is_translatable = file_lines[ctr]
        if is_translatable == TRANSLATABLE:
            tmp = divide_string_with_link(log, line)
            file_lines[ctr:ctr + 1] = tmp
            ctr = ctr + len(tmp)
        ctr = ctr + 1
    translatable = []
    for key, line in enumerate(file_lines):
        if line[1] == TRANSLATABLE:
            translatable.append(line[0])
    translations = translate_lines_with_smart_cache(log, key, translatable, target)
    translations = translations[::-1]
    file_lines = file_lines[::-1]
    result_file = []
    while len(file_lines) != 0:
        line, is_translate = file_lines.pop()
        if is_translate == TRANSLATABLE:
            result_file.append(translations.pop())
        else:
            result_file.append(line)
    # Todo: This function should return 404 if the one of the t_queue.get() is 404
    return " ".join(result_file).replace("  ", " ")


# @auditit()
def translate_file_to_targets(log, key, text, target, content_type):
    threads = []
    files = {}
    for t in target:
        q = Queue()
        thread = Thread(target=file_thread, args=(log, key, text, t, content_type, q))
        threads.append((t, thread, q))
        thread.start()
    for t, thread, q in threads:
        files[t] = q.get()
    return files


# @auditit()
def file_thread(log, key, text, target, content_type, t_queue):
    t_queue.put(translate_file(log, key, text, target, content_type))


# @auditit()
def translate_thread(log, key, is_text, text, target, t_queue):
    if is_text == TRANSLATABLE:
        t_queue.put(translate_with_smart_cache(log, key, text, target))
    else:
        t_queue.put(text)


# @auditit()
def divide_string_with_link(log, raw_str):
    strs = []
    links = re.findall(WEB_URL_REGEX, raw_str)[::-1]
    if len(links) == 0:
        # There is no links just return the text.
        return [(raw_str, TRANSLATABLE)]
    while len(links) > 0:
        link = links.pop()[0]
        before_link = raw_str.split(link)[0]
        raw_str = raw_str.replace(before_link + link, "")
        strs.append((before_link, TRANSLATABLE if before_link != "\n"
                                                  and before_link != " "
                                                  and before_link != "" else NOT_TRANSLATABLE))
        strs.append((link, NOT_TRANSLATABLE))
    strs.append((raw_str, TRANSLATABLE))
    return strs


# @auditit()
def divide_string_with_pattern(log, pattern, raw_str):
    strs = []
    matches = re.findall(r"(?P<all>{})".format(pattern), raw_str)[::-1]
    if len(matches) == 0:
        # There is no links just return the text.
        return [(raw_str, TRANSLATABLE)]
    while len(matches) > 0:
        link = matches.pop()[0]
        before_link = raw_str.split(link)[0]
        # Removing the ...link from the global string
        raw_str = raw_str.replace(before_link + link, "")
        strs.append((before_link, NOT_TRANSLATABLE))
        # finding the match params
        match = re.match(pattern, link)
        if match is not None and match.group('ltexto') is not None:
            text = match.group('ltexto')
            after_text = link.split(text)
            before_text = after_text[0]
            after_text = after_text[-1]
            strs.append((before_text, NOT_TRANSLATABLE))
            strs.append((text, TRANSLATABLE))
            strs.append((after_text, NOT_TRANSLATABLE))
        else:
            strs.append((link, TRANSLATABLE))
    strs.append((raw_str, NOT_TRANSLATABLE))
    return strs


# @auditit()
def save_original(log, text, original):
    db_original = OriginalText.objects.filter(original=original)
    if len(db_original) != 0:
        db_original = db_original[0]
        db_original.count = db_original.count + 1
        db_original.text = text
    else:
        db_original = OriginalText()
        db_original.original = original
        db_original.text = text
    db_original.save()


# @auditit()
def translate_with_smart_cache(log, key, original, target):
    # check in the db.
    # text = LenguaText.objects.filter(
    #    Q(values__icontains="¾{}½".format(original)) | Q(values__endswith="¾{}".format(original)))
    # very slow ^^
    original = original.strip()
    original, numbers = escape_numbers(log, original)
    # check in the db.
    smart = SmartText.objects.filter(text=original)

    # check if we have the original in the ORIGINAL db.
    if len(smart) == 0:
        db_original = OriginalText.objects.filter(original=original)
        if len(db_original) != 0:
            smart = SmartText()
            smart.text_origin = db_original[0].text
            smart = [smart]
    else:
        tmp = smart[0]
        tmp.count = tmp.count + 1
        tmp.save()

    if len(smart) == 0:
        gt_result = get_google_result(log, key, original, 'en')
        try:
            from_language = gt_result['detectedSourceLanguage']
            en_result = html.unescape(gt_result['translatedText'])
            # Check if we have it in english maybe?
            # check in the db.
            smart = SmartText.objects.filter(text=en_result)
            if len(smart) == 0:
                if from_language == target:
                    return return_numbers(log, original, numbers)
                text = LenguaText()
                text.uuid = uuid.uuid4()
                text.add_translation(en_result, 'en')
                text.save()
                save_smart(log, en_result, text, 'en')
            else:
                text = smart[0].text_origin
        except Exception:
            return gt_result
    else:
        text = smart[0].text_origin

    translation_value = text.get_text(target)
    if translation_value is None:
        gt_result = get_google_result(log, key, text.get_text('en'), target)
        try:
            translation_value = html.unescape(gt_result['translatedText'])
            text.add_translation(translation_value, target)
            text.save()
            save_smart(log, translation_value, text, target)
        except Exception as e:
            return gt_result

    Thread(target=save_original, kwargs={"log": log, "text": text, "original": original}).start()
    return return_numbers(log, translation_value, numbers)


# @auditit()
def translate_lines_with_smart_cache(log, key, original, target):
    textholder = {}
    # getting the lengua english texts
    ltextos = [get_lengua_result(log, key, text.strip(), 'en') for text in original]
    unknown = []
    # are there any unknowns?
    for key, text in enumerate(original):
        if ltextos[key] is None:
            unknown.append(text)
            # unknown get english

    if len(unknown) != 0:
        unknown = get_google_result(log, key, unknown, 'en')[::-1]
        # unknown english process
        for key, text in enumerate(original):
            if ltextos[key] is None:
                # Save the english We didnt find it in the get_lengua_result^^
                t = unknown.pop()
                from_language = t['detectedSourceLanguage']
                t = html.unescape(t['translatedText'])
                ltexto = LenguaText()
                ltexto.uuid = uuid.uuid4()
                ltexto.add_translation(t, 'en')
                ltexto.save()
                textholder[t] = ltexto
                save_smart(log, t, ltexto, 'en')
                ltextos[key] = t, 'en'

    # getting the lengua target texts and resetting unknown
    results = [get_lengua_result(log, key, text, target) for text, language in ltextos]
    unknown = []
    # are there any unknowns?
    for key, text in enumerate(original):
        if results[key][1] is not target:
            unknown.append(ltextos[key][0])
    if len(unknown) != 0:
        # unknown get target
        unknown = get_google_result(log, key, unknown, target)[::-1]
        # unknown target process
        for key, text in enumerate(original):
            if results[key][1] is not target:
                t = unknown.pop()
                from_language = t['detectedSourceLanguage']
                t = html.unescape(t['translatedText'])
                results[key] = t, target
                # Save the english We didnt find it in the get_lengua_result^^
                ltexto = textholder.get(ltextos[key][0], get_lengua_result(log, key, ltextos[key][0]))
                ltexto.add_translation(t, target)
                ltexto.save()
                save_smart(log, t, ltexto, target)

    return [result for result, language in results]


# @auditit()
def save_smart(log, key, text, language):
    smart = SmartText.objects.filter(text=key)
    if len(smart) != 0:
        smart = smart[0]
        smart.count = smart.count + 1
        smart.text = key
        smart.text_origin = text
    else:
        smart = SmartText()
        smart.language = language
        smart.text = key
        smart.text_origin = text
    smart.save()


# @auditit()
def get_lengua_result(log, key, q, target=None):
    q, numbers = escape_numbers(log, q)
    # check in the db.
    smart = SmartText.objects.filter(text=q)

    # check if we have the q in the ORIGINAL db.
    if len(smart) == 0:
        db_original = OriginalText.objects.filter(original=q)
        if len(db_original) != 0:
            smart = SmartText()
            smart.text_origin = db_original[0].text
            smart = [smart]
    else:
        tmp = smart[0]
        tmp.count = tmp.count + 1
        tmp.save()

    if len(smart) == 0:
        return None
    else:
        text = smart[0].text_origin

    if target is None:
        return text

    translation_value = text.get_text(target)
    if translation_value is None:
        return return_numbers(log, text.get_text('en'), numbers), 'en'

    return return_numbers(log, translation_value, numbers), target


# @auditit()
def get_google_result(log, key, q, target):
    arr = False
    if isinstance(q, list):
        if len(q) > MAX_WORD_FOR_REQUEST:
            return get_google_result(log, key, q[:MAX_WORD_FOR_REQUEST], target) + get_google_result(key, q[
                                                                                                          MAX_WORD_FOR_REQUEST:],
                                                                                                     target)
        arr = True
        q = "&q=".join(q)
    gt_result = r.get(
        r'https://www.googleapis.com/language/translate/v2?key=AIzaSyDSiZkiZX4_HLXlGwrVTQv1WmUgqUbZbFc&target={}&q={}'.format(
            target, q))
    if not gt_result.ok:
        return HttpResponseNotFound("<h1>Google Translate Error</h1><br><br>{}".format(gt_result.content))
    try:
        gt_result = gt_result.json()
        if arr:
            gt_result = gt_result['data']['translations']
        else:
            gt_result = gt_result['data']['translations'][-1]
        return gt_result
    except Exception as e:
        return HttpResponseNotFound("<h1>Google Translate API mismatch</h1><br><br>{}".format(gt_result.content))


# @auditit()
def escape_numbers(log, raw_str):
    strs = []
    numbers = []
    links = re.findall(NUMBERS_REGEX, raw_str)[::-1]
    if len(links) == 0:
        # There is no links just return the text.
        return raw_str, numbers
    while len(links) > 0:
        number = links.pop()[0]
        before_link = raw_str.split(number)[0]
        raw_str = raw_str.replace(before_link + number, "")
        strs.append(before_link + '18')
        numbers.append(number)
    strs.append(raw_str)
    return "".join(strs), numbers


# @auditit()
def return_numbers(log, raw_str, numbers):
    if len(numbers) == 0:
        # There is no links just return the text.
        return raw_str
    strs = []
    numbers = numbers[::-1]
    links = re.findall('18', raw_str)[::-1]
    while len(links) > 0:
        fake = links.pop()
        before_link = raw_str.split(fake)[0]
        raw_str = raw_str.replace(before_link + fake, "")
        strs.append(before_link + numbers.pop())
    strs.append(raw_str)
    return "".join(strs)

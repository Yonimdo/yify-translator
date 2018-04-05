import uuid
import requests as r
from django.http import HttpResponseNotFound
from texts.models import LenguaText
import re
from threading import Thread
from queue import Queue
import html

WEB_URL_REGEX = r'(http|ftp|https?\:?\/?\/?)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
TRANSLATABLE = 'text'
NOT_TRANSLATABLE = 'not_text'
str = '''
The regex patterns in this gist are intended only to match web URLs -- http,
https, and naked https://play.google.com/store/apps/details?id=com.facebook.katana domains like "example.com". For a pattern that attempts to
match all URLs, regardless of protocol, see: https://gist.github.com/gruber/249502
'''


def translate(key, original, target):
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
    texts = divide_string_with_link(original)
    texts = [(key, is_text, text, target, Queue()) for text, is_text in texts]
    threads = []
    for text in texts:
        t = Thread(target=translate_thread, args=text)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # Todo: This function should return 404 if the one of the t_queue.get() is 404
    return " ".join([t_queue.get() for key, is_text, text, target, t_queue in texts])


def translate_thread(key, is_text, text, target, t_queue):
    if is_text == TRANSLATABLE:
        t_queue.put(translate_with_cache(key, text, target))
    else:
        t_queue.put(text)


def divide_string_with_link(raw_str):
    strs = []
    links = re.findall(WEB_URL_REGEX, raw_str)[::-1]
    if len(links) == 0:
        # There is no links just return the text.
        return [(raw_str, TRANSLATABLE)]
    while len(links) > 0:
        link = ''.join(links.pop())
        before_link = raw_str.split(link)[0]
        raw_str = raw_str.replace(before_link + link, "")
        strs.append((before_link, TRANSLATABLE if before_link != "\n"
                                                  and before_link != " "
                                                  and before_link != "" else NOT_TRANSLATABLE))
        strs.append((link, NOT_TRANSLATABLE))
    return strs


def translate_with_cache(key, original, target):
    text = LenguaText.objects.filter(values__icontains="¾{}½".format(original))

    if len(text) == 0:
        gt_result = get_google_result(key, original, target)
        try:
            from_language = gt_result['detectedSourceLanguage']
            g_text = html.unescape(gt_result['translatedText'])
            text = LenguaText()
            text.uuid = uuid.uuid4()
            text.add_translation(original, from_language)
            text.add_translation(g_text, target)
            text.save()
        except Exception:
            return gt_result
    else:
        text = text[0]

    translation_value = text.get_text(target)
    if translation_value is None:
        gt_result = get_google_result(key, original, target)
        try:
            g_text = html.unescape(gt_result['translatedText'])
            text.add_translation(g_text, target)
            text.save()
            translation_value = text.get_text(target)
        except Exception:
            return gt_result

    return translation_value


def get_google_result(key, q, target):
    gt_result = r.get(r'https://www.googleapis.com/language/translate/v2', {
        'key': 'AIzaSyDSiZkiZX4_HLXlGwrVTQv1WmUgqUbZbFc',
        'q': q,
        'target': target,
    })
    if not gt_result.ok:
        return HttpResponseNotFound("<h1>Google Translate Error</h1><br><br>{}".format(gt_result.content))
    try:
        gt_result = gt_result.json()
        gt_result = gt_result['data']['translations'][-1]
        return gt_result
    except Exception:
        return HttpResponseNotFound("<h1>Google Translate API mismatch</h1><br><br>{}".format(gt_result.content))

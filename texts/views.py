import json
import re
from urllib import parse as urllib

from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from dauditlog.views import logit
from texts.models import Suggestion
from translator import translate as lenuga_translate


def fix_plus_url(original):
    original.strip()
    ms = re.findall(r'([\+]{4,})', original)[::-1]
    while len(ms):
        m = ms.pop()[0]
        original = original.replace(m, " " * len(m), 1)

    ms = re.findall(r'([\w]([\+]{3})[\w])', original)[::-1]
    while len(ms):
        m = ms.pop()
        original = original.replace(m[0], "{} + {}".format(m[0][0], m[0][-1]), 1)

    ms = re.findall(r'([\w]([\+]{2})[\w])', original)[::-1]
    while len(ms):
        m = ms.pop()
        original = original.replace(m[0], "{} {}".format(m[0][0], m[0][-1]), 1)

    ms = re.findall(r'([[a-zA-Z]([\+])[a-zA-Z])', original)[::-1]
    while len(ms):
        m = ms.pop()
        original = original.replace(m[0], "{} {}".format(m[0][0], m[0][-1]), 1)

    ms = re.findall(r'([\+]{3})', original)[::-1]
    while len(ms):
        m = ms.pop()
        str = m[0].replace("+", " + ")
        original = original.replace(m[0], str, 1)

    ms = re.findall(r'([\+]{2})', original)[::-1]
    return original


@logit()
@csrf_exempt
def translate(request, log):
    if request.GET is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    get = {}
    for val in request.GET:
        get[val] = request.GET[val]

    key = request.GET.get('key', None)
    target = request.GET.get('target', None)
    # original = request.GET.get('q', None)
    query = re.findall(r'&q=[^⑳❾]+', request.build_absolute_uri())
    if not query:
        return HttpResponseNotFound('<h1>Bad request.</h1>')
    original = urllib.unquote(query[0].replace("&q=", ''))
    original = original.split('&target=')[0]
    original = original.split('&key=')[0]
    original = fix_plus_url(original)

    if key != 'AIzaSyDSiZkiZX4_HLXlGwrVTQv1WmUgqUbZbFc':
        return HttpResponseNotFound('<h1>Key not found.</h1>')
    if original is None or original == "":
        return HttpResponseNotFound('<h1>Bad request.</h1>')
    if target is None or target == "":
        return HttpResponseNotFound('<h1>target language is not specified.</h1>')

    translation_value = lenuga_translate(log, key=key, original=original.strip(), target=target)

    return JsonResponse({
        "data": {
            "translations": [
                {
                    "translatedText": translation_value,
                    "detectedSourceLanguage": "",
                }
            ]
        }
    }, json_dumps_params={'ensure_ascii': False}, safe=False)


@logit()
@csrf_exempt
def suggestion(request, log):
    if request.GET is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    data = json.loads(request.body.decode('utf-8'))

    sg = Suggestion()
    sg.original = data.get('original', '')
    sg.translation = data.get('translation', '')
    sg.user_translation = data.get('user_translation', '')
    sg.from_language = data.get('from_language', '')
    sg.to_language = data.get('to_language', '')
    sg.save()

    return JsonResponse({}, json_dumps_params={'ensure_ascii': False}, safe=False)

import uuid

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound

# Create your views here.
from .models import LenguaText
import requests as r


def translate(request):
    if request.GET is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    key = request.GET.get('key', None)
    original = request.GET.get('q', None)
    target = request.GET.get('target', None)

    if key != 'AIzaSyDSiZkiZX4_HLXlGwrVTQv1WmUgqUbZbFc':
        return HttpResponseNotFound('<h1>Key not found.</h1>')
    if original is None or original == "":
        return HttpResponseNotFound('<h1>Bad request.</h1>')
    if target is None or target == "":
        return HttpResponseNotFound('<h1>target language is not specified.</h1>')


    text = LenguaText.objects.filter(values__icontains="¾{}½".format(original))

    if len(text) == 0:
        gt_result = get_google_reeult(key, original, target)
        try:
            from_language = gt_result['detectedSourceLanguage']
            g_text = gt_result['translatedText']
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
        gt_result = get_google_reeult(key, original, target)
        try:
            g_text = gt_result['translatedText']
            text.add_translation(g_text, target)
            text.save()
        except Exception:
            return gt_result

    return JsonResponse({
        "data": {
            "translations": [
                {
                    "translatedText": translation_value,
                    "detectedSourceLanguage": "",
                }
            ]
        }
    })


def get_google_reeult(key, q, target):
    gt_result = r.get(r'https://www.googleapis.com/language/translate/v2', {
        'key': 'AIzaSyDSiZkiZX4_HLXlGwrVTQv1WmUgqUbZbFc',
        'q': q,
        'target': target,
    })
    if not gt_result.ok:
        return HttpResponseNotFound("<h1>Google Translate Error</h1><br><br>{}".format(gt_result.content))
    try:
        gt_result = gt_result.json()
        gt_result = gt_result['data']['translations'][0]
        return gt_result
    except Exception:
        return HttpResponseNotFound("<h1>Google Translate API mismatch</h1><br><br>{}".format(gt_result.content))

import json

from django.http import JsonResponse, HttpResponseNotFound

from translator import translate as lenuga_translate


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

    translation_value = lenuga_translate(key=key, original=original.strip(), target=target)

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

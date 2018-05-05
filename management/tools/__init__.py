import requests
from html2text import HTML2Text


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

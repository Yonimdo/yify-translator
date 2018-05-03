TITLE = "## {}"
SUB = "#### {}"
ERROR = '''
    `{}`
'''
NORMAL = "{}"

BASE_DIR = 'movies/tools/tmps'
BASE_JSON_DIR = 'movies/tools/jsons'


def sublog(text, doc=None):
    if doc:
        doc.log(text)
    print(text)


class SubDoc:
    def __init__(self):
        self.lines = []
    def log(self, line, type=NORMAL):
        self.lines.append(type.format(line))

    def get(self):
        l = '\n'.join(self.lines)
        self.lines = []
        return l

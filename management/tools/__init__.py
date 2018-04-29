TITLE = "## {}"
SUB = "#### {}"
ERROR = '''
    `{}`
'''
NORMAL = "{}"


def sublog(text, doc=None):
    if doc:
        doc.log(text)
    print(text)


class SubDoc:
    lines = []

    def log(self, line, type=NORMAL):
        self.lines.append(type.format(line))

    def get(self):
        return '\n'.join(self.lines)

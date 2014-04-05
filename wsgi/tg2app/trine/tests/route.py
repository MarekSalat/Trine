import re

__author__ = 'Marek'


class Route:
    RE_ID = r'[\w]+'
    RE_CONTROLLER = RE_ID
    RE_ACTION = RE_ID
    RE_PLACEHOLDER = r'[^/]+'

    def __init__(self, patter: str, name: str=None, defaults: dict={}):
        self.originalPattern = patter

        patter = re.sub(r'\[', '(', patter)
        patter = re.sub(r']', ')?', patter)

        patter.replace('{controller}', self.RE_CONTROLLER)
        patter.replace('{action}', self.RE_ACTION)
        patter = re.sub(r'{%s}' % self.RE_ID, self.RE_ID, patter)
        patter += '(\?.*)?'

        self.pattern = patter
        self.name = name
        self.defaults = defaults

    def match(self, url):
        url = re.sub(r'/$', '', url)
        url = re.sub(r'/\?', '?', url)

        result = re.match(self.pattern, url)
        if not result is None:
            return result.group(0)

        return None

    def generate(self, url, **kwargs):
        pass

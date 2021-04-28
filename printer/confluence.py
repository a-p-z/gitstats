from typing import List

from core.model.author import Author
from printer.formatter import Formatter


class ConfluenceWikiFormatter(Formatter):

    def __init__(self):
        pass

    def section(self):
        return "{section}"

    def column(self):
        return "{column}"

    def sep(self):
        return "----"

    def h2(self, title):
        return "h2. " + title

    def h3(self, title):
        return "h3. " + title

    def h6(self, title):
        return "h6. " + title

    def link(self, alias, url):
        return "[%s|%s]" % (alias, url)

    def bold(self, text):
        return "*%s*" % text

    def chart(self, header, data, confluence=None, md=None):
        confluence = map(lambda x: (x[0], str(x[1])), confluence.items())
        confluence = "|".join(map(lambda x: "%s=%s" % x, confluence))
        table = self.table(header, data)
        return "\n".join(["{chart:%s}" % confluence, table, "{chart}"])

    def table(self, header, data: List[List], md=None):
        header = map(lambda x: x.username if isinstance(x, Author) else x, header)
        header = "||%s||" % "||".join(header)
        data = map(lambda x: map(str, x) if isinstance(x, list) or isinstance(x, tuple) else [str(x)], data)
        data = map(lambda x: "|%s|" % "|".join(x), data)
        data = "\n".join(data)
        return "\n".join([header, data])

    def card(self, title, text, data):
        options = map(lambda x: (x[0], str(x[1])), {"borderColor": "#999999", "bgColor": "#f5f5f5"}.items())
        options = "|".join(map(lambda x: "%s=%s" % x, options))
        title = self.h3(title)
        profile = self.profile(data[0][0])
        description = text % (data[0][1], data[1][0].name, data[1][1], data[2][0].name, data[2][1])
        return "\n".join(["{panel:%s}" % options, title, profile, description, "{panel}"])

    def profile(self, author):
        return "{profile: user = %s}" % author.username if isinstance(author, Author) else author

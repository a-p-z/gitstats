from typing import List

from core.model.author import Author
from core.utilities import apply_to_column
from printer.formatter import Formatter


class MarkdownFormatter(Formatter):

    def __init__(self):
        pass

    def section(self):
        return ""

    def column(self):
        return ""

    def sep(self):
        return "\n ---"

    def h2(self, title):
        return "## %s" % title

    def h3(self, title):
        return "### %s" % title

    def h6(self, title):
        return "###### %s" % title

    def link(self, alias, url):
        return "[%s](%s)" % (alias, url)

    def bold(self, text):
        return "**%s**" % text

    def chart(self, header, data, confluence=None, md=None):
        apply_to_column(data, 0, self.bold)
        return self.table(header, data, md=md)

    def table(self, header, data: List[List], md=None):
        separator = md if md else "|%s|" % "|".join(["---"] * len(header))
        header = list(map(lambda author: author.name if isinstance(author, Author) else author, header))
        header = "|%s|" % "|".join(header)
        data = map(lambda x: map(str, x) if isinstance(x, list) or isinstance(x, tuple) else [str(x)], data)
        data = list(map(lambda x: "|%s|" % "|".join(x), data))
        data = "\n".join(data)
        return "\n".join([header, separator, data])

    def card(self, title, text, data):
        title = self.h3(title)
        profile = self.profile(data[0][0])
        description = text % (data[0][1], data[1][0].name, data[1][1], data[2][0].name, data[2][1])
        return "\n".join([title, profile, description])

    def profile(self, author):
        return self.bold(author.name if isinstance(author, Author) else author)

from typing import List


class Formatter:

    def print(self):
        pass

    def section(self):
        pass

    def column(self):
        pass

    def sep(self):
        pass

    def h2(self, title):
        pass

    def h3(self, title):
        pass

    def h6(self, title):
        pass

    def link(self, alias, url):
        pass

    def bold(self, text):
        pass

    def chart(self, header, data, confluence=None, md=None):
        pass

    def table(self, header, data: List[List], md=None):
        pass

    def card(self, title, text, data):
        pass

    def profile(self, author):
        pass

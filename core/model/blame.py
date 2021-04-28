import re

from core.mailmap import Mailmap
from core.model.author import Author


class Blame:

    def __init__(self, _hash: str, author: Author, committer: Author, summary: str, filename: str, content: str):
        self.hash = _hash
        self.author = author
        self.committer = committer
        self.summary = summary
        self.file = filename
        self.content = content

    def __getitem__(self, item):
        return getattr(self, item)

    @staticmethod
    def of(raw_git_blame):
        _hash = None
        author = Author("", "", "")
        committer = Author("", "", "")
        summary = None
        filename = None
        content = None

        for line in raw_git_blame.split("\n"):
            if line.startswith("author ") and len(author.name) == 0:
                author.name = line[7:]

            elif line.startswith("author-mail ") and len(author.email) == 0:
                email = line[13:-1].lower()
                author = Mailmap.get_or_default(author.name, email)

            elif line.startswith("committer ") and len(committer.name) == 0:
                committer.name = line[10:]

            elif line.startswith("committer-mail ") and len(committer.email) == 0:
                email = line[16:-1].lower()
                committer.email = Mailmap.get_or_default(committer.name, email)

            elif line.startswith("summary "):
                summary = line[8:]

            elif line.startswith("filename "):
                filename = line[9:]

            elif line.startswith("\t"):
                content = line[1:]

            elif re.match(r".{,40} \d+ \d+", line):
                _hash = line[:40]

        return Blame(_hash, author, committer, summary, filename, content)

    def is_valid(self):
        return self.hash and \
               self.author.name and \
               self.author.email and \
               self.committer.name and \
               self.committer.email and \
               self.summary and \
               self.file

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
        summary = None
        filename = None
        content = None
        author_name = None
        author_email = None
        committer_name = None
        committer_email = None

        for line in raw_git_blame.split("\n"):
            if line.startswith("author "):
                author_name = line[7:]

            elif line.startswith("author-mail "):
                author_email = line[13:-1].lower()

            elif line.startswith("committer "):
                committer_name = line[10:]

            elif line.startswith("committer-mail "):
                committer_email = line[16:-1].lower()

            elif line.startswith("summary "):
                summary = line[8:]

            elif line.startswith("filename "):
                filename = line[9:]

            elif line.startswith("\t"):
                content = line[1:]

            elif re.match(r".{,40} \d+ \d+", line):
                _hash = line[:40]

        author = Mailmap.instance().get(author_name, author_email)
        committer = Mailmap.instance().get(committer_name, committer_email)
        return Blame(_hash, author, committer, summary, filename, content)

    def is_valid(self):
        return self.hash and \
               self.author.name and \
               self.author.email and \
               self.committer.name and \
               self.committer.email and \
               self.summary and \
               self.file

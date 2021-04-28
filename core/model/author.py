from datetime import datetime


class Author:

    def __init__(self, name: str, email: str, username: str = None):
        self.name = name
        self.email = email.lower()
        self.username = username if username else email.partition("@")[0]
        self.start = datetime.max
        self.end = datetime.min

    def register_active_date(self, date):
        if not date:
            return
        self.start = min(date, self.start)
        self.end = max(date, self.end)

    def is_active(self):
        return (datetime.now() - self.end).days <= 30

    def __str__(self):
        return self.email

    def __eq__(self, other):
        return self.email == other.email

    def __lt__(self, other):
        return self.start < other.start

    def __hash__(self):
        return hash(self.email)

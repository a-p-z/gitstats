import logging
import os
from typing import Dict

import yaml

from core.model.author import Author


class Mailmap:
    _instance = None

    def __init__(self):
        self.authors_by_email = Mailmap.__authors_by_email()

    def register_active_date(self, author, date):
        if not date:
            return
        for a in filter(lambda x: x == author, self.authors_by_email.values()):
            a.register_active_date(date)

    def get_by_username(self, username, date=None):
        authors = list(filter(lambda x: x.username == username, self.authors_by_email.values()))
        if len(authors) == 0:
            logging.warning("%s not found in mailmap.yaml", username)
            authors.append(Author(username, username, username))
            Mailmap.instance().authors_by_email[username] = Author(username, username, username)
        author = Mailmap.instance().authors_by_email.get(authors[0].email)
        Mailmap.instance().register_active_date(author, date)
        return author

    @staticmethod
    def get_or_default(name, email, date=None):
        email = email.lower()
        if email not in Mailmap.instance().authors_by_email.keys():
            logging.warning("%s not found in mailmap.yaml", email)
            Mailmap.instance().authors_by_email[email] = Author(name, email)
        author = Mailmap.instance().authors_by_email.get(email)
        Mailmap.instance().register_active_date(author, date)
        return author

    @staticmethod
    def instance():
        if not Mailmap._instance:
            Mailmap._instance = Mailmap()
        return Mailmap._instance

    @staticmethod
    def __authors_by_email() -> Dict[str, Author]:
        script_dir = os.path.dirname(__file__)
        mailmap_yaml = os.path.join(script_dir, r"../resources/mailmap.yaml")
        if not os.path.isfile(mailmap_yaml):
            return {}
        with open(mailmap_yaml) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            mailmap = yaml.load(file, Loader=yaml.FullLoader)
            _authors_by_email: Dict[str, Author] = dict()
            for username in mailmap.keys():
                name = mailmap[username]["name"]
                email = mailmap[username]["email"]
                _authors_by_email[email] = Author(name, email, username)
                for alias in mailmap[username].get("aliases", []):
                    _authors_by_email[alias] = Author(name, email, username)
            return _authors_by_email

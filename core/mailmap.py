from __future__ import annotations
import logging
import os
from datetime import datetime
from typing import Dict, Set

import yaml

from core.model.author import Author


class Mailmap:
    _instance = None

    def __init__(self):
        self.__authors = Mailmap.__load_authors_from_mailmap_yaml()

    def get(self, name, email, date=None) -> Author:
        email = email.lower()
        if email not in self.__authors.keys():
            logging.warning("%s not found in mailmap.yaml", email)
            return self.__add(name, email)
        author = self.__authors.get(email)
        self.__register_active_date(author, date)
        return author

    def get_all(self) -> Set[Author]:
        return set(self.__authors.values())

    def get_dict(self) -> Dict[str, Author]:
        return self.__authors

    def set_dict(self, authors):
        self.__authors = authors

    @staticmethod
    def instance() -> Mailmap:
        if not Mailmap._instance:
            Mailmap._instance = Mailmap()
        return Mailmap._instance

    @staticmethod
    def __load_authors_from_mailmap_yaml() -> Dict[str, Author]:
        script_dir = os.path.dirname(__file__)
        mailmap_yaml = os.path.join(script_dir, r"../resources/mailmap.yaml")
        if not os.path.isfile(mailmap_yaml):
            return {}
        with open(mailmap_yaml) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            mailmap = yaml.load(file, Loader=yaml.FullLoader)
            authors: Dict[str, Author] = dict()
            for username in mailmap.keys():
                name = mailmap[username]["name"]
                email = mailmap[username]["email"]
                author = Author(name, email, username)
                authors[email] = author
                authors[username] = author
                for alias in mailmap[username].get("aliases", []):
                    authors[alias] = author
            return authors

    def __register_active_date(self, _author, date):
        if not date:
            return
        for author in self.__authors.values():
            if author == _author:
                author.register_active_date(date)

    def __add(self, name: str, email: str, username: str = None, date: datetime = None) -> Author:
        author = Author(name, email, username)
        author.register_active_date(date)
        self.__authors[email] = author
        self.__authors[username] = author
        return author

import logging
import os

import yaml


class Regexes:
    _instance = None

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        regexes_yaml = os.path.join(script_dir, r"../resources/regexes.yaml")
        if not os.path.isfile(regexes_yaml):
            self.subject_regexes = []
            self.reviewer_regex = None
            return
        with open(regexes_yaml) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            regexes = yaml.load(file, Loader=yaml.FullLoader)
            self.subject_regexes = regexes.get("subject_regexes", []) if regexes else []
            self.reviewer_regex = regexes.get("reviewer_regex", None) if regexes else None

    @staticmethod
    def instance():
        if not Regexes._instance:
            Regexes._instance = Regexes()
        return Regexes._instance

import re

HASH_PATTERN = re.compile(r"[0-9a-f]{40}")

LOG_PATTERN = re.compile(r"(\d+|-)\t(\d+|-)\t.*")

LOG_PRETTY = (
    "tformat:"
    "hash %H%n"
    "author-date %aI%n"
    "author-email %aE%n"
    "author-name %aN%n"
    "committer-date %cI%n"
    "committer-email %cE%n"
    "committer-name %cN%n"
    "parent %P%n"
    "subject %s"
)

LOG_NUMSTAT_PRETTY = "tformat:hash %H"

REF_FORMAT = (
    "name %(refname) " "author-name %(authorname) " "author-email %(authoremail) " "date %(" "committerdate:iso8601)"
)

REF_REMOTE_PATTERN = re.compile(r"name (.*) author-name (.*) author-email (<.*>) date (.*)")

SHORT_LOGS_PATTERN = re.compile(r"\s*(\d+)\t(.+) <(.+)>")

USERNAME_MAP_PATTERN = re.compile(r"([\w ]+) (<[\w._%+-]+@[\w.-]+>)")

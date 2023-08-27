import binascii
import os
import random
import sys
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock

from dateutil.relativedelta import relativedelta
from git import Git
from importlib_resources import files

from gitstats.data.model.author import Author
from gitstats.data.model.blame import Blame
from gitstats.data.model.diffstat import Diffstat
from gitstats.data.model.file import File
from gitstats.data.model.log import Log
from gitstats.data.model.numstat import Numstat
from gitstats.data.model.ref import Ref
from gitstats.data.model.shortlog import ShortLog


def an_author(start: datetime | None = None, end: datetime | None = None) -> Author:
    start = start if start else datetime.now(tz=UTC) - timedelta(30)
    end = end if end else datetime.now(tz=UTC)
    name, email, username = random.choice(
        [
            ("Romolo", "romolo@gitstats.org", "romolo"),
            ("Numa Pompilio", "numa.pompilio@gitstats.org", "pompnum"),
            ("Tullo Ostilio", "tullo.ostilio@gitstats.org", "ostitul"),
            ("Anco Marzio", "anco.marzio@gitstats.org", "marzanc"),
            ("Tarquinio Prisco", "tarquinio.prisco@gitstats.org", "pristar"),
            ("Servio Tullio", "servio.tullio@gitstats.org", "tullser"),
            ("Tarquinio il Superbo", "tarquinio.il.superbo.@gitstats.org", "supetar"),
        ]
    )
    return Author(name, email, start, end, username)


def a_base_uri() -> str:
    return f"https://base-uri{random.randint(0, sys.maxsize)}"


def a_blame(
    hash_: str | None = None,
    author: Author | None = None,
    committer: Author | None = None,
    summary: str | None = None,
    filename: str | None = None,
    content: str | None = None,
) -> Blame:
    hash_ = hash_ or a_hash()
    author = author or an_author()
    committer = committer or an_author()
    summary = summary or a_summary()
    filename = filename or a_filename()
    content = a_content() if content is None else content
    return Blame(hash_, author, committer, summary, File(filename), content)


def a_content() -> str:
    return " ".join(
        random.choices(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
            "incididunt ut labore et "
            "dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco "
            "laboris nisi ut aliquip "
            "ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit "
            "esse cillum dolore eu "
            "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa "
            "qui officia deserunt "
            "mollit anim id est laborum.".split(" "),
            k=5,
        )
    )


def a_date(start=None, end=None, fmt=None) -> str:
    start = datetime.now(tz=UTC) - relativedelta(days=1, microsecond=0) if start is None else start
    end = datetime.now(tz=UTC) if end is None else end
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    date = start + timedelta(seconds=random_second)
    return date.isoformat() if fmt is None else date.strftime(fmt)


def a_diffstat(hash=None, filename=None, insertions=None, deletions=None) -> Diffstat:
    hash = hash or a_hash()
    filename = a_filename() if filename is None else filename
    insertions = random.randint(0, sys.maxsize) if insertions is None else insertions
    deletions = random.randint(0, sys.maxsize) if deletions is None else deletions
    return Diffstat(hash, File(filename), insertions, deletions)


def a_filename(ext: str | None = None) -> str:
    ext = ext if ext else random.choice(["java", "kt", "groovy", "js", "ts", "css", "json", "sql"])
    return f"file-{random.randint(0, sys.maxsize)}.{ext}"


def a_file(ext: str | None = None) -> File:
    return File(f"./{a_filename(ext)}")


def a_hash() -> str:
    return binascii.b2a_hex(os.urandom(20)).decode()


def a_content_id() -> int:
    return random.randint(0, sys.maxsize)


def a_log(
    hash_=None,
    parent=None,
    date_=None,
    subject=None,
    author=None,
    committer=None,
    diffstats=None,
) -> Log:
    hash_ = hash_ or a_hash()
    parent = parent or a_hash()
    date_ = datetime.fromisoformat(a_date()) if date_ is None else datetime.fromisoformat(date_)
    subject = subject or a_subject()
    author = author or an_author()
    committer = committer or an_author()
    diffstats = diffstats or []
    return Log(hash_, parent, date_, subject, author, committer, diffstats)


def a_numstat(
    hash_=None,
    parent=None,
    date_=None,
    subject=None,
    author=None,
    committer=None,
    filename=None,
    insertions=0,
    deletions=0,
) -> Numstat:
    hash_ = hash_ or a_hash()
    parent = parent or a_hash()
    date_ = datetime.fromisoformat(a_date()) if date_ is None else datetime.fromisoformat(date_)
    subject = subject or a_subject()
    author = author or an_author()
    committer = committer or an_author()

    return Numstat(
        hash_,
        parent,
        date_,
        subject,
        author,
        committer,
        filename,
        insertions,
        deletions,
    )


def a_password() -> str:
    return f"password{random.randint(0, sys.maxsize)}"


def a_ref(name=None, author=None, date=None) -> Ref:
    name = a_ref_name() if name is None else name
    author = an_author() if author is None else author
    date_ = datetime.fromisoformat(a_date()) if date is None else datetime.fromisoformat(date)
    return Ref(name, author, date_)


def a_ref_name() -> str:
    return f"refs/remotes/origin/{random.randint(0, sys.maxsize)}"


def a_subject() -> str:
    return f"subject {random.randint(0, sys.maxsize)}"


def a_summary() -> str:
    return f"summary {random.randint(0, sys.maxsize)}"


def a_title() -> str:
    return f"title {random.randint(0, sys.maxsize)}"


def a_username() -> str:
    return f"username {random.randint(0, sys.maxsize)}"


def a_value() -> str:
    return f"value {random.randint(0, sys.maxsize)}"


def a_version() -> int:
    return random.randint(0, sys.maxsize)


def another_author(*authors) -> Author:
    author = an_author()
    while author in authors:
        author = an_author()
    return author


def a_shortlog(author: Author = an_author(), commits: int = random.randint(0, sys.maxsize)) -> ShortLog:
    return ShortLog(author, commits)


def mock_scope_resolver(interface):
    resources = files("tests") / "resources"

    if interface == "users":
        return []

    if interface == Git:
        git = MagicMock()
        git.log.side_effect = (
            lambda date, pretty, numstat=False: (resources / "log_numstat").read_text()  # noqa: ARG005
            if numstat
            else (resources / "log").read_text()
        )
        git.for_each_ref.return_value = (files("tests") / "resources" / "for_each_ref").read_text()
        git.ls_files.return_value = (
            "resources/binary_file\n"
            "resources/blame_1\n"
            "resources/blame_2\n"
            "resources/empty_file\n"
            "resources/not_exist"
        )
        git.rev_list.return_value = "42"
        git.shortlog.return_value = (files("tests") / "resources" / "shortlog").read_text()
        git.blame.side_effect = lambda file, line_porcelain: (files("tests") / file).read_text()  # noqa: ARG005
        git.working_dir = str(files("tests"))

        return git

    return MagicMock()


def mock_scope_resolver_with_username_map(interface):
    resources = files("tests") / "resources"

    if interface == "users":
        return [
            {"email": "numa.pompilio@gitstats.org", "username": "Numa Pompilio"},
            {"email": "romolo1@gitstats.org", "username": "Romolo"},
            {"email": "romolo@gitstats.org", "username": "Romolo"},
            {"email": "tarquinio.il.superbo.@gitstats.org", "username": "Tarquinio il Superbo"},
        ]  # TODO await get_usernames(str(resources / "username_map"))

    if interface == Git:
        git = MagicMock()
        git.log.side_effect = (
            lambda date, pretty, numstat=False: (resources / "log_numstat").read_text()  # noqa: ARG005
            if numstat
            else (resources / "log").read_text()
        )
        return git

    return MagicMock()


def clear_cache():
    from gitstats.data.authors import get_authors
    from gitstats.data.authors import get_authors_by_email
    from gitstats.data.blames import get_blames
    from gitstats.data.committers import get_committers
    from gitstats.data.committers import get_committers_by_email
    from gitstats.data.files import get_files
    from gitstats.data.logs import get_diffstats
    from gitstats.data.logs import get_diffstats_by_hash
    from gitstats.data.logs import get_logs
    from gitstats.data.numstats import get_numstats
    from gitstats.data.references import get_origin_remote_references
    from gitstats.data.reviewers import get_reviewers
    from gitstats.data.shortlog import get_commits
    from gitstats.data.shortlog import get_merges
    from gitstats.infrastructure.git.blame import blame
    from gitstats.infrastructure.git.files import files
    from gitstats.infrastructure.git.log import log
    from gitstats.infrastructure.git.log import log_numstat
    from gitstats.infrastructure.git.refs_remotes_origin import refs_remotes_origin
    from gitstats.infrastructure.git.rev_list import rev_list_no_merges_count_head
    from gitstats.infrastructure.git.shortlog import shortlog_merges
    from gitstats.infrastructure.git.shortlog import shortlog_no_merges
    from gitstats.infrastructure.git.usernames import get_usernames_by_email

    blame.cache._cache.clear()
    files.cache._cache.clear()
    get_authors.cache._cache.clear()
    get_authors_by_email.cache._cache.clear()
    get_blames.cache._cache.clear()
    get_commits.cache._cache.clear()
    get_committers.cache._cache.clear()
    get_committers_by_email.cache._cache.clear()
    get_diffstats.cache._cache.clear()
    get_diffstats_by_hash.cache._cache.clear()
    get_files.cache._cache.clear()
    get_logs.cache._cache.clear()
    get_merges.cache._cache.clear()
    get_numstats.cache._cache.clear()
    get_origin_remote_references.cache._cache.clear()
    get_reviewers.cache._cache.clear()
    get_usernames_by_email.cache._cache.clear()
    log.cache._cache.clear()
    log_numstat.cache._cache.clear()
    refs_remotes_origin.cache._cache.clear()
    rev_list_no_merges_count_head.cache._cache.clear()
    shortlog_merges.cache._cache.clear()
    shortlog_no_merges.cache._cache.clear()

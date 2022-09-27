import logging
import re
from collections import defaultdict
from typing import Tuple, List, Dict, Any

from core import gitls, gitforeachref
from core.mailmap import Mailmap
from core.model.author import Author
from core.model.blame import Blame
from core.model.fileType import FileType
from core.model.numstat import Numstat
from core.utilities import second_column, aggregate_and_sum, first_column


def count_commits_and_impacts_by_author(numstat: List[Numstat]) -> List[List]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :return: list of [author, email, commits, insertions, deletions]
    """
    logging.info("counting commits and impacts by author")
    email_by_author = {
        x.author: x.email for x in numstat 
    }
    insertions_by_author = aggregate_and_sum(numstat, "author", "insertions")
    deletions_by_author = aggregate_and_sum(numstat, "author", "deletions")
    numstat = __unique_by(numstat, "hash")
    commits_by_author = __count_by_attr(numstat, "author")


    author_commits_insertions_deletions = list()
    for author in sorted(insertions_by_author.keys()):
        email = email_by_author[author]
        commits = commits_by_author[author]
        insertions = insertions_by_author[author]
        deletions = deletions_by_author[author]
        author_commits_insertions_deletions.append([author, commits, insertions, deletions, email])

    return sorted(author_commits_insertions_deletions, key=second_column, reverse=True)


def count_commits_and_impacts_by_author_and_date(numstat_date: List[Numstat]) -> List[List]:
    """
    :param numstat_date: result of :func: git_log_numstat_no_merge_date
    :return: list of [author, emails, commits, insertions, deletions]
    """
    logging.info("counting commits and impacts by author and date")
    email_by_author = {
        x.author: x.email for x in numstat_date 
    }
    insertions_by_author = aggregate_and_sum(numstat_date, "author", "insertions")
    deletions_by_author = aggregate_and_sum(numstat_date, "author", "deletions")
    numstat_date = __unique_by(numstat_date, "hash")
    commits_by_author = __count_by_attr(numstat_date, "author")


    author_commits_insertions_deletions = list()
    for author in sorted(insertions_by_author.keys()):
        email = email_by_author[author]
        commits = commits_by_author[author]
        insertions = insertions_by_author[author]
        deletions = deletions_by_author[author]
        author_commits_insertions_deletions.append([author, commits, insertions, deletions, email])

    return sorted(author_commits_insertions_deletions, key=second_column, reverse=True)


def count_commits_on_behalf_of(numstat: List[Numstat]) -> Tuple[List, List[List]]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :return: list of [committer, commits, author]
    """
    logging.info("counting commits and on behalf of")
    commits_on_behalf_of = defaultdict(lambda: defaultdict(int))

    numstat = __unique_by(numstat, "hash")
    numstat = filter(lambda x: x.author != x.committer, numstat)
    authors = set()
    for n in numstat:
        commits_on_behalf_of[n.committer][n.author] += 1
        authors.add(n.author)

    authors = sorted(authors)
    header = ["    ┌─> author\ncommitter"]
    header.extend(authors)

    data = list()
    for committer in sorted(commits_on_behalf_of.keys()):
        data.append([committer] + list(map(lambda author: commits_on_behalf_of[committer][author], authors)))

    return header, data


def count_deletion_ratio_by_author(numstat: List[Numstat], file_types: List[FileType]) -> List[List]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :param file_types: list of file types
    :return: list of [author, deletion_ratio]
    """
    logging.info("counting deletion ratio by author")
    numstat = list(filter(lambda n: FileType.any_match(file_types, n.file), numstat))
    deletions_by_author = aggregate_and_sum(numstat, "author", "deletions")
    numstat = __unique_by(numstat, "hash")
    commits_by_author = __count_by_attr(numstat, "author")

    author_deletion_ratio = list()
    for author in commits_by_author.keys():
        deletion_ratio = deletions_by_author[author] / commits_by_author[author]
        author_deletion_ratio.append([author, deletion_ratio])
    return sorted(author_deletion_ratio, key=second_column, reverse=True)


def count_commits_over_month_by_author(numstat: List[Numstat]) -> Tuple[List, List[List]]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :return: ["date", "author1", "author2", ...], [[ date ,     n1   ,     n2   , ...],
                                                    ... ]
    """
    logging.info("counting commits over month by author")
    authors = set()
    aggregate_by_month_and_author = defaultdict(lambda: defaultdict(set))

    for n in numstat:
        date = n.date.strftime("%Y-%m")
        aggregate_by_month_and_author[date][n.author].add(n.hash)
        authors.add(n.author)

    authors = sorted(authors)
    header = ["date"]
    header.extend(authors)

    commits_over_month_by_author = list()
    for date in sorted(aggregate_by_month_and_author.keys()):
        commits = [date]
        commits.extend(map(lambda author: len(aggregate_by_month_and_author[date][author]), authors))
        commits_over_month_by_author.append(commits)
    commits_over_month_by_author[-1][0] = "now"
    return header, commits_over_month_by_author


def get_impacts_over_month(numstat: List[Numstat]) -> List[List]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :return: list of [date, insertions, deletions]
    """
    logging.info("calculating impacts over month")
    aggregate_by_date = defaultdict(lambda: defaultdict(int))
    for n in numstat:
        date = n.date.strftime("%Y-%m")
        aggregate_by_date[date]["insertions"] += n.insertions
        aggregate_by_date[date]["deletions"] += n.deletions

    impacts_over_month = list()
    for date in sorted(aggregate_by_date.keys()):
        label = date
        insertions = aggregate_by_date[date]["insertions"]
        deletions = aggregate_by_date[date]["deletions"]
        impacts_over_month.append([label, insertions, deletions])
    impacts_over_month[-1][0] = "now"
    return impacts_over_month


def count_edited_lines_of_code_by_author(blame: List[Blame],
                                         file_types: List[FileType],
                                         content_regex: str = r".*") -> List[List]:
    """
    :param blame:result of :func: git_blame
    :param file_types: list of file types
    :param content_regex: regular expression pattern
    :return: list of [author, eloc]
    """
    logging.info("counting edited lines of code by author for [%s] and content=%s",
                 ", ".join(map(str, file_types)),
                 content_regex)
    content_regex = re.compile(content_regex, flags=re.IGNORECASE)

    blame = list(filter(lambda x:
                        FileType.any_match(file_types, x.file) and
                        x.content and
                        content_regex.match(x.content),
                        blame))

    edited_lines_of_code_by_author = __count_by_attr(blame, "author")
    edited_lines_of_code_by_author = map(list, edited_lines_of_code_by_author.items())
    return sorted(edited_lines_of_code_by_author, key=second_column, reverse=True)


def count_edited_lines_of_code_and_stability_by_author(numstat: List[Numstat],
                                                       blame: List[Blame],
                                                       file_types: List[FileType]) -> List[List]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :param blame:result of :func: git_blame
    :param file_types: list of file types
    :return: list of [author, eloc, stability]
    """
    logging.info("counting edited lines of code and stability by author for [%s]", ", ".join(map(str, file_types)))

    blame = list(filter(lambda x: FileType.any_match(file_types, x.file) and x.content, blame))
    edited_lines_of_code_by_author = __count_by_attr(blame, "author")

    numstat = list(filter(lambda x: FileType.any_match(file_types, x.file), numstat))
    insertions_by_author = aggregate_and_sum(numstat, "author", "insertions")

    author_eloc_stability = list()
    for author in insertions_by_author.keys():
        eloc = edited_lines_of_code_by_author[author]
        insertions = insertions_by_author[author]
        try:
            stability = float("{:.2f}".format(100 * eloc / insertions))
        except ZeroDivisionError:
            stability = 100.00
        author_eloc_stability.append([author, eloc, stability])
    return sorted(author_eloc_stability, key=second_column, reverse=True)


def count_empty_lines_of_code_by_author(blame: List[Blame], file_types: List[FileType]) -> List[List]:
    """
    :param blame: result of :func: git_blame
    :param file_types: list of file types
    :return: list of [author, eloc]
    """
    logging.info("counting empty lines of code by author for [%s]", ", ".join(map(str, file_types)))
    blame = list(filter(lambda x:
                        FileType.any_match(file_types, x.file) and
                        x.content and
                        not x.content.strip(),
                        blame))

    empty_lines_of_code_by_author = __count_by_attr(blame, "author")
    empty_lines_of_code_by_author = map(list, empty_lines_of_code_by_author.items())
    return sorted(empty_lines_of_code_by_author, key=second_column, reverse=True)


def count_files_by_extension() -> List[List]:
    """
    :return: list of [ext, num]
    """
    logging.info("counting files by extension")
    extensions = map(lambda file: file.split(".")[-1] if "." in file else "NO EXT", gitls.git_ls_files())

    files_by_extension = defaultdict(int)
    for extension in extensions:
        files_by_extension[extension] += 1

    extension_num = map(list, files_by_extension.items())
    return sorted(extension_num, key=second_column, reverse=True)


def get_most_frequently_committed_files(numstat: List[Numstat]) -> List[List]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :return: list of [file, commits]
    """
    logging.info("getting most frequently committed files")
    commit_by_file = __count_by_attr(numstat, "file")
    file_commits = map(list, commit_by_file.items())
    return sorted(file_commits, key=second_column, reverse=True)


def sorted_commits_by_impact(numstat: List[Numstat]) -> List[List]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :return: list of [date, subject, author, num_of_files, insertions, deletions]
    """
    logging.info("ordering commits by impact")
    commits = defaultdict(lambda: ["0000-00-00", "", Author("", "", ""), 0, 0, 0])

    for n in numstat:
        commits[n.hash][0] = n.date.strftime("%Y-%m-%d")
        commits[n.hash][1] = n.subject
        commits[n.hash][2] = n.author
        commits[n.hash][3] += 1
        commits[n.hash][4] += n.insertions
        commits[n.hash][5] += n.deletions

    date_subject_author_num_of_files_insertions_deletions = commits.values()
    return sorted(date_subject_author_num_of_files_insertions_deletions, key=lambda x: x[4] + x[5], reverse=True)


def sorted_refs_remotes_origin_by_date() -> List[List]:
    """
    :return: list of [date, author, ref]
    """
    return sorted(gitforeachref.git_refs_remotes_origin(), key=first_column)


def count_refs_remotes_origin_by_author() -> List[List]:
    """
    :return: list of [author, total]
    """
    refs_remotes_origin_by_author = defaultdict(int)
    for item in gitforeachref.git_refs_remotes_origin():
        refs_remotes_origin_by_author[item[1]] += 1
    refs_remotes_origin_by_author = map(list, refs_remotes_origin_by_author.items())
    return sorted(refs_remotes_origin_by_author, key=second_column, reverse=True)


def count_not_compliant_subjects_by_author(numstat: List[Numstat], subject_regexes: List[str]) -> List[List]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :param subject_regexes: list of regular expression pattern
    :return: list of [author, non_compliant_commits]
    """
    logging.info("counting not compliant subjects by author")
    numstat = __unique_by(numstat, "hash")

    for subject_regex in subject_regexes:
        numstat = list(filter(lambda x: len(re.findall(subject_regex, x.subject)) == 0, numstat))
    not_compliant_subjects_by_author = __count_by_attr(numstat, "author")

    author_non_compliant_commits = list()
    for author in not_compliant_subjects_by_author.keys():
        row = [author, not_compliant_subjects_by_author[author]]
        author_non_compliant_commits.append(row)
    return sorted(author_non_compliant_commits, key=second_column, reverse=True)


def count_reviews(numstat: List[Numstat], reviewer_regex: str) -> Tuple[List[str], List[List]]:
    """
    :param numstat: result of :func: git_log_numstat_no_merge
    :param reviewer_regex: regular expression pattern
    :return: list of [, author1, author2, ...], [reviewer1, count, count, ...]
                                                [reviewer2, count, count, ...],
                                                ...
    """
    logging.info("counting reviews (reviewer_regex=%s)" % reviewer_regex)

    authors = set()
    reviewer_author_reviews = defaultdict(lambda: defaultdict(int))

    numstat = __unique_by(numstat, "hash")
    for n in numstat:
        reviewers = re.findall(reviewer_regex, n.subject)
        for reviewer in reviewers:
            reviewer = Mailmap.instance().get(reviewer, reviewer, n.date)
            reviewer_author_reviews[reviewer][n.author] += 1
            authors.add(n.author)

    authors = sorted(authors)
    header = ["    ┌─> author\nreviewer"]
    header.extend(authors)

    data = list()
    for reviewer in sorted(reviewer_author_reviews.keys()):
        data.append([reviewer] + list(map(lambda a: reviewer_author_reviews[reviewer][a], authors)))

    return header, data


def __count_by_attr(items: List[Any], attr: str) -> Dict[Any, int]:
    count_by_attr = defaultdict(int)
    for item in items:
        count_by_attr[item[attr]] += 1
    return count_by_attr


def __unique_by(items: List, attr: str) -> List:
    items_by_attr = dict()
    for item in items:
        items_by_attr[item[attr]] = item
    return list(items_by_attr.values())
